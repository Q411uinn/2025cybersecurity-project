import cv2
import numpy as np

def load_image(path, grayscale=False):
    if grayscale:
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    else:
        img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"图片文件未找到: {path}")
    return img

def save_image(path, img):
    cv2.imwrite(path, img)

def normalized_correlation(img1, img2):
    a = img1.flatten().astype(np.float32)
    b = img2.flatten().astype(np.float32)
    numerator = np.dot(a, b)
    denominator = np.linalg.norm(a) * np.linalg.norm(b) + 1e-10
    return numerator / denominator
