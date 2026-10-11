# Pass 11903: local grand unification of the 10 locks m_c = m_u (491-model census)

Producer: `analysis/w33_pass11903_local_ten_locks_charm_up.py`
Frozen census: `data/w33_pass11903_census491_frozen.json`
Certificate: `data/w33_pass11903_local_ten_locks_charm_up.json`
Regression: `tests/test_w33_pass11903.py`
Track: Claude.

## The census

**The models.** 491 distinct models:
* the 104 A8 SO(16)×SO(16) Standard Models of Pass 11095;
* the 387 inequivalent models of the Pass 11108 rescan (400,000 Wilson-line draws, WSL `~/orb/p1109x/a8/rescan`).

**The dumps.** The dumps of the 387 had been lost with an old Temp folder, so they were regenerated:
* `~/orb/build7/levdump2` with `ORB_MASS_LEVEL=0` and the sysroot GSL;
* `~/orb/nsobuild/nsosm`.

Both reproduce the archived Pass 11095 dumps **byte for byte** on a test model.

| | models |
|---|---|
| untwisted quark doublets: the up Yukawa is the antisymmetric E₈ cubic in all 1017 Higgs rows (top = charm, m_u = 0) | **339** |
| twisted families on one Wilson-line-free torus | **152** |
| — of which u^c and e^c sit at Q's point of both Wilson-line tori, in the same twisted sector (a complete local **10**) | **152** |
| — of which d^c and L (the **5̄**) are split across points or untwisted | 152 |
| up sector able to span a Wilson-line torus (escape) | **0** |
| down sector able to span a Wilson-line torus | 5 |

## Theorem

The setting is a prime ℤ₃ orbifold with the diagonal selection rule. Suppose Q and u^c of a family share a point g of
a Wilson-line torus.

1. The space-group rule g_Q + g_u + g_H ≡ 0 (mod 3) forces **g_H ≡ −2g ≡ g**. The up triangle is therefore
   single-pointed on that torus.
2. If this holds on every Wilson-line torus, then a = 0. The light couplings are θ₍±1,0,0₎ of the full Hermitian Kähler
   matrix, which are equal by evenness (Passes 11900–11901).
3. Hence **m_c = m_u at tree level for every Kähler modulus**.

**A localised 10 implies a locked charm–up pair.** In this class, local grand unification of the 10 and the charm–up
hierarchy are incompatible at tree level.

**Why the down sector can escape.** d^c lives in the 5̄, which these models split across points. The down triangle can
then span a Wilson-line torus. Through the W(3,3) (off-diagonal Kähler) modulus this gives an O(Z³) split, paid for by
the bottom's instanton factor on that torus.

## Reading

To split charm from up through the W(3,3) modulus, a model must **split the 10 across Wilson-line classes**: Q at one
point and u^c at another, with the Higgs at the third. That is the opposite of the local-GUT pattern every model in this
scan shows. It is a sharp requirement for any future scan, and it marks local GUTs as the structural cause of the
heterotic charm–up problem in prime orbifolds.

## Not established

* **Coverage.** Only this scan: the A8 SO(16)² Z₂W×Z₃ class, with V₀ and V₁ fixed. Whether split-10 three-generation
  models exist in other Z₃ classes, or with other V₀, is open.
* **Coupling order.** Renormalisable couplings only.

## Prior art

* **Local grand unification in heterotic orbifolds:** Buchmüller–Hamaguchi–Lebedev–Ratz (2005–06); Förste–Nilles–
  Vaudrevange–Wingerter, "Heterotic brane world" (2004).
* **Z_N Yukawa structure:** Casas–Gómez–Muñoz.
* **Corpus:** 11095, 11103, 11105, 11108, 11109, 11114, 11900–11902.
