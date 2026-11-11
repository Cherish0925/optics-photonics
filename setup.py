"""Include the catalogue and methods in installed wheels from their original sources."""
from pathlib import Path
import shutil
from setuptools import setup
from setuptools.command.build_py import build_py


class Build(build_py):
    def run(self):
        super().run()
        root = Path(__file__).parent
        target = Path(self.build_lib) / 'optics_photonics' / 'resources'
        for directory in ('data', 'skills'):
            shutil.copytree(root / directory, target / directory, dirs_exist_ok=True)
        shutil.copy2(root / 'LICENSE', target / 'LICENSE')
        binaries = root / 'src/optics_photonics/bin'
        if binaries.is_dir():
            shutil.copytree(binaries, Path(self.build_lib)/'optics_photonics/bin', dirs_exist_ok=True)


setup(cmdclass={'build_py': Build})
