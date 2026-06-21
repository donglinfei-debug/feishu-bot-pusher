# Feishu Bot Pusher

A Python module for sending multi-type messages to Feishu (Lark) via Bot API. Supports text, image, file, audio, video, rich text (post), and interactive card messages.

## Features

- **7 message types**: text, image, file, audio, video, rich text (post), interactive card
- **Bot identity**: sends messages as a Feishu Bot (not a webhook)
- **Auto token management**: caches tenant_access_token with auto-refresh
- **Media auto-upload**: uploads images/files before sending
- **Configurable**: environment variables, config file, or constructor args

## Quick Start

### 1. Install

```bash
pip install requests
```

### 2. Configure

Set environment variables:

```bash
export FEISHU_APP_ID=cli_xxxxxxxxxxxxxxxxxxxx
export FEISHU_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
export FEISHU_DEFAULT_USER_ID=ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Or create `feishu_config.json`:

```json
{
    "app_id": "cli_xxxxxxxxxxxxxxxxxxxx",
    "app_secret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "default_user_id": "ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
}
```

### 3. Send a message

```python
from feishu_bot import FeiShuBot

bot = FeiShuBot()

# Text
bot.send_text("Hello from Feishu Bot")

# Image
bot.send_image("screenshot.png")

# File
bot.send_file("report.pdf")

# Rich text
bot.send_post("Notice", [
    {"tag": "md", "text": "**Update**: v2.0 released"},
    {"tag": "a", "text": "Details", "href": "https://example.com"},
])

# Interactive card
bot.send_card(
    header_title="System Alert",
    header_template="red",
    elements=[
        {"tag": "markdown", "content": "**CPU**: 92%\n**Memory**: 78%"},
        {"tag": "hr"},
        {"tag": "note", "elements": [{"tag": "plain_text", "content": "Please take action"}]}
    ]
)
```

## Message Types

| Type | Method | Description |
|:----|:-------|:------------|
| Text | `send_text()` | Plain text |
| Image | `send_image()` | Image file (auto-upload) |
| File | `send_file()` | Any file format |
| Audio | `send_audio()` | Audio (opus/amr format) |
| Video | `send_video()` | Video with cover image |
| Rich Text | `send_post()` | Formatted text with markdown, links, mentions |
| Card | `send_card()` | Interactive card with color header and components |

## Configuration Priority

```
constructor args > environment variables > config file (feishu_config.json)
```

## Requirements

- Python 3.7+
- requests

## Configuration

Configuration priority:

```
constructor args > environment variables > config file (feishu_config.json)
```

To use `.env` files, install `python-dotenv` and add this to your script:

```python
from dotenv import load_dotenv
load_dotenv()
```

## Use Cases

- **AI agent output delivery** — route AI summaries, analysis results, or task completion notifications to Feishu
- **Multi-channel notification hub** — unify alerts from monitoring, CI/CD, and business systems into one Feishu bot
- **Personal productivity assistant** — receive file/note/reminder pushes from automated scripts to your Feishu
- **Team collaboration bot** — build custom bots that send formatted reports, charts, and interactive cards to group chats
- **Media sharing pipeline** — automatically forward screenshots, recordings, or video clips to Feishu contacts

## Author

**Ryan Dong** — Full-stack Developer & AI Product Manager

- Email: donglinfei@gmail.com
- GitHub: [github.com/donglinfei-debug](https://github.com/donglinfei-debug)

## License

MIT
