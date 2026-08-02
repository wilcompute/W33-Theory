# Passes 2482–2487 — the hook found a real bug, it was mine, and it was not a stale digest

---

## Pass 2482 — the root cause: **integer dict keys**

Pass 2478's hook flagged seven certificates, six of them mine. I assumed stale digests.
Wrong on both counts — the hook was also mis-calibrated a third time, and underneath that
there is a genuine defect.

**The third calibration.** The repo uses **two** legitimate serialisations, and I only
tried one:

```text
compact  : json.dumps(x, sort_keys=True, separators=(",", ":"))
indent2  : json.dumps(x, indent=2, sort_keys=True) + "\n"
```

`w33_pass1867_1871` hashes with `indent2` (its line 31). The checker now tries both.

**The real bug, which survives that fix.** Even freshly regenerated, the certificate
still failed under *every* convention. The producer does:

```python
result.pop("sha256_without_hash_field", None)
canonical = json.dumps(result, indent=2, sort_keys=True) + "\n"   # the LIVE dict
result["sha256_without_hash_field"] = hashlib.sha256(canonical.encode()).hexdigest()
output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
```

and `result` contains a nested dict `traces_1_to_16` whose keys are **Python integers**:

```text
nested dict keys that look like integers : 16
  /traces_1_to_16/1 .. /traces_1_to_16/16
```

> **`sort_keys=True` orders integer keys numerically — `1, 2, …, 9, 10, 11` — while the
> same keys after a JSON round-trip are strings ordering lexicographically —
> `1, 10, 11, …, 2`. The two byte streams differ, so the certificate could never
> reproduce its own digest from disk. Not stale: structurally unverifiable.**

**Fix**, applied to `analysis/w33_pass1867_1871_outer_doily_transfer_clock.py`: hash the
round-tripped object.

```python
canonical = json.dumps(json.loads(json.dumps(result)), indent=2, sort_keys=True) + "\n"
```

Regenerated and verified: `48b14b26a76531d2…` now reproduces exactly.

**Status of the rest.** `126/132` verify, up from 125. Five of mine remain flagged
(`1872_1876`, `1887`, `1891`, `2011_2015`, `2012`) plus `holonet_uor_shacl_export`. They
are the same class and have **not** been repaired this pass — each needs its producer
inspected, and a digest must never be patched without re-deriving the object.

**The lesson, fifth occurrence.** *A disagreement with the corpus is a bug in the new
code until proved otherwise.* Here it was true twice over: the checker's convention was
wrong, and beneath that the producer's was too. Neither was "the certificate went stale".

---

## Pass 2483 — what the 4-dimensional irreducible **is**

Pass 2476 showed `144 = 36 ×` the unique faithful 4-dimensional irreducible of
`N = C₅:C₈`. Identifying it:

`C₈` acts on `C₅` through `C₈ ↠ C₄ = Aut(C₅)` with kernel `⟨z⟩`, so `C₄` permutes the
four nontrivial characters of `C₅` in a single free orbit. The stabiliser of one such
character is therefore

```text
Stab = C5 x <z> = C10        index 4 in N
```

and inducing a character of it gives degree 4. The two degree-4 irreducibles are

```text
Ind_{C10}^{N} ( chi (x) psi ),    chi nontrivial on C5,  psi in {triv, sign} on <z>
```

and the one with `z → −I` is `psi = sign`.

> **The 4-dimensional irreducible is induced from a single pentagon's nontrivial
> rotation character, twisted by the antipode.** Its dimension 4 is exactly the number
> of nontrivial characters of `C₅` — the four rotation speeds of one pentagon.

That gives the 144 a geometric name rather than a dimension: it is 36 copies of
*(one pentagon's rotations, antipodally twisted, induced up)*. And it is consistent with
Pass 2466: the `E₈` carrier restricted to `C₅` is `(0, 2, 2, 2, 2)` — two copies of each
nontrivial pentagon rotation, no trivial part.

---

## Pass 2484 — the chiral carrier is a **different kind of object** at `q ≡ 1`

Pass 2477 withdrew the claim that the chiral carrier has no invariant form. The true
structural difference is about *reducibility*:

```text
q = 3 (q = 3 mod 4)   each degree-4 is NOT self-dual; you need 4 + 4bar to get a
                      self-dual carrier, and the carrier is then 8-dimensional with
                      one symmetric and one alternating invariant form

q = 5 (q = 1 mod 4)   each degree-12 IS self-dual, symplectically (FS = -1); a single
                      constituent is already a self-dual carrier
```

> **At `q ≡ 3 (mod 4)` the chiral carrier is reducible and complex — it is a real form
> of a complex space. At `q ≡ 1 (mod 4)` a single constituent is already self-dual and
> quaternionic.**

So the `E₈`-shaped object at `q = 3` exists *because* the two halves are conjugate and
must be glued; at `q = 5` there is nothing to glue. That is a sharper statement than
either Pass 2467 or its withdrawal, and it is the version worth keeping.

---

## Pass 2485 — the Burnside count: builders located, not executed

The frame/cover machinery already exists in the repo — the search in Pass 2479 was
looking in the wrong place:

```text
analysis/w33_pass1505_exact_cover_census_frontier.py
analysis/w33_pass1533_cover_orbit_frontier_audit.py
analysis/w33_pass1821_1825_complete_cover_signature.py
analysis/w33_pass1887_cpsat_the_resolution.py
analysis/w33_pass2412_verify_search.py
```

`w33_pass1533_cover_orbit_frontier_audit.py` is named for exactly the quantity the
Burnside route needs. **Not executed this pass** — reported so the next attempt starts
from these rather than rebuilding `H`.

This also corrects Pass 2479's claim that "the only missing input is the frame graph
`H`". `H` is not missing; I had not searched for it by result, which is the repo's own
first rule and my own memory's first line.

---

## Pass 2486 — the history sweep, superseded

Pass 2481 proposed running the hook over the whole history to see whether stale digests
correlate with renumberings or merges. **That question is now moot**: the flagged
certificates are not stale-from-history, they are structurally unverifiable from birth
because of the integer-key defect. A history sweep would find them broken at every
commit, which tells us nothing we do not already know.

Replaced by a better check: grep every certificate producer for the live-dict hashing
pattern. Not run this pass.

---

## Pass 2487 — ledger

| claim | discharged by | status |
|---|---|---|
| two legitimate digest conventions exist | producer source + verification | proved |
| integer dict keys make a certificate unverifiable | key census + regeneration | proved |
| `1867_1871` repaired | regenerated, digest reproduces | fixed |
| five of my certificates + one other | — | **flagged, NOT repaired** |
| the 4-dim is `Ind_{C₁₀}^{N}(χ ⊗ sign)` | index and stabiliser argument | derived |
| chiral carrier reducible at `q≡3`, irreducible at `q≡1` | FS indicators + degrees | proved |
| Burnside orbit count | — | **not executed; builders located** |
| history sweep | — | **superseded** |

---

## Prior art

- `scripts/check_rediscovery.py` — the calibration policy this hook keeps failing to
  copy correctly, now on the third attempt.
- Passes 1505/1533/1821/1887/2412 — the existing cover machinery.
- Pass 2476 (mine) — the module decomposition this names geometrically.

## Still open

- Five of my certificates and `holonet_uor_shacl_export`.
- The Burnside orbit count, which settles `73`.
- `χ(H) = 9`.
