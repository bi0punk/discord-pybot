# discord-pybot

Discord bot with mathematical calculation (safe AST evaluator), NLTK-based chatbot conversation, scheduled auto-messaging, and custom commands.

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://python.org)
[![CI](https://github.com/tu-usuario/discord-pybot/actions/workflows/ci.yml/badge.svg)](https://github.com/tu-usuario/discord-pybot/actions/workflows/ci.yml)

## Tabla de Contenidos

- [Características](#características)
- [Stack](#stack)
- [Arquitectura](#arquitectura)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Tests](#tests)
- [Configuración](#configuración)
- [CI](#ci)
- [Seguridad](#seguridad)
- [Limitaciones / Roadmap](#limitaciones--roadmap)
- [Licencia](#licencia)

## Características

- Evaluación matemática segura con `ast.parse()` (sin `eval`)
- Chatbot conversacional con NLTK (pattern matching)
- Comando `!saludo` con detección del owner
- Auto-mensaje programado cada 60s en canal configurado
- Sistema de comandos con prefijo `!`

## Stack

- Python 3.11+, discord.py 2.3, NLTK, python-dotenv

## Arquitectura

```
discord-pybot/
├── app.py                 # Bot principal
├── tests/
├── img/                   # Assets visuales
├── requirements.txt
├── pyproject.toml
├── .env.example
└── README.md
```

## Requisitos

- Python 3.11+
- Token de bot de Discord
- Intents de Mensajes habilitados en Discord Developer Portal

## Instalación

```bash
git clone https://github.com/tu-usuario/discord-pybot.git
cd discord-pybot
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Uso

```bash
# Configurar token en .env
cp .env.example .env
# Editar .env con DISCORD_TOKEN, OWNER_ID, CHANNEL_ID

# Iniciar bot
python app.py
```

**Comandos:**

| Comando                     | Descripción                                   |
|-----------------------------|-----------------------------------------------|
| `!calcular 2 + 3 * 4`      | Evalúa expresión matemática segura            |
| `!responder Hola`           | Chatbot con respuesta NLTK                    |
| `!saludo`                   | Saludo personalizado (diferente para el owner)|

## Tests

```bash
pip install pytest ruff
pytest -q
ruff check .
```

## Configuración

Variables de entorno (ver `.env.example`):

| Variable         | Descripción                          |
|------------------|--------------------------------------|
| `DISCORD_TOKEN`  | Token del bot de Discord             |
| `OWNER_ID`       | ID de usuario Discord del owner      |
| `CHANNEL_ID`     | ID del canal para auto-mensajes      |

## CI

GitHub Actions ejecuta ruff lint + pytest en cada push y PR.

## Seguridad

- `!calcular` usa `ast.parse()` + evaluador custom con operadores permitidos (+, -, \*, /, \*\*)
- No se usa `eval()` — no hay ejecución de código arbitrario
- Las expresiones inválidas son capturadas sin crash del bot

## Limitaciones / Roadmap

- [ ] Comandos con slash (discord.py 2.4+)
- [ ] Base de datos para persistencia de configuraciones por servidor
- [ ] Música y reproducción de audio
- [ ] Más patrones y respuestas para el chatbot

## Licencia

MIT
