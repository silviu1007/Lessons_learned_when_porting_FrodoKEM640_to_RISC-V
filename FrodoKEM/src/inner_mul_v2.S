.section .text
.globl inner_mul_row_v2


inner_mul_row_v2:

    addi   sp, sp, -16
    sd s0, 0(sp)     # save s0 on stack
    sd s1, 8(sp)     # save s1 on stack

    # s0 = current row byte offset into S^T (starts at 0, adds 1280 each iter)
    # s1 = current byte offset into out_row (starts at 0, adds 2 each iter)

    li    s0, 0
    li    s1, 0

    li   t6, 8

.Lk_loop:

    add a5, a0, s1     # a5 = &out_row[k]
    lhu a5, 0(a5)     # a5 = out_row[k] (initially 0)

    add a3, a1, s0     # a3 = &s[k*PARAMS_N]
    mv a4, a2        # a4 = &A_row[0]

    li t5, 320        # inner loop counter (PARAMS_N / 2)

.Lj_loop:

    lwu     a6, 0(a4)     # load A[j] and A[j+1]
    lwu     a7, 0(a3)     # load S^T[k][j] and S^T[k][j+1]

   slli t0, a6, 48
   srli t0, t0, 48
   slli t2, a7, 48
   srli t2, t2, 48

   srli t1, a6, 16
   srli t3, a7, 16
   
    mulw t4, t0, t2  # A[j] * S^T[k][j]
    addw a5, a5, t4  # acc += A[j] * S^T[k][j]

    mulw t4, t1, t3
    addw a5, a5, t4  # acc += A[j+1] * S^T[k][j+1]

    addi a3, a3, 4   # advance S^T pointer 
    addi a4, a4, 4   # advance A_row pointer by  

    addi t5, t5, -1  # inner loop counter decrement
    bnez t5, .Lj_loop

    add t4, a0, s1  # a0 + s1 = &out_row[k]
    sh a5, 0(t4)    # store out_row[k]

    li t4, 1280
    add s0, s0, t4
    addi s1, s1, 2

    addi t6, t6, -1  # outer loop counter decrement
    bnez t6, .Lk_loop

    ld s0, 0(sp)     # restore s0
    ld s1, 8(sp)     # restore s1
    addi sp, sp, 16
    ret
    
    