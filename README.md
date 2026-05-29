# discord-pybot

Discord bot with mathematical calculation, NLTK-based chatbot conversation, scheduled auto-messaging, and custom commands.

## Stack

Python 3, discord.py 2.3, NLTK

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file with your Discord bot token:
```
DISCORD_TOKEN=your_token_here
```

## Commands

- `!calcular <expression>` — Evaluate math expressions
- `!responder <message>` — NLTK-based chat response
- `!saludo` — Greeting with owner detection
- Auto-message every 60s

## License

MIT
