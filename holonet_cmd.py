#!/usr/bin/env python3
"""Installed entry point for the Holonet VM and Levi packet/runtime tools."""
from __future__ import annotations
import importlib
import os
import sys

_TYPED_COMMANDS = {"packet-info", "packet-demo", "packet-fuzz"}
_FAULT_COMMANDS = {"packet-fault-stack"}
_CLOSURE_COMMANDS = {"packet-sentinel-stack", "photonic-e8-compile", "levi-next5-v2"}
_V3_COMMANDS = {
    "formal-rank-v3": "w33_levi_next5_v3_formal",
    "discriminant-action-v3": "w33_levi_next5_v3_discriminant",
    "e6-runtime-map-v3": "w33_levi_next5_v3_e6",
    "photonic-tolerance-v3": "w33_levi_next5_v3_tolerance",
    "optical-packet-emulator-v3": "w33_levi_next5_v3_emulator",
    "levi-next5-v3": "w33_levi_next5_v3",
}
_V4_COMMANDS = {
    "formal-rank-v4": "w33_levi_next5_v4_formal",
    "discriminant-cohomology-v4": "w33_levi_next5_v4_cohomology",
    "e8-incidence-functor-v4": "w33_levi_next5_v4_functor",
    "foundry-calibrate-v4": "w33_levi_next5_v4_foundry",
    "hil-runtime-v4": "w33_levi_next5_v4_hil",
    "levi-next5-v4": "w33_levi_next5_v4",
}
_V5_COMMANDS = {
    "fourier-geometry-v5": "w33_levi_next5_v5_fourier",
    "extension-cohomology-v5": "w33_levi_next5_v5_extension",
    "e8-lanes-v5": "w33_levi_next5_v5_lanes",
    "hybrid-compiler-v5": "w33_levi_next5_v5_hybrid",
    "hardware-runtime-v5": "w33_levi_next5_v5_hardware",
    "levi-next5-v5": "w33_levi_next5_v5",
}

def main(argv=None):
    analysis = os.path.join(os.path.dirname(os.path.abspath(__file__)), "analysis")
    sys.path.insert(0, analysis)
    arguments = list(sys.argv[1:] if argv is None else argv)
    if arguments and arguments[0] in _TYPED_COMMANDS:
        import holonet_typed_packet
        raise SystemExit(holonet_typed_packet.main(arguments))
    if arguments and arguments[0] in _FAULT_COMMANDS:
        if len(arguments) != 1:
            raise SystemExit("packet-fault-stack takes no arguments")
        import holonet_typed_fault_stack
        raise SystemExit(holonet_typed_fault_stack.main())
    if arguments and arguments[0] in _CLOSURE_COMMANDS:
        import w33_levi_next5_v2
        command = "all" if arguments[0] == "levi-next5-v2" else arguments[0]
        raise SystemExit(w33_levi_next5_v2.main([command]))
    for commands in (_V3_COMMANDS, _V4_COMMANDS, _V5_COMMANDS):
        if arguments and arguments[0] in commands:
            if len(arguments) != 1:
                raise SystemExit(f"{arguments[0]} takes no arguments")
            module = importlib.import_module(commands[arguments[0]])
            if arguments[0] == "levi-next5-v4":
                # The aggregate has its own argparse parser.  Do not leak the
                # outer Holonet command name through sys.argv as an invalid
                # inner choice; explicitly select its aggregate route.
                raise SystemExit(module.main(["all"]))
            raise SystemExit(module.main())
    import holonet_cli
    holonet_cli.main(arguments)

if __name__ == "__main__":
    main()
