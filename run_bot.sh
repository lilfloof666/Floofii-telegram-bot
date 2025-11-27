#!/bin/bash
# Auto-restart script for Floofii Telegram Bot

cd "$(dirname "$0")"

echo "🐾 Floofii Bot Auto-Restart Script gestartet..."
echo "Bot wird bei Crashes automatisch neu gestartet."
echo "Zum Stoppen: pkill -f 'bash.*run_bot.sh' oder Ctrl+C"
echo ""

while true; do
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Bot wird gestartet..."
    python src/bot.py
    
    EXIT_CODE=$?
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Bot beendet mit Exit Code: $EXIT_CODE"
    
    if [ $EXIT_CODE -eq 0 ]; then
        echo "Bot wurde sauber beendet. Kein Neustart."
        break
    else
        echo "⚠️  Bot ist abgestürzt! Neustart in 5 Sekunden..."
        sleep 5
    fi
done
