`default_nettype none

module w33_pass3254_universe_admission (
    input  logic [1:0] universe_id,
    input  logic [3:0] opcode_count,
    input  logic       group_order_ok,
    input  logic       manifest_valid,
    input  logic       projection_valid,
    output logic       admitted,
    output logic       census_member,
    output logic       comparison_only,
    output logic       comparison_enabled
);
    always_comb begin
        admitted          = 1'b0;
        census_member     = 1'b0;
        comparison_only   = 1'b0;
        comparison_enabled= 1'b0;
        unique case (universe_id)
            2'b00: begin // exact universal four-opcode universe
                admitted        = group_order_ok && (opcode_count == 4);
                comparison_only = admitted;
            end
            2'b01: begin // exact 194-design five/six-opcode census
                admitted      = group_order_ok && ((opcode_count == 5) || (opcode_count == 6));
                census_member = admitted;
            end
            2'b10: begin // reserved future universe, fail closed without manifest
                admitted        = group_order_ok && manifest_valid;
                comparison_only = admitted;
            end
            default: begin
                admitted        = 1'b0;
                census_member   = 1'b0;
                comparison_only = 1'b0;
            end
        endcase
        comparison_enabled = admitted && projection_valid;
    end
endmodule

module w33_pass3257_authorized_reset (
    input  logic clk,
    input  logic rst_n,
    input  logic authorization_valid,
    input  logic proof_root_match,
    input  logic reset_request,
    input  logic passive_event,
    output logic armed,
    output logic reset_pulse
);
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            armed       <= 1'b0;
            reset_pulse <= 1'b0;
        end else begin
            reset_pulse <= 1'b0;

            // Passive sensing/synchronization never arms or resets the machine.
            if (passive_event) begin
                armed <= armed;
            end

            // Authorization is a distinct token and binds the currently supplied root.
            if (authorization_valid && proof_root_match && !reset_request) begin
                armed <= 1'b1;
            end

            // Reset is fail closed. A mismatched or missing root consumes the arm.
            if (reset_request) begin
                if (armed && proof_root_match) begin
                    reset_pulse <= 1'b1;
                end
                armed <= 1'b0;
            end
        end
    end
endmodule

module w33_pass3258_passive_terminal_guard (
    input  logic       terminal_valid,
    input  logic [1:0] terminal_class,
    input  logic       passive_event,
    input  logic [1:0] proposed_terminal_class,
    output logic [1:0] next_terminal_class,
    output logic       violation
);
    always_comb begin
        next_terminal_class = proposed_terminal_class;
        violation = 1'b0;
        if (terminal_valid && passive_event) begin
            next_terminal_class = terminal_class;
            violation = (proposed_terminal_class != terminal_class);
        end
    end
endmodule

module w33_pass3258_universe_hx8k_top (
    input  logic [7:0] pins_in,
    output logic [3:0] pins_out
);
    w33_pass3254_universe_admission u_admission (
        .universe_id(pins_in[1:0]),
        .opcode_count(pins_in[5:2]),
        .group_order_ok(pins_in[6]),
        .manifest_valid(pins_in[7]),
        .projection_valid(pins_in[0]),
        .admitted(pins_out[0]),
        .census_member(pins_out[1]),
        .comparison_only(pins_out[2]),
        .comparison_enabled(pins_out[3])
    );
endmodule

module w33_pass3258_reset_hx8k_top (
    input  logic clk,
    input  logic rst_n,
    input  logic authorization_valid,
    input  logic proof_root_match,
    input  logic reset_request,
    input  logic passive_event,
    output logic armed,
    output logic reset_pulse
);
    w33_pass3257_authorized_reset u_reset (
        .clk(clk),
        .rst_n(rst_n),
        .authorization_valid(authorization_valid),
        .proof_root_match(proof_root_match),
        .reset_request(reset_request),
        .passive_event(passive_event),
        .armed(armed),
        .reset_pulse(reset_pulse)
    );
endmodule

`default_nettype wire
