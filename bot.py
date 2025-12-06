import telebot
import os
import time
import json
import threading
import random
from datetime import datetime, date, timedelta
# Füge diesen Import hinzu, um spezifische Telegram API Fehler abfangen zu können
from telebot import apihelper 

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Fallback: read .env manually if python-dotenv not installed
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

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
# 💧 AGGRESSIVER WASSER-REMINDER – ALLE 3 STUNDEN (KORRIGIERT)
# =====================================================
WATER_LINES = [
    "💧 TRINK WASSER. Jetzt. Nicht später. Nicht 'gleich'. JETZT.",
    "🧃 Deine Organe sind kein Deko-Item. Hydratiere sie.",
    "🥤 Du: vertrocknete Rosine. Lösung: WASSER.",
    "💀 Du fühlst dich scheiße? Überraschung: du bist zu 90% Kaffee und 0% Wasser.",
    "🚰 *Aggressiver Hydrations-Reminder:* Füll dein Glas. Ich mein's ernst.",
    "🩸 Dein Blut ist kein Sirup. Mach es dünner. TRINK.",
    "🌊 Stell dir vor, wie viel Drama weniger wäre, wenn du einfach Wasser trinken würdest.",
]

last_water_time = None  # wichtig!


def send_water_reminder():
    """Send aggressive water reminder to the group."""
    global group_chat_id, last_water_time # last_water_time hinzugefügt

    if group_chat_id is None:
        print("Keine group_chat_id gesetzt – /setgroup in der Gruppe ausführen.")
        return # Bei fehlender ID abbrechen

    try:
        # Versuche, die Nachricht zu senden
        bot.send_message(group_chat_id, random.choice(WATER_LINES))
        print("💧 Wasser-Reminder gesendet.")
        
        # Nur bei Erfolg: Zeitpunkt aktualisieren, damit es nicht sofort wiederholt wird
        last_water_time = datetime.now() 
        
    except apihelper.ApiTelegramException as e:
        # Fängt Fehler beim Senden (z.B. Bot wurde aus Gruppe entfernt)
        print(f"Fehler beim Senden des Wasser-Reminders (API): {e}")
    except Exception as e:
        # Fängt andere unerwartete Fehler ab
        print(f"Unerwarteter Fehler beim Senden des Wasser-Reminders: {e}")


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
# 🔥 FUN COMMAND DATA
# =====================================================
POKEMON_LIST = [
    "Pikachu ⚡️", "Raichu ⚡️", "Eevee 🌟", "Vaporeon 💧", "Jolteon ⚡️",
    "Flareon 🔥", "Umbreon 🌑", "Espeon 🔮", "Leafeon 🍃", "Glaceon ❄️",
    "Sylveon 🎀", "Lucario 💙🐺", "Zoroark 🌌🦊", "Charizard 🔥🐉", "Gengar 👻",
    "Mew 🩷", "Mewtwo 💜", "Lugia 🌪", "Ho-Oh 🔥🌈", "Arcanine 🔥🐺",
    "Lapras 🌊", "Dragonite 🐉💛", "Snorlax 😴", "Greninja 🐸💨"
]

VIBES = [
    "✨ Soft but dangerous.",
    "🔥 Chaotic gremlin energy.",
    "🌙 Tired but hot.",
    "💫 Overthinking but vibing.",
]

SHADOW_FORMS = [
    "🩸 Blood-soaked nightmare wolf",
    "🌑 Void-touched fox spirit",
    "🦇 Night creature",
    "💀 Bone lich",
    "🔥 Hellflame sorcerer"
]

TRUTHS = [
    "What's a cringe memory that haunts you?",
    "What would you delete first from your search history?",
    "Who was your biggest secret crush?"
]

DARES = [
    "Send your most cursed meme.",
    "Type only in emojis for 5 messages.",
    "Compliment someone here."
]

FORTUNES = [
    "You will survive today out of pure spite.",
    "A tiny win is coming.",
    "Your energy rises later for no reason."
]

