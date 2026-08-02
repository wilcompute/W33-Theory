# W33 spread/chirality arc — consolidated claim-status ledger

This ledger is the current source of truth for the Passes-1612--1975 spread,
frame-colouring, and signed-edge-module arc. “Retracted” means the claim should
not be repeated. “Narrowed” preserves only the stated scope.

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
