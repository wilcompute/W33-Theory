# W33 spread/chirality arc — consolidated claim-status ledger

This ledger began as the source of truth for the Passes-1612--1975 spread,
frame-colouring, and signed-edge-module arc. The controlling post-1975
supersessions are recorded first so the historical rows are not mistaken for
the current frontier. “Retracted” means the claim should not be repeated.
“Narrowed” preserves only the stated scope.

## Controlling updates after Pass 1975

| claim | current status | controlling artifact |
|---|---|---|
| regular symplectic spreads form the predicted two-intersection graph | **proved for every odd prime power**; the `q+1` relation is the explicit SRG in Pass 2201 | [Passes 2200–2206](../PASS2200_2206_ALL_Q_SPREADS_NONREGULAR_CONTROLLER_RTL_RELEASE.md) |
| the same two-intersection scheme extends to arbitrary symplectic spreads | **refuted** | the q=27 Ree–Tits control has intersections `19,28,37,46,55`, Pass 2203 |
| the operative phase controller has order 48 | **narrowed** | order 48 is the abstract independent-two-register group; the canonical single-`J` image has order 24, Pass 2204 |
| the finite controller contains or selects the golden ratio | **refuted at that scope** | `R4^2 U6` has spectral radius `phi` only in the overlapping infinite `SL3(Z)` carrier; Passes 2106 and 2306 |
| the order-48, order-24, and rank-three controllers are coordinate versions of one object | **refuted** | minimal faithful rational degree 4 for the order-48 group; the rank-three carrier has common-inverter nullity 0, [Pass 2306](../PASS2306_CONTROLLER_REPRESENTATION_TRICHOTOMY.md) |
| historical quadratic target multiplicities on the signed-edge 90 | **Pass-2200 table stands only as the outer-even half** | full `PSp` dimensions are `Sym^2: 3,6,5,12`; `Lambda^2: 3,4,5,12`, with all 50 bases explicit, Pass 2301 |
| every q=27 symplectic spread has all hyperplane sections `1 mod 9` | **open in that universal scope** | exact for the regular, Kantor, Thas–Payne, and Ree–Tits coordinate families only; Passes 2300/2304 |
| the 50 quadratic maps have an unexplained `25+25` outer split | **closed structurally** | combined phase/outer module is `16*1 + 16*sgn + 9*std`, which forces `25+25` and `32+18`, [Pass 2307](../PASS2307_QUADRATIC_HOM_S3_DECOMPOSITION.md) |

