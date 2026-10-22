"""Watch a OneDrive folder and convert every new file to Markdown with markitdown.

Phone -> OneDrive/MarkItDown/Inbox  ->  PC converts  ->  OneDrive/MarkItDown/MD
Originals are moved to OneDrive/MarkItDown/Done (or Failed if conversion breaks).
"""

import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

from markitdown import MarkItDown

ROOT = Path.home() / "OneDrive" / "MarkItDown"
INBOX = ROOT / "Inbox"
OUT = ROOT / "MD"
DONE = ROOT / "Done"
FAILED = ROOT / "Failed"
POLL_SECONDS = 5
SKIP_SUFFIXES = {".tmp", ".crdownload", ".part"}


def log(msg: str) -> None:
    print(f"[{datetime.now():%H:%M:%S}] {msg}", flush=True)


def is_ready(path: Path) -> bool:
    """File is fully synced: size is stable for one poll cycle."""
    try:
        size = path.stat().st_size
        time.sleep(1)
        return size > 0 and size == path.stat().st_size
    except OSError:
        return False


def unique(path: Path) -> Path:
    if not path.exists():
        return path
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return path.with_name(f"{path.stem}-{stamp}{path.suffix}")


def convert(md: MarkItDown, src: Path) -> None:
    result = md.convert(str(src))
    target = unique(OUT / f"{src.stem}.md")
    target.write_text(result.text_content, encoding="utf-8")
    shutil.move(str(src), unique(DONE / src.name))
    log(f"OK   {src.name} -> {target.name}")


def main() -> None:
    for d in (INBOX, OUT, DONE, FAILED):
        d.mkdir(parents=True, exist_ok=True)
    md = MarkItDown()
    log(f"Watching {INBOX}")
    while True:
        for src in sorted(INBOX.iterdir()):
            if not src.is_file() or src.name.startswith(("~", ".")) or src.suffix.lower() in SKIP_SUFFIXES:
                continue
            if not is_ready(src):
                continue
            try:
                convert(md, src)
            except Exception as e:  # keep running whatever the file is
                log(f"FAIL {src.name}: {e}")
                shutil.move(str(src), unique(FAILED / src.name))
        time.sleep(POLL_SECONDS)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
