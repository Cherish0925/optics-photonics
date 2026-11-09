"""Exercise a real MCP client, scientific interpreter and IOP native executor."""
import asyncio
import json
import os
from pathlib import Path
import sys
import tempfile
import threading
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from ai4instruments.iop.config import initialize
from ai4instruments.iop.engine import Engine
from ai4instruments.iop.server import Server
from optics_photonics import environments
from optics_photonics.iop import Client
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def exercise(endpoint, token, home):
    scientific_python=os.environ.get('OPTICS_SCIENTIFIC_PYTHON',sys.executable)
    environments.bind('tmm',python=scientific_python,path=home,concurrency=2)
    env={**os.environ,'OPTICS_HOME':str(home),'IOP_ENDPOINT':endpoint,'IOP_TOKEN':token,'PYTHONPATH':str(ROOT/'src')}
    params=StdioServerParameters(command=sys.executable,args=['-m','optics_photonics','mcp'],env=env)
    async with stdio_client(params) as (read,write):
        async with ClientSession(read,write) as session:
            await session.initialize()
            listed=await session.list_tools()
            assert len(listed.tools)==11
            attached=await session.call_tool('attach_iop',{'tool':'tmm'})
            assert not getattr(attached,"is_error",getattr(attached,"isError",False)),attached
            # Retrying the same setup uses the existing registration.
            again=await session.call_tool('attach_iop',{'tool':'tmm'})
            assert not getattr(again,"is_error",getattr(again,"isError",False)),again
            source='import time,tmm,numpy as np\ntime.sleep(0.4)\nr=tmm.coh_tmm("s",[1,1.5],[np.inf,np.inf],0,INPUTS["wavelength_nm"])\nnp.savetxt(OUTPUT_DIR/"spectrum.csv",[[INPUTS["wavelength_nm"],r["R"]]],delimiter=",")\nRESULT={"R":float(r["R"])}'
            args={'tool':'tmm','source':source,'inputs':{'wavelength_nm':550},'request_id':'native-research-1'}
            result=await session.call_tool('submit_calculation',args)
            assert not getattr(result,"is_error",getattr(result,"isError",False)),result
            record=json.loads(result.content[0].text);run_id=record['submission']['id']
            repeated=await session.call_tool('submit_calculation',args)
            assert json.loads(repeated.content[0].text)['submission']['id']==run_id
    # The agent's MCP process has exited while the calculation belongs to IOP.
    client=Client(endpoint)
    client.token=token
    until=time.monotonic()+30
    while time.monotonic()<until:
        state=client.run(run_id)
        if state['state'] in ('completed','failed','cancelled'):break
        await asyncio.sleep(.05)
    assert state['state']=='completed',state
    assert abs(state['operation_records'][0]['result']['result']['R']-.04)<1e-12
    files=client.files(run_id)
    spectrum=next(f for f in files if f['name'].endswith('spectrum.csv'))
    destination=home/'download.csv'
    client.download(spectrum['id'],destination)
    assert '4.000000000000000' in destination.read_text()
    # A different client can retrieve the same completed calculation.
    async with stdio_client(params) as (read,write):
        async with ClientSession(read,write) as session:
            await session.initialize()
            result=await session.call_tool('run_status',{'run_id':run_id})
            assert not getattr(result,"is_error",getattr(result,"isError",False)),result
            assert json.loads(result.content[0].text)['state']=='completed'
    print(json.dumps({'mcp_tools':len(listed.tools),'native_calculation':'passed','repeat_submission':'same run','mcp_disconnect':'calculation continued','reconnect':'same result','file_download':destination.stat().st_size}))


def main():
    with tempfile.TemporaryDirectory() as tmp:
        directory=Path(tmp)
        config=initialize(directory/'iop',False,0)
        config['discovery_interval']=0
        engine=Engine(directory/'iop',config)
        server=Server(('127.0.0.1',0),engine)
        engine.start()
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:asyncio.run(exercise(engine.endpoint,config['token'],directory/'optics'))
        finally:server.shutdown();server.server_close();engine.close();thread.join()


if __name__=='__main__':main()