| claim | originating pass/file | current status | reason / controlling artifact |
|---|---|---|---|
| `H` is the union of 240 edge-indexed `K9`s | 1887 | **stands, exact q=3** | literal 540-frame/240-edge census |
| `chi(H)=9` | many | **open** | every exact solver run remains `UNKNOWN` |
| spread pairs give 45 independent frames | 1828/1865 | **stands, uniform incidence proof** | Pass 1974 Proposition 1 |
| the spread 45-set is maximal independent | 1828, note, Pass-1970 draft | **retracted: false** | 15 residual candidate frames are nonadjacent to the seed; Pass 1971 |
| the spread seed cannot complete to a 60-frame exact cover | 1865 | **stands, exact q=3** | candidates touch only 20 of 60 residual edges |
| completion failure is caused by maximality | 1828/1861 wording | **retracted** | correct mechanism is residual support deficiency |
| candidate count is `q(q^2+1)/2` and support fraction is `1/q` | 1865/1877 | **exact under candidate-orbit property; q=3,5,7 verified** | a linewise involution proves the orbit-generated subfamily, not exhaustiveness; Pass 1974 v2 |
| every arbitrary symplectic spread carries `sigma_S` | 1882 wording | **not established** | existence proved for associated Desarguesian spread; exhaustive q=3 only |
| `sigma_S` is fixed-point-free and linewise on its spread | 1882/1899 | **stands** | nonsquare similitude construction; q=3 uniqueness exact |
| exact q=3 `36/270` multiplier split | 1899 | **stands as finite computation; novelty open** | no located literature reference |
| a third disjoint cover does not exist | 1873 | **retracted** | Pass 1878 exhibits two extending pairs |
| phase on the 81 costs more than maximal subgroup reduction | 1876 | **retracted** | odd-dimensional parity forbids any `J^2=-1` |
| gauge bit equals point/line duality | 1874 | **refuted** | Pass 1879 character comparison |
| `k>=3` ladder rows diagnose infeasibility | 1883/1886 | **invalid evidence** | symmetry break was not WLOG below `k=9` |
| each class meets each spread `K10` in at most 5 | 1887 | **retracted: false** | exact cover attains 13; 5 was only the average |
| `max |class ∩ K10|=13` | 1898 | **open** | 13 attained; 14 not excluded |
| free cuts improve the solver | 1887 | **refuted operationally** | zero branching value; few conflicts; false cap also contaminated model |
| spread-variable branching is the best tested single encoding | 1892 | **stands for frozen benchmark** | 60,909 branches |
| one/few geometric lex generators cut a witness orbit | 1956/1957 | **stands only as witness/orbit statement** | audited feasible witnesses |
| more generators improve full solver search | 1957 inference | **refuted** | 40-generator combined run worse than 8-generator run |
| orbit-volume reduction predicts search-tree reduction | 1966 inference risk | **refuted as a general inference** | `25,920->807` exact, yet combined search is 7--8x worse than spread alone |
| combined spread+lex encoding is best | proposed before 1961 | **refuted** | 451,460/512,714 branches vs 60,909 |
| `assert_cuts` can audit the full 540-variable model by enumeration | 1958--1964 | **retracted** | cap, sampling, and time-truncation failures; v5 scope limit |
| class/octet/point percentage-cut figures from v3 | 1964 pre-correction | **provisional, not established** | enumeration truncated |
| named-witness/orbit audit proves global solution-count reduction | none | **not claimed** | v5 certifies only supplied witnesses/orbits |
| outer involution as complex conjugation is novel here | 1900/1907/1914 | **retracted as novelty** | Gow/Vinroot and in-repo Pass 355 priority |
| the signed 240-edge module contains one non-rational block | 1885 onward | **stands, exact** | `15+24+81+30+90`, only 90 Eisenstein |
| the 90 carries internal `C6` units | 1933 onward | **stands, exact representation theory** | character field/integral-unit certificate |
| internal `C6` is electric charge in thirds | 1933/1934 reading | **retracted** | phase is coexact, not Gauss/source block |
| internal `C6` is a Dirac/homological flux quantum | 1934 reading | **retracted** | integral boundary complex is torsion-free at tested primes |
| internal `C6` is QCD colour, generation, or neutrino label | exploratory wording | **not derived; withdrawn from promotion** | no supporting intertwiner or physical map |
| internal `C6` is linearly confined to the coexact 90 | 1954/1963/1968 | **stands, exact** | multiplicity-free `Hom_PSp(90,X)=0` for other blocks |
| internal `C6` equals the `E8` Coxeter six-cycle action | 1948 question | **refuted** | incompatible full-carrier character multiplicities |
| `C6` plus chirality gives `D12` on the phase label | 1968 | **stands, exact algebraically** | outer involution acts by inversion |
| the Pass-1970 manuscript is peer reviewed/published | none | **not claimed** | computational referee-shaped draft only |

## Rules for future claims

1. Solver `UNKNOWN` is not evidence for either satisfiability or infeasibility.
2. A finite witness-orbit reduction is not a runtime prediction.
3. Any new constraint must carry both a named rejected feasible witness and a
   surviving feasible representative, or an exact small-model proof.
4. Physics labels require a literal map into the relevant source, gauge,
   topological, or observable structure; numerical resemblance is insufficient.
5. Standard finite-geometry and representation-theory frameworks retain their
   literature ownership even when independently reconstructed here.
