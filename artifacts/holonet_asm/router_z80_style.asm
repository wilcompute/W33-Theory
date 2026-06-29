; Pass 49 Holonet router export: Z80-style accumulator target
; RAM $00..$03 = source address x0..x3
; RAM $04..$07 = destination address y0..y3
; RAM $08 = B(x,y) mod 3
; RAM $09/$0A/$0B/$0C = pos/neg/tmp/counter scratch

LD A, #0
LD ($09), A
LD A, ($05)
LD ($0C), A
x0y1_loop:
LD A, ($0C)
CP #0
JP Z, x0y1_done
LD A, ($09)
ADD A, ($00)
LD ($09), A
LD A, ($0C)
SUB #1
LD ($0C), A
JP x0y1_loop
x0y1_done:
x0y1_mod_reduce:
LD A, ($09)
CP #3
JP C, x0y1_mod_done
SUB #3
LD ($09), A
JP x0y1_mod_reduce
x0y1_mod_done:
LD A, #0
LD ($0B), A
LD A, ($07)
LD ($0C), A
x2y3_loop:
LD A, ($0C)
CP #0
JP Z, x2y3_done
LD A, ($0B)
ADD A, ($02)
LD ($0B), A
LD A, ($0C)
SUB #1
LD ($0C), A
JP x2y3_loop
x2y3_done:
x2y3_mod_reduce:
LD A, ($0B)
CP #3
JP C, x2y3_mod_done
SUB #3
LD ($0B), A
JP x2y3_mod_reduce
x2y3_mod_done:
LD A, ($09)
ADD A, ($0B)
LD ($09), A
pos_reduce:
LD A, ($09)
CP #3
JP C, pos_done
SUB #3
LD ($09), A
JP pos_reduce
pos_done:
LD A, #0
LD ($0A), A
LD A, ($04)
LD ($0C), A
x1y0_loop:
LD A, ($0C)
CP #0
JP Z, x1y0_done
LD A, ($0A)
ADD A, ($01)
LD ($0A), A
LD A, ($0C)
SUB #1
LD ($0C), A
JP x1y0_loop
x1y0_done:
x1y0_mod_reduce:
LD A, ($0A)
CP #3
JP C, x1y0_mod_done
SUB #3
LD ($0A), A
JP x1y0_mod_reduce
x1y0_mod_done:
LD A, #0
LD ($0B), A
LD A, ($06)
LD ($0C), A
x3y2_loop:
LD A, ($0C)
CP #0
JP Z, x3y2_done
LD A, ($0B)
ADD A, ($03)
LD ($0B), A
LD A, ($0C)
SUB #1
LD ($0C), A
JP x3y2_loop
x3y2_done:
x3y2_mod_reduce:
LD A, ($0B)
CP #3
JP C, x3y2_mod_done
SUB #3
LD ($0B), A
JP x3y2_mod_reduce
x3y2_mod_done:
LD A, ($0A)
ADD A, ($0B)
LD ($0A), A
neg_reduce:
LD A, ($0A)
CP #3
JP C, neg_done
SUB #3
LD ($0A), A
JP neg_reduce
neg_done:
LD A, ($09)
LD ($08), A
LD A, ($08)
ADD A, #3
SUB ($0A)
LD ($08), A
result_reduce:
LD A, ($08)
CP #3
JP C, result_done
SUB #3
LD ($08), A
JP result_reduce
result_done:
HALT
