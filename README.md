# Floofii Telegram Bot

Ein Telegram-Bot für die Floofii-Gruppe mit folgenden Features:

## Features

- 🎂 **Geburtstags-Reminders**: Automatische Benachrichtigungen zu Geburtstagen
- 🎲 **Random Fragen**: Tägliche Fragen für die Gruppe
- 🐾 **Floof-Skala**: Zufällige Floof-Prozentberechnung
- 👋 **Willkommensnachrichten**: Automatisches Begrüßen neuer Mitglieder
- ⚙️ **Gruppenverwaltung**: Einfache Konfiguration und Geburtstags-Management

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

```bash
python src/bot.py
```

## Commands

- `/start` - Hilfe und Informationen
- `/setgroup` - Diese Gruppe als Hauptgruppe speichern
- `/addbirthday DD.MM Name` - Geburtstag hinzufügen
- `/listbirthdays` - Alle Geburtstage anzeigen
- `/floofscale` - Deine Floof-Prozentage berechnen
- `/question` - Sofort eine random Frage posten

## Konfiguration

Die Geburtstags- und Frage-Zeiten können im Code angepasst werden:

```python
BIRTHDAY_HOUR = 10      # Geburtstags-Reminder um 10 Uhr
QUESTION_HOUR = 19      # Random Frage um 19 Uhr
```

## Daten

Der Bot speichert folgende Daten lokal:
- `config.json` - Gruppenkonfiguration
- `birthdays.json` - Geburtstags-Datenbank

Diese Dateien sind in `.gitignore` enthalten und werden nicht versioniert.

## Lizenz

MIT
