#!/usr/bin/env python3
"""Copy the pre-rendered front page to the grading output directory.

Standard library only. The grading sandbox has no Pillow and no
fonts, so this program never re-renders: it copies entry.png byte
for byte to $MAKEFUN_OUTPUT_DIR/entry.png (default /output).
v4: the copied image is the 68-story front page rendered by draw.py.
"""

import os
import shutil
import sys


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
