import streamlit as st
from pathlib import Path
import time
import uuid
from utils import handle_pdf_processing, translate_word_document, init_page

init_page("文档翻译", "📄", "wide")

st.title("📄 文档翻译")

# 目标语言选择 - 放在主界面顶部
col_lang1, col_lang2 = st.columns([1, 3])
with col_lang1:
    target_language = st.selectbox(
        "🎯 选择目标语言",
        ["中文", "英语", "日语", "法语", "德语", "西班牙语", "俄语", "韩语", "意大利语", "葡萄牙语", "阿拉伯语"],
        index=1
    )

st.markdown("---")

# 初始化 session_state
if "docx_path" not in st.session_state:
    st.session_state.docx_path = None
if "translated_path" not in st.session_state:
    st.session_state.translated_path = None
if "original_filename" not in st.session_state:
    st.session_state.original_filename = None


def save_uploaded_file(uploaded_file, temp_dir: Path) -> str:
    """
    保存上传的文件到临时目录
    
    参数:
        uploaded_file: Streamlit上传的文件对象
        temp_dir: 临时目录路径
    
    返回:
        str: 保存的文件路径
    """
    # 确保临时目录存在
    temp_dir.mkdir(exist_ok=True)
    
    # 生成唯一文件名
    unique_id = str(uuid.uuid4())
    file_extension = Path(uploaded_file.name).suffix
    file_path = temp_dir / f"uploaded_{unique_id}{file_extension}"
    
    # 保存文件
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return str(file_path)


def cleanup_temp_files(temp_dir: Path, keep_files: list = None):
    """
    清理临时文件夹中的文件
    
    参数:
        temp_dir: 临时目录路径
        keep_files: 需要保留的文件列表（完整路径）
    """
    if not temp_dir.exists():
        return
    
    keep_files = keep_files or []
    keep_paths = [Path(f) for f in keep_files]
    
    # 清理超过1小时的文件
    current_time = time.time()
    for file_path in temp_dir.iterdir():
        if file_path.is_file():
            # 如果文件在保留列表中，跳过
            if file_path in keep_paths:
                continue
            
            # 如果文件超过1小时，删除
            try:
                file_age = current_time - file_path.stat().st_mtime
                if file_age > 3600:  # 1小时 = 3600秒
                    file_path.unlink()
            except Exception as e:
                # 如果删除失败，忽略（可能文件正在使用）
                pass


# 侧边栏提示信息
st.sidebar.header("💡 使用提示")
st.sidebar.info("**支持格式：**\n\n- PDF 文档（自动转换为 Word）\n- Word 文档 (.docx)\n\n**注意事项：**\n\n- 扫描版 PDF 暂不支持\n- 翻译可能需要一些时间\n- 临时文件会自动清理")

# 主界面
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📤 上传文档")
    
    # 文件上传组件
    uploaded_file = st.file_uploader(
        "选择要翻译的文档",
        type=['docx', 'pdf'],
        help="支持 PDF 和 Word (.docx) 格式"
    )
    
    # 处理上传的文件
    if uploaded_file is not None:
        st.info(f"📎 已选择文件：**{uploaded_file.name}**")
        
        # 创建临时目录
        temp_dir = Path("temp")
        temp_dir.mkdir(exist_ok=True)
        
        # 根据文件类型处理
        file_extension = Path(uploaded_file.name).suffix.lower()
        
        if file_extension == '.pdf':
            # 情况A：处理PDF文件
            st.info("🔄 正在处理 PDF 文件...")
            
            with st.spinner("检查PDF文件并转换为Word格式..."):
                docx_path, error_msg = handle_pdf_processing(uploaded_file)
                
                if error_msg:
                    st.error(f"❌ **处理失败：** {error_msg}")
                    st.session_state.docx_path = None
                else:
                    st.success("✅ PDF 已成功转换为 Word 格式！")
                    st.session_state.docx_path = docx_path
                    st.session_state.original_filename = uploaded_file.name
        
        elif file_extension == '.docx':
            # 情况B：处理Word文件
            st.info("📄 正在保存 Word 文件...")
            
            with st.spinner("保存文件到临时目录..."):
                try:
                    docx_path = save_uploaded_file(uploaded_file, temp_dir)
                    st.success("✅ Word 文件已准备就绪！")
                    st.session_state.docx_path = docx_path
                    st.session_state.original_filename = uploaded_file.name
                except Exception as e:
                    st.error(f"❌ **保存失败：** {str(e)}")
                    st.session_state.docx_path = None

