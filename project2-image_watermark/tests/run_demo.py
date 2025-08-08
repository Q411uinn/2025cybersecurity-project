import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core_watermark import embed_watermark, extract_watermark
import cv2
import os

def main():
    os.makedirs('output', exist_ok=True)

    cover_path = 'samples/cover.jpg'
    watermark_path = 'samples/logo.png'

    cover = cv2.imread(cover_path)
    watermark = cv2.imread(watermark_path)

    if cover is None or watermark is None:
        print("请确保 samples 文件夹里有 cover.jpg 和 logo.png")
        return

    alpha = 0.08
    print("开始嵌入水印...")
    watermarked = embed_watermark(cover, watermark, alpha=alpha)
    watermarked_path = 'output/watermarked.jpg'
    cv2.imwrite(watermarked_path, watermarked)
    print(f"水印图已保存：{watermarked_path}")

    print("开始提取水印...")
    extracted = extract_watermark(watermarked, cover, watermark.shape[:2], alpha=alpha)
    extracted_path = 'output/extracted_watermark.png'
    cv2.imwrite(extracted_path, extracted)
    print(f"提取的水印已保存：{extracted_path}")

if __name__ == '__main__':
    main()

