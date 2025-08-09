// tests/test_sm3_comprehensive.c

#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include "sm3_common.h"

// SM3初始化IV
static const uint32_t IV[8] = {
    0x7380166f,0x4914b2b9,0x172442d7,0xda8a0600,
    0xa96f30bc,0x163138aa,0xe38dee4d,0xb0fb0e4e
};

// 辅助函数：打印hash状态
void print_hash(uint32_t hash[8]) {
    for (int i = 0; i < 8; i++) {
        printf("%08x", hash[i]);
    }
    printf("\n");
}

// 辅助函数：单块SM3压缩函数调用
void sm3_hash_block(const uint8_t *block, uint32_t hash[8]) {
    memcpy(hash, IV, sizeof(uint32_t)*8);
    sm3_compress(hash, block);
}

int main() {
    // 测试用例：空消息块（64字节全0）
    uint8_t message[64] = {0};
    uint32_t hash[8] = {0};

    sm3_hash_block(message, hash);

    printf("SM3 hash of 64-byte zero block:\n");
    print_hash(hash);


    return 0;
}
