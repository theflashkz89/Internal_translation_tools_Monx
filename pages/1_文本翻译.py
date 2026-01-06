import streamlit as st
import streamlit.components.v1 as components
from utils import translate_text, init_page

init_page("文本翻译", "📝", "wide")


# 页面专用样式 - 仅包含本页面特有的布局调整
st.markdown("""
<style>
    /* 移除 Column Gap - 用于左右翻译框紧密连接 */
    [data-testid="column"] {
        padding: 0 !important;
    }
    
    [data-testid="stHorizontalBlock"] {
        gap: 0 !important;
    }

    /* 翻译框高度统一 */
    .stTextArea textarea {
        min-height: 500px !important;
        height: 500px !important;
    }

    /* 左侧文本框: 左圆角 */
    .stTextArea textarea[aria-label="Source Input"] {
        border-right: none !important;
        border-radius: 12px 0 0 12px !important;
    }
    
    /* 右侧文本框: 右圆角 */
    .stTextArea textarea[aria-label="Translation Result"] {
        border-left: none !important;
        border-radius: 0 12px 12px 0 !important;
    }
    
    /* 隐藏 Labels */
    .stTextArea label, .stSelectbox label {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# 弱化标题
st.markdown("<h1>📝 文本翻译</h1>", unsafe_allow_html=True)

# 常用语言列表
languages = ["中文", "英文", "意大利语", "德语"]

# 初始化 session_state
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""

# 布局：三列 [10, 2, 10]
col_left, col_mid, col_right = st.columns([10, 2, 10], gap="small") 

with col_left:
    input_text = st.text_area(
        "Source Input",
        height=500,
        placeholder="输入文本...",
        key="input_text",
        label_visibility="collapsed"
    )

with col_mid:
    # 语言选择器
    target_language = st.selectbox(
        "目标语言",
        options=languages,
        index=1,  # 默认选择"英文"
        key="target_language",
        label_visibility="collapsed"
    )
    
    # 视觉分割线 (模拟两个文本框中间的线条)
    # 使用绝对定位或高容器来绘制
    st.markdown("""
    <div style="
        height: 450px; 
        border-right: 1px solid #e0e0e0; 
        width: 50%; 
        margin-top: 10px;
    "></div>
    """, unsafe_allow_html=True)

with col_right:
    result_text = st.text_area(
        "Translation Result",
        value=st.session_state.translated_text,
        height=500,
        key="output_text",
        label_visibility="collapsed",
        disabled=True
    )
    
    # 复制按钮 (仅当有结果时显示) - 移至右侧列底部
    if st.session_state.translated_text:
        import json
        escaped_text = json.dumps(st.session_state.translated_text)
        
        copy_button_html = f"""
        <div style="margin-top: 10px;">
            <button 
                id="copyBtn" 
                style="
                    width: 100%;
                    padding: 10px;
                    background-color: white;
                    color: #555;
                    border: 1px solid #eee;
                    border-radius: 8px;
                    font-size: 14px;
                    cursor: pointer;
                "
                onmouseover="this.style.backgroundColor='#f9f9f9'"
                onmouseout="this.style.backgroundColor='white'"
            >
                📋 复制译文
            </button>
        </div>
        
        <script>
        (function() {{
            const text = {escaped_text};
            const copyBtn = document.getElementById('copyBtn');
            
            if (!copyBtn) {{
                setTimeout(arguments.callee, 100);
                return;
            }}
            
            copyBtn.addEventListener('click', function() {{
                if (navigator.clipboard) {{
                    navigator.clipboard.writeText(text);
                    copyBtn.innerText = '✅ 已复制';
                    setTimeout(() => copyBtn.innerText = '📋 复制译文', 2000);
                }} else {{
                    const textarea = document.createElement('textarea');
                    textarea.value = text;
                    document.body.appendChild(textarea);
                    textarea.select();
                    document.execCommand('copy');
                    document.body.removeChild(textarea);
                    copyBtn.innerText = '✅ 已复制';
                    setTimeout(() => copyBtn.innerText = '📋 复制译文', 2000);
                }}
            }});
        }})();
        </script>
        """
        components.html(copy_button_html, height=60)

# 翻译按钮 (底部全宽)
translate_button = st.button("翻译", type="primary", use_container_width=True)


# 处理翻译逻辑
if translate_button:
    if not input_text.strip():
        st.warning("⚠️ 请输入要翻译的文本！")
    else:
        with st.spinner("Translating..."):
            try:
                translated = translate_text(input_text, target_language)
                st.session_state.translated_text = translated
                st.rerun()
            except Exception as e:
                st.error(f"❌ 翻译失败: {str(e)}")

