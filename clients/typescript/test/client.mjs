import {test} from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp,readFile,rm,writeFile} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join,resolve} from 'node:path';
import {OpticsLab} from '../dist/index.js';

test('submit arbitrary software, reconnect and retrieve its saved output',async()=>{
 const home=await mkdtemp(join(tmpdir(),'Optics TypeScript '));
 const command=process.env.OPTICS_PYTHON||(process.platform==='win32'?'python':'python3');
 const options={command,args:['-B',resolve('../../server.py'),'mcp'],home};
 let client=await OpticsLab.connect(options);
 try {
  const script=join(home,'solve.py');
  await writeFile(script,'import json,os,time\nfrom pathlib import Path\ntime.sleep(.1)\nPath(os.environ["OPTICS_RESULT_FILE"]).write_text(json.dumps({"value":42}))\n');
  await client.call('register_software',{tool:'my-solver',name:'My solver',description:'Independent research program',kind:'command'});
  await client.call('bind_environment',{tool:'my-solver',command:[command,script]});
  const submission=await client.submit([{id:'solve',tool:'my-solver'}],{request_id:'research-42'});
  client.close();client=await OpticsLab.connect(options);
  const result=await client.wait(submission.run_id,{timeout:15000});
  assert.equal(result.state,'succeeded');assert.equal('result' in result.steps[0],false);
  const full=await client.status(submission.run_id,{include_results:true});
  assert.equal(full.steps[0].result.result.value,42);
  const repeated=await client.submit([{id:'solve',tool:'my-solver'}],{request_id:'research-42'});
  assert.equal(repeated.run_id,submission.run_id);
 }finally{client.close();await rm(home,{recursive:true,force:true,maxRetries:20,retryDelay:50});}
});

test('a status wait does not delay other requests and can be aborted',async()=>{
 const home=await mkdtemp(join(tmpdir(),'Optics TypeScript '));
 const command=process.env.OPTICS_PYTHON||(process.platform==='win32'?'python':'python3');
 const client=await OpticsLab.connect({command,args:['-B',resolve('../../server.py'),'mcp'],home});
 try {
  const script=join(home,'slow.py');
  await writeFile(script,'import time\ntime.sleep(60)\n');
  await client.call('register_software',{tool:'slow',name:'Slow program',description:'Sleeps',kind:'command'});
  await client.call('bind_environment',{tool:'slow',command:[command,script]});
  const {run_id}=await client.submit([{id:'sleep',tool:'slow'}]);
  const controller=new AbortController();
  const started=Date.now();
  const waiting=client.wait(run_id,{signal:controller.signal});
  const found=await client.search('thin film',{limit:1});
  assert.ok(Date.now()-started<1500);
  assert.equal(found.items.length,1);
  controller.abort(new Error('Stop waiting'));
  await assert.rejects(waiting,/Stop waiting/);
  assert.ok(['queued','running'].includes((await client.status(run_id)).state));
  await client.cancel(run_id);
  assert.equal((await client.wait(run_id,{timeout:15000})).state,'cancelled');
 }finally{client.close();await rm(home,{recursive:true,force:true,maxRetries:20,retryDelay:50});}
});

test('download transfers binary and text files unchanged and file bindings pass locations',async()=>{
 const home=await mkdtemp(join(tmpdir(),'Optics TypeScript '));
 const command=process.env.OPTICS_PYTHON||(process.platform==='win32'?'python':'python3');
 const client=await OpticsLab.connect({command,args:['-B',resolve('../../server.py'),'mcp'],home});
 try {
  const write=join(home,'write.py');
  await writeFile(write,`import json,os
from pathlib import Path
out=Path(os.environ["OPTICS_OUTPUT_DIR"])
out.joinpath("field.bin").write_bytes(bytes(range(256))*800+b"\\xff\\xfe")
out.joinpath("notes.txt").write_text("场 + 物质 + 相互作用\\n"*9000,encoding="utf-8")
Path(os.environ["OPTICS_RESULT_FILE"]).write_text(json.dumps({"written":2}))
`);
  const size=join(home,'size.py');
  await writeFile(size,`import json,os
from pathlib import Path
inputs=json.loads(Path(os.environ["OPTICS_REQUEST_FILE"]).read_text())["inputs"]
Path(os.environ["OPTICS_RESULT_FILE"]).write_text(json.dumps({"bytes":Path(inputs["field"]).stat().st_size}))
`);
  for (const [tool,script] of [['writer',write],['sizer',size]]) {
   await client.call('register_software',{tool,name:tool,description:'Research program',kind:'command'});
   await client.call('bind_environment',{tool,command:[command,script]});
  }
  const {run_id}=await client.submit([{id:'write',tool:'writer'},{id:'size',tool:'sizer',bindings:{field:{step:'write',file:'field.bin'}}}]);
  const state=await client.wait(run_id,{timeout:20000});
  assert.equal(state.state,'succeeded');
  const full=await client.status(run_id,{include_results:true});
  assert.equal(full.steps[1].result.result.bytes,204802);
  for (const name of ['field.bin','notes.txt']) {
   const target=join(home,'copy-'+name);
   const copied=await client.download(run_id,'write/attempt-1/'+name,target);
   const original=await readFile(join(home,'runs',run_id,'write','attempt-1',name));
   assert.equal(copied.bytes,original.length);
   assert.ok((await readFile(target)).equals(original));
   await assert.rejects(client.download(run_id,'write/attempt-1/'+name,target));  // an existing destination is kept
  }
  await assert.rejects(client.download(run_id,'write/attempt-1/absent.bin',join(home,'absent.bin')));
  await assert.rejects(readFile(join(home,'absent.bin')));
 }finally{client.close();await rm(home,{recursive:true,force:true,maxRetries:20,retryDelay:50});}
});
