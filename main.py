#!/usr/bin/env python3
"""Place the finished entry image where the grader looks for it.

The image is rendered offline and shipped beside this file. At run time
there is no network, no image library and no font access, so this program
only copies the file into the output directory.

Before it copies, it checks the shipped image against the competition's
gates (a PNG of at most 1 MiB and 1024x1024) and, after the copy, checks
the output is byte-identical to the source. A bad image fails loudly
instead of submitting a broken entry.
"""
import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
MAX_BYTES = 1024 * 1024
MAX_SIDE = 1024


def fail(message):
    print("entry image rejected: " + message, file=sys.stderr)
    sys.exit(1)


source = os.path.join(HERE, "entry.png")
with open(source, "rb") as handle:
    data = handle.read()

if len(data) > MAX_BYTES:
    fail("entry.png is %d bytes, over the 1 MiB limit" % len(data))
if data[:8] != b"\x89PNG\r\n\x1a\n":
    fail("entry.png is not a PNG file")
width, height = struct.unpack(">II", data[16:24])
if width > MAX_SIDE or height > MAX_SIDE:
    fail("entry.png is %dx%d, over the 1024x1024 limit" % (width, height))

os.makedirs(OUT, exist_ok=True)
target = os.path.join(OUT, "entry.png")
shutil.copyfile(source, target)
with open(target, "rb") as handle:
    copied = handle.read()
if hashlib.sha256(copied).hexdigest() != hashlib.sha256(data).hexdigest():
    fail("copied entry.png differs from the shipped image")
