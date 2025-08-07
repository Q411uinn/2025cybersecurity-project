#include <stdio.h>
#include <stdint.h>
#include <time.h>
#include <string.h>

#include "../src/basic/sm4_basic.h"
#include "../src/simd/sm4_simd.h"
#include "../src/aesni/sm4_aesni.h"


void benchmark_basic() {
    uint8_t key[16] = {0};
    uint8_t in[16] = {0};
    uint8_t out[16];
    uint32_t rk[32];

    sm4_key_schedule(key, rk);

    clock_t start = clock();
    for (int i = 0; i < 1000000; i++) {
        sm4_encrypt_basic(in, out, rk);
    }
    clock_t end = clock();

    printf("BASIC:   %.2f sec\n", (double)(end - start) / CLOCKS_PER_SEC);
}

void benchmark_simd() {
    uint8_t key[16] = {0};
    uint8_t in[64] = {0}; // 4 blocks
    uint8_t out[64];
    uint32_t rk[32];

    sm4_key_schedule_simd(key, rk);

    clock_t start = clock();
    for (int i = 0; i < 250000; i++) { // 4x blocks, 所以循环数除4
        sm4_encrypt_simd(in, out, rk);
    }
    clock_t end = clock();

    printf("SIMD:    %.2f sec\n", (double)(end - start) / CLOCKS_PER_SEC);
}

void benchmark_aesni() {
    uint8_t key[16] = {0};
    uint8_t in[16] = {0};
    uint8_t out[16];
    uint32_t rk[32];

    sm4_key_schedule_aesni(key, rk);

    clock_t start = clock();
    for (int i = 0; i < 1000000; i++) {
        sm4_encrypt_aesni(in, out, rk);
    }
    clock_t end = clock();

    printf("AESNI:   %.2f sec\n", (double)(end - start) / CLOCKS_PER_SEC);
}

int main() {
    benchmark_basic();
    benchmark_simd();
    benchmark_aesni();
    return 0;
}
