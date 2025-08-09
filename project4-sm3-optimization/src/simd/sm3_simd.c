// AVX2 实现：对 8 个 64-byte blocks 并行做一次 SM3 压缩（每个 block 视为单块）
// 编译需要 -mavx2
#include "sm3_common.h"
#include <immintrin.h>
#include <stdint.h>
#include <string.h>

#define ROTL32(x,n) _mm256_or_si256(_mm256_slli_epi32((x),(n)), _mm256_srli_epi32((x),(32-(n))))

static inline __m256i rotl_32(__m256i x, int n) { return ROTL32(x,n); }

static inline __m256i P0_vec(__m256i x) {
    return _mm256_xor_si256(_mm256_xor_si256(x, rotl_32(x,9)), rotl_32(x,17));
}
static inline __m256i P1_vec(__m256i x) {
    return _mm256_xor_si256(_mm256_xor_si256(x, rotl_32(x,15)), rotl_32(x,23));
}

static inline __m256i FF0_vec(__m256i x, __m256i y, __m256i z) {
    return _mm256_xor_si256(_mm256_xor_si256(x,y), z);
}
static inline __m256i FF1_vec(__m256i x, __m256i y, __m256i z) {
    __m256i xy = _mm256_and_si256(x,y);
    __m256i xz = _mm256_and_si256(x,z);
    __m256i yz = _mm256_and_si256(y,z);
    return _mm256_or_si256(_mm256_or_si256(xy,xz), yz);
}
static inline __m256i GG0_vec(__m256i x, __m256i y, __m256i z) {
    return _mm256_xor_si256(_mm256_xor_si256(x,y), z);
}
static inline __m256i GG1_vec(__m256i x, __m256i y, __m256i z) {
    __m256i xy = _mm256_and_si256(x,y);
    __m256i nx = _mm256_andnot_si256(x, z); // ~x & z
    return _mm256_or_si256(xy, nx);
}

static const uint32_t Tj_scalar[64] = {
    0x79cc4519u,0x79cc4519u,0x79cc4519u,0x79cc4519u,0x79cc4519u,0x79cc4519u,0x79cc4519u,0x79cc4519u,
    0x79cc4519u,0x79cc4519u,0x79cc4519u,0x79cc4519u,0x79cc4519u,0x79cc4519u,0x79cc4519u,0x79cc4519u,
    0x7a879d8au,0x7a879d8au,0x7a879d8au,0x7a879d8au,0x7a879d8au,0x7a879d8au,0x7a879d8au,0x7a879d8au,
    0x7a879d8au,0x7a879d8au,0x7a879d8au,0x7a879d8au,0x7a879d8au,0x7a879d8au,0x7a879d8au,0x7a879d8au,
    0x7a879d8au,0x7a879d8au,0x7a879d8au,0x7a879d8au,0x7a879d8au,0x7a879d8au,0x7a879d8au,0x7a879d8au,
    0x7a879d8au,0x7a879d8au,0x7a879d8au,0x7a879d8au,0x7a879d8au,0x7a879d8au,0x7a879d8au,0x7a879d8au,
    0x7a879d8au,0x7a879d8au,0x7a879d8au,0x7a879d8au,0x7a879d8au,0x7a879d8au,0x7a879d8au,0x7a879d8au,
    0x7a879d8au,0x7a879d8au,0x7a879d8au,0x7a879d8au,0x7a879d8au,0x7a879d8au,0x7a879d8au,0x7a879d8au
};

static const uint32_t IV_scalar[8] = {
    0x7380166fu,0x4914b2b9u,0x172442d7u,0xda8a0600u,
    0xa96f30bcu,0x163138aau,0xe38dee4du,0xb0fb0e4eu
};

