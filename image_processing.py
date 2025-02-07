import argparse
import torch
import torch.nn as nn
from network.Math_Module import P, Q
from network.decom import Decom
import os
import torchvision.transforms as transforms
from PIL import Image
from utils import *
import time
import cv2
import numpy as np


# 定义模型推理类
class Inference(nn.Module):
    def __init__(self, opts):
        super().__init__()
        self.opts = opts
        # 加载分解模型
        self.model_Decom_low = Decom()
        self.model_Decom_low = load_initialize(self.model_Decom_low, self.opts.Decom_model_low_path)
        # 加载 R, L 模型
        self.unfolding_opts, self.model_R, self.model_L = load_unfolding(self.opts.unfolding_model_path)
        # 加载调整模型
        self.adjust_model = load_adjustment(self.opts.adjust_model_path)
        self.P = P()
        self.Q = Q()
        transform = [
            transforms.ToTensor(),
        ]
        self.transform = transforms.Compose(transform)

    def unfolding(self, input_low_img):
        for t in range(self.unfolding_opts.round):
            if t == 0:  # 初始化 R0, L0
                P, Q = self.model_Decom_low(input_low_img)
            else:  # 更新 P 和 Q
                w_p = (self.unfolding_opts.gamma + self.unfolding_opts.Roffset * t)
                w_q = (self.unfolding_opts.lamda + self.unfolding_opts.Loffset * t)
                P = self.P(I=input_low_img, Q=Q, R=R, gamma=w_p)
                Q = self.Q(I=input_low_img, P=P, L=L, lamda=w_q)
            R = self.model_R(r=P, l=Q)
            L = self.model_L(l=Q)
        return R, L

    def lllumination_adjust(self, L, ratio):
        ratio = torch.ones(L.shape) * self.opts.ratio
        return self.adjust_model(l=L, alpha=ratio)

    def forward(self, input_low_img):
        if torch.cuda.is_available():
            input_low_img = input_low_img.cuda()
        with torch.no_grad():
            start = time.time()
            R, L = self.unfolding(input_low_img)
            High_L = self.lllumination_adjust(L, self.opts.ratio)
            I_enhance = High_L * R
            p_time = (time.time() - start)
        return I_enhance, p_time

    def runForWeb(self, image):
        if image is None:
            return None
        max_pixel_limit = 600 * 600
        pyr_down_times = 0
        while True:
            a = len(image)
            b = len(image[0])
            c = a * b
            if (c <= max_pixel_limit):
                break
            pyr_down_times += 1
            image = cv2.pyrDown(image)

        low_img = self.transform(Image.fromarray(np.uint8(image))).unsqueeze(0)
        enhance, p_time = self.forward(input_low_img=low_img)
        result_image = result_for_gradio(enhance)
        for i in range(pyr_down_times):
            result_image = cv2.pyrUp(result_image)
        return result_image


def result_for_gradio(enhance):
    img = np.squeeze(enhance.cpu().permute(0, 2, 3, 1).numpy())
    return img


def process_image(input_image_path, output_image_path, ratio):
    opts = argparse.Namespace(
        ratio=ratio,
        Decom_model_low_path="./ckpt/init_low.pth",
        unfolding_model_path="./ckpt/unfolding.pth",
        adjust_model_path="./ckpt/L_adjust.pth"
    )

    # 加载图像
    image = cv2.imread(input_image_path)
    if image is None:
        print(f"无法读取图像: {input_image_path}")
        return
    model = Inference(opts)
    enhanced_image = model.runForWeb(image)
    enhanced_image = np.clip(enhanced_image, 0, 1)
    cv2.imwrite(output_image_path, (enhanced_image * 255).astype(np.uint8))
    print(f"处理后的图像已保存到: {output_image_path}")


if __name__ == "__main__":
    input_path = "./demo/input/123.png"
    output_path = "./demo/output/123_enhanced.png"
    ratio = 1.0
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    process_image(input_path, output_path, ratio)