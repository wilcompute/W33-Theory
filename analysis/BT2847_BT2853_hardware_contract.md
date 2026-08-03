# Pass 2853 hardware contract

## Encoder

`w33_pass2848_affine_square_feature_encoder`

Inputs are four legal two-bit trits `(x_p,z_p,x_f,z_f)`. The module evaluates twelve exact affine forms over `F3`, converts nonzero values to support bits, and duplicates every support bit to produce the 24-sample distance-four word. Invalid trit encoding `3` deasserts `legal` and forces all support samples low.

## Decoder

`w33_pass2853_affine_square_nn_decoder`

On `start`, the decoder scans all 81 legal frames using a ternary counter, recomputes each 24-bit codeword, and tracks the minimum Hamming distance. `decoded_frame={z_f,x_f,z_p,x_p}`. `corrected_valid` is asserted only when the minimum distance is at most one, the guaranteed unique-correction radius of the code.

Latency is 81 candidate cycles plus launch/completion handshaking. This architecture deliberately trades throughput for a small, auditable state machine. A parallel or tree decoder is a separate optimization target.

## Evidence classes

- Mathematical code distance and feature set: exact and frozen.
- RTL source and directed one-bit testbench: present.
- Icarus behavior, Yosys cell count, nextpnr placement/timing: workflow pending until observed.
- No area or frequency from the 43-LC minimal frame engine is transferred to this decoder.
