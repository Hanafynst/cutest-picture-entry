"""Copy the bundled picture into the output directory as entry.png.

The bundled picture.jpg is a soft stylized digital painting: a round,
fluffy ginger baby kitten with huge sparkling amber eyes and pink cheeks
wraps its little paws around a tiny yellow baby duckling. The duckling
wears a fragment of its own cracked eggshell like a small hat, and both
sit against a plain warm cream backdrop.

The program performs no network access and no processing of the image
bytes; it validates the bundled file and copies it verbatim, so every
run produces exactly the same output file.
"""

import hashlib
import os
import sys
from pathlib import Path

MAX_BYTES = 1_048_576
JPEG_MAGIC = b"\xff\xd8"


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / "picture.jpg"

    data = source.read_bytes()
    if not data.startswith(JPEG_MAGIC):
        raise ValueError(
            "picture.jpg does not start with the JPEG magic bytes ff d8"
        )
    if len(data) > MAX_BYTES:
        raise ValueError(
            f"picture.jpg is {len(data)} bytes, over the {MAX_BYTES} byte limit"
        )

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    target.write_bytes(data)

    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {target} ({len(data)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
