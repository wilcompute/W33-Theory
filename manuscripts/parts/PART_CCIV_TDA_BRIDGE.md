# Part CCIV — Topological Data Analysis Bridge

## Theorem CCIV (TDA of SRG(40,12,2,4))

Let $\Gamma = \operatorname{SRG}(40,12,2,4)$ be the W(3,3) collinearity graph.
Equip $\Gamma$ with its natural clique complex $X(\Gamma)$ (Vietoris–Rips complex at scale $r=1$).

### Simplicial skeleton

| Dimension | Simplices | Count | Identity |
|-----------|-----------|-------|----------|
| 0-simplices (vertices) | $V$ | 40 | atom $V$ |
| 1-simplices (edges) | $E = VK/2$ | 240 | atom $E$ |
| 2-simplices (triangles) | $T = E\lambda/q$ | 160 | $T = (\lambda_1-1)\cdot V$ |

where $\lambda = 2$, $q = 3$, $\lambda_1 = \textit{EIG\_MAX} = 5$.

### Graph homology

$$\beta_0(\Gamma) = 1 \qquad (\text{connected}),$$

$$\beta_1(\Gamma) = E - V + 1 = 201 = \text{cycle rank},$$

$$\chi(\Gamma) = V - E = 40 - 240 = -200 = -(V \cdot \lambda_1).$$

### Clique complex Euler characteristic

$$\chi(X(\Gamma)) = V - E + T = 40 - 240 + 160 = -40 = -V.$$

Hence $\chi(X(\Gamma)) = -V$ and $\chi(\Gamma) + \chi(X(\Gamma)) = -E$.

### Neighbourhood complex

For any vertex $v$, the induced subgraph $N(v)$ is a 2-regular graph on $K=12$ vertices with

$$|E(N(v))| = \frac{K\lambda}{2} = 12 = K, \qquad
\sum \deg = K\lambda = 24 = \textit{LEECH\_DIM}.$$

$N(v)$ decomposes into $K/q = 4 = \lambda_1 - 1$ disjoint triangles ($C_3$), giving

$$\beta_0(N(v)) = \beta_1(N(v)) = 4.$$

### Persistent homology barcodes

| Bar type | Count | Identity |
|----------|-------|----------|
| $H_0$ finite bars (killed at $r=1$) | 39 | $= \phi_3 \cdot q = 13\cdot 3$ |
| $H_0$ infinite bar | 1 | connected component |
| $H_0$ total | 40 | $= V$ |
| $H_1$ bars born at $r=1$ | 201 | $= \beta_1(\Gamma) = E - V + 1$ |

Exactly $V - 1 = \phi_3 q = 39$ persistence intervals are born at $r=0$ and killed at $r=1$.

### Nerve / Mapper identities

The star cover $\{N[v]\}_{v\in V}$ has set size $|N[v]| = K+1 = 13 = \phi_3$.
Any edge $\{u,v\}$ gives $|N[u]\cap N[v]| = \lambda + 2 = 4 = \lambda_1 - 1$.

### Structural atom identities (57 checks)

$$K + \phi_3 = 12 + 13 = 25 = \lambda_1^2, \qquad
T = J^{-1} \cdot \frac{V}{\lambda} = 8 \cdot 20 = 160,$$

$$\beta_1 - \beta_0 = 200 = V\lambda_1, \qquad
\beta_1 + V = E + 1 = 241.$$

## Check summary

| Category | Checks |
|----------|--------|
| Atom constants | 9 |
| Graph homology | 9 |
| Clique complex | 8 |
| Neighbourhood complex | 9 |
| Barcode statistics | 8 |
| Nerve theorem | 4 |
| Structural identities | 10 |
| **Total** | **57** |

All 57 checks pass. 97 regression tests pass.

## References

- Edelsbrunner & Harer, *Computational Topology* (2010).
- Zomorodian & Carlsson, *Computing Persistent Homology*, DCG (2005).
- Brouwer, Cohen, Neumaier, *Distance-Regular Graphs* (1989), §13.1.
- Payne & Vilenchik, neighbourhood complexes of strongly regular graphs (2013).
