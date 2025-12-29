import streamlit as st
from utils import apply_custom_styles, parse_ppt_content, generate_pptx
from pathlib import Path

st.set_page_config(
    page_title="PPT 生成",
    page_icon="📊",
    layout="wide"
)

apply_custom_styles()

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

