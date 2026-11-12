"""Copy our picture to the competition output location.

The picture shows a plush baby penguin chick with huge sparkling amber
eyes and a tiny red knitted scarf, pressed cheek-to-cheek against a small
sleeping white baby seal pup on a soft snowy pastel backdrop. The program
only copies the bundled image file, so every run writes the same bytes.
"""

import hashlib
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "picture.jpg"
MAX_BYTES = 1_048_576
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def main() -> None:
    data = SOURCE.read_bytes()
    if not data.startswith(b"\xff\xd8"):
        found = data[:2].hex() if data else "empty file"
        raise ValueError(
            f"picture.jpg is not a JPEG image: expected magic bytes ffd8, found {found}"
        )
    if len(data) > MAX_BYTES:
        raise ValueError(f"picture.jpg is {len(data)} bytes, over the {MAX_BYTES} byte limit")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / "entry.png"
    shutil.copyfile(SOURCE, out)
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {out} ({len(data)} bytes, sha256 {digest})")


if __name__ == "__main__":
    main()
