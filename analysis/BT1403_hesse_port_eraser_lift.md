# BT1403 -- Hesse Port as Quantum-Eraser Lift

BT1403 makes the physical non-Clifford handoff more concrete.

The BT1396 readout has three Bell branches:

```text
Omega, Z Omega, X Omega
```

The BT1385 Hesse-SIC/T port has nine outcomes:

```text
h in {0,...,8}
```

BT1403 records the ABI lift:

```text
9 = 3 route branches * 3 phase labels
h = 3 * route_trit + phase_trit
```

So the Hesse port is not a second computer bolted onto the Clifford runtime. It
is the same Bell-branch measurement boundary used by the quantum eraser, lifted
by one phase trit.  The result feeds a Clifford correction plus one T-frame
parity bit into the next 8-tick packet word.

This is still an ABI/alphabet theorem. It does not certify physical Hesse-SIC
optics, magic-state yield, detector dark-count budgets, or a full threshold.

BT1403 also builds a separate preview PDF:

```text
photonic_holonet_BT1403_preview.pdf
```

The existing `photonic_holonet.pdf` is not overwritten.

## Verification

```bash
python tools/bt1403_hesse_port_eraser_lift.py
python tests/test_bt1403_hesse_port_eraser_lift.py
python -m py_compile tools/bt1403_hesse_port_eraser_lift.py tests/test_bt1403_hesse_port_eraser_lift.py
python -m json.tool data/bt1403_hesse_port_eraser_lift.json
```
