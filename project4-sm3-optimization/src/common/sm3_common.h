#ifndef SM3_COMMON_H
#define SM3_COMMON_H

#include <stdint.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

// 基础压缩函数（单块，64 byte）
void sm3_compress(uint32_t state[8], const uint8_t block[64]);

// 基础单块接口：输入 len 为 64 时按单块处理并输出 32 字节 digest（大端）
void sm3_basic_hash(const uint8_t *msg, size_t len, uint8_t digest[32]);

// SIMD 8-way 接口：msgs 为 8 个指向 64-byte block 的指针，digests 为 8x32 输出
// 每个输入块被视为单个 64-byte block（未做额外填充）
void sm3_simd_8blocks(const uint8_t *msgs[8], uint8_t digests[8][32]);

#ifdef __cplusplus
}
#endif

#endif // SM3_COMMON_H
