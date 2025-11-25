# Floofii Telegram Bot

This repository contains a minimal Telegram bot that replies with the chat ID.

Important: a hard-coded token was removed from the source. If you previously committed a token, revoke it immediately in BotFather and create a new token.

## Run locally

1. Create a bot with BotFather and get a token.

2. Two ways to provide the token locally:

- Export to your shell:

```bash
export TELEGRAM_BOT_TOKEN="<your-new-token>"
python getid.py
```

- Or create a `.env` file (recommended for local development). Copy `.env.example` to `.env` and paste your token there:

```bash
cp .env.example .env
# edit .env and set TELEGRAM_BOT_TOKEN
python getid.py
```

The bot prints incoming chat IDs to stdout and replies with the chat ID.

## Docker

Build and run the container locally:

```bash
docker build -t floofii-telegram-bot:latest .
docker run -e TELEGRAM_BOT_TOKEN="$TELEGRAM_BOT_TOKEN" floofii-telegram-bot:latest
```

## Publish (CI)

A GitHub Actions workflow is included at `.github/workflows/docker-publish.yml`. It builds the image and pushes it to GitHub Container Registry (GHCR) as `ghcr.io/<owner>/floofii-telegram-bot:latest`.

To enable pushing to Docker Hub as well, add `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` secrets to your repository settings.

## Notes and security

- Never commit bot tokens to the repository. Use repository secrets and environment variables.
- If a token was exposed, revoke it immediately in BotFather and create a new one.
# Floofii-telegram-bot