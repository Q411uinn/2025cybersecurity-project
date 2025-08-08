import cv2
import numpy as np

def flip_image(image, mode='h'):
    if mode == 'h':
        return cv2.flip(image, 1)  # 水平翻转
    elif mode == 'v':
        return cv2.flip(image, 0)  # 垂直翻转
    else:
        raise ValueError("mode must be 'h' or 'v'")

def translate_image(image, tx, ty):
    rows, cols = image.shape[:2]
    M = np.float32([[1, 0, tx], [0, 1, ty]])
    return cv2.warpAffine(image, M, (cols, rows))

def crop_image(image, ratio=0.75):
    h, w = image.shape[:2]
    ch, cw = int(h * ratio), int(w * ratio)
    start_x = (w - cw) // 2
    start_y = (h - ch) // 2
    cropped = image[start_y:start_y+ch, start_x:start_x+cw]
    # 放回原尺寸，填充黑边
    result = np.zeros_like(image)
    result[start_y:start_y+ch, start_x:start_x+cw] = cropped
    return result

def adjust_contrast(image, alpha=1.0, beta=0):
    """
    线性调整对比度和亮度，避免gamma变换导致信息丢失严重。
    alpha: 对比度系数 >0，1不变，推荐0.5~1.5
    beta: 亮度调节，整数，-50~50
    """
    img = image.astype(np.float32)
    img_adj = img * alpha + beta
    img_adj = np.clip(img_adj, 0, 255)
    return img_adj.astype(np.uint8)

