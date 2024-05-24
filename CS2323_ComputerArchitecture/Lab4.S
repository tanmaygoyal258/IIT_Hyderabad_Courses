/*
 * hello.S
 *
 *  Created on: 19-Oct-2022
 *      Author: AI20BTECH11021_AI20BTECH11026 - TANMAY GOYAL, TANAY YADAV
 */

.section .data
L1: .word 1000000

.section .text
.global main

main:
la x3 , L1


lw t1, 0(x3)
lui tp, 0x10012
addi tp, tp, 0x004
lui t0, 0x0000
sw t0, 0(tp)
addi t0, t0, 0x020
sw t0, 4(tp)
lui gp, 0x10012
addi gp, gp, 0x00c

on:
sw zero, 0(gp)
add t2, zero, zero
beq zero, zero, delay1

delay1:
addi t2, t2, 1
beq t1, t2, off
beq zero, zero, delay1

off:
sw t0, 0(gp)
add t2, zero, zero
beq zero, zero, delay2

delay2:
addi t2, t2, 10
beq t1, t2, on
beq zero, zero, delay2

Lwhile1:
j Lwhile1
