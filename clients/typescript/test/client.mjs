import {test} from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp,rm,writeFile} from 'node:fs/promises';
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
