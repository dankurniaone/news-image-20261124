"""Entry program for news-image-20261124.

Checks the broadsheet image this repository ships (PNG signature, 680x1024,
at most 1 MiB, whole file ending in IEND) and copies it to the output
directory the grader reads (MAKEFUN_OUTPUT_DIR outside the grader, /output
inside it), verifying the copy landed whole. No network, no randomness:
every run writes the same bytes.
The image itself is built by tools/render.py from real, freely licensed
Pexels file photos and the day's verified news text; this program only
delivers it.
"""

import hashlib
import os
import shutil
import struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"

PNG_SIG = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
MAX_BYTES = 1048576
WANT_W, WANT_H = 680, 1024


def fail(msg: str) -> None:
    raise SystemExit(f"entry.png invalid: {msg}")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    buf = SRC.read_bytes()

    if len(buf) > MAX_BYTES:
        fail(f"too large: {len(buf)} bytes (max {MAX_BYTES})")
    if len(buf) < 8 or buf[:8] != PNG_SIG:
        fail("bad PNG signature")
    if len(buf) < 33 or buf[12:16] != b"IHDR":
        fail("no IHDR chunk")
    w, h = struct.unpack(">II", buf[16:24])
    if (w, h) != (WANT_W, WANT_H):
        fail(f"dimensions {w}x{h}, expected {WANT_W}x{WANT_H}")
    tail = buf[-12:]
    if struct.unpack(">I", tail[:4])[0] != 0 or tail[4:8] != b"IEND":
        fail("file does not end with an IEND chunk")

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    shutil.copyfile(SRC, dest)
    copied = dest.read_bytes()
    if len(copied) != len(buf) or digest(copied) != digest(buf):
        fail("copied file does not match entry.png")
    print(f"entry.png {w}x{h} {len(copied)} bytes sha256 {digest(buf)} -> {dest}")


if __name__ == "__main__":
    main()
