`timescale 1ns/1ps
module tb_w33_pass3514_3527;
    reg [4:0] message;
    wire [15:0] codeword;
    reg [3:0] axis;
    wire [2:0] label;
    integer m, i, j, p, q, weight, count8, count16;
    reg [18:0] words [0:136];
    reg [15:0] columns [0:15];
    reg [2:0] labels [0:15];

    w33_rm14_equivariant_encode rm(.message(message), .codeword(codeword));
    w33_clebsch_double_fault_locator3 loc(.axis(axis), .label(label));

    function integer pop16(input [15:0] x);
        integer k;
        begin pop16=0; for(k=0;k<16;k=k+1) pop16=pop16+x[k]; end
    endfunction

    initial begin
        columns[0]=16'h8117; columns[1]=16'h422b; columns[2]=16'h244d; columns[3]=16'h188e;
        columns[4]=16'h1871; columns[5]=16'h24b2; columns[6]=16'h42d4; columns[7]=16'h81e8;
        columns[8]=16'h1781; columns[9]=16'h2b42; columns[10]=16'h4d24; columns[11]=16'h8e18;
        columns[12]=16'h7118; columns[13]=16'hb224; columns[14]=16'hd442; columns[15]=16'he881;
        labels[0]=0; labels[1]=0; labels[2]=0; labels[3]=0; labels[4]=0; labels[5]=1;
        labels[6]=2; labels[7]=3; labels[8]=0; labels[9]=2; labels[10]=3; labels[11]=4;
        labels[12]=5; labels[13]=6; labels[14]=1; labels[15]=7;

        count8=0; count16=0;
        for(m=0;m<32;m=m+1) begin
            message=m; #1; weight=pop16(codeword);
            if(m==0 && weight!=0) $fatal(1,"zero word failure");
            if(m!=0 && weight==8) count8=count8+1;
            else if(m!=0 && weight==16) count16=count16+1;
            else if(m!=0) $fatal(1,"RM weight failure m=%0d w=%0d",m,weight);
        end
        if(count8!=30 || count16!=1) $fatal(1,"RM enumerator failure");
        for(i=0;i<16;i=i+1) begin axis=i; #1; if(label!==labels[i]) $fatal(1,"locator label failure"); end

        p=0; words[p]={3'd0,16'd0}; p=p+1;
        for(i=0;i<16;i=i+1) begin words[p]={labels[i],columns[i]}; p=p+1; end
        for(i=0;i<16;i=i+1) for(j=i+1;j<16;j=j+1) begin
            words[p]={labels[i]^labels[j],columns[i]^columns[j]}; p=p+1;
        end
        if(p!=137) $fatal(1,"pattern count failure");
        for(i=0;i<137;i=i+1) for(j=i+1;j<137;j=j+1)
            if(words[i]===words[j]) $fatal(1,"compound locator collision %0d %0d",i,j);
        $display("PASS RM14 words=32 compound_locator_patterns=137 extra_bits=3");
        $finish;
    end
endmodule
