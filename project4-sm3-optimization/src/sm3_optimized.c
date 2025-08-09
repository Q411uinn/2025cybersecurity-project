// src/optimized/sm3_optimized.c

#include "sm3_common.h"
#include <stdint.h>

#define ROTL(x,n) (((x) << (n)) | ((x) >> (32-(n))))

// 这里复用Tj、FF、GG、P0、P1函数，略去...

void sm3_compress_optimized(uint32_t state[8], const uint8_t block[64]) {
    uint32_t W[68], W1[64];
    uint32_t A = state[0], B = state[1], C = state[2], D = state[3];
    uint32_t E = state[4], F = state[5], G = state[6], H = state[7];
    uint32_t SS1, SS2, TT1, TT2;

    // 消息扩展（同基础版，但可以后续考虑循环展开）
    for (int i = 0; i < 16; i++) {
        W[i] = ((uint32_t)block[4*i] << 24) | ((uint32_t)block[4*i+1] << 16) | 
               ((uint32_t)block[4*i+2] << 8) | ((uint32_t)block[4*i+3]);
    }
    for (int j = 16; j < 68; j++) {
        W[j] = P1(W[j-16] ^ W[j-9] ^ ROTL(W[j-3], 15)) ^ ROTL(W[j-13], 7) ^ W[j-6];
    }
    for (int j = 0; j < 64; j++) {
        W1[j] = W[j] ^ W[j+4];
    }

    // 循环展开示例（每4轮一组展开，提升指令流水）
    for (int j = 0; j < 64; j += 4) {
        // 第1轮
        SS1 = ROTL((ROTL(A,12) + E + ROTL(Tj[j], j)) , 7);
        SS2 = SS1 ^ ROTL(A,12);
        TT1 = FF(A,B,C,j) + D + SS2 + W1[j];
        TT2 = GG(E,F,G,j) + H + SS1 + W[j];
        D = C; C = ROTL(B, 9); B = A; A = TT1; H = G; G = ROTL(F,19); F = E; E = P0(TT2);

        // 第2轮
        SS1 = ROTL((ROTL(A,12) + E + ROTL(Tj[j+1], j+1)) , 7);
        SS2 = SS1 ^ ROTL(A,12);
        TT1 = FF(A,B,C,j+1) + D + SS2 + W1[j+1];
        TT2 = GG(E,F,G,j+1) + H + SS1 + W[j+1];
        D = C; C = ROTL(B, 9); B = A; A = TT1; H = G; G = ROTL(F,19); F = E; E = P0(TT2);

        // 第3轮
        SS1 = ROTL((ROTL(A,12) + E + ROTL(Tj[j+2], j+2)) , 7);
        SS2 = SS1 ^ ROTL(A,12);
        TT1 = FF(A,B,C,j+2) + D + SS2 + W1[j+2];
        TT2 = GG(E,F,G,j+2) + H + SS1 + W[j+2];
        D = C; C = ROTL(B, 9); B = A; A = TT1; H = G; G = ROTL(F,19); F = E; E = P0(TT2);

        // 第4轮
        SS1 = ROTL((ROTL(A,12) + E + ROTL(Tj[j+3], j+3)) , 7);
        SS2 = SS1 ^ ROTL(A,12);
        TT1 = FF(A,B,C,j+3) + D + SS2 + W1[j+3];
        TT2 = GG(E,F,G,j+3) + H + SS1 + W[j+3];
        D = C; C = ROTL(B, 9); B = A; A = TT1; H = G; G = ROTL(F,19); F = E; E = P0(TT2);
    }

    // 更新状态
    state[0] ^= A;
    state[1] ^= B;
    state[2] ^= C;
    state[3] ^= D;
    state[4] ^= E;
    state[5] ^= F;
    state[6] ^= G;
    state[7] ^= H;
}
