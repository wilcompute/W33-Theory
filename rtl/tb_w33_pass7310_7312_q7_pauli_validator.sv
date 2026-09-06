`timescale 1ns/1ps

module tb_w33_pass7310_7312_q7_pauli_validator;
  reg clk=0,rst=1,in_valid=0;
  reg [11:0] point_in=0;
  reg [395:0] flat=0;
  wire parallel_valid;
  wire serial_ready,serial_done,serial_accept;
  wire bram_ready,bram_done,bram_accept;
  wire [9:0] serial_pairs,bram_pairs;
  integer i,elapsed,serial_latency,bram_latency;
  integer seen_serial,seen_bram;
  always #5 clk=~clk;

  w33_pass7311_q7_parallel u_parallel(.points_flat(flat),.valid(parallel_valid));
  w33_pass7311_q7_serial u_serial(
    .clk(clk),.rst(rst),.in_valid(in_valid),.point_in(point_in),
    .in_ready(serial_ready),.done(serial_done),.accept(serial_accept),
    .pairs_checked(serial_pairs));
  w33_pass7311_q7_bram u_bram(
    .clk(clk),.rst(rst),.in_valid(in_valid),.point_in(point_in),
    .in_ready(bram_ready),.done(bram_done),.accept(bram_accept),
    .pairs_checked(bram_pairs));

  function automatic [11:0] cert_point(input integer idx);
    begin
      case(idx)
        0:cert_point=12'ha08;  1:cert_point=12'h648;
        2:cert_point=12'h888;  3:cert_point=12'ha88;
        4:cert_point=12'h6c8;  5:cert_point=12'h588;
        6:cert_point=12'h881;  7:cert_point=12'hb41;
        8:cert_point=12'h181;  9:cert_point=12'h889;
       10:cert_point=12'hac9; 11:cert_point=12'h949;
       12:cert_point=12'hb49; 13:cert_point=12'h011;
       14:cert_point=12'h059; 15:cert_point=12'hcd9;
       16:cert_point=12'h359; 17:cert_point=12'h959;
       18:cert_point=12'hd99; 19:cert_point=12'h621;
       20:cert_point=12'h261; 21:cert_point=12'ha61;
       22:cert_point=12'h4e1; 23:cert_point=12'h629;
       24:cert_point=12'h269; 25:cert_point=12'h469;
       26:cert_point=12'h6a9; 27:cert_point=12'hca9;
       28:cert_point=12'h1a9; 29:cert_point=12'h431;
       30:cert_point=12'h471; 31:cert_point=12'ha71;
       32:cert_point=12'h7b1;
       default:cert_point=0;
      endcase
    end
  endfunction

  task run_case(input integer corrupt);
    begin
      for(i=0;i<33;i=i+1)
        flat[12*i +: 12]=(corrupt&&i==1)?cert_point(0):cert_point(i);
      #1;
      if(parallel_valid!==(corrupt?1'b0:1'b1))
        $fatal(1,"parallel verdict mismatch corrupt=%0d",corrupt);

      @(negedge clk);in_valid=1;
      for(i=0;i<33;i=i+1)begin
        point_in=(corrupt&&i==1)?cert_point(0):cert_point(i);
        @(negedge clk);
      end
      in_valid=0;point_in=0;elapsed=33;seen_serial=0;seen_bram=0;
      while(!(seen_serial&&seen_bram))begin
        @(negedge clk);elapsed=elapsed+1;
        if(serial_done&&!seen_serial)begin
          seen_serial=1;serial_latency=elapsed;
          if(serial_pairs!==528||serial_accept!==(corrupt?0:1))
            $fatal(1,"serial mismatch corrupt=%0d pairs=%0d",corrupt,serial_pairs);
        end
        if(bram_done&&!seen_bram)begin
          seen_bram=1;bram_latency=elapsed;
          if(bram_pairs!==528||bram_accept!==(corrupt?0:1))
            $fatal(1,"bram mismatch corrupt=%0d pairs=%0d",corrupt,bram_pairs);
        end
        if(elapsed>1700)$fatal(1,"timeout");
      end
      if(serial_latency!==562)$fatal(1,"serial latency %0d",serial_latency);
      if(bram_latency!==1618)$fatal(1,"bram latency %0d",bram_latency);
      @(negedge clk);
    end
  endtask

  initial begin
    repeat(2)@(negedge clk);rst=0;
    run_case(0);
    run_case(1);
    $display("PASS7310-7312: exact accepted, duplicate rejected, 528 pairs, cycles 562/1618");
    $finish;
  end
endmodule
