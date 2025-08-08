import cv2
import numpy as np

def embed_watermark(cover_img, watermark_img, alpha=0.1):
    cover_gray = cv2.cvtColor(cover_img, cv2.COLOR_BGR2GRAY)
    watermark_gray = cv2.cvtColor(watermark_img, cv2.COLOR_BGR2GRAY)
    watermark_resized = cv2.resize(watermark_gray, (cover_gray.shape[1], cover_gray.shape[0]))

    # 简单叠加水印
    watermarked = cv2.addWeighted(cover_gray, 1, watermark_resized, alpha, 0)
    watermarked_bgr = cv2.cvtColor(watermarked.astype(np.uint8), cv2.COLOR_GRAY2BGR)
    return watermarked_bgr

def extract_watermark(watermarked_img, original_img, watermark_shape, alpha=0.1):
    watermarked_gray = cv2.cvtColor(watermarked_img, cv2.COLOR_BGR2GRAY)
    original_gray = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)

    extracted = (watermarked_gray.astype(float) - original_gray.astype(float)) / alpha
    extracted = np.clip(extracted, 0, 255).astype(np.uint8)
    extracted_resized = cv2.resize(extracted, (watermark_shape[1], watermark_shape[0]))
    return extracted_resized
