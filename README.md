<div align="center">

# 📣 Feishu Bot Pusher

**Python module for sending 7 types of messages via Feishu (Lark) Bot API**

[![GitHub Stars](https://img.shields.io/github/stars/donglinfei-debug/feishu-bot-pusher?style=flat-square&logo=github)](https://github.com/donglinfei-debug/feishu-bot-pusher/stargazers)
[![GitHub Issues](https://img.shields.io/github/issues/donglinfei-debug/feishu-bot-pusher?style=flat-square&logo=github)](https://github.com/donglinfei-debug/feishu-bot-pusher/issues)
[![GitHub Forks](https://img.shields.io/github/forks/donglinfei-debug/feishu-bot-pusher?style=flat-square&logo=github)](https://github.com/donglinfei-debug/feishu-bot-pusher/forks)
[![License](https://img.shields.io/github/license/donglinfei-debug/feishu-bot-pusher?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg?style=flat-square&logo=python)](https://www.python.org/)
[![Feishu](https://img.shields.io/badge/Feishu-OpenAPI-blue.svg?style=flat-square&logo=data:image/svg%2bxml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNMTIgMkM2LjQ4IDIgMiA2LjQ4IDIgMTJzNC40OCAxMCAxMCAxMCAxMC00LjQ4IDEwLTEwUzE3LjUyIDIgMTIgMnptMCAxOGMtNC40MSAwLTgtMy41OS04LThzMy41OS04IDgtOCA4IDMuNTkgOCA4LTMuNTkgOC04IDh6IiBmaWxsPSJ3aGl0ZSIvPjwvc3ZnPg==)](https://open.feishu.cn/)

🌏 **Language / 语言**：[🇨🇳 中文](README.zh.md) | [🇬🇧 English](README.md)

</div>

---

A Python module for sending multi-type messages to **Feishu (Lark)** via the Open API Bot identity — not a webhook. Supports text, image, file, audio, video, rich text (post), and interactive card messages with automatic token management.


## 📌 Why This?

**You've built a Python script that needs to send messages to Feishu — but the webhook isn't enough.**

- **You want to send images, files, audio, video** — Feishu webhooks only support text and simple cards
- **Your token expires every 2 hours** — without automatic refresh, your bot goes silent until you manually re-authenticate
- **You need interactive cards** — the raw Feishu Open API is verbose and error-prone to call directly
- **You have multiple automation scripts** — each one ends up duplicating the same Feishu integration code

**Feishu Bot Pusher** wraps all of this into a single `from feishu_bot import FeiShuBot`. One import, 7 message types, automatic token management. Your scripts stay clean, your team stays notified.

## 🏗️ Architecture

```mermaid
flowchart LR
    subgraph YourCode["🧩 Your Application"]
        APP[Your Script]
    end
    subgraph Module["📦 feishu_bot.py"]
        FB[FeiShuBot Class]
        TM[Token Manager<br/>auto-refresh]
        FU[File Uploader<br/>auto-upload]
    end
    subgraph Feishu["☁️ Feishu OpenAPI"]
        API[Open API Gateway]
    end

    APP --> FB
    FB --> TM
    FB --> FU
    FB --> API

    style APP fill:#6366f1,color:#fff,stroke:none
    style FB fill:#0ea5e9,color:#fff,stroke:none
    style TM fill:#0ea5e9,color:#fff,stroke:none
    style FU fill:#0ea5e9,color:#fff,stroke:none
    style API fill:#f59e0b,color:#fff,stroke:none
```

## 📦 Features

| # | Feature | Description |
|:--|:--------|:------------|
| 1 | **7 Message Types** | Text, image, file, audio, video, rich text, interactive card |
| 2 | **Bot Identity** | Sends as a Feishu Bot (not a webhook) |
| 3 | **Auto Token Mgmt** | Caches `tenant_access_token` with auto-refresh |
| 4 | **Media Auto-Upload** | Uploads images/files before sending |
| 5 | **Flexible Config** | Env vars, config file, or constructor args |

## 📦 Requirements

| Requirement | Version |
|:------------|:--------|
| **Python** | 3.7+ |
| **requests** | Any recent version |
| **Feishu App** | Self-built app with Bot capability enabled |

## 🚀 Quick Start

```bash
pip install requests
```

```python
from feishu_bot import FeiShuBot

bot = FeiShuBot()

# Send text
bot.send_text("Hello from Feishu Bot")

# Send image
bot.send_image("screenshot.png")

# Send rich text
bot.send_post("Notice", [
    {"tag": "md", "text": "**Update**: v2.0 released"},
    {"tag": "a", "text": "Details", "href": "https://example.com"},
])
```

## 📁 Files

```
feishu-bot-pusher/
├── feishu_bot.py         # Core module — FeiShuBot class
├── feishu_config.json    # Config file (optional)
├── .env.example          # Environment variable template
├── requirements.txt      # requests
├── LICENSE               # MIT
└── README.md / README.zh.md
```



## ❓ FAQ

**Can I send messages to a group chat instead of an individual user?**
Yes. Feishu Bot supports both private chat and group chat. Set the receive_id_type to chat_id to send to a group.

**Does this support Feishu interactive cards with buttons?**
Yes. `send_card()` supports color headers, buttons, markdown content, and dividers. You pass a standard Feishu card JSON structure.

**How does token auto-refresh work?**
The FeiShuBot caches tenant_access_token in memory and automatically requests a new one before it expires — so you never get 99991663 auth errors.

**Can I use this with multiple Feishu apps?**
Yes. Create multiple FeiShuBot instances with different app_id/app_secret pairs. Each manages its own token lifecycle independently.

## 📄 License

MIT © 2026 Ryan Dong

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=donglinfei-debug/feishu-bot-pusher&type=Date)](https://star-history.com/#donglinfei-debug/feishu-bot-pusher&Date)



## 👤 About the Author

**Ryan Dong** — AI Product Manager & Full-Stack Developer

I bridge the gap between AI capabilities and production-ready software. My work spans the full stack: from designing AI-powered product features and integrating LLM APIs, to building modular backend services and shipping clean, documented code.

| Role | Focus |
|:-----|:------|
| 🧠 **AI Product Manager** | Product strategy, AI feature design, prompt engineering, model selection |
| 💻 **Full-Stack Developer** | Python, FastAPI, Google Apps Script, automation pipelines, API integration |

This repository is part of a personal toolbox — a growing collection of practical, reusable modules that solve real automation problems. Each project is designed to be independently useful and easily integrated into larger systems.

📬 **donglinfei@gmail.com** — open to business discussions, collaborations, and recruiting inquiries.

## 📬 Contact

Ryan Dong — donglinfei@gmail.com
