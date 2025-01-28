import streamlit as st
import numpy as np
from PIL import Image
import test

st.title("URetinex-Net暗光增强模型")
st.sidebar.header("使用指南")
st.sidebar.write("""  
1. 上传一张图像。  
2. 使用滑块选择增强比例（1~10）。  
3. 上传图像后会自动输出增强后图像。
4. 用户可在图像输出后快捷使用滑块改变增强比例，以达到合适的增强效果。  
""")

# 上传图像
uploaded_file = st.file_uploader("选择一张图像进行上传", type=["jpg", "jpeg", "png"])

# 输入增强比例
ratio = st.slider("选择增强比例", min_value=1, max_value=10, value=5)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    image = np.array(image)
    st.image(image, caption="原始图像", use_container_width=True)
    enhanced_image = test.functionForStreamlit(image, ratio)
    st.image(enhanced_image, caption="增强后的图像", use_container_width=True)

    # 添加反馈输入框
    feedback = st.text_area("请提供反馈或建议：", height=100)
    if st.button("提交反馈"):
        if feedback:
            st.success("感谢您的反馈！")
        else:
            st.warning("请填写反馈内容。")

