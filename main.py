"""Copy the pre-rendered front page to the output directory.

The entry image ships in this repository as entry.png. This program only
copies it, byte for byte, so every run produces identical output. It uses
only the Python standard library and needs no network access.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HERE / "entry.png", OUT / "entry.png")


if __name__ == "__main__":
    main()
