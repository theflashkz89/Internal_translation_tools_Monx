import streamlit as st
import streamlit.components.v1 as components
from utils import translate_text

st.set_page_config(
    page_title="文本翻译",
    page_icon="📝",
    layout="wide"
)

st.title("📝 文本翻译")

# 常用语言列表
languages = [
    "英语",
    "日语",
    "韩语",
    "法语",
    "德语",
    "西班牙语",
    "俄语",
    "意大利语",
    "葡萄牙语",
    "阿拉伯语",
    "泰语",
    "越南语",
    "印尼语",
    "荷兰语",
    "瑞典语",
    "挪威语",
    "丹麦语",
    "芬兰语",
    "波兰语",
    "土耳其语"
]

# 创建两列布局
col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 输入文本")
    input_text = st.text_area(
        "请输入要翻译的文本：",
        height=300,
        placeholder="在此输入需要翻译的文本...",
        key="input_text"
    )
    
    target_language = st.selectbox(
        "选择目标语言：",
        options=languages,
        index=0,
        key="target_language"
    )
    
    translate_button = st.button("🚀 开始翻译", type="primary", use_container_width=True)

with col2:
    st.subheader("📤 翻译结果")
    
    # 初始化 session_state
    if "translated_text" not in st.session_state:
        st.session_state.translated_text = ""
    
    if translate_button:
        if not input_text.strip():
            st.warning("⚠️ 请输入要翻译的文本！")
        else:
            with st.spinner("正在翻译中，请稍候..."):
                try:
                    translated = translate_text(input_text, target_language)
                    st.session_state.translated_text = translated
                    st.success("✅ 翻译完成！")
                except Exception as e:
                    error_msg = str(e)
                    st.error(f"❌ 翻译失败")
                    st.error(f"**错误信息：** {error_msg}")
                    
                    # 提供解决建议
                    if "连接" in error_msg or "timeout" in error_msg.lower():
                        st.info("💡 **建议：** 请检查网络连接，或稍后重试。")
                    elif "API Key" in error_msg or "认证" in error_msg:
                        st.info("💡 **建议：** 请检查 `.streamlit/secrets.toml` 中的 API Key 配置。")
                    
                    st.session_state.translated_text = ""
    
    # 显示翻译结果
    if st.session_state.translated_text:
        # 使用 text_area 显示结果
        result_text = st.text_area(
            "翻译结果：",
            value=st.session_state.translated_text,
            height=300,
            key="output_text",
            disabled=False  # 设置为可编辑，方便用户选择复制
        )
        
        # 创建自定义的复制按钮（使用 HTML + JavaScript）
        import json
        escaped_text = json.dumps(st.session_state.translated_text)
        
        copy_button_html = f"""
        <div style="margin-top: 10px;">
            <button 
                id="copyBtn" 
                style="
                    width: 100%;
                    padding: 10px;
                    background-color: #1f77b4;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-size: 16px;
                    cursor: pointer;
                    font-weight: bold;
                "
                onmouseover="this.style.backgroundColor='#1565a0'"
                onmouseout="this.style.backgroundColor='#1f77b4'"
            >
                📋 一键复制
            </button>
        </div>
        
        <script>
        (function() {{
            const text = {escaped_text};
            const copyBtn = document.getElementById('copyBtn');
            
            if (!copyBtn) {{
                // 如果按钮还没加载，等待一下
                setTimeout(arguments.callee, 100);
                return;
            }}
            
            copyBtn.addEventListener('click', function() {{
                copyToClipboard(text);
            }});
            
            function copyToClipboard(text) {{
                // 方法1: 使用现代 Clipboard API
                if (navigator.clipboard && window.isSecureContext) {{
                    navigator.clipboard.writeText(text).then(function() {{
                        showSuccess();
                    }}).catch(function(err) {{
                        console.log('Clipboard API failed, trying fallback:', err);
                        fallbackCopy(text);
                    }});
                }} else {{
                    fallbackCopy(text);
                }}
            }}
            
            function fallbackCopy(text) {{
                // 方法2: 使用传统方法
                const textarea = document.createElement('textarea');
                textarea.value = text;
                textarea.style.position = 'fixed';
                textarea.style.top = '0';
                textarea.style.left = '0';
                textarea.style.width = '2em';
                textarea.style.height = '2em';
                textarea.style.padding = '0';
                textarea.style.border = 'none';
                textarea.style.outline = 'none';
                textarea.style.boxShadow = 'none';
                textarea.style.background = 'transparent';
                textarea.style.opacity = '0';
                textarea.style.zIndex = '-1';
                document.body.appendChild(textarea);
                
                // 对于 iOS Safari
                if (navigator.userAgent.match(/ipad|iphone/i)) {{
                    const range = document.createRange();
                    range.selectNodeContents(textarea);
                    const selection = window.getSelection();
                    selection.removeAllRanges();
                    selection.addRange(range);
                    textarea.setSelectionRange(0, 999999);
                }} else {{
                    textarea.select();
                }}
                
                try {{
                    const successful = document.execCommand('copy');
                    if (successful) {{
                        showSuccess();
                    }} else {{
                        showError();
                    }}
                }} catch (err) {{
                    console.log('execCommand failed:', err);
                    showError();
                }}
                
                document.body.removeChild(textarea);
            }}
            
            function showSuccess() {{
                const successMsg = document.createElement('div');
                successMsg.textContent = '✅ 已复制到剪贴板！';
                successMsg.style.cssText = 'position: fixed; top: 20px; right: 20px; background: #4CAF50; color: white; padding: 15px 20px; border-radius: 5px; z-index: 10000; box-shadow: 0 4px 6px rgba(0,0,0,0.3); font-size: 14px; font-family: Arial, sans-serif;';
                document.body.appendChild(successMsg);
                setTimeout(function() {{ 
                    successMsg.style.transition = 'opacity 0.3s';
                    successMsg.style.opacity = '0';
                    setTimeout(function() {{ successMsg.remove(); }}, 300);
                }}, 2000);
            }}
            
            function showError() {{
                const errorMsg = document.createElement('div');
                errorMsg.textContent = '❌ 复制失败，请手动选择文本复制';
                errorMsg.style.cssText = 'position: fixed; top: 20px; right: 20px; background: #f44336; color: white; padding: 15px 20px; border-radius: 5px; z-index: 10000; box-shadow: 0 4px 6px rgba(0,0,0,0.3); font-size: 14px; font-family: Arial, sans-serif;';
                document.body.appendChild(errorMsg);
                setTimeout(function() {{ 
                    errorMsg.style.transition = 'opacity 0.3s';
                    errorMsg.style.opacity = '0';
                    setTimeout(function() {{ errorMsg.remove(); }}, 300);
                }}, 3000);
            }}
        }})();
        </script>
        """
        
        components.html(copy_button_html, height=80)
    else:
        st.info("👈 请在左侧输入文本并点击翻译按钮")

