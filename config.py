"""
配置文件
用于管理应用的配置信息，包括 API 密钥等
"""

import os
from typing import Optional

# DeepSeek API 配置
# 从环境变量或 Streamlit secrets 中读取 API 密钥
DEEPSEEK_API_KEY: Optional[str] = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_BASE: str = "https://api.deepseek.com/v1"
DEEPSEEK_MODEL: str = "deepseek-chat"  # 默认模型

# DeepL API 配置
# 从环境变量或 Streamlit secrets 中读取 API 密钥
DEEPL_API_KEY: Optional[str] = None
try:
    # 尝试从 Streamlit secrets 获取
    import streamlit as st
    if hasattr(st, 'secrets') and hasattr(st.secrets, 'get'):
        DEEPL_API_KEY = st.secrets.get("DEEPL_API_KEY")
except:
    pass

# 如果 secrets 中没有，尝试从环境变量获取
if not DEEPL_API_KEY:
    DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")

# 应用配置
APP_TITLE: str = "AI Office Assistant"
APP_DESCRIPTION: str = "智能办公助手 - 使用 AI 处理 Word 和 PPT 文档"

# 文件上传限制
MAX_FILE_SIZE_MB: int = 50  # 最大文件大小（MB）
ALLOWED_WORD_EXTENSIONS: list = [".docx", ".doc"]
ALLOWED_PPT_EXTENSIONS: list = [".pptx", ".ppt"]

# AI 请求配置
DEFAULT_TEMPERATURE: float = 0.7
DEFAULT_MAX_TOKENS: int = 2000
