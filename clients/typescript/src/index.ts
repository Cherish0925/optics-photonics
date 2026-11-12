import { spawn, type ChildProcessWithoutNullStreams } from 'node:child_process';
import { open, rm } from 'node:fs/promises';
import { createInterface } from 'node:readline';

export type Step = { id:string; tool:string; source?:string; action?:string; inputs?:Record<string,unknown>;
  after?:string[]; bindings?:Record<string,{step:string;path?:(string|number)[];file?:string}>; timeout?:number; requirements?:Record<string,number> };
export type Submission = {run_id:string;request_id:string};
export type RunStatus = {id:string;state:string;counts:Record<string,number>;next_offset:number|null;
  steps:{id:string;state:string;output?:string;result?:unknown;error?:string;attempt:number}[]};
export type Options = {command?:string;args?:string[];home?:string;env?:NodeJS.ProcessEnv;timeout?:number};
type Pending = {resolve:(value:any)=>void;reject:(error:Error)=>void;timer:ReturnType<typeof setTimeout>;release:()=>void};
export type RequestOptions = {signal?:AbortSignal};

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
        this.pending.delete(reply.id);clearTimeout(request.timer);request.release();
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
      await client.request('initialize',{protocolVersion:'2025-11-25',capabilities:{},clientInfo:{name:'optics-typescript',version:'0.6.0'}});
      client.notify('notifications/initialized');
      return client;
    } catch(error) { client.close(); throw error; }
  }
  private fail(error:Error) {
    this.closed=true;
    for (const request of this.pending.values()) {clearTimeout(request.timer);request.release();request.reject(error);}
    this.pending.clear();
  }
  private notify(method:string,params?:unknown) {
    if(!this.closed) this.child.stdin.write(JSON.stringify({jsonrpc:'2.0',method,...(params===undefined?{}:{params})})+'\n');
  }
  /** Requests are answered independently; aborting one stops its wait, not an accepted calculation. */
  private request(method:string,params:unknown,options:RequestOptions={}):Promise<any> {
    if(this.closed) return Promise.reject(new Error('Optics connection is closed'));
    const signal=options.signal;
    if(signal?.aborted) return Promise.reject(signal.reason);
    const id=++this.sequence;
    return new Promise((resolve,reject)=>{
      const withdraw=(error:unknown,reason:string)=>{
        const request=this.pending.get(id);
        if(!request) return;
        this.pending.delete(id);clearTimeout(request.timer);request.release();
        this.notify('notifications/cancelled',{requestId:id,reason});
        reject(error);
      };
      const timer=setTimeout(()=>withdraw(new Error(`Optics request timed out: ${method}`),'Client timeout'),this.options.timeout??35000);
      const abort=()=>withdraw(signal?.reason,'Aborted by client');
      const release=()=>signal?.removeEventListener('abort',abort);
      let message:string;
      try {message=JSON.stringify({jsonrpc:'2.0',id,method,params})+'\n';}
      catch(error){clearTimeout(timer);reject(error);return;}
      this.pending.set(id,{resolve,reject,timer,release});
      signal?.addEventListener('abort',abort,{once:true});
      this.child.stdin.write(message,error=>{
        if(error){clearTimeout(timer);release();this.pending.delete(id);reject(error);}
      });
    });
  }
  async call<T=unknown>(name:string,arguments_:Record<string,unknown>={},options:RequestOptions={}):Promise<T> {
    const result=await this.request('tools/call',{name,arguments:arguments_},options);
    if(result.isError) throw new Error(result.content?.map((c:{text?:string})=>c.text??'').join('\n')||'Optics operation failed');
    return result.structuredContent as T;
  }
  search(query='',options:Record<string,unknown>={}) {return this.call('software_search',{...options,query});}
  environments(options:Record<string,unknown>={}) {return this.call('environments',options);}
  resources(cpu?:number,pools?:Record<string,number>) {return this.call('compute_resources',{...(cpu===undefined?{}:{cpu}),...(pools===undefined?{}:{pools})});}
  submit(steps:Step[],options:{name?:string;request_id?:string;run_id?:string}={}) {return this.call<Submission>('submit_workflow',{steps,...options});}
  status(run_id:string,options:{wait?:number;offset?:number;limit?:number;include_results?:boolean;signal?:AbortSignal}={}) {
    const {signal,...query}=options;
    return this.call<RunStatus>('run_status',{run_id,...query},{signal});
  }
  async wait(run_id:string,options:{signal?:AbortSignal;timeout?:number}={}) {
    const end=options.timeout===undefined?Infinity:Date.now()+options.timeout;
    for(;;){
      options.signal?.throwIfAborted();
      const remaining=end-Date.now();
      if(remaining<=0) throw new Error('Calculation is still running: '+run_id);
      const state=await this.status(run_id,{wait:Math.min(25,remaining/1000),signal:options.signal});
      if(['succeeded','failed','cancelled','blocked','interrupted'].includes(state.state)) return state;
    }
  }
  files(run_id:string,offset=0,limit=100,prefix=''){return this.call('result_files',{run_id,offset,limit,...(prefix?{prefix}:{})});}
  /** Part of an NPY array or NPZ member; index entries are positions or [start, stop, step]. */
  array(run_id:string,file:string,options:{member?:string;index?:(number|null|(number|null)[])[];max_elements?:number}={}){return this.call('read_array',{run_id,file,...options});}
  read(run_id:string,file:string,offset=0,limit=16384){return this.call('read_result',{run_id,file,offset,limit});}
  /** Copy a result file to this computer; the server may run elsewhere, for example over SSH. */
  async download(run_id:string,file:string,destination:string,options:RequestOptions={}):Promise<{path:string;bytes:number}> {
    const output=await open(destination,'wx');
    let offset=0,bytes=0,complete=false;
    try {
      for(;;){
        const part=await this.call<{encoding:string;data:string;next_offset:number|null}>('read_result',{run_id,file,offset,limit:65536},options);
        const chunk=Buffer.from(part.data,part.encoding==='base64'?'base64':'utf8');
        await output.writeFile(chunk);bytes+=chunk.length;
        if(part.next_offset===null) break;
        offset=part.next_offset;
      }
      complete=true;
    } finally {
      await output.close();
      if(!complete) await rm(destination,{force:true});
    }
    return {path:destination,bytes};
  }
  cancel(run_id:string){return this.call('cancel_run',{run_id});}
  resume(run_id:string){return this.call('resume_run',{run_id});}
  close(){this.child.stdin.end();this.child.kill();this.fail(new Error('Optics client closed'));}
}
