# Passes 2300–2305 — Five Frontiers Release

## Status

`PASS_FOUR_EXACT_MATHEMATICAL_FRONTS_AND_REVIEWED_HARDWARE_HARNESS_WITH_EXTERNAL_RUNNER_PENDING`

The complete code, certificates, tests, formal properties, synthesis scripts and manuscript inserts are on `master`. The Pass-2303 Icarus/Yosys execution remains fail-closed until the isolated GitHub-hosted job posts its run ID and result to issue 194. No tool version, SAT result or FPGA cell count is claimed before that record exists.

## 2300 — complete Ree–Tits divisible-code theorem

Every one of the 551,881 projective hyperplanes of `PG(4,27)` was evaluated against the specified 730-point Ree–Tits ovoid. The complete section spectrum is

`1^730, 10^4563, 19^96174, 28^408294, 37^36504, 46^4914, 55^702`.

All section sizes are `1 mod 9`. The associated projective `[730,5]_27` code is exactly 9-divisible, with seven nonzero weights. Its codeword count and first three Pless factorial moments are exact.

Certificate SHA-256:

`dc6a1b4262e96210af832d098a4140f58e022bea979b7cdf3c030246dbf956e9`

## 2301 — complete quadratic Hom bases

The full `PSp(4,3)`-equivariant quadratic map dimensions from the canonical 90 are

| target | `Sym^2(90)` | `Lambda^2(90)` |
|---:|---:|---:|
| 15 | 3 | 3 |
| 24 | 6 | 4 |
| 30 | 5 | 5 |
| 81 | 12 | 12 |

The complete quadratic space has dimension 50: 26 symmetric and 24 alternating. The outer involution splits it into two equal 25-dimensional sectors. The previously frozen target-identified PGSp table is exactly the outer-even half; the new outer-odd half supplies the remaining PSp maps.

All fifty compressed signed-orbit representatives are frozen. Exact modular full-rank tests certify independence and surjectivity of the integral tensors; the dimensions are independently fixed by character multiplicities.

Certificate SHA-256:

`26eab93605eeb603e3a899c2ecda2a39e268c65e3286b86dce9449f0540b8c43`

## 2302 — q=7 and q=11 Weil inversion

The canonical Schrödinger Weil representations split by parity into complex dimensions

- q=7: `25+24`;
- q=11: `61+60`.

For the nonsquare similitude `h=diag(I_2,-I_2)`, entrywise complex conjugation sends the chirp parameter to its negative, fixes the real Levi permutation and sends the normalized Fourier operator to its inverse. On realification,

`J^2=-I, K^2=I, KJK=-J`,

so the two structures generate `D4` on every parity constituent. This closes the two-i theorem for the canonical Weil family without identifying these constituents with the q=3 signed-edge 90.

Certificate SHA-256:

`d850de3ddaad56765d692fcdba838e2e05bd13340da0194f56c7996807b651a7`

## 2303 — reviewed hardware harness and external-runtime boundary

Merged RTL and verification assets include

- the packed 36-lane exact spread mixer;
- the faithful `D24=C12:C2` phase action;
- deterministic Icarus mixer simulation and exhaustive phase-command simulation;
- Yosys SAT assertions for `A^2=9I+6J`, D24 associativity and the shared-clock kernel;
- explicit `W=4, OW=8` generic, iCE40 and ECP5 synthesis flows;
- the official `YosysHQ/setup-oss-cad-suite@v4` action pinned to the 2026-07-06 suite.

Review found and fixed three concrete HDL defects before runtime certification:

1. `expect` was a reserved SystemVerilog keyword;
2. phase addition truncated the carry before assignment to the five-bit temporary;
3. the formal composition law had the same carry-width defect.

The isolated toolchain trigger is issue 194. GitHub had not allocated a runner before this release was frozen. A local fallback was attempted, but the isolated container could not resolve Debian, GitHub or PyPI package hosts; therefore no local tool output is substituted for the missing hosted run.

## 2304 — complete four-family q=27 taxonomy

Complete hyperplane and regular-section spectra were computed for the regular, Kantor, Thas–Payne and Ree–Tits coordinate families.

All four have section sizes `1 mod 9`, but their spectra and weight enumerators are pairwise distinct:

- regular: a 27-divisible `[730,4]_27` code;
- Kantor: an exactly 9-divisible `[730,5]_27` code;
- Thas–Payne: an exactly 9-divisible `[730,5]_27` code;
- Ree–Tits: an exactly 9-divisible `[730,5]_27` code.

The numbers of regular-spread intersection values are 3, 5, 7 and 6 respectively. This is an exact classification inside four named q=27 coordinate families, not a classification of all symplectic spreads.

Certificate SHA-256:

`559653e8cd1b32f70596a0b334cae02abc4426c694146beaac4ca96970239b72`

## 2305 — integration and reproduction

Both `w33_paper.tex` and `photonic_holonet.tex` include

`analysis/BT2305_five_frontiers_insert.tex`.

`analysis/w33_pass2300_2305_verify_frozen.py` checks every semantic hash, namespace owner, manuscript hook, reviewed RTL repair and formal assertion. The packet-level workflow separately runs all frozen certificate checks and focused regression tests.

## Boundaries

The coordinate spread families, ovoid/spread correspondence, projective-code correspondence, Weil representations and extended similitude action retain literature ownership. Hom-space dimensions and code divisibility do not define physical coupling constants. FPGA synthesis reports implementation properties for a chosen RTL and target family; they do not establish fabricated-device timing, power or physical interpretation.
