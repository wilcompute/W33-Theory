`timescale 1ns/1ps
module tb_w33_pass3570_3576;
    reg [3:0] axis;
    wire [4:0] table_label;
    wire [4:0] quadratic_label;
    integer i,j,p,d;
    reg [20:0] words [0:136];
    reg [15:0] columns [0:15];

    w33_clebsch_double_fault_locator5 table_impl(.axis(axis),.label(table_label));
    w33_clebsch_double_fault_locator5_quadratic quad_impl(.axis(axis),.label(quadratic_label));

    function integer pop21(input [20:0] x);
        integer k;
        begin pop21=0; for(k=0;k<21;k=k+1) pop21=pop21+x[k]; end
    endfunction

    initial begin
        columns[0]=16'h8117; columns[1]=16'h422b; columns[2]=16'h244d; columns[3]=16'h188e;
        columns[4]=16'h1871; columns[5]=16'h24b2; columns[6]=16'h42d4; columns[7]=16'h81e8;
        columns[8]=16'h1781; columns[9]=16'h2b42; columns[10]=16'h4d24; columns[11]=16'h8e18;
        columns[12]=16'h7118; columns[13]=16'hb224; columns[14]=16'hd442; columns[15]=16'he881;
        for(i=0;i<16;i=i+1) begin
            axis=i; #1;
            if(quadratic_label!==table_label) $fatal(1,"quadratic/table mismatch %0d",i);
        end
        p=0; words[p]={5'd0,16'd0}; p=p+1;
        for(i=0;i<16;i=i+1) begin axis=i; #1; words[p]={quadratic_label,columns[i]}; p=p+1; end
        for(i=0;i<16;i=i+1) for(j=i+1;j<16;j=j+1) begin
            axis=i; #1; words[p][20:16]=quadratic_label;
            axis=j; #1; words[p][20:16]=words[p][20:16]^quadratic_label;
            words[p][15:0]=columns[i]^columns[j]; p=p+1;
        end
        if(p!=137) $fatal(1,"pattern count failure");
        for(i=0;i<137;i=i+1) for(j=i+1;j<137;j=j+1) begin
            d=pop21(words[i]^words[j]);
            if(d<3) $fatal(1,"compound distance failure %0d %0d d=%0d",i,j,d);
        end
        $display("PASS quadratic_locator equivalent=16 patterns=137 minimum_distance=3 and_gates=5");
        $finish;
    end
endmodule
