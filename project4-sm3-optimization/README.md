# project4-sm3-optimization

本项目实现了 SM3 哈希算法，包含基础版本和基于 AVX2 指令的 SIMD 优化版本。支持性能测试，方便对比不同实现的效率

## 目录结构

project4-sm3-optimization/
├── src/
│   ├── basic/           # 基础版 SM3 实现
│   ├── simd/            # SIMD 优化实现（AVX2）
│   └── common/          # 通用头文件和工具代码
├── tests/
│   └── benchmark_simd.c # 性能测试代码
├── build/               # 编译生成文件目录
├── README.md            # 本说明文件


## 编译步骤

1. 创建输出目录：
```bash
mkdir build
```

2. 编译项目：
```bash
gcc -O3 -mavx2 -Wall -I./src/common tests/benchmark_simd.c src/basic/sm3_basic.c src/simd/sm3_simd.c -o build/benchmark_simd.exe
```
3. 运行性能测试：
```bash
.\build\benchmark_simd.exe
```

## 功能特点

- 基础版实现：纯 C 语言实现，结构清晰，便于理解。
- SIMD 优化版：利用 AVX2 指令集提升计算速度，性能显著改善。
- 性能测试：对比两种实现的速度和吞吐率，直观体现优化效果。利用 AVX2 指令集提升计算速度，性能显著改善。

## 运行示例

运行性能测试程序后，你会看到类似输出：

```bash
Benchmark SM3: 8000 blocks (64 bytes each), repeat=10
Basic avg time: 0.002134 s, throughput: 228.76 MB/s
SIMD  avg time: 0.000645 s, throughput: 756.80 MB/s

```