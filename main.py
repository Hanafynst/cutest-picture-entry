"""Copy our picture to the entry output location.

The picture bundled with this entry shows a plush baby penguin chick
with enormous sparkling amber eyes and rosy cheeks, wearing a tiny red
knitted scarf and hugging a snowball. This program simply copies that
bundled JPEG to ``entry.png`` inside the output directory, so every
run produces exactly the same bytes.
"""

import hashlib
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "picture.jpg"
MAX_BYTES = 1_048_576
JPEG_MAGIC = b"\xff\xd8"


def main() -> None:
    data = SOURCE.read_bytes()
    if not data.startswith(JPEG_MAGIC):
        found = data[:2].hex() if data else "empty file"
        raise ValueError(
            f"picture.jpg is not a JPEG image: expected magic bytes ffd8, found {found}"
        )
    if len(data) > MAX_BYTES:
        raise ValueError(
            f"picture.jpg is {len(data)} bytes, over the {MAX_BYTES} byte limit"
        )
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "entry.png"
    shutil.copyfile(SOURCE, out)
    digest = hashlib.sha256(out.read_bytes()).hexdigest()
    print(f"wrote {out} ({len(data)} bytes)")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
