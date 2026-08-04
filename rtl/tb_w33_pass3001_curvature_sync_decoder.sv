`timescale 1ns/1ps
module tb_w33_pass3001_curvature_sync_decoder;
  logic [23:0] rx;
  logic [3:0] phase, distance;
  logic valid_unique;
  integer p,i,a,cases;
  logic [1:0] orig,alt;

  w33_pass3001_curvature_sync_decoder dut(
    .rx_symbols(rx),.phase(phase),.distance(distance),.valid_unique(valid_unique));

  function automatic logic [1:0] base_symbol(input integer idx);
    begin
      case(idx)
        0:base_symbol=1; 1:base_symbol=0; 2:base_symbol=2; 3:base_symbol=3;
        4:base_symbol=3; 5:base_symbol=2; 6:base_symbol=0; 7:base_symbol=0;
        8:base_symbol=1; 9:base_symbol=1; 10:base_symbol=2; 11:base_symbol=3;
        default:base_symbol=2'bxx;
      endcase
    end
  endfunction

  task automatic load_shift(input integer sh);
    integer j;
    begin
      for(j=0;j<12;j=j+1) rx[2*j +:2]=base_symbol((sh+j)%12);
    end
  endtask

  initial begin
    cases=0;
    for(p=0;p<12;p=p+1) begin
      load_shift(p); #1;
      if(!valid_unique || phase!==p[3:0] || distance!==0)
        $fatal(1,"clean shift %0d phase=%0d d=%0d valid=%0d",p,phase,distance,valid_unique);
      cases=cases+1;
      for(i=0;i<12;i=i+1) begin
        load_shift(p); orig=rx[2*i +:2];
        for(a=1;a<=3;a=a+1) begin
          alt=(orig+a)%4; rx[2*i +:2]=alt; #1;
          if(!valid_unique || phase!==p[3:0] || distance!==1)
            $fatal(1,"single substitution p=%0d i=%0d a=%0d",p,i,a);
          cases=cases+1;
          rx[2*i +:2]=orig;
        end
      end
    end
    $display("PASS %0d curvature synchronization cases",cases);
    $finish;
  end
endmodule
