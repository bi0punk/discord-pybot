# discord-pybot

Discord bot with mathematical calculation, NLTK-based chatbot conversation, scheduled auto-messaging, and custom commands.

**Security:** Math expressions use a safe AST evaluator instead of `eval()`, preventing arbitrary code execution.

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
OWNER_ID=your_discord_id
CHANNEL_ID=target_channel_id
```

## Commands

- `!calcular <expression>` — Evaluate math expressions (safe AST-based, no eval)
- `!responder <message>` — NLTK-based chat response
- `!saludo` — Greeting with owner detection
- Auto-message every 60s

## Security

- `!calcular` uses `ast.parse()` + custom evaluator with whitelisted operators only
- No arbitrary code execution possible through math expressions
- Supports: `+`, `-`, `*`, `/`, `**` operators and parentheses

## License

MIT