WHOLESOME = [
    "You are not hard to love.",
    "Someone is grateful for you.",
    "Your softness is power."
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
        "• Erinnere dich aggressiv ans Wassertrinken 💧 (alle 3h)\n\n"
        "<b>Setup Commands:</b>\n"
        "• /setgroup – diese Gruppe als Hauptgruppe speichern\n"
        "• /addbirthday DD.MM Name – Geburtstag eintragen\n"
        "• /listbirthdays – eingetragene Geburtstage anzeigen\n\n"
        "<b>Fun Commands:</b>\n"
        "• /floofscale – wie viel % floof bist du? 💖\n"
        "• /pokemon – welches Pokémon bist du heute?\n"
        "• /soulrank – soul corruption level\n"
        "• /fruitme – welches Obst/Gemüse bist du?\n"
        "• /loaf – loaf energy check 🍞\n"
        "• /howgay – gay energy level 🏳️‍🌈\n"
        "• /howfurry – furry level 🐾\n"
        "• /vibecheck – current vibe check\n"
        "• /666 – unholy level\n"
        "• /shadowform – deine dunkle Form\n"
        "• /boop – boop someone's snoot\n"
        "• /truth – truth question\n"
        "• /dare – dare challenge\n"
        "• /fortune – dein Fortune\n"
        "• /wholesome – wholesome message\n"
        "• /bonk – horny jail!\n"
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
# 🔥 FUN COMMANDS
# =====================================================

@bot.message_handler(commands=['pokemon'])
def pokemon_cmd(message):
    """Which Pokémon are you today?"""
    mon = random.choice(POKEMON_LIST)
    bot.reply_to(message, f"🔮 Today you are: <b>{mon}</b>")


@bot.message_handler(commands=['soulrank'])
def soulrank(message):
    """Check your soul corruption level."""
    percent = random.randint(0, 100)
    bot.reply_to(message, f"💀 Soul corruption: <b>{percent}%</b>.")


@bot.message_handler(commands=['fruitme'])
def fruitme(message):
    """What fruit/vegetable are you today?"""
    items = [
        "🍎 Apfel", "🍌 Banane", "🍒 Kirsche", "🍉 Wassermelone", "🥝 Kiwi",
        "🍍 Ananas", "🍋 Zitrone", "🍏 Grüner Apfel", "🍅 Tomate",
        "🍆 Aubergine", "🥑 Avocado", "🥕 Karotte", "🌽 Mais", "🥔 Kartoffel",
        "🍄 Pilz", "🍑 Pfirsich 😳", "🍇 Dunkle Traube"
    ]
    bot.reply_to(message, f"Du bist heute: <b>{random.choice(items)}</b> 😈")


@bot.message_handler(commands=['loaf'])
def loaf_cmd(message):
    """Check your loaf energy level."""
    percent = random.randint(0, 100)
    bot.reply_to(message, f"🍞 Loaf energy: <b>{percent}%</b>")


@bot.message_handler(commands=["howgay"])
def cmd_howgay(message):
    """Check your gay energy today."""
    percent = random.randint(0, 100)
    bot.reply_to(message, f"🏳️‍🌈 Gay energy today: <b>{percent}%</b>")


@bot.message_handler(commands=["vibecheck"])
def cmd_vibecheck(message):
    """Check your current vibe."""
    bot.reply_to(message, f"🔮 Vibe check:\n{random.choice(VIBES)}")


@bot.message_handler(commands=["666"])
def cmd_666(message):
    """Check your unholy level."""
    percent = random.randint(0, 100)
    bot.reply_to(message, f"🩸 Unholy Level: <b>{percent}%</b>.")


@bot.message_handler(commands=["shadowform"])
def cmd_shadowform(message):
    """Discover your shadow form."""
    bot.reply_to(message, f"🌑 Your shadow form:\n<b>{random.choice(SHADOW_FORMS)}</b>")


@bot.message_handler(commands=["boop"])
def cmd_boop(message):
    """Boop someone's snoot!"""
    if message.reply_to_message:
        target = message.reply_to_message.from_user.first_name
        bot.reply_to(message, f"👆 *boop* on {target}'s snoot 🐾")
    else:
        bot.reply_to(message, f"👆 *boop* on your own snoot 🐾")


@bot.message_handler(commands=["howfurry"])
def cmd_howfurry(message):
    """Check your furry level."""
    percent = random.randint(0, 100)
    bot.reply_to(message, f"🐾 Furry Level: <b>{percent}%</b>")


@bot.message_handler(commands=["truth"])
def cmd_truth(message):
    """Get a truth question."""
    bot.reply_to(message, f"❓ TRUTH:\n{random.choice(TRUTHS)}")


@bot.message_handler(commands=["dare"])
def cmd_dare(message):
    """Get a dare challenge."""
    bot.reply_to(message, f"🎲 DARE:\n{random.choice(DARES)}")


@bot.message_handler(commands=["fortune"])
def cmd_fortune(message):
    """Get your fortune."""
    bot.reply_to(message, f"🔮 Fortune:\n{random.choice(FORTUNES)}")


@bot.message_handler(commands=["wholesome"])
def cmd_wholesome(message):
    """Get a wholesome message."""
    bot.reply_to(message, f"🤍 Wholesome:\n{random.choice(WHOLESOME)}")


@bot.message_handler(commands=["bonk"])
def cmd_bonk(message):
    """Bonk someone to horny jail!"""
    if message.reply_to_message:
        user = message.reply_to_message.from_user.first_name
        bot.reply_to(message, f"🔨 BONK! {user} go to horny jail 🚓")
    else:
        bot.reply_to(message, "🔨 BONK! You go to horny jail 😼")


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
# SCHEDULER THREAD (KORRIGIERT)
# =====================================================

last_birthday_day = None
last_question_day = None


def scheduler_loop():
    """Background scheduler for daily tasks + water reminders."""
    global last_birthday_day, last_question_day, last_water_time, group_chat_id

    while True:
        try:
            now = datetime.now()
            today = date.today()

            # 💧 Wasser-Reminder: Initialisierung und 3-Stunden-Check
            if last_water_time is None:
                # Setze last_water_time initial auf jetzt, 
                # damit der erste Reminder erst in 3h kommt (wenn group_chat_id gesetzt ist).
                if group_chat_id is not None:
                    last_water_time = now
                else:
                    # Wenn keine Gruppe gesetzt, nur warten.
                    pass 
            else:
                # Alle 3 Stunden
                diff = now - last_water_time
                if diff.total_seconds() >= 3 * 60 * 60:
                    # send_water_reminder() setzt last_water_time nur bei Erfolg!
                    send_water_reminder() 

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
            # Fängt alle Fehler in der Scheduler-Logik ab (außerhalb der Bot-API Calls)
            print("Unerwarteter Fehler im Scheduler-Loop:", e)

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

    # Fehlerbehandlung für API-Call hier beibehalten (wird auch im Loop abgefangen, aber schadet nicht)
    try:
        bot.send_message(group_chat_id, "\n".join(lines))
    except apihelper.ApiTelegramException as e:
        print(f"Fehler beim Senden des Geburtstags-Reminders (API): {e}")


def send_daily_question():
    """Send a daily question to the group."""
    global group_chat_id

    if group_chat_id is None:
        print("Keine group_chat_id gesetzt – /setgroup in der gewünschten Gruppe ausführen.")
        return

    question = random.choice(RANDOM_QUESTIONS)
    text = f"❓ <b>Daily Question:</b>\n{question}"
    
    # Fehlerbehandlung für API-Call hier beibehalten
    try:
        bot.send_message(group_chat_id, text)
    except apihelper.ApiTelegramException as e:
        print(f"Fehler beim Senden der täglichen Frage (API): {e}")


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