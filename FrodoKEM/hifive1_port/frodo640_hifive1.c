#include "../src/api_frodo640.h"
#include "../src/frodo_macrify.h"

// Parameters for FrodoKEM-640
#define PARAMS_N 640
#define PARAMS_NBAR 8
#define PARAMS_LOGQ 15
#define PARAMS_Q (1 << PARAMS_LOGQ)
#define PARAMS_EXTRACTED_BITS 2
#define PARAMS_STRIPE_STEP 8
#define PARAMS_PARALLEL 4
#define BYTES_SEED_A 16
#define BYTES_MU (PARAMS_EXTRACTED_BITS*PARAMS_NBAR*PARAMS_NBAR)/8
#define BYTES_SALT (2*CRYPTO_BYTES)
#define BYTES_SEED_SE (2*CRYPTO_BYTES)
#define BYTES_PKHASH CRYPTO_BYTES

#if (PARAMS_NBAR % 8 != 0)
#error You have modified the cryptographic parameters. FrodoKEM assumes PARAMS_NBAR is a multiple of 8.
#endif

#define shake     shake128

uint16_t CDF_TABLE[13] = {4643, 13363, 20579, 25843, 29227, 31145, 32103, 32525, 32689, 32745, 32762, 32766, 32767};
uint16_t CDF_TABLE_LEN = 13;

#define crypto_kem_keypair  crypto_kem_keypair_Frodo640
#define crypto_kem_enc      crypto_kem_enc_Frodo640
#define crypto_kem_dec      crypto_kem_dec_Frodo640

#include "kem_hifive1.c"
#include "../src/noise.c"
#include "../src/frodo_macrify_reference.c"