# Remote evidence plan

The pull-request workflow executes the following fail-closed sequence:

1. Install NumPy, SciPy, SymPy, and pytest.
2. Recompute all eight exact/modelled release checks and semantically verify the frozen certificate.
3. Run six focused regressions.
4. Install Icarus, Yosys, nextpnr-ice40, and icestorm.
5. Simulate directed one-bit correction.
6. Synthesize the encoder and decoder for iCE40.
7. Place both designs on HX8K/CT256 and retain utilization/timing logs.
8. Integrate the W33 paper, Photonic Holonet, machine blueprint, site index, and pass registry.
9. Compile all three canonical manuscripts with Tectonic and reject overfull or undefined-control-sequence logs.
10. Upload the certificate, FPGA logs, and PDFs as one evidence artifact.
