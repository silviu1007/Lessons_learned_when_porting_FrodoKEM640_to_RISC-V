#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include "../src/api_frodo640.h"

#define crypto_kem_keypair  crypto_kem_keypair_Frodo640
#define crypto_kem_enc      crypto_kem_enc_Frodo640
#define crypto_kem_dec      crypto_kem_dec_Frodo640

void uart_init(void);

// Not cryptographically secure - testing only
void randombytes(uint8_t *out, size_t outlen) {
    for (size_t i = 0; i < outlen; i++)
        out[i] = (uint8_t)(i ^ 0xA5);
}

// Placed in flash instead of RAM using section attribute
// Flash is at 0x20000000 (32MB) on the FE310
// RAM is at 0x80000000 (16KB) on the FE310
static uint8_t pk[CRYPTO_PUBLICKEYBYTES]  __attribute__((section(".rodata")));
static uint8_t sk[CRYPTO_SECRETKEYBYTES]  __attribute__((section(".rodata")));
static uint8_t ct[CRYPTO_CIPHERTEXTBYTES] __attribute__((section(".rodata")));
static uint8_t ss_encap[CRYPTO_BYTES]     __attribute__((section(".rodata")));
static uint8_t ss_decap[CRYPTO_BYTES]     __attribute__((section(".rodata")));

int main(void) {
    uart_init();
    printf("=== FrodoKEM-640 HiFive1 port ===\n");

    printf("\n[1/3] Running key generation...\n");
    if (crypto_kem_keypair(pk, sk) != 0) {
        printf("ERROR: key generation failed\n");
        while(1);
    }
    printf("Key generation OK\n");

    printf("\n[2/3] Running encapsulation...\n");
    if (crypto_kem_enc(ct, ss_encap, pk) != 0) {
        printf("ERROR: encapsulation failed\n");
        while(1);
    }
    printf("Encapsulation OK\n");

    printf("\n[3/3] Running decapsulation...\n");
    crypto_kem_dec(ss_decap, ct, sk);

    if (memcmp(ss_encap, ss_decap, CRYPTO_BYTES) != 0) {
        printf("ERROR: shared secrets do not match!\n");
        while(1);
    }

    printf("\n=== SUCCESS: shared secrets match! ===\n");
    while(1);
    return 0;
}