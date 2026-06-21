"""
飞书机器人消息通知模块（Bot 身份）
直接调用飞书 OpenAPI，不依赖 lark-cli 的 strict-mode 配置。

使用方法：
    from feishu_bot import FeiShuBot

    bot = FeiShuBot()
    bot.send_text("你好，这是一条机器人消息")

配置方式：
    方式 A：环境变量（推荐公开分享时使用）
        FEISHU_APP_ID=xxx
        FEISHU_APP_SECRET=xxx
        FEISHU_DEFAULT_USER_ID=ou_xxx

    方式 B：配置文件（本地开发）
        {"app_id": "xxx", "app_secret": "xxx", "default_user_id": "ou_xxx"}

    配置优先级：环境变量 > 配置文件 > 构造参数

依赖：
    pip install requests
"""

import requests
import json
import os
import time
import logging
from typing import Optional, Dict

logger = logging.getLogger(__name__)


class FeiShuBot:
    """飞书机器人消息通知器（Bot 身份）"""

    # 飞书 API 基础地址
    BASE_URL = "https://open.feishu.cn/open-apis"

    def __init__(self, app_id: Optional[str] = None, app_secret: Optional[str] = None,
                 default_user_id: Optional[str] = None,
                 config_path: Optional[str] = None):
        """
        初始化机器人

        配置优先级（高→低）：
            1. 构造参数 app_id/app_secret/default_user_id
            2. 环境变量 FEISHU_APP_ID / FEISHU_APP_SECRET / FEISHU_DEFAULT_USER_ID
            3. 配置文件（默认 feishu_config.json）

        Args:
            app_id: 飞书应用 App ID
            app_secret: 飞书应用 App Secret
            default_user_id: 默认收件人 open_id
            config_path: 配置文件路径，默认同目录下的 feishu_config.json
        """
        config_path = config_path or os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "feishu_config.json"
        )

        loaded = {}
        if os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                logger.info(f"已从配置文件加载: {config_path}")
            except Exception as e:
                logger.warning(f"读取配置文件失败: {e}")

        # 配置优先级：构造参数 > 环境变量 > 配置文件
        self.app_id = (
            app_id
            or os.environ.get("FEISHU_APP_ID")
            or loaded.get("app_id", "")
        )
        self.app_secret = (
            app_secret
            or os.environ.get("FEISHU_APP_SECRET")
            or loaded.get("app_secret", "")
        )
        self.default_user_id = (
            default_user_id
            or os.environ.get("FEISHU_DEFAULT_USER_ID")
            or loaded.get("default_user_id", "")
        )

        if not self.app_id or not self.app_secret:
            raise ValueError(
                "App ID 和 App Secret 未配置。请通过以下任一方式配置：\n"
                f"  1. 创建配置文件 {config_path}\n"
                "  2. 设置环境变量 FEISHU_APP_ID / FEISHU_APP_SECRET\n"
                "  3. 直接传入构造参数"
            )

        self._tenant_access_token: Optional[str] = None
        self._token_expire_time: float = 0

    def _get_tenant_access_token(self) -> str:
        """
        获取 Tenant Access Token（应用级 Token）
        会自动缓存，过期前自动刷新
        """
        if self._tenant_access_token and time.time() < self._token_expire_time:
            return self._tenant_access_token

        url = f"{self.BASE_URL}/auth/v3/tenant_access_token/internal"
        resp = requests.post(url, json={
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }, timeout=30)

        data = resp.json()
        if data.get("code") != 0:
            raise RuntimeError(f"获取 Token 失败: {data.get('msg')}")

        self._tenant_access_token = data["tenant_access_token"]
        self._token_expire_time = time.time() + data.get("expire", 7200) - 300
        logger.info("Tenant Access Token 已刷新")
        return self._tenant_access_token

    def _api_call(self, method: str, path: str, payload: Optional[Dict] = None) -> Dict:
        """调用飞书 API，带 Token 过期自动重试"""
        token = self._get_tenant_access_token()
        url = f"{self.BASE_URL}{path}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8"
        }

        resp = requests.request(method, url, headers=headers, json=payload, timeout=30)
        result = resp.json()

        if result.get("code") == 99991663:  # token expired
            logger.info("Token 过期，自动刷新...")
            self._tenant_access_token = None
            self._token_expire_time = 0
            token = self._get_tenant_access_token()
            headers["Authorization"] = f"Bearer {token}"
            resp = requests.request(method, url, headers=headers, json=payload, timeout=30)
            result = resp.json()

        return result

    def send_text(self, text: str, user_id: Optional[str] = None) -> bool:
        """
        发送纯文本消息

        Args:
            text: 消息文本内容
            user_id: 收件人的飞书 open_id，默认使用配置中的 default_user_id

        Returns:
            True 发送成功，False 发送失败
        """
        target = user_id or self.default_user_id
        if not target:
            logger.error("未指定收件人 user_id，且未配置 default_user_id")
            return False

        result = self._api_call("POST", f"/im/v1/messages?receive_id_type=open_id", {
            "receive_id": target,
            "msg_type": "text",
            "content": json.dumps({"text": text})
        })

        if result.get("code") == 0:
            logger.info(f"消息发送成功: message_id={result['data'].get('message_id')}")
            return True
        else:
            logger.error(f"消息发送失败: {result.get('msg')}")
            return False

    def send_to_group(self, chat_id: str, text: str) -> bool:
        """
        发送消息到群聊

        Args:
            chat_id: 群聊 ID（oc_xxx 格式）
            text: 消息文本内容

        Returns:
            True 发送成功，False 发送失败
        """
        result = self._api_call("POST", "/im/v1/messages?receive_id_type=chat_id", {
            "receive_id": chat_id,
            "msg_type": "text",
            "content": json.dumps({"text": text})
        })

        if result.get("code") == 0:
            logger.info(f"群消息发送成功: chat_id={chat_id}")
            return True
        else:
            logger.error(f"群消息发送失败: {result.get('msg')}")
            return False

    # ===== 图片消息 =====

    def upload_image(self, image_path: str) -> Optional[str]:
        """
        上传图片到飞书，获取 image_key

        Args:
            image_path: 本地图片文件路径

        Returns:
            image_key 字符串，上传失败返回 None
        """
        token = self._get_tenant_access_token()
        url = f"{self.BASE_URL}/im/v1/images"

        if not os.path.exists(image_path):
            logger.error(f"图片文件不存在: {image_path}")
            return None

        # 判断图片类型
        ext = os.path.splitext(image_path)[1].lower()
        mime_map = {".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                     ".png": "image/png", ".gif": "image/gif",
                     ".webp": "image/webp"}
        image_type = mime_map.get(ext, "image/jpeg")
        if ext not in mime_map:
            logger.warning(f"未知图片格式 {ext}，将尝试作为 JPEG 发送")

        with open(image_path, "rb") as f:
            resp = requests.post(
                url,
                headers={"Authorization": f"Bearer {token}"},
                files={"image": (os.path.basename(image_path), f, image_type)},
                data={"image_type": "message"},
                timeout=60
            )

        result = resp.json()
        if result.get("code") == 0:
            image_key = result["data"]["image_key"]
            logger.info(f"图片上传成功: image_key={image_key}")
            return image_key
        else:
            logger.error(f"图片上传失败: {result.get('msg')}")
            return None

    def send_image(self, image_path: str, user_id: Optional[str] = None) -> bool:
        """
        发送图片消息（自动上传+发送）

        Args:
            image_path: 本地图片文件路径
            user_id: 收件人 open_id，默认使用配置中的 default_user_id

        Returns:
            True 发送成功，False 发送失败
        """
        image_key = self.upload_image(image_path)
        if not image_key:
            return False
        return self._send_by_key("image", image_key, user_id)

    def send_image_to_group(self, chat_id: str, image_path: str) -> bool:
        """发送图片消息到群聊"""
        image_key = self.upload_image(image_path)
        if not image_key:
            return False
        return self._send_by_key("image", image_key, chat_id=chat_id, is_group=True)

    # ===== 文件/音频/视频消息 =====

    def upload_file(self, file_path: str, file_type_name: str = "stream") -> Optional[str]:
        """
        上传文件到飞书，获取 file_key

        Args:
            file_path: 本地文件路径
            file_type_name: 飞书文件类型标识
                "stream" = 普通文件 | "mp4" = 视频 | "opus" = 音频 | "pdf"/"doc"/"xls" 等

        Returns:
            file_key 字符串，上传失败返回 None
        """
        token = self._get_tenant_access_token()
        url = f"{self.BASE_URL}/im/v1/files"

        if not os.path.exists(file_path):
            logger.error(f"文件不存在: {file_path}")
            return None

        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        logger.info(f"上传文件: {file_name} ({file_size / 1024:.1f} KB, type={file_type_name})")

        with open(file_path, "rb") as f:
            resp = requests.post(
                url,
                headers={"Authorization": f"Bearer {token}"},
                files={"file": (file_name, f)},
                data={"file_type": file_type_name, "file_name": file_name},
                timeout=120
            )

        result = resp.json()
        if result.get("code") == 0:
            file_key = result["data"]["file_key"]
            logger.info(f"文件上传成功: file_key={file_key}")
            return file_key
        else:
            logger.error(f"文件上传失败: {result.get('msg')}")
            return None

    def send_file(self, file_path: str, user_id: Optional[str] = None) -> bool:
        """发送文件消息"""
        file_key = self.upload_file(file_path, "stream")
        if not file_key:
            return False
        return self._send_by_key("file", file_key, user_id)

    def send_audio(self, audio_path: str, user_id: Optional[str] = None) -> bool:
        """发送音频消息（支持 opus/amr 格式，MP3 建议用 send_file）"""
        file_key = self.upload_file(audio_path, "opus")
        if not file_key:
            return False
        return self._send_by_key("audio", file_key, user_id)

    def send_video(self, video_path: str, cover_image_key: str,
                   user_id: Optional[str] = None) -> bool:
        """
        发送视频消息

        Args:
            video_path: 视频文件路径
            cover_image_key: 视频封面 image_key（需提前通过 upload_image 获取）
            user_id: 收件人 open_id
        """
        file_key = self.upload_file(video_path, "mp4")
        if not file_key:
            return False
        return self._send_by_key("media", file_key, user_id, extra={"image_key": cover_image_key})

    def _send_by_key(self, msg_type: str, file_key: str,
                     user_id: Optional[str] = None,
                     extra: Optional[Dict] = None,
                     chat_id: Optional[str] = None,
                     is_group: bool = False) -> bool:
        """通用：通过 file_key/image_key 发送媒体类消息"""
        if is_group and chat_id:
            target = chat_id
            id_type = "chat_id"
        else:
            target = user_id or self.default_user_id
            id_type = "open_id"

        if not target:
            logger.error("未指定收件人")
            return False

        content = {"file_key": file_key}
        if extra:
            content.update(extra)

        result = self._api_call("POST", f"/im/v1/messages?receive_id_type={id_type}", {
            "receive_id": target,
            "msg_type": msg_type,
            "content": json.dumps(content)
        })

        msg_name = {"file": "文件", "audio": "音频", "media": "视频",
                     "image": "图片", "text": "文本", "post": "富文本", "interactive": "卡片"}
        label = msg_name.get(msg_type, msg_type)
        if result.get("code") == 0:
            logger.info(f"{label}消息发送成功: message_id={result['data'].get('message_id')}")
            return True
        else:
            logger.error(f"{label}消息发送失败: {result.get('msg')}")
            return False

    # ===== 富文本消息 (post) =====

    def send_post(self, title: str, paragraphs: list, user_id: Optional[str] = None) -> bool:
        """
        发送富文本消息（支持加粗/链接/分段/Markdown）

        Args:
            title: 消息标题
            paragraphs: 段落列表，每个元素可以是：
                - str: 纯文本
                - {"tag": "md", "text": "**Markdown**"}
                - {"tag": "a", "text": "链接文字", "href": "https://..."}
            user_id: 收件人 open_id

        Returns:
            True 发送成功，False 发送失败
        """
        target = user_id or self.default_user_id
        if not target:
            logger.error("未指定收件人")
            return False

        content_lines = []
        for para in paragraphs:
            if isinstance(para, str):
                content_lines.append([{"tag": "text", "text": para}])
            elif isinstance(para, dict):
                content_lines.append([para])

        payload = {
            "receive_id": target,
            "msg_type": "post",
            "content": json.dumps({
                "zh_cn": {
                    "title": title,
                    "content": content_lines
                }
            })
        }

        result = self._api_call("POST", "/im/v1/messages?receive_id_type=open_id", payload)

        if result.get("code") == 0:
            logger.info(f"富文本消息发送成功: message_id={result['data'].get('message_id')}")
            return True
        else:
            logger.error(f"富文本消息发送失败: {result.get('msg')}")
            return False

    # ===== 交互卡片 (interactive) =====

    def send_card(self, header_title: str, header_template: str,
                  elements: list, user_id: Optional[str] = None) -> bool:
        """
        发送交互卡片消息

        Args:
            header_title: 卡片标题
            header_template: 颜色模板
                (blue/red/green/orange/grey/carmine)
            elements: 卡片元素列表
                [{"tag": "markdown", "content": "**文字**"},
                 {"tag": "hr"},
                 {"tag": "note", "elements": [...]}]
            user_id: 收件人 open_id

        Returns:
            True 发送成功，False 发送失败
        """
        target = user_id or self.default_user_id
        if not target:
            logger.error("未指定收件人")
            return False

        card = {
            "header": {
                "template": header_template,
                "title": {"tag": "plain_text", "content": header_title}
            },
            "elements": elements
        }

        payload = {
            "receive_id": target,
            "msg_type": "interactive",
            "content": json.dumps(card)
        }

        result = self._api_call("POST", "/im/v1/messages?receive_id_type=open_id", payload)

        if result.get("code") == 0:
            logger.info(f"卡片消息发送成功: message_id={result['data'].get('message_id')}")
            return True
        else:
            logger.error(f"卡片消息发送失败: {result.get('msg')}")
            return False


# ===== 快捷函数 =====

_bot_instance: Optional[FeiShuBot] = None


def _get_bot() -> FeiShuBot:
    global _bot_instance
    if _bot_instance is None:
        _bot_instance = FeiShuBot()
    return _bot_instance


def bot_notify(text: str) -> bool:
    """
    快捷发送文本消息

    用法：
        from feishu_bot import bot_notify
        bot_notify("任务完成！")
    """
    return _get_bot().send_text(text)
