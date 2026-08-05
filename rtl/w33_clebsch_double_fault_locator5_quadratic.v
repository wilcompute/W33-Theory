// Pass 3575: multiplicatively optimal quadratic implementation.
// Five AND terms are necessary because the output quadratic-span rank is five.
module w33_clebsch_double_fault_locator5_quadratic(
    input  wire [3:0] axis,
    output wire [4:0] label
);
    wire x0 = axis[0];
    wire x1 = axis[1];
    wire x2 = axis[2];
    wire x3 = axis[3];

    wire a = x0 & x2;
    wire b = x0 & x3;
    wire c = x1 & x2;
    wire d = x1 & x3;
    wire e = x2 & x3;

    wire t0 = a ^ b;
    wire y0 = t0 ^ d;
    wire t1 = x2 ^ t0;
    wire y1 = t1 ^ c;
    wire t2 = y1 ^ a;
    wire y2 = t2 ^ y0;
    wire y3 = t0 ^ y2;
    wire y4 = t2 ^ e;

    assign label = {y4,y3,y2,y1,y0};
endmodule
