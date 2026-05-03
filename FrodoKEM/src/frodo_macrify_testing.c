/********************************************************************************************
* FrodoKEM: Learning with Errors Key Encapsulation
*
* Abstract: matrix arithmetic functions used by the KEM
*********************************************************************************************/

#if defined (USE_SHAKE128_FOR_A)
    #include "../../common/sha3/fips202.h"
#endif    
extern void inner_mul_row(uint16_t *out_row, const uint16_t *s, const uint16_t *A_row);
extern void inner_mul_row_v2(uint16_t *out_row, const uint16_t *s, const uint16_t *A_row);



int frodo_mul_add_as_plus_e(uint16_t *out, const uint16_t *s, const uint16_t *e, const uint8_t *seed_A) 
{ // Generate-and-multiply: generate matrix A (N x N) row-wise, multiply by s on the right.
  // Inputs: s, e (N x N_BAR)
  // Output: out = A*s + e (N x N_BAR)
    int i,  j;//, k;
    uint16_t A_row[PARAMS_N] = {0};
   // uint16_t s_col[PARAMS_NBAR];
    uint8_t seed_A_separated[2 + BYTES_SEED_A];
    uint16_t* seed_A_origin = (uint16_t*)&seed_A_separated;
    memcpy(&seed_A_separated[2], seed_A, BYTES_SEED_A);
    memcpy(out, e, PARAMS_NBAR * PARAMS_N * sizeof(uint16_t));
    for (i = 0; i < PARAMS_N; i++) {
        seed_A_origin[0] = UINT16_TO_LE((uint16_t) i);
        shake128((unsigned char*)A_row, (unsigned long long)(2*PARAMS_N), seed_A_separated, 2 + BYTES_SEED_A);
        for (j = 0; j < PARAMS_N; j++) {
            A_row[j] = LE_TO_UINT16(A_row[j]);
        }
        // for (j = 0; j < PARAMS_N; j++) {
        //     for (k = 0; k < PARAMS_NBAR; k++)
        //         s_col[k] = s[k*PARAMS_N + j];
        //     for (k = 0; k < PARAMS_NBAR; k++)
        //         out[i*PARAMS_NBAR + k] += A_row[j] * s_col[k];
        // }
        //inner_mul_row(out + i*PARAMS_NBAR, s, A_row);
        inner_mul_row_v2(out + i*PARAMS_NBAR, s, A_row);
        
    }
    return 1;
}


int frodo_mul_add_sa_plus_e(uint16_t *out, const uint16_t *s, uint16_t *e, const uint8_t *seed_A) 
{ // Generate-and-multiply: generate matrix A (N x N) column-wise, multiply by s' on the left.
  // Inputs: s', e' (N_BAR x N)
  // Output: out = s'*A + e' (N_BAR x N)
    int i, j, k;
    uint16_t A_row[PARAMS_N] = {0};
    uint8_t seed_A_separated[2 + BYTES_SEED_A];
    uint16_t* seed_A_origin = (uint16_t*)&seed_A_separated;
    memcpy(&seed_A_separated[2], seed_A, BYTES_SEED_A);
    memcpy(out, e, PARAMS_NBAR * PARAMS_N * sizeof(uint16_t));
    for (i = 0; i < PARAMS_N; i++) {
        seed_A_origin[0] = UINT16_TO_LE((uint16_t) i);
        shake128((unsigned char*)A_row, (unsigned long long)(2*PARAMS_N), seed_A_separated, 2 + BYTES_SEED_A);
        for (j = 0; j < PARAMS_N; j++) {
            A_row[j] = LE_TO_UINT16(A_row[j]);
        }
        for (k = 0; k < PARAMS_NBAR; k++) {
            uint16_t s_prime = s[k*PARAMS_N + i];
            for (j = 0; j < PARAMS_N; j++) {
                out[k*PARAMS_N + j] += s_prime * A_row[j];
            }
        }
    }
    return 1;
}


void frodo_mul_bs(uint16_t *out, const uint16_t *b, const uint16_t *s) 
{ // Multiply by s on the right
  // Inputs: b (N_BAR x N), s (N x N_BAR)
  // Output: out = b*s (N_BAR x N_BAR)
    int i, j, k;

    for (i = 0; i < PARAMS_NBAR; i++) {
        for (j = 0; j < PARAMS_NBAR; j++) {
            out[i*PARAMS_NBAR + j] = 0;
            for (k = 0; k < PARAMS_N; k++) {
                out[i*PARAMS_NBAR + j] += b[i*PARAMS_N + k] * (int16_t)s[j*PARAMS_N + k];
            }
            out[i*PARAMS_NBAR + j] = (uint32_t)(out[i*PARAMS_NBAR + j]) & ((1<<PARAMS_LOGQ)-1);
        }
    }
}


