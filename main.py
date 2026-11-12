"""Write our picture to /output/entry.png.

The picture is a generated image: a chubby baby otter sitting up facing
the camera, huge round bright eyes wide open, hugging its favorite
smooth round pebble to its chest with both paws, round belly, warm
golden light. The program only copies the bundled image file, so every
run writes exactly the same bytes.
"""

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
        raise ValueError(
            f"picture.jpg is not a JPEG image: it starts with {data[:2]!r}, "
            "expected the JPEG magic bytes b'\\xff\\xd8'"
        )
    if len(data) > MAX_BYTES:
        raise ValueError(f"picture.jpg is {len(data)} bytes, over the {MAX_BYTES} byte limit")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / "entry.png"
    shutil.copyfile(SOURCE, out)
    print(f"wrote {out} ({len(data)} bytes)")


if __name__ == "__main__":
    main()
