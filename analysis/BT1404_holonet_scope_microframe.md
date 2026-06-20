# BT1404 -- Holonet Scope Microframe

BT1404 turns the BT1403 eraser-lift port into a visible packet machine.

The key identity is:

```text
9 Hesse outcomes * 8 packet ticks = 72 ticks = one microframe
```

So the complete Hesse non-Clifford outcome alphabet fits exactly inside one
BT1385/BT1391 microframe.  Each outcome owns one 8-tick return word:

```text
tick 0: erase the Bell branch
tick 1: record route trit r
tick 2: record phase trit p
tick 3: apply X^r frame correction
tick 4: apply Z^p frame correction
tick 5: store T-frame bit
tick 6: restore Clifford ABI
tick 7: hand off to the next word
```

The parity convention used by the scope is the canonical display projection

```text
t_frame_bit = (route_trit + phase_trit) mod 2 = h mod 2.
```

The page

```text
docs/bt1404_holonet_scope.html
```

is a static holonet oscilloscope for the nine Hesse outcomes.  It is not a
physical SIC-optics implementation.  It is an ABI display: the whole eraser-lift
boundary, one microframe wide.

## Verification

```bash
python tools/bt1404_holonet_scope_microframe.py
python tests/test_bt1404_holonet_scope_microframe.py
python -m py_compile tools/bt1404_holonet_scope_microframe.py tests/test_bt1404_holonet_scope_microframe.py
python -m json.tool data/bt1404_holonet_scope_microframe.json
```
