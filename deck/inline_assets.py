# docs/demos/adc_demo/deck/inline_assets.py
"""Inline local image assets as base64 data URIs to produce a single-file deck.

Large media (video) is intentionally NOT inlined: the repo caps committed
files at 1 MB, so the bundle keeps a relative ``assets/<file>.mp4`` reference
and the video must travel alongside the bundle when presenting.
"""

from __future__ import annotations

import base64
import mimetypes
import re
from pathlib import Path

DECK_DIR = Path(__file__).parent
SRC = DECK_DIR / "security-of-ai-agents.html"
OUT = DECK_DIR / "security-of-ai-agents.bundle.html"

# Skip inlining these — kept as relative refs to keep the bundle committable.
SKIP_INLINE = (".mp4", ".mov", ".webm")

# Inline all images (no name-based skips): the bundle is gitignored and tracked
# locally only, so the 1 MB repo cap does not apply. Only large media in
# SKIP_INLINE (video) stays as a relative sidecar ref.
SKIP_INLINE_NAMES: tuple[str, ...] = ()


def _should_skip(rel_path: str) -> bool:
    low = rel_path.lower()
    return low.endswith(SKIP_INLINE) or any(n in low for n in SKIP_INLINE_NAMES)


def _data_uri(rel_path: str) -> str:
    path = DECK_DIR / rel_path
    mime = mimetypes.guess_type(path.name)[0] or "image/png"
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def main() -> None:
    html = SRC.read_text()
    # Inline <img src="assets/..."> and CSS url('assets/...') / url("assets/...") / url(assets/...)
    # Video stays as a relative ref (see SKIP_INLINE).
    html = re.sub(
        r'src="(assets/[^"]+)"',
        lambda m: m.group(0) if _should_skip(m.group(1)) else f'src="{_data_uri(m.group(1))}"',
        html,
    )
    html = re.sub(
        r"""url\((['"]?)(assets/[^'")]+)\1\)""",
        lambda m: f"url({m.group(1)}{_data_uri(m.group(2))}{m.group(1)})",
        html,
    )
    OUT.write_text(html)
    print(f"-> {OUT} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
