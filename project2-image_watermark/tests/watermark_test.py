import cv2
import numpy as np
import pytest

from src.core_watermark import embed_watermark, extract_watermark

def test_embed_and_extract():
    cover = cv2.imread('samples/cover.jpg')
    watermark = cv2.imread('samples/logo.png')

    assert cover is not None, "cover.jpg not found in samples/"
    assert watermark is not None, "logo.png not found in samples/"

    alpha = 0.08

    watermarked_img = embed_watermark(cover, watermark, alpha=alpha)
    extracted_wm = extract_watermark(watermarked_img, cover, watermark.shape[:2], alpha=alpha)

    # 二值化水印比较
    wm_bin = (cv2.cvtColor(watermark, cv2.COLOR_BGR2GRAY) > 127).astype(np.uint8)
    extracted_bin = (extracted_wm > 127).astype(np.uint8)

    # 计算相似度
    nc = np.sum(wm_bin == extracted_bin) / wm_bin.size
    print(f"Normalized Correlation (NC): {nc:.4f}")

    assert nc > 0.7, "水印提取相似度太低，可能失败了"
