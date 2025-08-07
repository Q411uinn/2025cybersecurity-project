#ifndef SM4_AESNI_H
#define SM4_AESNI_H

#include <stdint.h>

void sm4_key_schedule_aesni(const uint8_t key[16], uint32_t rk[32]);
void sm4_encrypt_aesni(const uint8_t in[16], uint8_t out[16], const uint32_t rk[32]);

#endif // SM4_AESNI_H
