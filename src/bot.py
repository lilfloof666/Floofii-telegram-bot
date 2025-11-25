import telebot
import os
import time
import json
import threading
import random
from datetime import datetime, date
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# =====================================================
# Configuration
# =====================================================
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is required!")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")

CONFIG_FILE = "config.json"
BIRTHDAY_FILE = "birthdays.json"

# Uhrzeit für Geburtstags-Reminder (Serverzeit!)
BIRTHDAY_HOUR = 10      # 10 Uhr
BIRTHDAY_MINUTE = 0

# Uhrzeit für random Fragen
QUESTION_HOUR = 19      # 19 Uhr
QUESTION_MINUTE = 0


# =====================================================
# Helper functions for file operations
# =====================================================
def load_json(path, default):
    """Load JSON from file, return default if not found or invalid."""
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return default
    return default


def save_json(path, data):
    """Save JSON to file."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# =====================================================
# Load configuration
# =====================================================
config = load_json(CONFIG_FILE, {})
group_chat_id = config.get("group_chat_id")

# =====================================================
# Load birthday data
# =====================================================
birthdays = load_json(BIRTHDAY_FILE, {"birthdays": []})


def save_birthdays():
    """Save birthday data."""
    save_json(BIRTHDAY_FILE, birthdays)


# =====================================================
# Random questions for the group
# =====================================================
RANDOM_QUESTIONS = [
    "Welcher deiner OCs braucht heute am meisten Liebe? 💖",
    "Wenn du jetzt irgendwohin teleportieren könntest – wohin? 🌍",
    "Was war heute das Kleinste, was dich glücklich gemacht hat?",
    "Welche Musik läuft, wenn du im Fursuit bist? 🎧",
    "Was ist dein comfort game / comfort movie gerade? 🎮🎬",
    "Mit welchem Pokémon würdest du am liebsten chillen? 🔥❄️",
    "Was ist dein aktuelles Hyperfixation-Thema? 👀",
    "Wenn du ein Furry-Species wechseln müsstest – was wärst du? 🐺🦊",
]


# =====================================================
# COMMANDS
# =====================================================

@bot.message_handler(commands=["start", "help"])
def cmd_start(message):
    """Show help message."""
    text = (
        "Hey floofy hooman/fur 🐾\n\n"
        "Ich bin dein Gruppen-Bot:\n"
        "• Begrüße neue Mitglieder\n"
        "• Merke mir Geburtstage & erinnere daran 🎂\n"
        "• Poste random Fragen in die Gruppe ❓\n"
        "• /floofscale – sag dir, wie viel % floof du bist 💖\n\n"
        "Wichtige Commands:\n"
        "• /setgroup – diese Gruppe als Hauptgruppe speichern\n"
        "• /addbirthday DD.MM Name – Geburtstag eintragen\n"
        "• /listbirthdays – eingetragene Geburtstage anzeigen\n"
        "• /question – sofort eine random Frage posten\n"
    )
    bot.reply_to(message, text)


@bot.message_handler(commands=["setgroup"])
def cmd_setgroup(message):
    """Set the main group for scheduled messages."""
    global group_chat_id, config
    chat_id = message.chat.id
    group_chat_id = chat_id
    config["group_chat_id"] = chat_id
    save_json(CONFIG_FILE, config)
    bot.reply_to(message, "Diese Gruppe wurde als Hauptgruppe gespeichert ✅")


@bot.message_handler(commands=["addbirthday"])
def cmd_add_birthday(message):
    """Add a birthday: /addbirthday 01.02 Name"""
    try:
        # Parse command arguments
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            bot.reply_to(
                message,
                "Benutzung: <code>/addbirthday DD.MM Name</code>\n"
                "Beispiel: <code>/addbirthday 24.12 Nightclaw</code>",
            )
            return

        rest = args[1].strip()
        date_part, name = rest.split(maxsplit=1)

        day_str, month_str = date_part.split(".")
        day = int(day_str)
        month = int(month_str)

        entry = {
            "chat_id": message.chat.id,
            "name": name,
            "day": day,
            "month": month,
        }
        birthdays["birthdays"].append(entry)
        save_birthdays()

        bot.reply_to(
            message,
            f"🎂 Geburtstag gespeichert: <b>{name}</b> am <b>{day:02d}.{month:02d}.</b>",
        )

    except Exception as e:
        bot.reply_to(
            message,
            "Konnte das nicht verstehen 😿\n"
            "Benutzung: <code>/addbirthday DD.MM Name</code>",
        )
        print("Error in /addbirthday:", e)


@bot.message_handler(commands=["listbirthdays"])
def cmd_list_birthdays(message):
    """List all saved birthdays for this group."""
    chat_id = message.chat.id
    entries = [
        b for b in birthdays["birthdays"] if b.get("chat_id") == chat_id
    ]

    if not entries:
        bot.reply_to(message, "Für diese Gruppe sind noch keine Geburtstage gespeichert.")
        return

    lines = ["🎂 Gespeicherte Geburtstage:"]
    for b in entries:
        lines.append(f"- {b['name']} – {b['day']:02d}.{b['month']:02d}.")
    bot.reply_to(message, "\n".join(lines))


@bot.message_handler(commands=["floofscale", "floof"])
def cmd_floofscale(message):
    """Calculate your floof scale (random percentage)."""
    percent = random.randint(0, 100)
    user = message.from_user
    name = user.first_name or "Floof"
    text = f"✨ Floof-Skala für <b>{name}</b>: <b>{percent}% floof</b> 🐾"
    
    if percent == 100:
        text += "\n\nDu bist offiziell überflooft. Pls send help. 💀"
    elif percent < 20:
        text += "\n\nMehr kuscheln, dann steigt der Wert. 📉➡📈"
    
    bot.reply_to(message, text)


@bot.message_handler(commands=["question"])
def cmd_question(message):
    """Send a random question immediately."""
    question = random.choice(RANDOM_QUESTIONS)
    bot.send_message(message.chat.id, f"❓ <b>Random Frage des Moments:</b>\n{question}")


# =====================================================
# EVENTS
# =====================================================

@bot.message_handler(content_types=["new_chat_members"])
def welcome_new_members(message):
    """Welcome new members to the group."""
    for user in message.new_chat_members:
        name = user.first_name or "Floof"
        text = (
            f"Willkommen, <b>{name}</b>! 🐾\n"
            f"Mach es dir bequem, lies die Regeln und stay floofy. ✨"
        )
        bot.send_message(message.chat.id, text)


# =====================================================
# SCHEDULER THREAD
# =====================================================

last_birthday_day = None
last_question_day = None


def scheduler_loop():
    """Background scheduler for daily tasks."""
    global last_birthday_day, last_question_day, group_chat_id

    while True:
        try:
            now = datetime.now()
            today = date.today()

            # Check for birthdays once per day
            if (
                now.hour == BIRTHDAY_HOUR
                and now.minute == BIRTHDAY_MINUTE
                and today != last_birthday_day
            ):
                send_birthday_reminders()
                last_birthday_day = today

            # Check for daily question once per day
            if (
                now.hour == QUESTION_HOUR
                and now.minute == QUESTION_MINUTE
                and today != last_question_day
            ):
                send_daily_question()
                last_question_day = today

        except Exception as e:
            print("Fehler im Scheduler:", e)

        time.sleep(30)  # Check every 30 seconds


def send_birthday_reminders():
    """Send birthday reminders for today."""
    global group_chat_id

    if group_chat_id is None:
        print("Keine group_chat_id gesetzt – /setgroup in der gewünschten Gruppe ausführen.")
        return

    today = date.today()
    today_birthdays = [
        b
        for b in birthdays["birthdays"]
        if b["day"] == today.day and b["month"] == today.month and b["chat_id"] == group_chat_id
    ]

    if not today_birthdays:
        return

    lines = ["🎂 <b>Birthday Alert!</b>"]
    for b in today_birthdays:
        lines.append(f"• Heute hat <b>{b['name']}</b> Geburtstag! 🥳")

    bot.send_message(group_chat_id, "\n".join(lines))


def send_daily_question():
    """Send a daily question to the group."""
    global group_chat_id

    if group_chat_id is None:
        print("Keine group_chat_id gesetzt – /setgroup in der gewünschten Gruppe ausführen.")
        return

    question = random.choice(RANDOM_QUESTIONS)
    text = f"❓ <b>Daily Question:</b>\n{question}"
    bot.send_message(group_chat_id, text)


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":
    print("Floof Group Bot startet… 🐾")

    # Start scheduler in background
    t = threading.Thread(target=scheduler_loop, daemon=True)
    t.start()

    # Run bot
    try:
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except KeyboardInterrupt:
        print("Bot beendet.")
