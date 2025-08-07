<<<<<<< HEAD
# 2025cybersecurity-project
2025网络空间安全创新实践
=======
# SM4 Software Optimization Project

本项目实现了 SM4 国密对称加密算法的基础版本，支持完整的密钥扩展、加密与解密流程，作为后续各种优化版本的基础参考。

## 📁 项目结构
```
project1-sm4-optimization/
├── src/
│ ├── basic/ # 基础实现代码
│ ├── simd/ # SIMD优化实现
│ └── aesni/ # AES-NI优化实现
├── tests/ # 功能测试代码
├── benchmarks/ # 性能测试代码
├── Makefile # 编译脚本
├── build.bat # Windows下编译脚本
└── README.md # 项目说明
```

## 编译与运行

### 使用 Make 编译

```bash
make all          # 编译所有版本及基准测试
make basic        # 仅编译基础版本
make simd         # 编译SIMD优化版本
make aesni        # 编译AES-NI优化版本
make clean        # 清理可执行文件
```

### 运行测试
```bash
./test_sm4_basic
./test_sm4_simd
./test_sm4_aesni
```

### 性能测试
```bash
make benchmark-all
```

## ✅ 功能特性
- 支持16字节密钥的密钥扩展
- 基础实现兼容国标GM/T 0002-2012
- SIMD并行加速（SSE指令集）
- AES-NI指令集加速
- 模块清晰、易扩展

---

如果你有任何问题或建议，欢迎提 Issue 或 Pull Request！
