// Proof-carrying packet admission gate.
//
// A packet may start the downstream W33 microsequencer only when:
//   * the software/profile admission bit is valid,
//   * its full 256-bit execution-passport digest equals the admitted digest,
//   * requested and host construction-time carrier bits match,
//   * Clifford-lift and projective/Weyl namespace IDs remain distinct,
//   * the requested non-Clifford token count does not exceed the admitted budget,
//   * the packet capability epoch equals the current authority epoch, and
//   * the externally verified revocation-root predicate is true.
//
// This is a finite RTL integrity gate. It does not compute SHA-256 or the
// revocation root internally, authenticate who admitted them, or prove physical
// non-Clifford fidelity.

module w33_passport_packet_gate(
    input  wire         start_in,
    input  wire         profile_valid,
    input  wire [255:0] packet_passport,
    input  wire [255:0] admitted_passport,
    input  wire         requested_carrier,
    input  wire         host_carrier,
    input  wire [7:0]   clifford_ns,
    input  wire [7:0]   projective_weyl_ns,
    input  wire [15:0]  magic_required,
    input  wire [15:0]  magic_budget,
    input  wire [31:0]  packet_capability_epoch,
    input  wire [31:0]  current_capability_epoch,
    input  wire         revocation_root_match,
    output wire         start_out,
    output wire [7:0]   reject_vector
);
    wire passport_match = (packet_passport == admitted_passport);
    wire carrier_match = (requested_carrier == host_carrier);
    wire namespaces_distinct = (clifford_ns != projective_weyl_ns);
    wire magic_ok = (magic_required <= magic_budget);
    wire epoch_match = (packet_capability_epoch == current_capability_epoch);

    assign reject_vector[0] = ~profile_valid;
    assign reject_vector[1] = ~passport_match;
    assign reject_vector[2] = ~carrier_match;
    assign reject_vector[3] = ~namespaces_distinct;
    assign reject_vector[4] = ~magic_ok;
    assign reject_vector[5] = ~epoch_match;
    assign reject_vector[6] = ~revocation_root_match;
    assign reject_vector[7] = 1'b0;

    assign start_out = start_in & profile_valid & passport_match & carrier_match &
                       namespaces_distinct & magic_ok & epoch_match & revocation_root_match;
endmodule

module w33_passport_packet_gate_formal(
    input wire         start_in,
    input wire         profile_valid,
    input wire [255:0] packet_passport,
    input wire [255:0] admitted_passport,
    input wire         requested_carrier,
    input wire         host_carrier,
    input wire [7:0]   clifford_ns,
    input wire [7:0]   projective_weyl_ns,
    input wire [15:0]  magic_required,
    input wire [15:0]  magic_budget,
    input wire [31:0]  packet_capability_epoch,
    input wire [31:0]  current_capability_epoch,
    input wire         revocation_root_match
);
    wire start_out;
    wire [7:0] reject_vector;

    w33_passport_packet_gate dut(
        .start_in(start_in),
        .profile_valid(profile_valid),
        .packet_passport(packet_passport),
        .admitted_passport(admitted_passport),
        .requested_carrier(requested_carrier),
        .host_carrier(host_carrier),
        .clifford_ns(clifford_ns),
        .projective_weyl_ns(projective_weyl_ns),
        .magic_required(magic_required),
        .magic_budget(magic_budget),
        .packet_capability_epoch(packet_capability_epoch),
        .current_capability_epoch(current_capability_epoch),
        .revocation_root_match(revocation_root_match),
        .start_out(start_out),
        .reject_vector(reject_vector)
    );

    always @* begin
        assert(start_out == (start_in && profile_valid &&
                             (packet_passport == admitted_passport) &&
                             (requested_carrier == host_carrier) &&
                             (clifford_ns != projective_weyl_ns) &&
                             (magic_required <= magic_budget) &&
                             (packet_capability_epoch == current_capability_epoch) &&
                             revocation_root_match));

        if (start_out) begin
            assert(profile_valid);
            assert(packet_passport == admitted_passport);
            assert(requested_carrier == host_carrier);
            assert(clifford_ns != projective_weyl_ns);
            assert(magic_required <= magic_budget);
            assert(packet_capability_epoch == current_capability_epoch);
            assert(revocation_root_match);
            assert(reject_vector[6:0] == 7'b0000000);
        end

        if (start_in && packet_passport != admitted_passport)
            assert(!start_out);
        if (start_in && requested_carrier != host_carrier)
            assert(!start_out);
        if (start_in && clifford_ns == projective_weyl_ns)
            assert(!start_out);
        if (start_in && magic_required > magic_budget)
            assert(!start_out);
        if (start_in && packet_capability_epoch != current_capability_epoch)
            assert(!start_out);
        if (start_in && !revocation_root_match)
            assert(!start_out);
    end
endmodule
