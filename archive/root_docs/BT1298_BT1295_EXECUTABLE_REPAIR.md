# BT1298 — BT1295 Executable Witness Repair

## Result

After absorbing the BT1194-BT1297 remote batch, the BT1295 report stated that
the q=3 master identity had 13/13 verified faces, but the executable witness
still returned `PARTIAL` with 11/13 faces.

The failure was not conceptual. It came from two stale formulas inside
`BT1295_q3_master_identity.py`:

- the W(3,3) point count used `q*(q^3+1)/2`, which gives 42 at q=3;
- the Cayley diameter face used the q=3-only coincidence `q^2+q+2`.

BT1298 repairs the executable witness to match the newer BT1296 structure:

```text
v(GQ(q,q)) = (q+1)(q^2+1), so v(W(3,3)) = 40
diameter(Sp(4,q)) = 4q+2, so diameter(Sp(4,3)) = 14
40 = 20 + 20 = 2*(2*(q^2+1)) at q=3
```

The BT1295 witness now verifies all thirteen faces and regenerates a PASS JSON
artifact.

## Boundary

This repair does not add a new independent proof of the general Cayley diameter
formula. It makes BT1295 explicitly depend on the BT1296 statement
`diameter(Sp(4,q)) = 4q+2`, and removes the older q=3 numerical coincidence
from the master identity witness.

## Verification

```text
python3 BT1295_q3_master_identity.py
python3 tests/test_bt1295_master_identity_repair.py
python3 -m py_compile BT1295_q3_master_identity.py tests/test_bt1295_master_identity_repair.py
python3 -m json.tool BT1295_q3_master_identity_results.json
```

The local environment still has no `pytest` module, so the new regression is
written to run both under pytest and directly with `python3`.
