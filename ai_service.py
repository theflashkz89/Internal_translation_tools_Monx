"""
AI 服务模块
负责与 DeepSeek API 的交互
"""

import openai
from typing import Optional, List, Dict, Any
from config import DEEPSEEK_API_KEY, DEEPSEEK_API_BASE, DEEPSEEK_MODEL, DEFAULT_TEMPERATURE, DEFAULT_MAX_TOKENS


class AIService:
    """AI 服务类，封装 DeepSeek API 调用"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化 AI 服务
        
        Args:
            api_key: DeepSeek API 密钥，如果为 None 则使用配置文件中的密钥
        """
        self.api_key = api_key or DEEPSEEK_API_KEY
        if not self.api_key:
            raise ValueError("未设置 DeepSeek API 密钥，请在环境变量或配置文件中设置 DEEPSEEK_API_KEY")
        
        # 初始化 OpenAI 客户端（DeepSeek 兼容 OpenAI SDK）
        self.client = openai.OpenAI(
            api_key=self.api_key,
            base_url=DEEPSEEK_API_BASE
        )
        self.model = DEEPSEEK_MODEL
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = DEFAULT_MAX_TOKENS
    ) -> str:
        """
        发送聊天请求到 DeepSeek API
        
        Args:
            messages: 消息列表，格式为 [{"role": "user", "content": "..."}]
            temperature: 温度参数，控制输出的随机性（0-1）
            max_tokens: 最大生成 token 数
        
        Returns:
            AI 返回的文本内容
        
        Raises:
            Exception: API 调用失败时抛出异常
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"AI API 调用失败: {str(e)}")
    
    def summarize_text(self, text: str, max_length: int = 500) -> str:
        """
        总结文本内容
        
        Args:
            text: 要总结的文本
            max_length: 总结的最大长度
        
        Returns:
            总结后的文本
        """
        prompt = f"""请总结以下文本内容，总结长度控制在 {max_length} 字以内：

{text}

总结："""
        
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        return self.chat_completion(messages, temperature=0.5)
    
    def translate_text(self, text: str, target_language: str = "英文") -> str:
        """
        翻译文本
        
        Args:
            text: 要翻译的文本
            target_language: 目标语言（如：英文、中文、日文等）
        
        Returns:
            翻译后的文本
        """
        prompt = f"""请将以下文本翻译成{target_language}，保持原意和格式：

{text}

翻译结果："""
        
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        return self.chat_completion(messages, temperature=0.3)
    
    def improve_text(self, text: str, instruction: str = "优化表达，使其更加专业和流畅") -> str:
        """
        改进文本内容
        
        Args:
            text: 要改进的文本
            instruction: 改进指令
        
        Returns:
            改进后的文本
        """
        prompt = f"""请根据以下要求改进文本：

要求：{instruction}

原文：
{text}

改进后的文本："""
        
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        return self.chat_completion(messages, temperature=0.7)
    
    def generate_content(self, topic: str, content_type: str = "文章", length: str = "中等") -> str:
        """
        生成内容
        
        Args:
            topic: 主题
            content_type: 内容类型（如：文章、摘要、大纲等）
            length: 长度（短、中等、长）
        
        Returns:
            生成的内容
        """
        length_map = {"短": 200, "中等": 500, "长": 1000}
        target_length = length_map.get(length, 500)
        
        prompt = f"""请根据以下主题生成一篇{content_type}：

主题：{topic}
长度：约 {target_length} 字

请开始生成："""
        
        messages = [
            {"role": "user", "content": prompt}
        ]
        
        return self.chat_completion(messages, max_tokens=target_length * 2)

