`timescale 1ns/1ps
module tb_w33_pass3486_3499;
    reg [1:0] k0,k1,k2;
    reg [2:0] row_channel,col_channel;
    wire signed [4:0] coefficient;
    reg [4:0] message;
    wire [27:0] codeword;
    reg [15:0] point_error;
    wire [15:0] syndrome;
    integer a,b,c,r,s,m,i,j,wt,minwt,cases;
    integer cols [0:27];
    reg [15:0] masks [0:15];
    integer expected;

    w33_five_channel_torus_engine torus(.k0(k0),.k1(k1),.k2(k2),.row_channel(row_channel),.col_channel(col_channel),.coefficient(coefficient));
    w33_equivariant_linear28_encode encoder(.message(message),.codeword(codeword));
    w33_clebsch_biplane_locator locator(.point_error(point_error),.syndrome(syndrome));

    function integer ch(input integer x); begin ch=(x==0)?2:-1; end endfunction
    function integer xk(input integer rr,input integer cc);
      begin xk=0; if(rr==0&&cc==1)xk=2; else if((rr==1&&(cc==0||cc==1))||(rr==3&&(cc==2||cc==3)))xk=1; else if(rr==2&&cc==3)xk=2; end
    endfunction
    function integer yk(input integer rr,input integer cc);
      begin yk=0; if((rr==0&&cc==2)||(rr==1&&cc==3))yk=2; else if((rr==2&&(cc==0||cc==2))||(rr==3&&(cc==1||cc==3)))yk=1; end
    endfunction
    initial begin
      cols[0]=1;cols[1]=2;cols[2]=4;cols[3]=7;cols[4]=8;cols[5]=16;cols[6]=24;cols[7]=8;cols[8]=16;cols[9]=24;cols[10]=9;cols[11]=12;cols[12]=18;cols[13]=20;cols[14]=25;cols[15]=26;cols[16]=10;cols[17]=17;cols[18]=28;cols[19]=11;cols[20]=14;cols[21]=19;cols[22]=21;cols[23]=29;cols[24]=30;cols[25]=13;cols[26]=22;cols[27]=27;
      masks[0]=16'h8117;masks[1]=16'h422b;masks[2]=16'h244d;masks[3]=16'h188e;masks[4]=16'h1871;masks[5]=16'h24b2;masks[6]=16'h42d4;masks[7]=16'h81e8;masks[8]=16'h1781;masks[9]=16'h2b42;masks[10]=16'h4d24;masks[11]=16'h8e18;masks[12]=16'h7118;masks[13]=16'hb224;masks[14]=16'hd442;masks[15]=16'he881;
      cases=0;
      for(a=0;a<3;a=a+1)for(b=0;b<3;b=b+1)for(c=0;c<3;c=c+1)for(r=0;r<5;r=r+1)for(s=0;s<5;s=s+1)begin
        k0=a;k1=b;k2=c;row_channel=r;col_channel=s;#1;
        if(r<4&&s<4)expected=ch(a)*xk(r,s)+ch(b)*yk(r,s)+((r==s)?ch(c):0);else if(r==4&&s==4)expected=-ch(a)-ch(b)+ch(c);else expected=0;
        if($signed(coefficient)!==expected)$fatal(1,"torus mismatch"); cases=cases+1;
      end
      minwt=99;
      for(m=0;m<32;m=m+1)begin message=m;#1;wt=0;for(i=0;i<28;i=i+1)begin expected=^((m)&cols[i]);if(codeword[i]!==expected)$fatal(1,"encoder mismatch");wt=wt+codeword[i];end if(m!=0&&wt<minwt)minwt=wt;end
      if(minwt!=11)$fatal(1,"distance mismatch");
      point_error=0;#1;if(syndrome!=0)$fatal(1,"zero locator");
      for(i=0;i<16;i=i+1)begin point_error=(16'h1<<i);#1;for(j=0;j<16;j=j+1)if(syndrome[j]!==^(point_error&masks[j]))$fatal(1,"locator mismatch");end
      $display("PASS torus_entries=%0d code_messages=32 biplane_singles=17 distance=11",cases);
      $finish;
    end
endmodule
