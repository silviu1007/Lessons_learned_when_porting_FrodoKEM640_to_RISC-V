#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include "../src/api_frodo640.h"

#define crypto_kem_keypair  crypto_kem_keypair_Frodo640
#define crypto_kem_enc      crypto_kem_enc_Frodo640
#define crypto_kem_dec      crypto_kem_dec_Frodo640

// Stub randombytes - replace with real entropy source later
void randombytes(uint8_t *out, size_t outlen) {
    for (size_t i = 0; i < outlen; i++)
        out[i] = (uint8_t)(i ^ 0xA5);
}

// Static buffers to avoid blowing the stack
static uint8_t pk[CRYPTO_PUBLICKEYBYTES];
static uint8_t sk[CRYPTO_SECRETKEYBYTES];
static uint8_t ct[CRYPTO_CIPHERTEXTBYTES];
static uint8_t ss_encap[CRYPTO_BYTES];
static uint8_t ss_decap[CRYPTO_BYTES];

int main(void) {    
    printf("FrodoKEM-640 test on HiFive1\n");

    // Key generation
    printf("Running keygen...\n");
    if (crypto_kem_keypair(pk, sk) != 0) {
        printf("ERROR: keygen failed\n");
        return 1;
    }
    printf("Keygen OK\n");

    // Encapsulation
    printf("Running encaps...\n");
    if (crypto_kem_enc(ct, ss_encap, pk) != 0) {
        printf("ERROR: encaps failed\n");
        return 1;
    }
    printf("Encaps OK\n");

    // Decapsulation
    printf("Running decaps...\n");
    crypto_kem_dec(ss_decap, ct, sk);
    printf("Decaps OK\n");

    // Check shared secrets match
    if (memcmp(ss_encap, ss_decap, CRYPTO_BYTES) != 0) {
        printf("ERROR: shared secrets do not match!\n");
        return 1;
    }

    printf("SUCCESS: shared secrets match!\n");
    return 0;
}