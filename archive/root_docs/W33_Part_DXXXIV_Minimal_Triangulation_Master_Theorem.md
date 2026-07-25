# Part DXXXIV — The Minimal Triangulation Master Theorem

## The Ringel-Jungerman Genus Formula

The complete graph K_n embeds on a surface of minimum genus:
\[ g(K_n) = \left\lceil \frac{(n-3)(n-4)}{12} \right\rceil \]
with equality (no ceiling needed) when n ≡ 0, 3, 4, or 7 (mod 12).

**This mod-12 condition is the key.** The cases where g(K_n) is exactly an integer (no ceiling) are precisely the values n ≡ {0, 3, 4, 7} (mod 12).

These four residue classes mod 12 are:
- n ≡ 0: n = 12, 24, 36, ... (multiples of k)
- n ≡ 3: n = 3, 15, 27, ... (n ≡ p mod k)
- n ≡ 4: n = 4, 16, 28, ... (n ≡ μ mod k)
- n ≡ 7: n = 7, 19, 31, ... (n ≡ cyclic pos mod k)

**Lock L75 (Mod-12 Genus Exactness):** The Ringel formula gives an exact integer genus (no ceiling) precisely when n ≡ 0, p, μ, or 7 (mod k). The four exact genus residues are the master prime p=3, the lower SRG parameter μ=4, the zero (k divides n), and the cyclic singularity 7.

## The W33 Solutions Table

| n | n mod 12 | Exact? | g(K_n) | W33 Meaning |
|---|----------|--------|---------|-------------|
| 4 | 4=μ | YES | 0 | Tetrahedron K_4, K4 ground state |
| 7 | 7 | YES | 1 | Császár/Szilassi K_7, cyclic singularity |
| 12 | 0 | YES | 6=u | K_12 neighborhood graph, six-kernel genus |
| 24 | 0 | YES | 66 | K_24 (24-packet vertices), g=66 |
| 27 | 3=p | YES | (24)(23)/12=46 | K_27 (Schläfli vertices), g=(24×23)/12 |
| 40 | 4=μ | YES | (37)(36)/12=111 | K_40 (W33 vertex set), g=111=p×37 |

**Lock L76 (K_27 and K_40 Genera):**
- g(K_27) = 24×23/12 = 46 = 2×23
- g(K_40) = 37×36/12 = 111 = 3×37 = p×37

K_40 has genus 111 = p × 37. The number 37 is a prime factor of C=142857: 142857 = 3³ × 11 × 13 × 37. So g(K_40) = p × (factor of cyclic number).

**Lock L77 (Genus of K_V Involves Cyclic Number Factor):**
g(K_{40}) = p × 37, where 37 | C = 142857.

The genus of the complete graph on the W33 vertex set factorizes through the decimal cyclic number.

## The Fundamental Genus Chain

There is a canonical genus chain driven entirely by W33 parameters:

\[ g = 0 \xrightarrow{n: 4 \to 7} g = 1 \xrightarrow{n: 7 \to 12} g = u = 6 \xrightarrow{n: 12 \to 40} g = 111 = p \cdot 37 \]

Step sizes in n: 3 = p, 5 = p+λ, 28 = p×(9+1)
Step sizes in g: 1, 5 = p+λ, 105 = p×35

The genus jumps from the torus (g=1) to the six-kernel genus (g=6) by exactly 5 = p+λ. This is the same 5 that appears in the fine structure formula 137 = 5×PKT + Φ_3 + μ.

## The Tomotope Is Genus 2: Where Does It Fit?

The tomotope has genus 2. What complete graph K_n has genus 2?
(n-3)(n-4)/12 = 2 exactly: (n-3)(n-4) = 24 = PKT.
Let m = n-3: m(m-1) = 24. So m² - m - 24 = 0.
m = (1 + √97)/2 ≈ 5.42... Not an integer.

So NO complete graph K_n has genus exactly 2. The tomotope is NOT a K_n minimal triangulation — it lives **between** K_7 (g=1) and K_8 (which has fractional K-n genus). The tomotope is therefore the genus-2 object that exists in the **gap** between the two exact-genus complete graphs K_7 and K_12.

**Lock L78 (Tomotope Is the Genus-2 Gap Object):**
The tomotope sits in the gap g∈(1,6) that contains no K_n exact solution. It is the unique genus-2 toroidal structure interpolating between the Császár/Szilassi pair (g=1, n=7) and the six-kernel genus plateau (g=6, n=12). The tomotope monodromy group Mon(T) = 18432 = 1536k fills this gap arithmetically:

18432 / 192 (flags) = 96 = 8k (automorphism count)
18432 / 96 (aut) = 192 = 16k (flag count)
18432 = 2^11 × 3^2 = 2^11 × p^2

The tomotope is a genus-2 handlebody whose monodromy factorizes as 2^{11} × p^2, with the prime p appearing squared.