void sm3_simd_8blocks(const uint8_t *msgs[8], uint8_t digests[8][32]) {
    // load IV into vectors (lane i: msgs[i])
    __m256i A = _mm256_setr_epi32(
        IV_scalar[0], IV_scalar[0], IV_scalar[0], IV_scalar[0],
        IV_scalar[0], IV_scalar[0], IV_scalar[0], IV_scalar[0]
    );
    // But we want lane i corresponding to different messages, so we'll build lanes per-message below.
    // Simpler: construct A..H so lane i contains IV_scalar[*] (same across lanes), then after compress
    // we'll extract lanes to form per-message states. This keeps semantics identical for single-block behaviour.
    A = _mm256_setr_epi32(IV_scalar[0],IV_scalar[0],IV_scalar[0],IV_scalar[0],IV_scalar[0],IV_scalar[0],IV_scalar[0],IV_scalar[0]);
    __m256i B = _mm256_setr_epi32(IV_scalar[1],IV_scalar[1],IV_scalar[1],IV_scalar[1],IV_scalar[1],IV_scalar[1],IV_scalar[1],IV_scalar[1]);
    __m256i C = _mm256_setr_epi32(IV_scalar[2],IV_scalar[2],IV_scalar[2],IV_scalar[2],IV_scalar[2],IV_scalar[2],IV_scalar[2],IV_scalar[2]);
    __m256i D = _mm256_setr_epi32(IV_scalar[3],IV_scalar[3],IV_scalar[3],IV_scalar[3],IV_scalar[3],IV_scalar[3],IV_scalar[3],IV_scalar[3]);
    __m256i E = _mm256_setr_epi32(IV_scalar[4],IV_scalar[4],IV_scalar[4],IV_scalar[4],IV_scalar[4],IV_scalar[4],IV_scalar[4],IV_scalar[4]);
    __m256i F = _mm256_setr_epi32(IV_scalar[5],IV_scalar[5],IV_scalar[5],IV_scalar[5],IV_scalar[5],IV_scalar[5],IV_scalar[5],IV_scalar[5]);
    __m256i G = _mm256_setr_epi32(IV_scalar[6],IV_scalar[6],IV_scalar[6],IV_scalar[6],IV_scalar[6],IV_scalar[6],IV_scalar[6],IV_scalar[6]);
    __m256i H = _mm256_setr_epi32(IV_scalar[7],IV_scalar[7],IV_scalar[7],IV_scalar[7],IV_scalar[7],IV_scalar[7],IV_scalar[7],IV_scalar[7]);

    // Build W vectors: W[i] holds 8 lanes: i-th word of each block
    __m256i W[68];
    __m256i W1[64];

    // load W[0..15] by constructing each lane from each block's 4 bytes
    for (int i = 0; i < 16; i++) {
        uint32_t lanes[8];
        for (int lane = 0; lane < 8; lane++) {
            const uint8_t *blk = msgs[lane];
            lanes[lane] = ((uint32_t)blk[4*i] << 24) | ((uint32_t)blk[4*i+1] << 16) |
                          ((uint32_t)blk[4*i+2] << 8) | ((uint32_t)blk[4*i+3]);
        }
        W[i] = _mm256_setr_epi32(lanes[0],lanes[1],lanes[2],lanes[3],lanes[4],lanes[5],lanes[6],lanes[7]);
    }

    // expansion W[16..67]
    for (int j = 16; j < 68; j++) {
        __m256i t = _mm256_xor_si256(_mm256_xor_si256(W[j-16], W[j-9]), rotl_32(W[j-3], 15));
        __m256i p1 = P1_vec(t);
        W[j] = _mm256_xor_si256(_mm256_xor_si256(p1, rotl_32(W[j-13], 7)), W[j-6]);
    }
    for (int j = 0; j < 64; j++) {
        W1[j] = _mm256_xor_si256(W[j], W[j+4]);
    }

    // main loop
    for (int j = 0; j < 64; j++) {
        __m256i Tj_vec = _mm256_set1_epi32(Tj_scalar[j]);
        __m256i rotA12 = rotl_32(A, 12);
        __m256i SS1 = rotl_32(_mm256_add_epi32(_mm256_add_epi32(rotA12, E), rotl_32(Tj_vec, j)), 7);
        __m256i SS2 = _mm256_xor_si256(SS1, rotA12);
        __m256i TT1, TT2;

        if (j < 16) {
            TT1 = _mm256_add_epi32(_mm256_add_epi32(_mm256_add_epi32(FF0_vec(A,B,C), D), SS2), W1[j]);
            TT2 = _mm256_add_epi32(_mm256_add_epi32(_mm256_add_epi32(GG0_vec(E,F,G), H), SS1), W[j]);
        } else {
            TT1 = _mm256_add_epi32(_mm256_add_epi32(_mm256_add_epi32(FF1_vec(A,B,C), D), SS2), W1[j]);
            TT2 = _mm256_add_epi32(_mm256_add_epi32(_mm256_add_epi32(GG1_vec(E,F,G), H), SS1), W[j]);
        }

        D = C;
        C = rotl_32(B, 9);
        B = A;
        A = TT1;
        H = G;
        G = rotl_32(F, 19);
        F = E;
        E = P0_vec(TT2);
    }

    // extract lanes and build per-message digests (state after xor with IV)
    uint32_t tmp[8];

    // For each state word index k = 0..7, extract lane vector and xor with IV_scalar[k], then store big-endian bytes into digests
    _mm256_storeu_si256((__m256i*)tmp, A); // lanes -> tmp[0..7]
    for (int lane = 0; lane < 8; lane++) {
        uint32_t v = tmp[lane] ^ IV_scalar[0];
        digests[lane][0] = (uint8_t)(v >> 24);
        digests[lane][1] = (uint8_t)(v >> 16);
        digests[lane][2] = (uint8_t)(v >> 8);
        digests[lane][3] = (uint8_t)(v);
    }
    _mm256_storeu_si256((__m256i*)tmp, B);
    for (int lane = 0; lane < 8; lane++) {
        uint32_t v = tmp[lane] ^ IV_scalar[1];
        digests[lane][4] = (uint8_t)(v >> 24);
        digests[lane][5] = (uint8_t)(v >> 16);
        digests[lane][6] = (uint8_t)(v >> 8);
        digests[lane][7] = (uint8_t)(v);
    }
    _mm256_storeu_si256((__m256i*)tmp, C);
    for (int lane = 0; lane < 8; lane++) {
        uint32_t v = tmp[lane] ^ IV_scalar[2];
        digests[lane][8] = (uint8_t)(v >> 24);
        digests[lane][9] = (uint8_t)(v >> 16);
        digests[lane][10] = (uint8_t)(v >> 8);
        digests[lane][11] = (uint8_t)(v);
    }
    _mm256_storeu_si256((__m256i*)tmp, D);
    for (int lane = 0; lane < 8; lane++) {
        uint32_t v = tmp[lane] ^ IV_scalar[3];
        digests[lane][12] = (uint8_t)(v >> 24);
        digests[lane][13] = (uint8_t)(v >> 16);
        digests[lane][14] = (uint8_t)(v >> 8);
        digests[lane][15] = (uint8_t)(v);
    }
    _mm256_storeu_si256((__m256i*)tmp, E);
    for (int lane = 0; lane < 8; lane++) {
        uint32_t v = tmp[lane] ^ IV_scalar[4];
        digests[lane][16] = (uint8_t)(v >> 24);
        digests[lane][17] = (uint8_t)(v >> 16);
        digests[lane][18] = (uint8_t)(v >> 8);
        digests[lane][19] = (uint8_t)(v);
    }
    _mm256_storeu_si256((__m256i*)tmp, F);
    for (int lane = 0; lane < 8; lane++) {
        uint32_t v = tmp[lane] ^ IV_scalar[5];
        digests[lane][20] = (uint8_t)(v >> 24);
        digests[lane][21] = (uint8_t)(v >> 16);
        digests[lane][22] = (uint8_t)(v >> 8);
        digests[lane][23] = (uint8_t)(v);
    }
    _mm256_storeu_si256((__m256i*)tmp, G);
    for (int lane = 0; lane < 8; lane++) {
        uint32_t v = tmp[lane] ^ IV_scalar[6];
        digests[lane][24] = (uint8_t)(v >> 24);
        digests[lane][25] = (uint8_t)(v >> 16);
        digests[lane][26] = (uint8_t)(v >> 8);
        digests[lane][27] = (uint8_t)(v);
    }
    _mm256_storeu_si256((__m256i*)tmp, H);
    for (int lane = 0; lane < 8; lane++) {
        uint32_t v = tmp[lane] ^ IV_scalar[7];
        digests[lane][28] = (uint8_t)(v >> 24);
        digests[lane][29] = (uint8_t)(v >> 16);
        digests[lane][30] = (uint8_t)(v >> 8);
        digests[lane][31] = (uint8_t)(v);
    }
}