void frodo_mul_add_sb_plus_e(uint16_t *out, const uint16_t *b, const uint16_t *s, const uint16_t *e) 
{ // Multiply by s on the left
  // Inputs: b (N x N_BAR), s (N_BAR x N), e (N_BAR x N_BAR)
  // Output: out = s*b + e (N_BAR x N_BAR)
    int i, j, k;

    for (k = 0; k < PARAMS_NBAR; k++) {
        for (i = 0; i < PARAMS_NBAR; i++) {
            out[k*PARAMS_NBAR + i] = e[k*PARAMS_NBAR + i];
            for (j = 0; j < PARAMS_N; j++) {
                out[k*PARAMS_NBAR + i] += (int16_t)s[k*PARAMS_N + j] * b[j*PARAMS_NBAR + i];
            }
            out[k*PARAMS_NBAR + i] = (uint32_t)(out[k*PARAMS_NBAR + i]) & ((1<<PARAMS_LOGQ)-1);
        }
    }
}


void frodo_add(uint16_t *out, const uint16_t *a, const uint16_t *b) 
{ // Add a and b
  // Inputs: a, b (N_BAR x N_BAR)
  // Output: c = a + b
    for (int i = 0; i < (PARAMS_NBAR*PARAMS_NBAR); i++) {
        out[i] = (a[i] + b[i]) & ((1<<PARAMS_LOGQ)-1);
    }
}


void frodo_sub(uint16_t *out, const uint16_t *a, const uint16_t *b) 
{ // Subtract a and b
  // Inputs: a, b (N_BAR x N_BAR)
  // Output: c = a - b
    for (int i = 0; i < (PARAMS_NBAR*PARAMS_NBAR); i++) {
        out[i] = (a[i] - b[i]) & ((1<<PARAMS_LOGQ)-1);
    }
}


void frodo_key_encode(uint16_t *out, const uint16_t *in) 
{ // Encoding
    unsigned int i, j, npieces_word = 8;
    unsigned int nwords = (PARAMS_NBAR*PARAMS_NBAR)/8;
    uint64_t temp, mask = ((uint64_t)1 << PARAMS_EXTRACTED_BITS) - 1;
    uint16_t* pos = out;

    for (i = 0; i < nwords; i++) {
        temp = 0;
        for(j = 0; j < PARAMS_EXTRACTED_BITS; j++) 
            temp |= ((uint64_t)((uint8_t*)in)[i*PARAMS_EXTRACTED_BITS + j]) << (8*j);
        for (j = 0; j < npieces_word; j++) { 
            *pos = (uint16_t)((temp & mask) << (PARAMS_LOGQ - PARAMS_EXTRACTED_BITS));  
            temp >>= PARAMS_EXTRACTED_BITS;
            pos++;
        }
    }
}


void frodo_key_decode(uint16_t *out, const uint16_t *in)
{ // Decoding
    unsigned int i, j, index = 0, npieces_word = 8;
    unsigned int nwords = (PARAMS_NBAR * PARAMS_NBAR) / 8;
    uint16_t temp, maskex=((uint16_t)1 << PARAMS_EXTRACTED_BITS) -1, maskq =((uint16_t)1 << PARAMS_LOGQ) -1;
    uint8_t  *pos = (uint8_t*)out;
    uint64_t templong;

    for (i = 0; i < nwords; i++) {
        templong = 0;
        for (j = 0; j < npieces_word; j++) {
            temp = ((in[index] & maskq) + (1 << (PARAMS_LOGQ - PARAMS_EXTRACTED_BITS - 1))) >> (PARAMS_LOGQ - PARAMS_EXTRACTED_BITS);
            templong |= ((uint64_t)(temp & maskex)) << (PARAMS_EXTRACTED_BITS * j);
            index++;
        }
        for(j = 0; j < PARAMS_EXTRACTED_BITS; j++) 
            pos[i*PARAMS_EXTRACTED_BITS + j] = (templong >> (8*j)) & 0xFF;
    }
}