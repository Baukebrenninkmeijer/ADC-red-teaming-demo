"""Reverse of inline_assets.py: rebuild the clean source html from the bundle.

The original ``security-of-ai-agents.html`` source was lost; only the inlined
``*.bundle.html`` survived. inline_assets.py is deterministic (base64 of each
asset under ``assets/``), so we regenerate each asset's data URI and swap it
back to its relative ``assets/<rel>`` path.
"""

from __future__ import annotations

import base64
import mimetypes
from pathlib import Path

DECK_DIR = Path(__file__).parent
SRC = DECK_DIR / "security-of-ai-agents.bundle.html"
OUT = DECK_DIR / "security-of-ai-agents.html"
ASSETS = DECK_DIR / "assets"
SKIP = (".mp4", ".mov", ".webm")


def _data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def main() -> None:
    html = SRC.read_text()
    swapped = 0
    for path in sorted(ASSETS.rglob("*")):
        if not path.is_file() or path.suffix.lower() in SKIP:
            continue
        rel = path.relative_to(DECK_DIR).as_posix()
        uri = _data_uri(path)
        if uri in html:
            html = html.replace(uri, rel)
            swapped += 1
    OUT.write_text(html)
    leftover = html.count("data:image") + html.count("data:font") + html.count(";base64,")
    print(f"-> {OUT} ({OUT.stat().st_size // 1024} KB), {swapped} assets restored, {leftover} base64 refs left")


if __name__ == "__main__":
    main()
