# Graph-to-asymmetric-qutrit CSS codes: generalization beyond W33

**2026-11-20.** A verified standard hypergraph-product specialization, not a new coding-theory invention or a Theory of Everything.

The first mixed Levi/repetition experiment gave `[[638,81,dX=3,dZ=8]]_3`. Its underlying mechanism is *not* unique to the W33 incidence graph.

## Finite graph theorem

Let `G` be a finite, connected, **bridgeless**, simple graph with minimum degree at least 3, `V` vertices, `E` edges, and girth `g`. Delete one row from its oriented vertex-edge incidence matrix over `F3`, obtaining `A` of size `(V-1) x E` and rank `V-1`. Take the ternary three-site repetition parity check

```text
B = [[1,-1,0],[0,1,-1]]
```

and the CSS check matrices

```text
HX = [A (x) I3       | I_(V-1) (x) B^T]
HZ = [I_E (x) B      | -A^T (x) I2]
```

Then `HX HZ^T=0` over `F3`; the independent ranks are `3(V-1)` and `2E`. There are `N=3E+2(V-1)` physical qutrits and `K=E-V+1` logical qutrits. The logical distances are exactly

```text
dX = 3,  dZ = g.
```

The `dZ=g` argument projects `ker HX` onto graph cycles by summing the three repetition coordinates. Every vector of zero projected cycle is an `HZ` stabilizer. Girth gives the lower bound, and a directed girth cycle gives the witness. The `dX=3` lower bound follows by checking the `HZ` column supports: for a simple graph with minimum degree >=3, they have neither zero columns nor projectively equal pairs. A cycle edge times the triple `(1,1,1)` is an X logical of weight three with nonzero symplectic pairing with the cycle Z logical.

This is a rigorous finite-code construction; it does not claim a new general HGP framework. The **Z** distance grows with graph girth; the **X** distance remains 3.

## Independently reconstructed graph examples

| Base graph | V | E | Girth | Exact ternary CSS parameters |
|---|---:|---:|---:|---|
| 3-cube Q3 | 8 | 12 | 4 | `[[50,5,dX=3,dZ=4]]_3` |
| Petersen | 10 | 15 | 5 | `[[63,6,dX=3,dZ=5]]_3` |
| Heawood | 14 | 21 | 6 | `[[89,8,dX=3,dZ=6]]_3` |
| W33 Levi | 80 | 160 | 8 | `[[638,81,dX=3,dZ=8]]_3` |

The code tests all four constructions, including exact mod-3 check commutation, full stabilizer-rank formulas, nonzero logical pairings, and absence of weight-one/two X operators. Known graph girths yield exact Z-distance by the projection argument.

## Infinite cubic-graph family

For connected bridgeless cubic graphs, `E=3V/2` and hence

```text
N = 13V/2 - 2,  K = V/2 + 1,  dX = 3,  dZ = girth(G).
```

Since large-girth cubic graph families exist, this standard HGP specialization yields an **asymmetric, constant-rate** ternary quantum LDPC family: asymptotic rate `1/13`; bounded X-check weight 5, Z-check weight 4; growing `dZ` but *constant full code distance 3*. No growing-distance symmetric fault tolerance follows.

## Experimental relevance and boundary

This family is potentially relevant to strongly **Z-biased** errors: its phase-error distance can grow without sacrificing asymptotic rate. This is a structural possibility, not a numerical noise-threshold benchmark, decoder guarantee, circuit fault-tolerance claim, or demonstration of a single-photon Holonet.

**External foundations:** Tillich and Zemor, https://arxiv.org/abs/0903.0566 ; constructive cubic high-girth graphs, https://www.combinatorics.org/ojs/index.php/eljc/article/view/v5i1a1 ; biased-noise code evaluation, https://arxiv.org/abs/2202.01702 . **Repo prior art:** `analysis/w33_20261009_toe28_hypergraph_product_rate_distance.py`.

**Reproduce:** `python analysis/toe_20261120_graph_repetition_asymmetric_family.py`; `python -m unittest discover -s tests -p 'test_toe_20261120_graph_repetition_asymmetric_family.py' -v`.
