# Five TOE followthroughs: representations, Hodge storage, inference, recovery and null tests

September 20, 2026. These are five executed computational investigations. Physical calibration and full CFT amplitudes remain unresolved, rather than silently replaced with simulations or gauge-neutrality tests.

## 1. Actual singlets replace hypothetical inputs

Holotrade's `flagship_singlet_invariant_audit.py` imports the full projected flagship weight dump from the locally installed orbifolder 1.2.1 engine. It verifies 628 weight rows in 274 fields, including 65 singlet fields carrying 132 weights. All singlet weights have zero pairing with all four simple roots of the selected A4. The four co-local fields n_14 through n_17 are exactly the four additional weights of the prior local nine-weight orbit. Thus the branching 9 -> 5 + four singlets is grounded in actual model fields.

Solving the 16 adjacent raising/lowering intertwiner constraints gives a one-dimensional local fundamental bilinear invariant space. All 64 cached mu and 144 triplet coupling rows through total order five have explicit full-16D momentum-neutral weight channels. This closes a necessary gauge-invariance replay, not the nonzero-amplitude problem. Local invariant tensors, projected global amplitudes and Wilson-line-dressed interactions remain distinct. See Holotrade's `FLAGSHIP_SINGLET_INVARIANTS.md` for reproducible engine provenance and limits.

## 2. Harmonic storage has an exact map and an exact limitation

`w33_surface_hodge_transport.py` uses the earlier verified Lutz genus-six surface. For its boundary matrices d1,d2, the declared unit-edge inner product gives L1=d1^T d1+d2 d2^T. If B omits one dependent face-boundary column and C is the previous integral lattice cycle map, then

Q = (I - B(B^T B)^(-1)B^T) C

is the unique minimum-norm cycle representative of every marked lattice class. The certificate stores all 66x12 rational entries and their Gram matrix. It proves d1 Q=0, d2^T Q=0 and preservation of homology coordinates exactly. With a second positive diagonal edge metric, the representatives change but the classes do not. This is a discrete Hodge construction with a chosen metric, not a conformal realization of the earlier hyperelliptic curve.

The orthogonal projector onto Q annihilates both boundary and gradient errors. It **cannot** detect harmonic errors: those are logical changes. This connects the surface to a precisely bounded storage/recovery operation. The method is classical; see prior `BT994_edgewise_hodge_laplacians.md` and [Crane's DEC course](https://www.cs.cmu.edu/~kmcrane/Projects/DGPDEC/).

The exact positive spectral gap is **2-sqrt(2)**. The producer factors the 44x44 face Laplacian polynomial and uses rational isolating intervals to rule out smaller positive roots; the vertex block has only 0 and 12. The appearance of sqrt(2) beside the earlier Heawood response is a spectral connection between specified discrete models, not proof of a common physical generator.

## 3. A calibrated inference process, validated on synthetic data

`w33_oscillator_calibration_test.py` fits mechanical and first-order response models to alternating samples of an 801-point trace, then scores the remaining 400 samples. Units are seconds, normalized return amplitude and radians per second. The trace is explicitly synthetic Gaussian data, seeded before the fit; no laboratory measurement is claimed.

For the illustrative omega0=2pi*30 rad/s and damping 5/s, the mechanical frequencies are 37.7784 and 63.0301 Hz. The fitted omega0 is 188.4973 rad/s and damping 4.9971/s. Held-out chi-square is 432.53 for the mechanical model and 124199.74 for the first-order model. This is strong discrimination within these two specified response families, not against arbitrary drive/readout transfer functions.

To apply the process to hardware, supply the actual time and normalized return arrays to `fit(t,y,mechanical)`, retain independent validation samples, and estimate noise covariance from repeated traces. Independently measure mass or stiffness: the dynamics identifies k/m, and simultaneous rescaling of both leaves it unchanged. The illustrative 1 gram and 35.5306 N/m are simulation parameters. Actual hardware calibration remains open.

## 4. Topology changes transport logical operators and recover state

The generic tree-cotree chain builder now works beyond K12. ALLOCATE includes each old edge cycle in the new surface and constructs a complementary symplectic pair. Exact intersection checks prove preservation of all twelve original logical generators, with two generators added for the new handle. The implementation preserves global orientation rather than silently resetting it after removing a face; this was caught by the first transport regression.

`DurableSurface` retains the cycle map, logical coordinates and surgery receipts. It writes a checksummed temporary snapshot, fsyncs it, atomically replaces the committed snapshot and fsyncs the directory. Recovery verifies the checksum and the exact cycle/intersection constraints. Tests reject corrupt snapshots and live-handle deletion, and show an incomplete next write leaves the committed snapshot recoverable. This is a single-writer classical prototype; the unkeyed checksum is not authentication, and these instructions alone do not establish universal quantum computation.

## 5. Formula tests use the frozen search universe and measurement precision

`w33_frozen_formula_null_audit.py` verifies the frozen universe hash and audits three coarse formulas already present in the corpus: alpha^-1=137, mp/me=1836 and sin²(theta_MSbar(MZ))=3/13. The frozen census contains 51,294 exact families and 49,872 structural families. It includes false positives and is a conservative search-accounting object, not a probability distribution over theories.

Against [CODATA 2022](https://physics.nist.gov/cuu/pdf/wall_2022.pdf), the first two residuals are about 1.71 million and 4.77 million quoted measurement standard uncertainties if the integer predictions are treated as exact. Against [PDG 2025's MSbar-at-MZ value](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-standard-model.pdf), 3/13 differs by about 7.51 quoted uncertainties. Coarse percentage agreement therefore does not establish exact agreement; any correction needs a specified calculation, scale and uncertainty.

For explicitly illustrative uniform-observable null intervals, all three Bonferroni sensitivity bounds saturate at one after multiplying by the full frozen family count. These are conditional bounds, not posterior odds or a calibrated theory-selection p-value. The test does not validate the historical unpriced template/observable choices in `w33_look_elsewhere.py`, and does not reinterpret its heuristic bit count as frequentist evidence. All three tests are retrospective and receive no prospective credit.

## Reproduce

Run the three W33 producers with `--write` to refresh their adjacent JSON certificates. Run Holotrade's singlet producer similarly. The earlier `w33_genus_six_execution.json` is an explicit dependency. Exact symbolic tests are separated from numerical inference, and all physical boundary conditions above remain part of the result.

## Parallel synthesis: the actual extra-U1 charge rank is now closed

The new parallel W33 hypercharge-duad certificate supplies the rank-four Higgs target. Applying its preexisting Holotrade A5 basis to the actual singlet dump gives a 65x4 charge matrix of rank four; n_3,n_6,n_8,n_9 suffice. An exact positive solution of the four projected zero-FI D equations has t_i=1/100 except t_32=19/100,t_42=3/20,t_60=1/25. The mass-Gram determinant is 204557/81000000, with all leading principal minors positive. This closes the charge-rank and projected-D questions, not the remaining D/F/FI vacuum equations. The selected nonabelian A4 and the extra-Abelian organizing A4 are orthogonal spaces; their shared name must not identify them. Full matrix, rational weights and proof are in Holotrade's updated singlet certificate.

Validation: four W33 focused tests passed, including consecutive surgery and recovery with updated original state; two Holotrade focused tests also passed after the added rank certificate (2.82 seconds). Rediscovery warnings for alpha@100 and alpha@200 refer to explicit illustrative null interval endpoints, not new code parameters or alpha formulas. The three coarse formulas are explicitly prior-owned and retrospective.
