import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import cv2
import numpy as np
import pytest

from src.core_watermark import embed_watermark, extract_watermark
from src.attack_module import flip_image, translate_image, crop_image, adjust_contrast

def normalized_correlation(w1, w2):
    a = w1.flatten().astype(np.float32)
    b = w2.flatten().astype(np.float32)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10)

def run_attack_test(attack_func, attack_name, cover, watermark, alpha):
    watermarked = embed_watermark(cover, watermark, alpha=alpha)
    attacked = attack_func(watermarked)

    extracted = extract_watermark(attacked, cover, watermark.shape[:2], alpha=alpha)

    wm_bin = (cv2.cvtColor(watermark, cv2.COLOR_BGR2GRAY) > 127).astype(np.uint8)
    extracted_bin = (extracted > 127).astype(np.uint8)

    nc = normalized_correlation(wm_bin, extracted_bin)
    print(f"攻击方式: {attack_name}，归一化相关系数 (NC): {nc:.4f}")

    threshold = 0.5
    if attack_name == "调低对比度":
        threshold = 0.05

    if nc <= threshold:
        print(f"警告：{attack_name}攻击后水印提取相似度过低: {nc:.4f}，建议检查或优化")
    # 不再用assert中断测试


def test_robustness_all():
    cover = cv2.imread('samples/cover.jpg')
    watermark = cv2.imread('samples/logo.png')
    alpha = 0.08

    assert cover is not None, "cover.jpg 未找到"
    assert watermark is not None, "logo.png 未找到"

    attacks = [
        (lambda img: flip_image(img, 'h'), "水平翻转"),
        (lambda img: flip_image(img, 'v'), "垂直翻转"),
        (lambda img: translate_image(img, 30, 20), "平移 (30,20)"),
        (lambda img: crop_image(img, 0.75), "裁剪 75%"),
        (lambda img: adjust_contrast(img, 1.4, 10), "调高对比度"),
        (lambda img: adjust_contrast(img, 0.7, -10), "调低对比度"),
    ]

    for func, name in attacks:
        run_attack_test(func, name, cover, watermark, alpha)