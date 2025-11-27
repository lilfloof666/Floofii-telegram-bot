# Floofii Telegram Bot 🐾

Ein vielseitiger Telegram-Bot für die Floofii-Gruppe mit Gruppen-Management, Fun-Commands und aggressiven Wasser-Reminders!

## Features

### 🤖 Automatische Features
- 🎂 **Geburtstags-Reminders**: Automatische Benachrichtigungen zu Geburtstagen (täglich 10 Uhr)
- 🎲 **Random Fragen**: Tägliche Fragen für die Gruppe (täglich 19 Uhr)
- 💧 **Wasser-Reminder**: Aggressive Hydrations-Erinnerungen alle 3 Stunden
- 👋 **Willkommensnachrichten**: Automatisches Begrüßen neuer Mitglieder

### 🎮 Fun Commands
- 🐾 `/floofscale` - Wie viel % floof bist du?
- ⚡️ `/pokemon` - Welches Pokémon bist du heute?
- 💀 `/soulrank` - Soul corruption level
- 🍎 `/fruitme` - Welches Obst/Gemüse bist du?
- 🍞 `/loaf` - Loaf energy check
- 🏳️‍🌈 `/howgay` - Gay energy level
- 🐺 `/howfurry` - Furry level
- 🔮 `/vibecheck` - Current vibe check
- 🩸 `/666` - Unholy level
- 🌑 `/shadowform` - Deine dunkle Form
- 👆 `/boop` - Boop someone's snoot
- ❓ `/truth` - Truth question
- 🎲 `/dare` - Dare challenge
- 🔮 `/fortune` - Dein Fortune
- 🤍 `/wholesome` - Wholesome message
- 🔨 `/bonk` - Horny jail!

### ⚙️ Management Commands
- `/setgroup` - Diese Gruppe als Hauptgruppe speichern
- `/addbirthday DD.MM Name` - Geburtstag hinzufügen
- `/listbirthdays` - Alle Geburtstage anzeigen
- `/question` - Sofort eine random Frage posten

## Installation

1. Clone das Repository
2. Installiere Dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Erstelle eine `.env` Datei basierend auf `.env.example`:
   ```bash
   cp .env.example .env
   ```

4. Trage deinen Bot Token ein (von [@BotFather](https://t.me/botfather) auf Telegram)

## Verwendung

### Einmalig starten (Entwicklung)
```bash
python src/bot.py
```

### Permanent laufen lassen (Produktion)

#### Option 1: screen (empfohlen für einfache Setups)
```bash
screen -S floofbot
python src/bot.py
# Drücke Ctrl+A dann D zum Detachen
# Zurück mit: screen -r floofbot
```

#### Option 2: systemd Service (empfohlen für Server)
Erstelle `/etc/systemd/system/floofbot.service`:
```ini
[Unit]
Description=Floofii Telegram Bot
After=network.target

[Service]
Type=simple
User=dein-username
WorkingDirectory=/pfad/zum/Floofii-telegram-bot
ExecStart=/usr/bin/python3 /pfad/zum/Floofii-telegram-bot/src/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Dann:
```bash
sudo systemctl daemon-reload
sudo systemctl enable floofbot
sudo systemctl start floofbot
sudo systemctl status floofbot  # Status prüfen
```

#### Option 3: nohup (einfach aber nicht persistent nach Neustart)
```bash
nohup python src/bot.py > bot.log 2>&1 &
# Prozess stoppen: pkill -f "python src/bot.py"
```

#### Option 4: tmux
```bash
tmux new -s floofbot
python src/bot.py
# Drücke Ctrl+B dann D zum Detachen
# Zurück mit: tmux attach -t floofbot
```

## Erste Schritte nach dem Start

1. **In Telegram**: Schreibe `/start` an deinen Bot
2. **In deiner Gruppe**: Schreibe `/setgroup` - damit weiß der Bot, wohin automatische Nachrichten gesendet werden
3. **Geburtstage hinzufügen**: `/addbirthday 24.12 Nightclaw`
4. **Commands testen**: Probiere `/pokemon`, `/vibecheck`, `/bonk` etc.

Der Wasser-Reminder startet automatisch beim Bot-Start und wiederholt sich alle 3 Stunden! 💧

## Konfiguration

Die automatischen Nachrichten-Zeiten können in `src/bot.py` angepasst werden:

```python
BIRTHDAY_HOUR = 10      # Geburtstags-Reminder um 10 Uhr
QUESTION_HOUR = 19      # Random Frage um 19 Uhr
# Wasser-Reminder: alle 3 Stunden automatisch
```

## Daten

Der Bot speichert folgende Daten lokal:
- `config.json` - Gruppenkonfiguration
- `birthdays.json` - Geburtstags-Datenbank

Diese Dateien sind in `.gitignore` enthalten und werden nicht versioniert.

## Auto-Restart bei Crashes

Verwende das mitgelieferte `run_bot.sh` Script für automatische Neustarts:

```bash
chmod +x run_bot.sh
nohup ./run_bot.sh > bot.log 2>&1 &
```

Das Script startet den Bot automatisch neu, falls er abstürzt. Bei sauberem Beenden (Ctrl+C) wird nicht neu gestartet.

**Bot-Logs ansehen:**
```bash
tail -f bot.log
```

**Bot komplett stoppen:**
```bash
pkill -f "bash.*run_bot.sh"
pkill -f "python.*bot.py"
```

## Lizenz

MIT
