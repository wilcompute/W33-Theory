#!/usr/bin/env python3
"""
holonet_cmd -- console-script entry point for the holonet CLI.

After ``pip install -e .`` this shim exposes both the original universal-VM
commands and the typed Levi packet ABI:

    holonet verify
    holonet route 0001 0010
    holonet packet-info
    holonet packet-demo
    holonet packet-fuzz --trials 1000
"""
from __future__ import annotations

import os
import sys


_TYPED_COMMANDS = {"packet-info", "packet-demo", "packet-fuzz"}


def main(argv=None):
    analysis = os.path.join(os.path.dirname(os.path.abspath(__file__)), "analysis")
    sys.path.insert(0, analysis)
    arguments = list(sys.argv[1:] if argv is None else argv)
    if arguments and arguments[0] in _TYPED_COMMANDS:
        import holonet_typed_packet  # noqa: E402

        raise SystemExit(holonet_typed_packet.main(arguments))

    import holonet_cli  # noqa: E402

    holonet_cli.main(arguments)


if __name__ == "__main__":
    main()
