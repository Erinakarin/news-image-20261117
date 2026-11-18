#!/usr/bin/env python3
"""Place the finished entry image where the grader looks for it.

The image is rendered offline and shipped beside this file. At run time
there is no network, no image library and no font access, so this program
only copies the file into the output directory.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT, exist_ok=True)
shutil.copyfile(os.path.join(HERE, "entry.png"),
                os.path.join(OUT, "entry.png"))
