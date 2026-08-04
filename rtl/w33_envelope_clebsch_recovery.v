// Passes 3338-3340: minimum four-bit antipodal-axis checksum decoder.
// The trusted tag labels one of the 16 antipodal axes of Q5.  The two
// candidate words are {0,tag} and its five-bit complement.  Their distance is
// five, so radius-two balls are disjoint.  Envelope membership then yields
// exact correction of any <=2 state-bit faults.
module w33_envelope_clebsch_recovery(
    input  wire [4:0] observed,
    input  wire [3:0] axis_tag,
    output reg  [4:0] corrected,
    output reg        valid,
    output reg        changed,
    output reg  [1:0] distance
);
  wire [4:0] candidate0 = {1'b0, axis_tag};
  wire [4:0] candidate1 = {1'b1, ~axis_tag};
  reg valid0, valid1;
  reg [2:0] d0, d1;

  function is_envelope;
    input [4:0] x;
    begin
      case (x)
        5'd0,5'd1,5'd2,5'd3,5'd4,5'd5,5'd6,5'd8,5'd10,5'd11,5'd12,
        5'd13,5'd16,5'd17,5'd19,5'd20,5'd22,5'd24,5'd25,5'd26,5'd29,5'd30:
          is_envelope=1'b1;
        default:is_envelope=1'b0;
      endcase
    end
  endfunction

  function [2:0] pop5;
    input [4:0] x;
    begin pop5=x[0]+x[1]+x[2]+x[3]+x[4]; end
  endfunction

  always @* begin
    valid0=is_envelope(candidate0);
    valid1=is_envelope(candidate1);
    d0=pop5(observed^candidate0);
    d1=pop5(observed^candidate1);
    corrected=5'd0;
    valid=1'b0;
    changed=1'b0;
    distance=2'd3;
    if (valid0 && d0<=2 && !(valid1 && d1<=2)) begin
      corrected=candidate0; valid=1'b1; changed=(observed!=candidate0); distance=d0[1:0];
    end else if (valid1 && d1<=2 && !(valid0 && d0<=2)) begin
      corrected=candidate1; valid=1'b1; changed=(observed!=candidate1); distance=d1[1:0];
    end
  end
endmodule
