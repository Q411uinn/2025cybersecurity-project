#ifndef SM4_SIMD_H
#define SM4_SIMD_H

#include <stdint.h>

void sm4_key_schedule_simd(const uint8_t key[16], uint32_t rk[32]);
void sm4_encrypt_simd(const uint8_t in[64], uint8_t out[64], const uint32_t rk[32]);

#endif // SM4_SIMD_H
