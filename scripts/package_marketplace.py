"""Publish the generated Research OS package at a directly installable GitHub path."""
from pathlib import Path
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from optics_photonics.packages import package


def files(root):
    return {path.relative_to(root).as_posix(): path.read_bytes()
            for path in root.rglob("*") if path.is_file() and "__pycache__" not in path.parts}


def main():
    destination = ROOT / "connect" / "agentic-research-os"
    with tempfile.TemporaryDirectory() as temporary:
        generated = Path(temporary) / "optics-photonics"
        package(generated, "agentic-research-os")
        if "--check" in sys.argv:
            if files(generated) != files(destination):
                raise SystemExit("Regenerate the Research OS package: python scripts/package_marketplace.py")
        else:
            if destination.exists():
                shutil.rmtree(destination)
            shutil.copytree(generated, destination)
    print("Research OS package matches the published source.")


if __name__ == "__main__":
    main()
