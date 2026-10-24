# Telegram-бот: файл → Markdown

Кидаешь боту файл в Telegram (PDF, Excel, Word, PowerPoint, картинку, HTML…) — он отвечает `.md`.
Работает, пока включён ПК. Отвечает только тебе (`ALLOWED_USER_ID`).

## Установка (один раз, на ПК)
1. Python 3.12 с python.org, галочка **Add python.exe to PATH**.
2. В Telegram: @BotFather → `/newbot` → получить токен.
3. Двойной клик `install.bat` → откроется блокнот с `.env` → вставить токен в `TELEGRAM_BOT_TOKEN=`, сохранить, закрыть.
4. Написать боту любое сообщение — он пришлёт твой user id.
5. Вписать его в `.env` как `ALLOWED_USER_ID=`, затем `stop.bat` и `start-hidden.vbs`.

Бот стартует вместе с Windows, без окна.

- `run-console.bat` — запустить с окном и видеть лог
- `stop.bat` — остановить
- `.env` в git не попадает
