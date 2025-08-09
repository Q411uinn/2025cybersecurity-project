@echo off
if not exist build mkdir build
gcc -O3 -mavx2 -Wall -I./src/common tests/benchmark_simd.c src/basic/sm3_basic.c src/simd/sm3_simd.c -o build\benchmark_simd.exe
if errorlevel 1 (
    echo 编译失败，请检查 gcc 和 AVX2 支持。
    pause
    exit /b 1
)
echo 正在运行性能测试...
build\benchmark_simd.exe
pause
