# Passes 4878–4882 — corrected historical ledger

**Original date:** 2026-08-11  
**Current status:** correction ledger; not a theorem frontier.

The original packet mixed valid finite observations with four unsupported
inferences and one parameter-only graph identification. Pass 4948 rebuilt the
modular algebra and group arithmetic in native GAP. Passes 4954, 4963, and 4966
then settled the point/line and Witting-phase questions. The legacy producers
now emit fail-closed tombstones instead of regenerating the retired claims.

| Pass | Current status | Exact disposition |
|---|---|---|
| 4878 | **CORRECTED by 4948** | The congruence (2\equiv-4\pmod3) survives. The full modular adjacency algebra has dimension 3, not 2, and the congruence does not cause the unrelated quadratic Hom dimension. |
| 4879 | **CORRECTED by 4948** | The certified dual-code interval is (6\leq\rho(K^\perp)\leq36). The old lower bound 10 used a nonexistent general duality. |
| 4880 | **WITHDRAWN by 4948** | The marked (\mathbf F_2^6) chart remains useful on its binary carrier, but no cross-characteristic map or modular (24+15) splitting was built. |
| 4881 | **WITHDRAWN by 4948** | The exact orders 6,912 and 33,592,320 survive. Pass 4873 compares (S_6\times C_2) with \(\operatorname{Aut}(S_6)\), not (2.S_6), and no compiler quotient was constructed. |
| 4882 | **WITHDRAWN; superseded by 4963/4966** | Steiner fibers carry the (Q(4,3)) line action, while Witting rays carry the nonisomorphic (W(3,3)) point action. Oriented Witting phase realizes the outer sign on the point carrier. |

## Exact modular replacement

For the actual W33 point adjacency matrix over (\mathbf F_3), Pass 4948 proves

\[
\dim\langle I,A,J\rangle=3,
\qquad (A+I)^2=J,
\qquad R=A(A+I),
\qquad R^2=0,
\qquad \operatorname{rank}R=10.
\]

On the 39-dimensional augmentation module the Loewy layers are
(10\mid19\mid10). Exhaustive enumeration of all 27 scheme-algebra elements
finds idempotent ranks only (0,1,39,40); there is no modular rank-24 or
rank-15 scheme idempotent. The radical image is the outer-sign twist of the
ten-dimensional adjoint module.

## Exact dual-radius replacement

The syndrome space has size (2^{36}). The number of errors of weight at most
5 is below (2^{36}), so radius 5 cannot cover every syndrome and
\(\rho(K^\perp)\geq6\). Conversely, 36 independent parity-check columns form
a syndrome basis, giving \(\rho(K^\perp)\leq36\). No exact radius is claimed.
This dual interval is separate from the primal-code covering-radius program.

## Authoritative evidence

- Pass 4948 GAP certificate:
  `data/PART_W33_PASS4948_MODULAR_BOSE_MESNER_CORRECTION.json`
- Pass 4948 owner:
  `analysis/w33_pass4948_modular_bose_mesner_correction.g`
- Pass 4963 Witting re-audit:
  `data/PART_W33_PASS4963_WITTING_PANCHARATNAM_W33_REAUDIT.json`
- Fail-closed legacy regression:
  `tests/test_w33_pass4878_4882_correction_tombstones.py`

## Boundary

The corrected statements are finite algebra, code, group, graph, and phase
results. They do not construct a cross-characteristic splitting, an
order-1440 compiler quotient, a Steiner/Witting identification, a continuum
field, a particle, a coupling, or a hardware security property.
