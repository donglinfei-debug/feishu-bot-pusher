<div align="center">

# 📣 飞书消息推送器 (Feishu Bot Pusher)

**Python 飞书 Bot 推送模块 · 7 种消息类型 · Token 自动管理**

[![GitHub Stars](https://img.shields.io/github/stars/donglinfei-debug/feishu-bot-pusher?style=flat-square&logo=github)](https://github.com/donglinfei-debug/feishu-bot-pusher/stargazers)
[![GitHub Issues](https://img.shields.io/github/issues/donglinfei-debug/feishu-bot-pusher?style=flat-square&logo=github)](https://github.com/donglinfei-debug/feishu-bot-pusher/issues)
[![GitHub Forks](https://img.shields.io/github/forks/donglinfei-debug/feishu-bot-pusher?style=flat-square&logo=github)](https://github.com/donglinfei-debug/feishu-bot-pusher/forks)
[![License](https://img.shields.io/github/license/donglinfei-debug/feishu-bot-pusher?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg?style=flat-square&logo=python)](https://www.python.org/)
[![Feishu](https://img.shields.io/badge/飞书-OpenAPI-blue.svg?style=flat-square)](https://open.feishu.cn/)

🌏 **语言 / Language**：[🇨🇳 中文](README.zh.md) | [🇬🇧 English](README.md)

</div>

---

基于飞书 OpenAPI 自建应用 Bot 身份的消息推送模块。支持 7 种消息类型：文本、图片、文件、音频、视频、富文本、交互卡片。自动管理 Token 生命周期，内置文件上传能力。


## 📌 为什么需要这个模块？

**你的 Python 脚本需要发消息到飞书，但 Webhook 机器人根本不够用。**

- **你想发图片、文件、音频、视频**——飞书 Webhook 只支持文本和简单的卡片
- **Token 每两小时过期**——没有自动刷新，Bot 就静默罢工了
- **你需要交互卡片**——飞书 Open API 的原始调用极其冗长，容易出错
- **你有多个自动化脚本**——每个脚本都得重写一遍飞书集成代码

**Feishu Bot Pusher** 把所有复杂封装成一行 `from feishu_bot import FeiShuBot`。一个 import，7 种消息类型，Token 自动管理。

## 🏗️ 架构示意

```mermaid
flowchart LR
    subgraph YourCode["🧩 你的应用"]
        APP[你的脚本]
    end
    subgraph Module["📦 feishu_bot.py"]
        FB[FeiShuBot 类]
        TM[Token 管理器<br/>自动刷新]
        FU[文件上传器<br/>自动上传]
    end
    subgraph Feishu["☁️ 飞书 OpenAPI"]
        API[开放平台网关]
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

## 📦 功能特性

| # | 特性 | 说明 |
|:--|:-----|:------|
| 1 | **7 种消息类型** | 文本、图片、文件、音频、视频、富文本、交互卡片 |
| 2 | **Bot 身份发送** | 自建应用 Bot 身份，非 Webhook |
| 3 | **Token 自动管理** | 缓存 `tenant_access_token`，过期自动刷新 |
| 4 | **媒体自动上传** | 图片/文件自动上传后再发送 |
| 5 | **灵活配置** | 环境变量 / 配置文件 / 构造参数三种方式 |

## 📦 系统要求

| 要求 | 说明 |
|:-----|:------|
| **Python** | 3.7+ |
| **依赖** | `requests` |
| **飞书应用** | 自建应用，已开启机器人能力 |

## 🚀 快速开始

```bash
pip install requests
```

```python
from feishu_bot import FeiShuBot

bot = FeiShuBot()
bot.send_text("你好，飞书机器人")
bot.send_image("截图.png")
bot.send_file("报告.pdf")
```

## 📁 文件结构

```
feishu-bot-pusher/
├── feishu_bot.py         # 核心模块 — FeiShuBot 类
├── feishu_config.json    # 配置文件（可选）
├── .env.example          # 环境变量模板
├── requirements.txt      # requests
├── LICENSE               # MIT
└── README.md / README.zh.md
```



---

## 🔍 搜索关键词

IBKR 期权自动化交易、Interactive Brokers Python API、期权交易机器人架构、铁鹰策略自动化、SPX 期权交易、IBKR API 连接管理、TWS API Python、IB Gateway 集成、期权链数据批量获取、限价单价格调整、交易风控防抖机制、飞书 Bot 消息推送、钉钉 Webhook 集成、Gmail AI 摘要通知、Google Apps Script 邮件监控、AI 字幕校对、ASR 语音识别、DeepSeek API 集成、阿里云通义听悟 fun-asr、字幕自动生成、Claude Code 规划技能、AI 结构化规划框架、GitHub 公开仓库预处理、开源项目安全清洗、密钥自动检测、公开仓库操作清单
## 📄 许可证

MIT © 2026 Ryan Dong

## 🌟 Star 历史

[![Star History Chart](https://api.star-history.com/svg?repos=donglinfei-debug/feishu-bot-pusher&type=Date)](https://star-history.com/#donglinfei-debug/feishu-bot-pusher&Date)

## 📬 联系方式

Ryan Dong — donglinfei@gmail.com
