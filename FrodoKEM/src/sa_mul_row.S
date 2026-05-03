.section .text
.globl sa_mul_row


# Equivalent C:
#   for (j = 0; j < PARAMS_N; j++)
#       out[k*PARAMS_N + j] += s_prime * A_row[j];


sa_mul_row:
    addi    sp, sp, -64
    sd      s0,  0(sp)
    sd      s1,  8(sp)
    sd      s2, 16(sp)
    sd      s3, 24(sp)
    sd      s4, 32(sp)
    sd      s5, 40(sp)
    sd      s6, 48(sp)
    sd      s7, 56(sp)

    # window loop: 80 iterations 
    li      t5, 80

.Lwindow_loop:
    lhu     s0,  0(a0)
    lhu     s1,  2(a0)
    lhu     s2,  4(a0)
    lhu     s3,  6(a0)
    lhu     s4,  8(a0)
    lhu     s5, 10(a0)
    lhu     s6, 12(a0)
    lhu     s7, 14(a0)

    lwu     a3,  0(a1)      # a3 bits 15:0  = A[j],   bits 31:16 = A[j+1]
    lwu     a4,  4(a1)      # a4 bits 15:0  = A[j+2], bits 31:16 = A[j+3]
    lwu     a5,  8(a1)      # a5 bits 15:0  = A[j+4], bits 31:16 = A[j+5]
    lwu     a6, 12(a1)      # a6 bits 15:0  = A[j+6], bits 31:16 = A[j+7]

    slli    t0, a3, 48
    srli    t0, t0, 48      # t0 = A[j]
    srli    t1, a3, 16      # t1 = A[j+1]

    mulw    t4, t0, a2  ;  addw    s0, s0, t4
    mulw    t4, t1, a2  ;  addw    s1, s1, t4

    slli    t2, a4, 48
    srli    t2, t2, 48      # t2 = A[j+2]
    srli    t3, a4, 16      # t3 = A[j+3]

    mulw    t4, t2, a2  ;  addw    s2, s2, t4
    mulw    t4, t3, a2  ;  addw    s3, s3, t4

    slli    t0, a5, 48
    srli    t0, t0, 48      # t0 = A[j+4]
    srli    t1, a5, 16      # t1 = A[j+5]

    mulw    t4, t0, a2  ;  addw    s4, s4, t4
    mulw    t4, t1, a2  ;  addw    s5, s5, t4

    slli    t2, a6, 48
    srli    t2, t2, 48      # t2 = A[j+6]
    srli    t3, a6, 16      # t3 = A[j+7]

    mulw    t4, t2, a2  ;  addw    s6, s6, t4
    mulw    t4, t3, a2  ;  addw    s7, s7, t4

    sh      s0,  0(a0)
    sh      s1,  2(a0)
    sh      s2,  4(a0)
    sh      s3,  6(a0)
    sh      s4,  8(a0)
    sh      s5, 10(a0)
    sh      s6, 12(a0)
    sh      s7, 14(a0)

    addi    a0, a0, 16
    addi    a1, a1, 16

    addi    t5, t5, -1
    bnez    t5, .Lwindow_loop

    ld      s0,  0(sp)
    ld      s1,  8(sp)
    ld      s2, 16(sp)
    ld      s3, 24(sp)
    ld      s4, 32(sp)
    ld      s5, 40(sp)
    ld      s6, 48(sp)
    ld      s7, 56(sp)
    addi    sp, sp, 64

    ret