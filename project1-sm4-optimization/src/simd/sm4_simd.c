#include "sm4_simd.h"
#include <emmintrin.h>  // SSE2
#include <tmmintrin.h>  // SSSE3（用于shuffle）
#include <string.h>

extern void sm4_key_schedule(const uint8_t key[16], uint32_t rk[32]);

// 轮函数F（我们暂时模拟，未向量化S盒）
static inline __m128i sm4_round(__m128i x0, __m128i x1, __m128i x2, __m128i x3, uint32_t rk) {
    __m128i t = _mm_xor_si128(_mm_xor_si128(x1, x2), x3);
    t = _mm_xor_si128(t, _mm_set1_epi32(rk));
    
    // 模拟S盒：这里只能用 C 实现（如果要向量化 SBox，需要 PSHUFB）
    // 暂时跳过，继续流程

    // 模拟线性变换 L
    uint32_t buf[4];
    _mm_storeu_si128((__m128i*)buf, t);
    for (int i = 0; i < 4; i++) {
        uint32_t tmp = buf[i];
        buf[i] = tmp ^ (tmp << 2 | tmp >> 30) ^ (tmp << 10 | tmp >> 22)
                 ^ (tmp << 18 | tmp >> 14) ^ (tmp << 24 | tmp >> 8);
    }
    t = _mm_loadu_si128((__m128i*)buf);

    return _mm_xor_si128(x0, t);
}

void sm4_key_schedule_simd(const uint8_t key[16], uint32_t rk[32]) {
    sm4_key_schedule(key, rk);
}

void sm4_encrypt_simd(const uint8_t in[64], uint8_t out[64], const uint32_t rk[32]) {
    __m128i X0, X1, X2, X3;
    // 每一组 block 有 4 个 32bit word，对应 X0 ~ X3
    // 我们将每个位置的 word 合并到一个 __m128i 中（即并行处理同一位置）

    uint32_t buf[16];  // 4 blocks × 4 word = 16 word
    memcpy(buf, in, 64);

    // 并行装载每个 word：4 blocks 的 X0
    __m128i x0 = _mm_set_epi32(buf[0], buf[4], buf[8], buf[12]);
    __m128i x1 = _mm_set_epi32(buf[1], buf[5], buf[9], buf[13]);
    __m128i x2 = _mm_set_epi32(buf[2], buf[6], buf[10], buf[14]);
    __m128i x3 = _mm_set_epi32(buf[3], buf[7], buf[11], buf[15]);

    for (int i = 0; i < 32; i++) {
        __m128i tmp = sm4_round(x0, x1, x2, x3, rk[i]);
        // 向左滑动窗口
        x0 = x1;
        x1 = x2;
        x2 = x3;
        x3 = tmp;
    }

    // 输出顺序翻转：X35, X34, X33, X32
    __m128i r0 = x3;
    __m128i r1 = x2;
    __m128i r2 = x1;
    __m128i r3 = x0;

    // 拆出每组 4 × 32bit 并存储
    uint32_t outbuf[16];
    _mm_storeu_si128((__m128i*)&outbuf[0], r0);
    _mm_storeu_si128((__m128i*)&outbuf[4], r1);
    _mm_storeu_si128((__m128i*)&outbuf[8], r2);
    _mm_storeu_si128((__m128i*)&outbuf[12], r3);

    // 按 block 写回
    for (int i = 0; i < 4; i++) {
        uint32_t* blk = &outbuf[i];
        for (int j = 0; j < 4; j++) {
            ((uint32_t*)(out + i*16))[j] = blk[j * 4];
        }
    }
}
