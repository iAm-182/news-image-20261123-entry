"""Write the finished front page to the grader's output directory.

The image is rendered in advance and shipped in this repository as
``entry.png``. This program does nothing but copy that file, so the bytes
it produces are identical on every run. Only the Python standard library
is used, and no network access is needed.
"""
import os
import shutil
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent
DEST_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main():
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(REPO_DIR / "entry.png", DEST_DIR / "entry.png")


if __name__ == "__main__":
    main()
