#!/usr/bin/env python3
"""Deliver the finished 24 November broadsheet to the grader.

The image is baked into this repository as entry.png. This program only
checks it against the competition limits (a whole PNG, 680x1024, at most
1 MiB) and copies it to /output/entry.png (or $MAKEFUN_OUTPUT_DIR when
set), then reads the copy back and refuses to finish unless it matches
the original byte for byte. No network, no randomness, no third-party
code: two runs write identical bytes.

    python3 main.py
"""
import hashlib
import os
import shutil
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
IMAGE = HERE / "entry.png"
MAX_BYTES = 1_048_576
EXPECT_W, EXPECT_H = 680, 1024

PNG_MAGIC = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])


def reject(why):
    sys.exit(f"entry.png rejected: {why}")


def check(blob):
    if len(blob) > MAX_BYTES:
        reject(f"{len(blob)} bytes is over the {MAX_BYTES} cap")
    if blob[:8] != PNG_MAGIC:
        reject("missing PNG signature")
    if blob[12:16] != b"IHDR":
        reject("missing IHDR chunk")
    w, h = struct.unpack(">II", blob[16:24])
    if (w, h) != (EXPECT_W, EXPECT_H):
        reject(f"dimensions are {w}x{h}, expected {EXPECT_W}x{EXPECT_H}")
    if blob[-12:-8] != b"\x00\x00\x00\x00" or blob[-8:-4] != b"IEND":
        reject("file does not end with an IEND chunk")
    return w, h


def main():
    blob = IMAGE.read_bytes()
    w, h = check(blob)

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    shutil.copyfile(IMAGE, dest)

    written = dest.read_bytes()
    if written != blob:
        reject("copy differs from entry.png")
    print(f"wrote {dest} ({w}x{h}, {len(written)} bytes, "
          f"sha256 {hashlib.sha256(blob).hexdigest()})")


if __name__ == "__main__":
    main()
