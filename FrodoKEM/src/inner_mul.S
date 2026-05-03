.section .text
.globl inner_mul_row


inner_mul_row:
    # putting stack pointer 128 bytes below the caller's stack frame, to save s0..s11 and ra
    #and also to have space for two row pointers for s rows 6 and 7

    addi    sp, sp, -128
    sd      s0,   0(sp)
    sd      s1,   8(sp)
    sd      s2,  16(sp)
    sd      s3,  24(sp)
    sd      s4,  32(sp)
    sd      s5,  40(sp)
    sd      s6,  48(sp)
    sd      s7,  56(sp)
    sd      s8,  64(sp)
    sd      s9,  72(sp)
    sd      s10, 80(sp)
    sd      s11, 88(sp)
    sd      ra,  96(sp)
    # sp+104: row 6 pointer
    # sp+112: row 7 pointer

    # load the e values for this out_row into s0..s7
    lhu     s0,  0(a0)
    lhu     s1,  2(a0)
    lhu     s2,  4(a0)
    lhu     s3,  6(a0)
    lhu     s4,  8(a0)
    lhu     s5, 10(a0)
    lhu     s6, 12(a0)
    lhu     s7, 14(a0)

    #  pre-compute row pointers for s rows 2..7 and save on stack  (offsets can be up to 2048)
    li      t0, 2560
    add     s8,  a1, t0
    li      t0, 3840
    add     s9,  a1, t0
    li      t0, 5120
    add     s10, a1, t0
    li      t0, 6400
    add     s11, a1, t0
    li      t0, 7680
    add     t1,  a1, t0
    sd      t1, 104(sp)
    li      t0, 8960
    add     t1,  a1, t0
    sd      t1, 112(sp)

    # number of iterations
    li      t6, 640

.Lj_loop:
    # load s_col[0..5] for this j
    lhu     t0,    0(a1)      # s[0*640 + j]
    lhu     t1, 1280(a1)      # s[1*640 + j]
    lhu     t2,    0(s8)      # s[2*640 + j]
    lhu     t3,    0(s9)      # s[3*640 + j]
    lhu     t4,    0(s10)     # s[4*640 + j]
    lhu     t5,    0(s11)     # s[5*640 + j]

    # load s_col[6] and s_col[7]
    ld      a3, 104(sp)
    ld      a4, 112(sp)
    lhu     a3, 0(a3)         # s[6*640 + j]
    lhu     a4, 0(a4)         # s[7*640 + j]

    # load A_row[j]
    lhu     a5, 0(a2)

    # multiply A_row[j] against all 8 s_col values, accumulate into s0..s7
    # builds each element of the current row of B
    mulw    a6, a5, t0  ;  addw    s0, s0, a6
    mulw    a6, a5, t1  ;  addw    s1, s1, a6
    mulw    a6, a5, t2  ;  addw    s2, s2, a6
    mulw    a6, a5, t3  ;  addw    s3, s3, a6
    mulw    a6, a5, t4  ;  addw    s4, s4, a6
    mulw    a6, a5, t5  ;  addw    s5, s5, a6
    mulw    a6, a5, a3  ;  addw    s6, s6, a6
    mulw    a6, a5, a4  ;  addw    s7, s7, a6

    # advance pointers by 2 bytes (one j step)
    addi    a1,  a1,  2
    addi    s8,  s8,  2
    addi    s9,  s9,  2
    addi    s10, s10, 2
    addi    s11, s11, 2

    # advance row 6 and row 7 pointers on stack
    ld      a3, 104(sp)
    addi    a3, a3, 2
    sd      a3, 104(sp)
    ld      a4, 112(sp)
    addi    a4, a4, 2
    sd      a4, 112(sp)

    addi    a2, a2, 2         # A_row pointer advance (e.g from a0 to a1)x

    # loop counter update and loop condition check
    addi    t6, t6, -1
    bnez    t6, .Lj_loop

    # write the 8 final accumulated values back to memory (the output row of B + e)
    sh      s0,  0(a0)
    sh      s1,  2(a0)
    sh      s2,  4(a0)
    sh      s3,  6(a0)
    sh      s4,  8(a0)
    sh      s5, 10(a0)
    sh      s6, 12(a0)
    sh      s7, 14(a0)

    # restore all borrowed registers to their original values
    ld      s0,   0(sp)
    ld      s1,   8(sp)
    ld      s2,  16(sp)
    ld      s3,  24(sp)
    ld      s4,  32(sp)
    ld      s5,  40(sp)
    ld      s6,  48(sp)
    ld      s7,  56(sp)
    ld      s8,  64(sp)
    ld      s9,  72(sp)
    ld      s10, 80(sp)
    ld      s11, 88(sp)
    ld      ra,  96(sp)
    addi    sp, sp, 128

    ret