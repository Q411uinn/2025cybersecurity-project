<<<<<<< HEAD
# 2025cybersecurity-project
2025网络空间安全创新实践
=======
# SM4 Software Optimization Project

本项目实现了 SM4 国密对称加密算法的基础版本，支持完整的密钥扩展、加密与解密流程，作为后续各种优化版本的基础参考。

## 📁 项目结构
```
project1-sm4-optimization/
├── src/             # 源代码
│   └── basic/       # 基础实现（C语言）
├── tests/           # 功能测试
├── benchmarks/      # 性能测试
├── Makefile         # 构建配置
├── README.md        # 项目说明
```

## 🔧 构建与运行

### 编译测试程序
```bash
make
```

### 运行测试
```bash
make run
```

### 性能测试
```bash
make benchmark
```

## ✅ 功能特性
- 支持16字节密钥的密钥扩展
- 支持加密、解密流程
- 兼容国标GM/T 0002-2012
- 模块清晰、易扩展

---

### 4. src/basic/sm4_basic.h

```c
#ifndef SM4_BASIC_H
#define SM4_BASIC_H

#include <stdint.h>

void sm4_key_schedule(const uint8_t key[16], uint32_t rk[32]);
void sm4_encrypt_basic(const uint8_t in[16], uint8_t out[16], const uint32_t rk[32]);
void sm4_decrypt_basic(const uint8_t in[16], uint8_t out[16], const uint32_t rk[32]);

#endif // SM4_BASIC_H
>>>>>>> b9bd1d8 (Initial commit: SM4 optimized project)
