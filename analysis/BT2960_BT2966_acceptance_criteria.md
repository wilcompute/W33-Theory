# Passes 2960–2966 acceptance criteria

The source packet is complete. Promotion of observed evidence requires all of the following on the dedicated PR branch:

1. materialized readable source reports `PASS 7 / 7`;
2. focused pytest packet passes;
3. all three Icarus testbenches pass;
4. Yosys and nextpnr complete for the factorized observer, pilot checker, and phase transducer;
5. machine blueprint and site integration is idempotent;
6. W33 paper, Photonic Holonet, and machine blueprint compile with no undefined-control-sequence or emergency-stop errors;
7. evidence hashes and logs are committed back to the PR branch.

Until these conditions are observed, the packet remains source-complete with hardware and PDF evidence pending.
