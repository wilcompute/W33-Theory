`timescale 1ns/1ps
module tb_w33_pass3542_3555;
    reg [3:0] axis;
    wire [4:0] label;
    integer i,j,p,d;
    reg [20:0] words [0:136];
    reg [15:0] columns [0:15];
    reg [4:0] labels [0:15];
    w33_clebsch_double_fault_locator5 dut(.axis(axis),.label(label));

    function integer pop21(input [20:0] x);
        integer k;
        begin pop21=0; for(k=0;k<21;k=k+1) pop21=pop21+x[k]; end
    endfunction

    initial begin
        columns[0]=16'h8117; columns[1]=16'h422b; columns[2]=16'h244d; columns[3]=16'h188e;
        columns[4]=16'h1871; columns[5]=16'h24b2; columns[6]=16'h42d4; columns[7]=16'h81e8;
        columns[8]=16'h1781; columns[9]=16'h2b42; columns[10]=16'h4d24; columns[11]=16'h8e18;
        columns[12]=16'h7118; columns[13]=16'hb224; columns[14]=16'hd442; columns[15]=16'he881;
        labels[0]=0; labels[1]=0; labels[2]=0; labels[3]=0; labels[4]=30; labels[5]=25;
        labels[6]=0; labels[7]=7; labels[8]=0; labels[9]=27; labels[10]=13; labels[11]=22;
        labels[12]=14; labels[13]=18; labels[14]=29; labels[15]=1;
        for(i=0;i<16;i=i+1) begin axis=i; #1; if(label!==labels[i]) $fatal(1,"locator label failure %0d",i); end
        p=0; words[p]={5'd0,16'd0}; p=p+1;
        for(i=0;i<16;i=i+1) begin words[p]={labels[i],columns[i]}; p=p+1; end
        for(i=0;i<16;i=i+1) for(j=i+1;j<16;j=j+1) begin
            words[p]={labels[i]^labels[j],columns[i]^columns[j]}; p=p+1;
        end
        if(p!=137) $fatal(1,"pattern count failure");
        for(i=0;i<137;i=i+1) for(j=i+1;j<137;j=j+1) begin
            d=pop21(words[i]^words[j]);
            if(d<3) $fatal(1,"compound distance failure %0d %0d d=%0d",i,j,d);
        end
        $display("PASS compound_fault_patterns=137 companion_bits=5 minimum_distance=3");
        $finish;
    end
endmodule
