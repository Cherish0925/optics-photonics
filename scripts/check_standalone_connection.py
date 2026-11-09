"""Exercise a real MCP client and independently running scientific programs."""
import asyncio
import json
import os
from pathlib import Path
import sys
import tempfile
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from optics_photonics import environments, jobs
from optics_photonics.mcp import TOOLS
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


def result(response):
    assert not getattr(response,'is_error',getattr(response,'isError',False)),response
    return json.loads(response.content[0].text)


async def exercise(home):
    environments.bind('tmm',python=sys.executable,path=home,concurrency=2)
    env={**os.environ,'OPTICS_HOME':str(home),'PYTHONPATH':str(ROOT/'src')}
    params=StdioServerParameters(command=sys.executable,args=['-m','optics_photonics','mcp'],env=env)
    async with stdio_client(params) as (read,write):
        async with ClientSession(read,write) as session:
            await session.initialize()
            listed=await session.list_tools()
            assert len(listed.tools)==len(TOOLS)
            source='import time,tmm,numpy as np\ntime.sleep(0.5)\nr=tmm.coh_tmm("s",[1,1.5],[np.inf,np.inf],0,INPUTS["wavelength_nm"])\nnp.savetxt(OUTPUT_DIR/"spectrum.csv",[[INPUTS["wavelength_nm"],r["R"]]],delimiter=",")\nRESULT={"R":float(r["R"])}'
            args={'tool':'tmm','source':source,'inputs':{'wavelength_nm':550},'request_id':'native-research-1'}
            submitted=result(await session.call_tool('submit_calculation',args));run_id=submitted['run_id']
            repeated=result(await session.call_tool('submit_calculation',args));assert repeated['run_id']==run_id
    # The scientific task continues after the submitting MCP server has exited.
    until=time.monotonic()+40
    while time.monotonic()<until:
        state=jobs.status(run_id,path=home)
        if state['state'] in jobs.TERMINAL:break
        await asyncio.sleep(.05)
    assert state['state']=='succeeded',state
    assert abs(state['steps'][0]['result']['result']['R']-.04)<1e-12
    async with stdio_client(params) as (read,write):
        async with ClientSession(read,write) as session:
            await session.initialize()
            found=result(await session.call_tool('list_runs',{}));assert found['runs'][0]['id']==run_id
            assert result(await session.call_tool('run_status',{'run_id':run_id}))['state']=='succeeded'
            files=result(await session.call_tool('result_files',{'run_id':run_id}))['files']
            spectrum=next(f['file'] for f in files if f['file'].endswith('spectrum.csv'))
            text=result(await session.call_tool('read_result',{'run_id':run_id,'file':spectrum}))['data']
            assert '4.000000000000000' in text
            copied=result(await session.call_tool('download_result',{'run_id':run_id,'file':spectrum,'destination':str(home/'download.csv')}))
            assert (home/'download.csv').read_bytes()==text.encode('utf-8')
    until=time.monotonic()+5
    while time.monotonic()<until:
        with jobs.worker_lock(home,run_id) as available:
            if available:break
        await asyncio.sleep(.05)
    print(json.dumps({'mcp_tools':len(TOOLS),'independent_calculation':'passed','mcp_disconnect':'calculation continued','reconnect':'same result','file_download':copied['bytes']}))


if __name__=='__main__':
    with tempfile.TemporaryDirectory() as tmp:asyncio.run(exercise(Path(tmp)/'optics'))
