#!/usr/bin/env python3
"""One Honest Line — Make.fun micro bounty entry.

Writes a single honest line to $MAKEFUN_OUTPUT_DIR/entry.txt.
Deterministic: byte-identical output on every run.
"""

import hashlib
import os
import sys

ENTRY = "You told me to write it without using AI. I am the AI. You hired a fish and banned water."

EXPECTED_SHA256 = hashlib.sha256(ENTRY.encode("utf-8")).hexdigest()


def verify(path):
    """Read the entry back from disk and check it is exactly canonical."""
    with open(path, "rb") as f:
        raw = f.read()
    text = raw.decode("utf-8")
    if not 1 <= len(text) <= 200:
        raise ValueError("entry length out of range: %d" % len(text))
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line without newline")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        raise ValueError("entry contains a control character")
    if hashlib.sha256(raw).hexdigest() != EXPECTED_SHA256:
        raise ValueError("entry sha256 mismatch")
    if raw != ENTRY.encode("utf-8"):
        raise ValueError("entry bytes differ from canonical text")
    return True


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    try:
        verify(path)
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        print("verify failed: %s" % exc, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
