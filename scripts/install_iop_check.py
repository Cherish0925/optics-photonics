"""Install the released IOP package, including its native executor, for integration checks."""
import io
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
from urllib.request import urlopen
from zipfile import ZipFile

system={'Windows':'windows','Darwin':'macos','Linux':'linux'}[platform.system()]
arch='arm64' if platform.machine().lower() in ('arm64','aarch64') else 'x86_64'
url=f'https://github.com/Cherish0925/AI4Instruments/releases/download/iop-v0.8.5/IOP-0.8.5-{system}-{arch}.zip'
with urlopen(url,timeout=120) as response:content=response.read()
with tempfile.TemporaryDirectory() as tmp, ZipFile(io.BytesIO(content)) as archive:
    name=next(n for n in archive.namelist() if '/dist/ai4instruments-' in n and n.endswith('.whl'))
    file=Path(tmp)/Path(name).name
    file.write_bytes(archive.read(name))
    subprocess.run([sys.executable,'-m','pip','install','--no-deps',str(file)],check=True)
# Wheel installation does not preserve an executable bit on every packaging tool.
if system!='windows':
    import ai4instruments.iop
    binary=Path(ai4instruments.iop.__file__).parent/'bin/iop-execd'
    binary.chmod(binary.stat().st_mode|0o111)
print('Installed IOP 0.8.5 for',system,arch)
