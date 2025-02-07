---
title: URetinex Net 003
emoji: 💻
colorFrom: yellow
colorTo: blue
sdk: streamlit
sdk_version: 1.41.1
app_file: app.py
pinned: false
short_description: low light image enhance
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

---

# URetinex-Net 模型部署步骤：

欢迎使用 URetinex-Net！以下是部署和使用该模型进行低光图像增强的步骤。  

## 新闻更新  
增强版本 [URetinex-Net++](https://github.com/AndersonYong/URetinex-Net-PLUS) 已发布！我们发布了 URetinex-Net++ 的训练代码，该版本与 URetinex-Net 共享分解模块和展开模块。  

## URetinex-Net: 基于 Retinex 的深度展开网络用于低光图像增强  
URetinex-Net 是在 CVPR 2022 上公布的用于低光图像增强的 Retinex 基深度展开网络的官方 PyTorch 实现。  

![模型框架图](./figure/framework.png)  

[[论文]](https://openaccess.thecvf.com/content/CVPR2022/papers/Wu_URetinex-Net_Retinex-Based_Deep_Unfolding_Network_for_Low-Light_Image_Enhancement_CVPR_2022_paper.pdf)  
[[附录]](https://openaccess.thecvf.com/content/CVPR2022/supplemental/Wu_URetinex-Net_Retinex-Based_Deep_CVPR_2022_supplemental.pdf)  
[[视频]](https://www.youtube.com/watch?v=MJZ5HT1jGrA)  

## 环境要求  
请确保您的环境满足以下要求：  
1. python==3.8.20 
2. PyTorch == 2.4.1 
3. torchvision == 0.20.0cd
4. torchsummary==1.5.1
5. numpy==1.24.4
6. opencv_python==4.11.0.86
7. Pillow==11.1.0
8. streamlit==1.40.1

## 部署步骤  

### 1. 克隆项目  
首先，您需要将项目代码克隆到本地：  
```bash  
git clone https://github.com/JackPeng-0311/URetinex-Net-003.git  
cd URetinex-Net
```

### 2. 安装依赖
然后，使用pip命令安装项目所需的依赖项:
```bash  
pip install -r requirements.txt
```
### 3. 准备数据
如果您只想处理单个图像，请确保将要处理的图像放在.demo/input/目录下。

### 4. 运行代码
```bash  
streamlit run app.py
```

### 5. 测试和验证结果  
完成部署后，您可以通过以下步骤测试和验证图像增强的效果：  
1. **上传测试图像**：  
   在 Streamlit 应用程序界面中，您可以通过文件上传功能选择要增强的图像。  

2. **运行应用**：  
   上传图像后，模型将自动开始处理图像。  

3. **查看结果**：  
   增强后的图像将会在界面上显示，您可以与原图进行对比。  
