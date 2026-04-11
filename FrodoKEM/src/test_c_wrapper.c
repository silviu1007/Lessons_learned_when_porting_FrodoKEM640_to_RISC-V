// Temporary C version of inner_mul_row to verify the calling structure is correct
// before debugging the assembly
#include <stdint.h>
void inner_mul_row(uint16_t *out_row, const uint16_t *s, const uint16_t *A_row)
{
    int j, k;
    for (j = 0; j < 640; j++) {
        for (k = 0; k < 8; k++) {
            out_row[k] += A_row[j] * s[k*640 + j];
        }
    }
}