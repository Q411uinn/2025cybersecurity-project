@echo off
if not exist build mkdir build
gcc -O3 -mavx2 -Wall -I./src/common tests/benchmark_simd.c src/basic/sm3_basic.c src/simd/sm3_simd.c -o build\benchmark_simd.exe
if errorlevel 1 (
    echo ����ʧ�ܣ����� gcc �� AVX2 ֧�֡�
    pause
    exit /b 1
)
echo �����������ܲ���...
build\benchmark_simd.exe
pause