with col2:
    st.subheader("🌐 翻译结果")
    
    # 检查是否有可用的Word文件路径
    if st.session_state.docx_path and Path(st.session_state.docx_path).exists():
        st.success("✅ 文档已准备就绪，可以开始翻译")
        
        # 显示文件信息
        file_info = Path(st.session_state.docx_path)
        st.caption(f"📄 文件：{st.session_state.original_filename}")
        st.caption(f"🎯 目标语言：{target_language}")
        
        # 开始翻译按钮
        translate_button = st.button("🚀 开始翻译", type="primary", use_container_width=True)
        
        if translate_button:
            # 创建进度显示区域
            progress_container = st.container()
            with progress_container:
                progress_bar = st.progress(0)
                status_text = st.empty()
                stats_text = st.empty()
            
            # 定义进度回调函数
            def update_progress(current, total, status):
                if total > 0:
                    progress = current / total
                    progress_bar.progress(progress)
                    percentage = int(progress * 100)
                    stats_text.markdown(f"**进度：** {current}/{total} ({percentage}%)")
                else:
                    stats_text.empty()
                status_text.markdown(f"📝 {status}")
            
            try:
                # 调用翻译函数，传入进度回调
                translated_path = translate_word_document(
                    st.session_state.docx_path,
                    target_language,
                    progress_callback=update_progress
                )
                
                # 完成时更新进度条和状态
                progress_bar.progress(1.0)
                status_text.markdown("✅ **翻译完成！**")
                stats_text.empty()
                
                st.session_state.translated_path = translated_path
                st.success("✅ **翻译完成！**")
                
                # 延迟后清空进度显示
                time.sleep(2)
                progress_bar.empty()
                status_text.empty()
                stats_text.empty()
                
            except Exception as e:
                error_msg = str(e)
                progress_bar.empty()
                status_text.empty()
                st.error(f"❌ **翻译失败**")
                st.error(f"**错误信息：** {error_msg}")
                
                # 提供解决建议
                if "连接" in error_msg or "timeout" in error_msg.lower():
                    st.info("💡 **建议：** 请检查网络连接，或稍后重试。")
                elif "API Key" in error_msg or "认证" in error_msg:
                    st.info("💡 **建议：** 请检查 `.streamlit/secrets.toml` 中的 API Key 配置。")
        
        # 显示下载按钮（如果翻译完成）
        if st.session_state.translated_path and Path(st.session_state.translated_path).exists():
            st.markdown("---")
            st.success("🎉 **翻译成功！** 您可以下载翻译后的文档了。")
            
            # 读取翻译后的文件内容
            with open(st.session_state.translated_path, "rb") as f:
                file_content = f.read()
            
            # 生成下载文件名
            original_name = Path(st.session_state.original_filename).stem if st.session_state.original_filename else "document"
            # 确保文件名是字符串
            download_filename = f"translated_{original_name}_{target_language}.docx"
            
            # 下载按钮
            st.download_button(
                label="📥 下载翻译后的文档",
                data=file_content,
                file_name=download_filename,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
                type="primary",
                key="download_btn"
            )
            
            # 清理提示
            st.caption("💡 下载完成后，临时文件将在1小时后自动清理")
    
    else:
        st.info("👆 请先上传文档")

# 页面底部：清理临时文件
st.markdown("---")
with st.expander("🗑️ 清理临时文件"):
    if st.button("清理所有临时文件（保留当前会话文件）"):
        temp_dir = Path("temp")
        keep_files = []
        if st.session_state.docx_path:
            keep_files.append(st.session_state.docx_path)
        if st.session_state.translated_path:
            keep_files.append(st.session_state.translated_path)
        
        cleanup_temp_files(temp_dir, keep_files)
        st.success("✅ 临时文件清理完成！")

# 自动清理：每次页面加载时清理旧文件
temp_dir = Path("temp")
if temp_dir.exists():
    keep_files = []
    if st.session_state.docx_path:
        keep_files.append(st.session_state.docx_path)
    if st.session_state.translated_path:
        keep_files.append(st.session_state.translated_path)
    cleanup_temp_files(temp_dir, keep_files)

