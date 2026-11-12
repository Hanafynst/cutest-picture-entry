"""Copy our cutest-picture entry image to the output directory.

The picture shows a chubby white baby seal drawn in a soft kawaii
style: oversized starry eyes, pink cheeks, and a bright orange
starfish hugged against its chest, floating on a mint-blue backdrop.
The script only copies the bundled JPEG, so the result is identical
on every run.
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
        raise ValueError(f"picture.jpg is not a JPEG image: expected magic bytes ffd8, found {found}")
    if len(data) > MAX_BYTES:
        raise ValueError(f"picture.jpg is {len(data)} bytes, over the {MAX_BYTES} byte limit")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / "entry.png"
    shutil.copyfile(SOURCE, out)
    digest = hashlib.sha256(out.read_bytes()).hexdigest()
    print(f"wrote {out} ({len(data)} bytes, sha256 {digest})")


if __name__ == "__main__":
    main()
