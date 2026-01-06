import streamlit as st
import streamlit.components.v1 as components
from utils import init_page, generate_email_draft
import json

init_page("邮件助手", "✉️", "wide")

st.title("✉️ 邮件助手")
st.markdown("使用 AI 协助您撰写专业的邮件草稿")

# 初始化 session_state
if "email_draft" not in st.session_state:
    st.session_state.email_draft = ""

# 邮件类型选择
email_type = st.selectbox(
    "📋 邮件类型",
    ["商务邮件", "感谢信", "请求邮件", "通知邮件", "回复邮件"],
    index=0,
    help="选择您要撰写的邮件类型"
)

# 语气风格选择
tone = st.selectbox(
    "🎭 语气风格",
    ["正式", "友好", "简洁", "礼貌"],
    index=0,
    help="选择邮件的语气风格"
)

# 邮件语言选择
language = st.selectbox(
    "🌐 邮件语言",
    ["中文", "英文", "意大利语"],
    index=1,
    help="选择邮件的撰写语言"
)

# 收件人称呼（可选）
recipient = st.text_input(
    "👤 收件人称呼（可选）",
    placeholder="例如：张总、Dear John、尊敬的客户",
    help="输入收件人的称呼，可以为空"
)

# 邮件主题
subject = st.text_input(
    "📌 邮件主题",
    placeholder="例如：关于项目进展的汇报",
    help="输入邮件的主题"
)

# 关键要点/背景信息
key_points = st.text_area(
    "📝 关键要点/背景信息",
    height=200,
    placeholder="在此输入邮件的关键要点、背景信息或需要包含的内容...\n\n例如：\n- 项目已完成第一阶段\n- 需要客户确认下一步计划\n- 预计下周五前完成",
    help="详细描述邮件需要包含的关键信息和背景"
)

# 生成按钮
if st.button("🚀 生成邮件", type="primary", use_container_width=True):
    if not subject.strip():
        st.warning("⚠️ 请输入邮件主题")
    elif not key_points.strip():
        st.warning("⚠️ 请输入关键要点或背景信息")
    else:
        with st.spinner("正在生成邮件草稿..."):
            try:
                draft = generate_email_draft(
                    email_type=email_type,
                    tone=tone,
                    language=language,
                    recipient=recipient,
                    subject=subject,
                    key_points=key_points
                )
                st.session_state.email_draft = draft
                st.rerun()
            except Exception as e:
                st.error(f"❌ 生成失败: {str(e)}")

# 显示生成的邮件草稿
if st.session_state.email_draft:
    st.markdown("---")
    st.subheader("📄 生成的邮件草稿")
    
    # 显示邮件内容
    st.text_area(
        "邮件正文",
        value=st.session_state.email_draft,
        height=300,
        key="email_result",
        label_visibility="collapsed"
    )
    
    # 复制按钮
    escaped_text = json.dumps(st.session_state.email_draft)
    
    copy_button_html = f"""
    <div style="margin-top: 10px;">
        <button 
            id="copyEmailBtn" 
            style="
                width: 100%;
                padding: 12px;
                background-color: #2b77ff;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 500;
                cursor: pointer;
            "
            onmouseover="this.style.backgroundColor='#1a60e0'"
            onmouseout="this.style.backgroundColor='#2b77ff'"
        >
            📋 复制邮件内容
        </button>
    </div>
    
    <script>
    (function() {{
        const text = {escaped_text};
        const copyBtn = document.getElementById('copyEmailBtn');
        
        if (!copyBtn) {{
            setTimeout(arguments.callee, 100);
            return;
        }}
        
        copyBtn.addEventListener('click', function() {{
            if (navigator.clipboard) {{
                navigator.clipboard.writeText(text);
                copyBtn.innerText = '✅ 已复制';
                copyBtn.style.backgroundColor = '#28a745';
                setTimeout(() => {{
                    copyBtn.innerText = '📋 复制邮件内容';
                    copyBtn.style.backgroundColor = '#2b77ff';
                }}, 2000);
            }} else {{
                const textarea = document.createElement('textarea');
                textarea.value = text;
                document.body.appendChild(textarea);
                textarea.select();
                document.execCommand('copy');
                document.body.removeChild(textarea);
                copyBtn.innerText = '✅ 已复制';
                copyBtn.style.backgroundColor = '#28a745';
                setTimeout(() => {{
                    copyBtn.innerText = '📋 复制邮件内容';
                    copyBtn.style.backgroundColor = '#2b77ff';
                }}, 2000);
            }}
        }});
    }})();
    </script>
    """
    components.html(copy_button_html, height=50)
    
    # 重新生成按钮
    if st.button("🔄 重新生成", use_container_width=True):
        st.session_state.email_draft = ""
        st.rerun()

