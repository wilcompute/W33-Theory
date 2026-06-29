; Pass 49 Holonet router export: 4004-flavoured 4-bit target
; RAM $0..$3 = source address x0..x3
; RAM $4..$7 = destination address y0..y3
; RAM $8 = B(x,y) mod 3
; This target keeps Pass 47's primitive MUL and MOD3 opcodes.

0000: LD  R0, $00
0001: LD  R1, $05
0002: MUL R0, R1
0003: LD  R2, $02
0004: LD  R3, $07
0005: MUL R2, R3
0006: ADD R0, R2
0007: MOD3 R0
0008: LD  R4, $01
0009: LD  R5, $04
000A: MUL R4, R5
000B: LD  R6, $03
000C: LD  R7, $06
000D: MUL R6, R7
000E: ADD R4, R6
000F: MOD3 R4
0010: LDI R8, #3
0011: SUB R8, R4
0012: ADD R0, R8
0013: MOD3 R0
0014: ST  $08, R0
0015: HLT
