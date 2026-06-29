; Pass 49 Holonet router export: 6502-style accumulator target
; No MUL and no MOD3.  Arithmetic is synthesized from load/store,
; add/subtract, compare, and branches.

LDA #0
STA $9
LDA $5
STA $12
x0y1_loop:
LDA $12
CMP #0
BEQ x0y1_done
LDA $9
CLC
ADC $0
STA $9
LDA $12
SEC
SBC #1
STA $12
JMP x0y1_loop
x0y1_done:
x0y1_mod_reduce:
LDA $9
CMP #3
BCC x0y1_mod_done
SEC
SBC #3
STA $9
JMP x0y1_mod_reduce
x0y1_mod_done:
LDA #0
STA $11
LDA $7
STA $12
x2y3_loop:
LDA $12
CMP #0
BEQ x2y3_done
LDA $11
CLC
ADC $2
STA $11
LDA $12
SEC
SBC #1
STA $12
JMP x2y3_loop
x2y3_done:
x2y3_mod_reduce:
LDA $11
CMP #3
BCC x2y3_mod_done
SEC
SBC #3
STA $11
JMP x2y3_mod_reduce
x2y3_mod_done:
LDA $9
CLC
ADC $11
STA $9
pos_reduce:
LDA $9
CMP #3
BCC pos_done
SEC
SBC #3
STA $9
JMP pos_reduce
pos_done:
LDA #0
STA $10
LDA $4
STA $12
x1y0_loop:
LDA $12
CMP #0
BEQ x1y0_done
LDA $10
CLC
ADC $1
STA $10
LDA $12
SEC
SBC #1
STA $12
JMP x1y0_loop
x1y0_done:
x1y0_mod_reduce:
LDA $10
CMP #3
BCC x1y0_mod_done
SEC
SBC #3
STA $10
JMP x1y0_mod_reduce
x1y0_mod_done:
LDA #0
STA $11
LDA $6
STA $12
x3y2_loop:
LDA $12
CMP #0
BEQ x3y2_done
LDA $11
CLC
ADC $3
STA $11
LDA $12
SEC
SBC #1
STA $12
JMP x3y2_loop
x3y2_done:
x3y2_mod_reduce:
LDA $11
CMP #3
BCC x3y2_mod_done
SEC
SBC #3
STA $11
JMP x3y2_mod_reduce
x3y2_mod_done:
LDA $10
CLC
ADC $11
STA $10
neg_reduce:
LDA $10
CMP #3
BCC neg_done
SEC
SBC #3
STA $10
JMP neg_reduce
neg_done:
LDA $9
STA $8
LDA $8
CLC
ADC #3
SEC
SBC $10
STA $8
result_reduce:
LDA $8
CMP #3
BCC result_done
SEC
SBC #3
STA $8
JMP result_reduce
result_done:
HLT
