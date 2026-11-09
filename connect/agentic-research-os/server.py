from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent/"lib"))
from optics_photonics.cli import main
main()
