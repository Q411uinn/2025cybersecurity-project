# Project2 - Image Watermarking System

## 项目简介
本项目实现了基于数字图像的水印嵌入与提取功能，支持对图像进行鲁棒性测试，包括翻转、平移、裁剪、调节对比度等攻击。代码结构清晰，便于扩展和二次开发。


## 目录结构

```
project2-image-watermark/
├── src/ # 源代码
│ ├── core_watermark.py # 核心水印算法
│ ├── attack_module.py # 图像攻击测试模块
│ └── helper_funcs.py # 工具函数
├── tests/ # 测试代码
│ ├── watermark_test.py # 功能测试
│ └── robustness_test.py # 鲁棒性测试
├── samples/ # 测试样例图片
├── output/ # 输出结果目录
├── docs/ # 项目文档
│ └── 设计文档.md
└── README.md # 项目说明文件
```

---

## 环境依赖

- Python 3.7+
- OpenCV
- NumPy
- pytest (用于测试)

可通过如下命令安装依赖：
```bash
python -m venv venv_watermark
# Windows PowerShell 激活虚拟环境
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\venv_watermark\Scripts\activate

# 安装项目依赖
pip install -r requirements.txt
```

---

## 使用说明

### 1. 演示水印嵌入与提取

```bash
python tests/run_demo.py

```

会自动完成：

- 从 `samples/cover.jpg` 载入封面图  
- 从 `samples/logo.png` 载入水印图  
- 嵌入水印，保存含水印图到 `output/watermarked.jpg`  
- 提取水印，保存提取结果到 `output/extracted_watermark.png`  

---

### 2. 功能测试（自动化）

```bash
pytest tests/watermark_test.py -v
```

验证水印嵌入和提取功能是否正确。

---

### 3. 鲁棒性测试（攻击测试）

```bash
pytest tests/robustness_test.py -v
```

会对含水印图施加翻转、平移、裁剪、调对比度等攻击，验证提取水印的鲁棒性。

---

## 代码结构说明

-src/core_watermark.py：实现水印嵌入和提取的核心算法

-src/attack_module.py：实现各种图像攻击函数（翻转、平移、裁剪、对比度调整）

-src/helper_funcs.py：常用的辅助函数

-tests/：测试用例，包含功能测试和鲁棒性测试

-samples/：放置测试图片

-output/：存放测试运行输出的结果图片和日志

---

## 注意事项

- 请确保 `samples/` 目录下有有效的 `cover.jpg` 和 `logo.png`，推荐大小合适，清晰对比明显  
- 不同攻击可能对水印提取影响较大，调整参数可提升鲁棒性
- Python 环境推荐使用虚拟环境隔离依赖 
- 欢迎根据需求进行二次开发和改进  

---


