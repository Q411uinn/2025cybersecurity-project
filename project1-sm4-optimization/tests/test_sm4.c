#include <stdio.h>
#include <string.h>
#include <stdint.h>

#if defined(TEST_BASIC)
    #include "../src/basic/sm4_basic.h"
#elif defined(TEST_SIMD)
    #include "../src/simd/sm4_simd.h"
#elif defined(TEST_AESNI)
    #include "../src/aesni/sm4_aesni.h"
#endif

int main() {
    uint8_t key[16] = {
        0x01,0x23,0x45,0x67,0x89,0xab,0xcd,0xef,
        0xfe,0xdc,0xba,0x98,0x76,0x54,0x32,0x10
    };
    uint8_t plaintext[64] = {0};  // 64 bytes for simd (4 blocks)
    memcpy(plaintext, (uint8_t[]){
        0x01,0x23,0x45,0x67,0x89,0xab,0xcd,0xef,
        0xfe,0xdc,0xba,0x98,0x76,0x54,0x32,0x10
    }, 16);
    
    uint8_t ciphertext[64] = {0};
    uint8_t decrypted[64] = {0};
    uint32_t rk[32];

#if defined(TEST_BASIC) || defined(TEST_AESNI)
    sm4_key_schedule(key, rk);
#elif defined(TEST_SIMD)
    sm4_key_schedule_simd(key, rk);
#endif

#if defined(TEST_BASIC)
    sm4_encrypt_basic(plaintext, ciphertext, rk);
    sm4_decrypt_basic(ciphertext, decrypted, rk);
#elif defined(TEST_AESNI)
    sm4_encrypt_aesni(plaintext, ciphertext, rk);
    sm4_decrypt_basic(ciphertext, decrypted, rk);  // aesni没写解密，用basic解密
#elif defined(TEST_SIMD)
    sm4_encrypt_simd(plaintext, ciphertext, rk);
    // SIMD解密暂时没有实现，这里用basic逐块解密
    for (int i = 0; i < 4; i++) {
        sm4_decrypt_basic(ciphertext + i*16, decrypted + i*16, rk);
    }
#endif

    printf("Plaintext:  ");
    for (int i = 0; i < 16; i++) printf("%02x ", plaintext[i]);
    printf("\n");

    printf("Ciphertext: ");
    for (int i = 0; i < 16; i++) printf("%02x ", ciphertext[i]);
    printf("\n");

    printf("Decrypted:  ");
    for (int i = 0; i < 16; i++) printf("%02x ", decrypted[i]);
    printf("\n");

    if (memcmp(plaintext, decrypted, 16) == 0) {
        printf("SM4 test passed!\n");
    } else {
        printf("SM4 test failed!\n");
    }

    return 0;
}
