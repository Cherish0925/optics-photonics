import { spawn, type ChildProcessWithoutNullStreams } from 'node:child_process';
import { createInterface } from 'node:readline';

export type Step = { id:string; tool:string; source?:string; action?:string; inputs?:Record<string,unknown>;
  after?:string[]; bindings?:Record<string,{step:string;path?:(string|number)[]}>; timeout?:number; requirements?:Record<string,number> };
export type Submission = {run_id:string;request_id:string};
export type RunStatus = {id:string;state:string;counts:Record<string,number>;next_offset:number|null;
  steps:{id:string;state:string;output?:string;result?:unknown;error?:string;attempt:number}[]};
export type Options = {command?:string;args?:string[];home?:string;env?:NodeJS.ProcessEnv;timeout?:number};
type Pending = {resolve:(value:any)=>void;reject:(error:Error)=>void;timer:ReturnType<typeof setTimeout>};

/** One connection per host. Accepted calculations outlive this client. */
export class OpticsLab {
  private readonly child:ChildProcessWithoutNullStreams;
  private readonly pending=new Map<number,Pending>();
  private sequence=0;
  private closed=false;
  private stderr='';
  private constructor(private readonly options:Options) {
    const env={...process.env,...options.env,...(options.home ? {OPTICS_HOME:options.home}: {})};
    this.child=spawn(options.command ?? (process.platform==='win32'?'python':'python3'),
      options.args ?? ['-m','optics_photonics','mcp'],{env,stdio:'pipe',windowsHide:true});
    const lines=createInterface({input:this.child.stdout});
    lines.on('line',line=>{
      try {
        const reply=JSON.parse(line);
        const request=this.pending.get(reply.id);
        if (!request) return;
        this.pending.delete(reply.id);clearTimeout(request.timer);
        if (reply.error) request.reject(new Error(reply.error.message));
        else request.resolve(reply.result);
      } catch(error) { this.fail(new Error('Invalid MCP response: '+String(error)));this.child.kill(); }
    });
    this.child.stderr.on('data',data=>{this.stderr=(this.stderr+String(data)).slice(-4000);});
    this.child.on('error',error=>this.fail(error));
    this.child.on('close',code=>this.fail(new Error(`Optics connection closed (${code ?? 'signal'}): ${this.stderr}`)));
    this.child.stdin.on('error',error=>this.fail(error));
  }
  static async connect(options:Options={}) {
    const client=new OpticsLab(options);
    try {
      await client.request('initialize',{protocolVersion:'2025-11-25',capabilities:{},clientInfo:{name:'optics-typescript',version:'0.5.0'}});
      client.child.stdin.write(JSON.stringify({jsonrpc:'2.0',method:'notifications/initialized'})+'\n');
      return client;
    } catch(error) { client.close(); throw error; }
  }
  private fail(error:Error) {
    this.closed=true;
    for (const request of this.pending.values()) {clearTimeout(request.timer);request.reject(error);}
    this.pending.clear();
  }
  private request(method:string,params:unknown):Promise<any> {
    if(this.closed) return Promise.reject(new Error('Optics connection is closed'));
    const id=++this.sequence;
    return new Promise((resolve,reject)=>{
      const timer=setTimeout(()=>{this.pending.delete(id);reject(new Error(`Optics request timed out: ${method}`));},this.options.timeout??35000);
      let message:string;
      try {message=JSON.stringify({jsonrpc:'2.0',id,method,params})+'\n';}
      catch(error){clearTimeout(timer);reject(error);return;}
      this.pending.set(id,{resolve,reject,timer});
      this.child.stdin.write(message,error=>{
        if(error){clearTimeout(timer);this.pending.delete(id);reject(error);}
      });
    });
  }
  async call<T=unknown>(name:string,arguments_:Record<string,unknown>={}):Promise<T> {
    const result=await this.request('tools/call',{name,arguments:arguments_});
    if(result.isError) throw new Error(result.content?.map((c:{text?:string})=>c.text??'').join('\n')||'Optics operation failed');
    return result.structuredContent as T;
  }
  search(query='',options:Record<string,unknown>={}) {return this.call('software_search',{...options,query});}
  environments(options:Record<string,unknown>={}) {return this.call('environments',options);}
  resources(cpu?:number,pools?:Record<string,number>) {return this.call('compute_resources',{...(cpu===undefined?{}:{cpu}),...(pools===undefined?{}:{pools})});}
  submit(steps:Step[],options:{name?:string;request_id?:string;run_id?:string}={}) {return this.call<Submission>('submit_workflow',{steps,...options});}
  status(run_id:string,options:{wait?:number;offset?:number;limit?:number;include_results?:boolean}={}) {return this.call<RunStatus>('run_status',{run_id,...options});}
  async wait(run_id:string,options:{signal?:AbortSignal;timeout?:number}={}) {
    const end=options.timeout===undefined?Infinity:Date.now()+options.timeout;
    for(;;){
      options.signal?.throwIfAborted();
      const remaining=end-Date.now();
      if(remaining<=0) throw new Error('Calculation is still running: '+run_id);
      const state=await this.status(run_id,{wait:Math.min(25,remaining/1000)});
      if(['succeeded','failed','cancelled','blocked','interrupted'].includes(state.state)) return state;
    }
  }
  files(run_id:string,offset=0,limit=100){return this.call('result_files',{run_id,offset,limit});}
  read(run_id:string,file:string,offset=0,limit=16384){return this.call('read_result',{run_id,file,offset,limit});}
  cancel(run_id:string){return this.call('cancel_run',{run_id});}
  resume(run_id:string){return this.call('resume_run',{run_id});}
  close(){this.child.stdin.end();this.child.kill();this.fail(new Error('Optics client closed'));}
}
