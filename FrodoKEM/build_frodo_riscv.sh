#!/bin/bash
# Build FrodoKEM-640 for RISC-V 64-bit Linux at multiple optimization levels

set -e

CC=riscv64-linux-gnu-gcc
MARCH="-march=rv64gc -mabi=lp64d"
DEFINES="-DNIX -D_PPC_ -D_REFERENCE_ -D_SHAKE128_FOR_A_ -DNO_OPENSSL -DUSE_TESTING"
INCLUDES="-I./src -I../common -I../common/aes -I../common/sha3 -I../common/random"
COMMON_FLAGS="-std=gnu11 -static $MARCH $DEFINES $INCLUDES"

SRCS_LIB="src/frodo640.c src/util.c src/inner_mul.S src/inner_mul_v2.S src/sa_mul_row.S \
          ../common/random/random.c \
          ../common/aes/aes_c.c \
          ../common/sha3/fips202.c"

mkdir -p benchmarks

for OPT in O0 O1 O2 O3 Os; do
    OUT="benchmarks/frodo640_asm23_$OPT"

    $CC -$OPT $COMMON_FLAGS \
        $SRCS_LIB \
        tests/test_KEM640.c \
        -lm \
        -o $OUT

    echo "    Built: $OUT"
    file $OUT
done


ls -lh benchmarks/
