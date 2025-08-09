#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

#include "../src/common/sm3_common.h"

#ifdef _WIN32
#include <windows.h>
static double now_seconds(void) {
    LARGE_INTEGER freq, counter;
    QueryPerformanceFrequency(&freq);
    QueryPerformanceCounter(&counter);
    return (double)counter.QuadPart / (double)freq.QuadPart;
}
#else
#include <sys/time.h>
static double now_seconds(void) {
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return (double)tv.tv_sec + tv.tv_usec / 1e6;
}
#endif

#define BLOCK_SIZE 64
#define TEST_BLOCKS 8000  // must be multiple of 8
#define REPEAT 10

int main(void) {
    if (TEST_BLOCKS % 8 != 0) {
        printf("TEST_BLOCKS must be multiple of 8\n");
        return 1;
    }

    uint8_t *messages = (uint8_t*)malloc((size_t)TEST_BLOCKS * BLOCK_SIZE);
    if (!messages) {
        printf("malloc failed\n");
        return 1;
    }

    // seed deterministic random
    srand(12345);
    for (size_t i = 0; i < (size_t)TEST_BLOCKS * BLOCK_SIZE; i++) {
        messages[i] = (uint8_t)(rand() & 0xFF);
    }

    printf("Benchmark SM3: %d blocks (%d bytes each), repeat=%d\n", TEST_BLOCKS, BLOCK_SIZE, REPEAT);

    // basic
    double basic_accum = 0.0;
    uint8_t digest[32];
    for (int r = 0; r < REPEAT; r++) {
        double t0 = now_seconds();
        for (size_t i = 0; i < (size_t)TEST_BLOCKS; i++) {
            sm3_basic_hash(messages + i * BLOCK_SIZE, BLOCK_SIZE, digest);
        }
        double t1 = now_seconds();
        basic_accum += (t1 - t0);
    }
    double basic_avg = basic_accum / REPEAT;
    double basic_MBps = ((double)TEST_BLOCKS * BLOCK_SIZE) / (basic_avg * 1024.0 * 1024.0);

    // simd
    double simd_accum = 0.0;
    const uint8_t *ptrs[8];
    uint8_t digests[8][32];
    for (int r = 0; r < REPEAT; r++) {
        double t0 = now_seconds();
        for (size_t i = 0; i < (size_t)TEST_BLOCKS; i += 8) {
            for (int k = 0; k < 8; k++) ptrs[k] = messages + (i + k) * BLOCK_SIZE;
            sm3_simd_8blocks(ptrs, digests);
        }
        double t1 = now_seconds();
        simd_accum += (t1 - t0);
    }
    double simd_avg = simd_accum / REPEAT;
    double simd_MBps = ((double)TEST_BLOCKS * BLOCK_SIZE) / (simd_avg * 1024.0 * 1024.0);

    printf("Basic avg time: %.6f s, throughput: %.2f MB/s\n", basic_avg, basic_MBps);
    printf("SIMD  avg time: %.6f s, throughput: %.2f MB/s\n", simd_avg, simd_MBps);

    free(messages);
    return 0;
}

