# Pass 383 — the branch/phase control group is \(C_6\) unless an extra mirror lift is supplied

The Heawood calculation provides a two-sector reversible branch selector, and
Pass 380 provides a free scheduler \(C_3\) phase word.  Pass 381 now supplies
the sixteen row identities needed to place both in one **typed control-space**:

\[
  \{0,1\}_{\mathrm{branch}}
  \times\{0,\ldots,15\}_{\mathrm{bound\ row}}
  \times\mathbb Z/3_{\mathrm{phase}},
  \qquad |X|=2\cdot16\cdot3=96.
\]

This is a control interface, not a basis-level coupling of the Heawood
spectral shell to a Q6 edge or header flag.

## Two exact order-six possibilities

Let \(r\) advance scheduler phase:

\[
 r(b,e,p)=(b,e,p+1).
\]

The ordinary logic-switch lift changes only the branch label:

\[
 s(b,e,p)=(b+1,e,p).
\]

GAP checks \(r^3=s^2=1\), \(rs=sr\), and that \(rs\) has order six.  Therefore

\[
  \langle r,s\rangle\cong C_2\times C_3\cong C_6.
\]

There is a different possible involution,

\[
  m(b,e,p)=(b+1,e,-p),
\]

but it is extra structure: it reverses phase orientation.  GAP checks

\[
  m^{-1}rm=r^{-1},
  \qquad
  \langle r,m\rangle\cong S_3.
\]

So the precise answer is not “perhaps \(C_6\) or \(S_3\).” On the supplied
phase-orientation-preserving switch interface it is exactly \(C_6\).  An
\(S_3\) control group would require a separately specified phase-reflecting
\(C_2\) lift.  The sixteen-row binding table relabels row fibres but does not
choose between these two kinds of involution.

This is consistent with the existing outer-polarization \(S_3\) work: that
result uses an explicit reflection that inverts an order-three action.  Pass
383 neither imports that reflection into the scheduler nor identifies it with
the Heawood selector.

The compact search signature is `96/16xC6/C6-vs-S3-control-boundary`.

## Reproduce

```bash
gap -q analysis/w33_pass383_branch_phase_control_group.g
python3 -m pytest tests/test_pass383_gap_branch_phase_control_group.py -q
```

Artifacts:

- GAP witness: `analysis/w33_pass383_branch_phase_control_group.g`
- certificate: `data/w33_pass383_branch_phase_control_group.json`
- regression: `tests/test_pass383_gap_branch_phase_control_group.py`
