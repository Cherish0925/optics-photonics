"""Build a relocatable Research OS plugin and a portable source/launcher package."""
from pathlib import Path
import shutil
import sys
import tempfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from optics_photonics import __version__
from optics_photonics.packages import package

out=ROOT/'dist';out.mkdir(exist_ok=True)
with tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp)
    plugin=root/'optics-photonics'
    package(plugin,'agentic-research-os')
    shutil.make_archive(str(out/('Optics-Photonics-'+__version__+'-ResearchOS')),'zip',root,plugin.name)
    # Portable CLI bundle has no machine-specific MCP configuration.
    (plugin/'plugin.json').unlink()
    (plugin/'INSTALL.md').write_text('Run: python server.py connect HOST --output /new/host/package\nHOST: agentic-research-os, codex, claude, deepseek, qiushi, mcp\nPython 3.10+ runs the connector. Configure each scientific solver separately.\n',encoding='utf-8')
    shutil.make_archive(str(out/('Optics-Photonics-'+__version__+'-Connect')),'zip',root,plugin.name)
print('\n'.join(p.name for p in out.iterdir()))
