# Quack AR — вращающаяся утка на открытке

MindAR WebAR: распечатали открытку → отсканировали QR на ней → навели камеру → крутится утка + играет трек.

## Состав

| Файл | Назначение |
|------|------------|
| `index.html` | MindAR + A-Frame, Tap to start, rotation, audio |
| `assets/postcard.png` | Картинка-якорь (+ QR после `npm run build-print`) |
| `assets/targets.mind` | Скомпилированная цель MindAR |
| `assets/duck.glb` | Классическая утка Khronos Sample Models |
| `assets/duck-quack.mp3` | Кряканье кряквы (CC BY-SA 3.0) — см. [CREDITS.md](CREDITS.md) |

## Аудио

По умолчанию крутится loop кряканья (`duck-quack.mp3`). Лицензия требует указания автора — файл `CREDITS.md` уже в репо.

## Сборка targets.mind

Нужны Node.js 18+ и зависимости (нативная `canvas`):

```bash
cd webar-duck
npm install
npm run compile
```

Если `OfflineCompiler` в вашей версии `mind-ar` недоступен — скомпилируйте в браузере:

1. Откройте https://hiukim.github.io/mind-ar-js-doc/tools/compile/
2. Загрузите `assets/postcard.png`
3. Скачайте `.mind` → сохраните как `assets/targets.mind`

После смены открытки/QR всегда пересобирайте `.mind`.

## GitHub Pages

1. Создайте публичный репозиторий (например `webar-duck`), залейте содержимое этой папки **корнем** сайта (или включите Pages из `/docs` — тогда перенесите файлы).
2. Settings → Pages → Deploy from branch `main` / root.
3. Дождитесь URL вида `https://USERNAME.github.io/webar-duck/`
4. Вшейте QR и пересоберите печать:

```bash
set WEBAR_URL=https://USERNAME.github.io/webar-duck/
npm run build-print
npm run compile
```

5. Закоммитьте обновлённые `postcard.png`, `qr.png`, `targets.mind` (без mp3).

## Печать для подруги

- Отправьте **только** `assets/postcard.png` (или PDF с ним).
- Инструкция на листе: отсканировать QR → «Начать» → разрешить камеру → навести на открытку.
- Печать A5/A4, без сильного сжатия, бумага ровная, хороший свет.

## Локальная проверка

Нужен HTTPS или localhost:

```bash
npx --yes serve -l 5173 .
# телефон в той же Wi‑Fi не увидит камеру по http://LAN — для теста на телефоне нужен Pages или туннель
```

На своём ПК: Chrome → `http://127.0.0.1:5173` (localhost = secure context).
