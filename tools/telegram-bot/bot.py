"""Telegram bot: send it a file, get back Markdown made by markitdown.

Config lives in .env next to this file (never commit it):
    TELEGRAM_BOT_TOKEN=123456:ABC...
    ALLOWED_USER_ID=123456789
If ALLOWED_USER_ID is empty, the bot only replies with your user id so you can fill it in.
"""

import sys
import tempfile
import time
from datetime import datetime
from pathlib import Path

import requests
from markitdown import MarkItDown

HERE = Path(__file__).resolve().parent
MAX_BYTES = 20 * 1024 * 1024  # Telegram Bot API download limit


def log(msg: str) -> None:
    print(f"[{datetime.now():%H:%M:%S}] {msg}", flush=True)


def load_env() -> dict:
    env = {}
    path = HERE / ".env"
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env


class Bot:
    def __init__(self, token: str):
        self.api = f"https://api.telegram.org/bot{token}"
        self.files = f"https://api.telegram.org/file/bot{token}"

    def call(self, method: str, **kwargs):
        r = requests.post(f"{self.api}/{method}", timeout=70, **kwargs)
        r.raise_for_status()
        return r.json()["result"]

    def send_text(self, chat_id: int, text: str) -> None:
        self.call("sendMessage", data={"chat_id": chat_id, "text": text})

    def send_file(self, chat_id: int, path: Path) -> None:
        with path.open("rb") as f:
            self.call("sendDocument", data={"chat_id": chat_id}, files={"document": (path.name, f)})

    def download(self, file_id: str, dest: Path) -> None:
        info = self.call("getFile", data={"file_id": file_id})
        r = requests.get(f"{self.files}/{info['file_path']}", timeout=120)
        r.raise_for_status()
        dest.write_bytes(r.content)


def incoming_file(msg: dict):
    """Return (file_id, filename, size) for a document or photo, else None."""
    if "document" in msg:
        d = msg["document"]
        return d["file_id"], d.get("file_name") or "file", d.get("file_size", 0)
    if "photo" in msg:
        p = msg["photo"][-1]  # largest size
        return p["file_id"], f"photo-{msg['message_id']}.jpg", p.get("file_size", 0)
    return None


def handle(bot: Bot, md: MarkItDown, msg: dict, allowed: str) -> None:
    chat_id = msg["chat"]["id"]
    user_id = str(msg.get("from", {}).get("id", ""))

    if not allowed:
        bot.send_text(chat_id, f"Твой user id: {user_id}\nВпиши его в .env как ALLOWED_USER_ID и перезапусти бота.")
        return
    if user_id != allowed:
        log(f"ignored message from {user_id}")
        return

    f = incoming_file(msg)
    if not f:
        bot.send_text(chat_id, "Кидай файл: PDF, Excel, Word, PowerPoint, картинку, HTML… Верну Markdown.")
        return
    file_id, name, size = f
    if size > MAX_BYTES:
        bot.send_text(chat_id, "Файл больше 20 МБ — Telegram не даёт ботам скачивать такие.")
        return

    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / name
        bot.download(file_id, src)
        try:
            text = md.convert(str(src)).text_content
        except Exception as e:
            log(f"FAIL {name}: {e}")
            bot.send_text(chat_id, f"Не получилось сконвертировать {name}: {e}")
            return
        if not text.strip():
            bot.send_text(chat_id, "Получился пустой текст. Похоже, это скан без текстового слоя.")
            return
        out = Path(tmp) / f"{src.stem}.md"
        out.write_text(text, encoding="utf-8")
        bot.send_file(chat_id, out)
        log(f"OK   {name} -> {out.name}")


def main() -> None:
    env = load_env()
    token = env.get("TELEGRAM_BOT_TOKEN", "")
    if not token:
        sys.exit(f"Нет TELEGRAM_BOT_TOKEN в {HERE / '.env'}")
    allowed = env.get("ALLOWED_USER_ID", "")

    bot = Bot(token)
    md = MarkItDown()
    offset = 0
    log("Bot started")
    while True:
        try:
            updates = bot.call("getUpdates", data={"offset": offset, "timeout": 60})
        except requests.RequestException as e:
            log(f"network error: {e}")
            time.sleep(5)
            continue
        for u in updates:
            offset = u["update_id"] + 1
            msg = u.get("message")
            if not msg:
                continue
            try:
                handle(bot, md, msg, allowed)
            except Exception as e:  # never let one bad file kill the bot
                log(f"error: {e}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
