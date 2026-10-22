# Inbox watcher

Кидаешь файл с телефона в OneDrive → ПК сам делает из него Markdown.

| Папка (OneDrive/MarkItDown/) | Что там |
|---|---|
| `Inbox` | сюда кидать файлы (PDF, Excel, Word, PowerPoint, картинки, HTML, ...) |
| `MD` | готовые `.md` |
| `Done` | оригиналы после конвертации |
| `Failed` | файлы, которые не получилось сконвертировать |

## Установка (один раз, на ПК)
1. Поставить Python 3.12 с python.org (галочка **Add python.exe to PATH**).
2. Запустить `install.bat` двойным кликом.

После этого watcher стартует вместе с Windows, без окна.

- `run-console.bat` — запустить с окном и видеть лог
- `stop.bat` — остановить фоновый watcher
