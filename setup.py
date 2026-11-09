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


setup(cmdclass={'build_py': Build})
