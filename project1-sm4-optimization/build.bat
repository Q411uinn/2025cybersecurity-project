@echo off
echo [INFO] Building SM4 project...
gcc src\basic\sm4_basic.c tests\test_sm4.c -o test_sm4.exe -Wall -O2
if %errorlevel% neq 0 (
    echo [ERROR] Build failed!
    exit /b %errorlevel%
)
echo [INFO] Build succeeded. Run test_sm4.exe to test.
