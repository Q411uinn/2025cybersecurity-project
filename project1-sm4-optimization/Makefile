CC = gcc
CFLAGS = -Wall -O2 -msse3 -maes

SRC_BASIC = src/basic/sm4_basic.c
SRC_SIMD = src/simd/sm4_simd.c
SRC_AESNI = src/aesni/sm4_aesni.c

SRC_ALL = $(SRC_BASIC) $(SRC_SIMD) $(SRC_AESNI)

TEST = tests/test_sm4.c
BENCHMARK = benchmarks/benchmark.c

.PHONY: all basic simd aesni clean run benchmark benchmark-all

all: basic simd aesni

basic:
	$(CC) $(CFLAGS) -o test_sm4_basic $(SRC_BASIC) $(TEST)
	$(CC) $(CFLAGS) -o benchmark_basic $(SRC_ALL) $(BENCHMARK)

simd:
	$(CC) $(CFLAGS) -o test_sm4_simd $(SRC_BASIC) $(SRC_SIMD) $(TEST)
	$(CC) $(CFLAGS) -o benchmark_simd $(SRC_ALL) $(BENCHMARK)

aesni:
	$(CC) $(CFLAGS) -o test_sm4_aesni $(SRC_BASIC) $(SRC_AESNI) $(TEST)
	$(CC) $(CFLAGS) -o benchmark_aesni $(SRC_ALL) $(BENCHMARK)

run:
	./test_sm4_basic

benchmark:
	./benchmark_basic

benchmark-all: basic simd aesni
	@echo "===== BASIC ====="
	./benchmark_basic
	@echo "===== SIMD ====="
	./benchmark_simd
	@echo "===== AESNI ====="
	./benchmark_aesni

clean:
	del /f /q test_sm4_*.exe benchmark_*.exe 2>nul || echo No files to delete.
