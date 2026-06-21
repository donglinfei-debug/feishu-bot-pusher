# 飞书机器人推送器 (Feishu Bot Pusher)

一个 Python 飞书 Bot 消息推送模块，支持 7 种消息类型。基于飞书 OpenAPI 自建应用 Bot 身份发送，不是 Webhook 机器人。

## 功能特性

- **7 种消息类型**：文本、图片、文件、音频、视频、富文本、交互卡片
- **Bot 身份发送**：以自建应用 Bot 身份发送，不依赖群 Webhook
- **Token 自动管理**：缓存 tenant_access_token，过期自动刷新
- **媒体自动上传**：图片/文件自动上传后再发送
- **灵活配置**：支持环境变量、配置文件、构造参数三种方式

## 快速开始

### 1. 安装依赖

```bash
pip install requests
```

### 2. 配置

设置环境变量：

```bash
export FEISHU_APP_ID=cli_xxxxxxxxxxxxxxxxxxxx
export FEISHU_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
export FEISHU_DEFAULT_USER_ID=ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

或创建配置文件 `feishu_config.json`：

```json
{
    "app_id": "cli_xxxxxxxxxxxxxxxxxxxx",
    "app_secret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "default_user_id": "ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
}
```

### 3. 发送消息

```python
from feishu_bot import FeiShuBot

bot = FeiShuBot()

# 纯文本
bot.send_text("你好，这是一条飞书 Bot 消息")

# 图片
bot.send_image("截图.png")

# 文件
bot.send_file("报告.pdf")

# 富文本（含加粗、链接）
bot.send_post("通知标题", [
    {"tag": "md", "text": "**更新**: v2.0 已发布"},
    {"tag": "a", "text": "查看详情", "href": "https://example.com"},
])

# 交互卡片（带颜色标识）
bot.send_card(
    header_title="系统告警",
    header_template="red",
    elements=[
        {"tag": "markdown", "content": "**CPU**: 92%\n**内存**: 78%"},
        {"tag": "hr"},
        {"tag": "note", "elements": [{"tag": "plain_text", "content": "请及时处理"}]}
    ]
)
```

## 消息类型一览

| 类型 | 方法 | 说明 |
|:----|:-----|:------|
| 文本 | `send_text()` | 纯文字消息 |
| 图片 | `send_image()` | 自动上传后发送 |
| 文件 | `send_file()` | 任意格式文件，可下载 |
| 音频 | `send_audio()` | 音频消息（opus/amr 格式） |
| 视频 | `send_video()` | 视频消息（需附带封面图） |
| 富文本 | `send_post()` | 带格式、链接、@人的排版消息 |
| 交互卡片 | `send_card()` | 带颜色头/按钮/组件的结构化卡片 |

> **音频说明**：飞书 `audio` 消息仅支持 opus/amr 格式。MP3 等常见格式建议使用 `send_file()` 以文件形式发送。

## 配置优先级

```
构造参数 > 环境变量 > 配置文件 (feishu_config.json)
```

## 配置方式

配置优先级：

```
构造参数 > 环境变量 > 配置文件 (feishu_config.json)
```

如需使用 `.env` 文件自动加载，安装 `python-dotenv` 并在脚本开头添加：

```python
from dotenv import load_dotenv
load_dotenv()
```

## 适用场景

- **AI Agent 输出推送** — 把 AI 摘要、分析结果、任务完成通知推送到飞书
- **多通道通知中枢** — 将监控告警、CI/CD 结果、业务系统的消息统一汇聚到飞书
- **个人效率助手** — 脚本自动把文件、备忘、提醒推送到你的飞书
- **团队协作 Bot** — 构建自定义 Bot，向群聊发送格式化报告、图表和交互卡片
- **媒体传输管道** — 截图、录音、视频片段自动转发到飞书联系人

## 作者

**Ryan Dong** — 全栈开发者 & AI 产品经理

- 邮箱：donglinfei@gmail.com
- GitHub：[github.com/donglinfei-debug](https://github.com/donglinfei-debug)

## 许可证

MIT
