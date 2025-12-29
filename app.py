import streamlit as st
import os
from utils import apply_custom_styles, translate_text, handle_pdf_processing, translate_word_document

# 1. 页面配置
st.set_page_config(page_title="智能翻译助手", page_icon="🌐", layout="wide")
apply_custom_styles()

# 2. 侧边栏导航
with st.sidebar:
    st.header("功能菜单")
    selected_page = st.radio(
        "请选择功能:", 
        ["📝 在线文本翻译", "📂 文档文件翻译", "📊 PPT生成"]
    )
    st.markdown("---")
    st.caption("v2.1 Stable")

# ==================================================
# 页面 1: 在线文本翻译
# ==================================================
if selected_page == "📝 在线文本翻译":
    st.title("📝 在线文本翻译")
    st.markdown("使用 DeepL 引擎进行精准翻译")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        source_text = st.text_area("输入原文", height=300, placeholder="在此输入需要翻译的文本...")
    with col2:
        target_lang = st.selectbox(
            "目标语言", 
            ["中文", "英语", "日语", "法语", "德语", "西班牙语", "俄语", "韩语"], 
            index=1,
            key="text_lang"
        )
        # 结果占位符
        result_area = st.empty()
    
    if st.button("开始翻译", type="primary"):
        if not source_text:
            st.warning("请输入需要翻译的文本")
        else:
            try:
                with st.spinner("正在翻译..."):
                    result = translate_text(source_text, target_lang)
                    with col2:
                        st.success("翻译完成")
                        st.text_area("译文", value=result, height=250)
            except Exception as e:
                st.error(f"翻译出错: {str(e)}")

# ==================================================
# 页面 2: 文档文件翻译
# ==================================================
elif selected_page == "📂 文档文件翻译":
    st.title("📂 文档文件翻译")
    st.markdown("支持上传 Word (.docx) 或 PDF 文件，保持原有排版。")
    
    # 文件上传
    uploaded_file = st.file_uploader("上传文件", type=["docx", "pdf"])
    
    col1, col2 = st.columns([1, 2])
    with col1:
        target_lang_doc = st.selectbox(
            "文档目标语言", 
            ["中文", "英语", "日语", "法语", "德语"], 
            index=1,
            key="doc_lang"
        )
    
    if uploaded_file and st.button("开始处理文档", type="primary"):
        try:
            with st.spinner("正在处理文件，请稍候..."):
                # 1. 创建临时目录并保存文件
                temp_dir = "temp"
                if not os.path.exists(temp_dir):
                    os.makedirs(temp_dir)
                    
                file_path = os.path.join(temp_dir, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # 2. 预处理 (PDF 转 Word)
                process_path = file_path
                if uploaded_file.name.lower().endswith(".pdf"):
                    st.info("检测到 PDF 文件，正在尝试转换为 Word...")
                    converted_path, error = handle_pdf_processing(uploaded_file)
                    if error:
                        st.error(error)
                        st.stop()
                    process_path = converted_path
                
                # 3. 执行翻译 (带进度条)
                st.info("正在翻译文档段落...")
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                def update_progress(current, total, msg):
                    if total > 0:
                        progress = min(current / total, 1.0)
                        progress_bar.progress(progress)
                    status_text.text(msg)
                
                output_path = translate_word_document(
                    process_path, 
                    target_lang_doc, 
                    progress_callback=update_progress
                )
                
                # 4. 完成并下载
                st.success("✅ 文档翻译完成！")
                with open(output_path, "rb") as f:
                    file_data = f.read()
                    st.download_button(
                        label="⬇️ 下载翻译后的文档",
                        data=file_data,
                        file_name=f"Translated_{uploaded_file.name}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                    
        except Exception as e:
            st.error(f"处理文档时发生错误: {str(e)}")
            import traceback
            st.code(traceback.format_exc())

# ==================================================
# 页面 3: PPT生成
# ==================================================
elif selected_page == "📊 PPT生成":
    from utils import parse_ppt_content, generate_pptx
    
    st.title("📊 PPT 生成")
    st.markdown("将文本内容转换为 PowerPoint 演示文稿")
    
    # 使用说明
    with st.expander("📖 使用说明", expanded=False):
        st.markdown("""
        **支持的内容格式：**
        
        ```
        Slide 1: 第一页标题
        - 内容要点1
        - 内容要点2
        
        Slide 2: 第二页标题
        - 更多内容
        ```
        
        或者：
        
        ```
        第一页：标题
        内容...
        
        第二页：标题
        内容...
        ```
        """)
    
    # 输入区域
    st.subheader("📝 输入内容")
    ppt_content = st.text_area(
        "粘贴 PPT 内容",
        height=400,
        placeholder="在此粘贴 AI 生成的 PPT 内容...\n\n示例：\nSlide 1: 项目介绍\n- 背景说明\n- 目标定义\n\nSlide 2: 主要内容\n- 要点一\n- 要点二"
    )
    
    # 生成按钮
    if st.button("🚀 生成 PPT", type="primary", use_container_width=True):
        if not ppt_content.strip():
            st.warning("⚠️ 请输入 PPT 内容")
        else:
            with st.spinner("正在生成 PPT..."):
                try:
                    # 解析内容
                    slides = parse_ppt_content(ppt_content)
                    
                    if not slides:
                        st.error("❌ 无法解析内容，请检查格式")
                    else:
                        st.info(f"📑 已识别 {len(slides)} 页幻灯片")
                        
                        # 预览
                        with st.expander("📋 内容预览", expanded=True):
                            for i, slide in enumerate(slides, 1):
                                st.markdown(f"**第 {i} 页: {slide.get('title', '无标题')}**")
                                for item in slide.get('content', []):
                                    st.markdown(f"  - {item}")
                                st.markdown("---")
                        
                        # 生成 PPTX
                        output_path = generate_pptx(slides)
                        
                        # 提供下载
                        with open(output_path, "rb") as f:
                            st.download_button(
                                label="📥 下载 PPT 文件",
                                data=f.read(),
                                file_name="generated_presentation.pptx",
                                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                                type="primary",
                                use_container_width=True
                            )
                        
                        st.success("✅ PPT 生成成功！")
                        
                except Exception as e:
                    st.error(f"❌ 生成失败: {str(e)}")
