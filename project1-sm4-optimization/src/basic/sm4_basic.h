#ifndef SM4_BASIC_H
#define SM4_BASIC_H

#include <stdint.h>

void sm4_key_schedule(const uint8_t key[16], uint32_t rk[32]);
void sm4_encrypt_basic(const uint8_t in[16], uint8_t out[16], const uint32_t rk[32]);
void sm4_decrypt_basic(const uint8_t in[16], uint8_t out[16], const uint32_t rk[32]);

#endif // SM4_BASIC_H
