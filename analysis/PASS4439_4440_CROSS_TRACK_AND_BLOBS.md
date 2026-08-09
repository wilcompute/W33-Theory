# Passes 4439–4440 — a note to the other track, and where the corrupt blobs came from

## Pass 4439 — the seven `semantic_sha256` failures are not mine to fix

Pass 4428 found that seven of the thirteen broken passes fail on the same line:

```python
assert semantic_hash(CERT) == CERT["semantic_sha256"]
```

A certificate that recomputes its own digest and disagrees with itself did not *drift* — it
was **never verifiable**. This is exactly the trap `CLAUDE.md` records at Pass 2482: hash the
round-tripped object, never the live dict, because a nested dict with integer keys sorts
numerically before a JSON round-trip and lexicographically after.

The affected passes are:

| pass | assertion |
|---|---|
| `w33_pass3989_3996_physical_w33_coupler` | `assert set(np.unique(np.round(target,12))) == {-0.2, 2/15}` |
| `w33_pass4049_4056_five_front_outside_box` | `saved = data.pop('semantic_sha256')` |
| `w33_pass4065_4072_explicit_qsp_dirac_magic_gauge` | `saved = x.pop('semantic_sha256')` |
| `w33_pass4081_4088_deep_physics` | `assert semantic_sha(c) == c["semantic_sha256"]` |
| `w33_pass4105_4112_carrier_reference_netlist_decoder_turing` | `assert canonical_hash(cert) == cert["semantic_sha256"]` |
| `w33_pass4113_4120_gauge_horizon_dimension_scar_curvature` | `assert frozen["semantic_sha256"] == x["semantic_sha256"]` |
| `w33_pass4169_4176_discrete_c2_hawking_...` | `assert semantic_hash(CERT) == CERT["semantic_sha256"]` |
| `w33_pass4185_4192_adaptive_c2_hawking_...` | `assert semantic_hash(CERT) == CERT['semantic_sha256']` |

**These are all in the 3989–4192 physics arc and belong to the other track.** The fix is
mechanical — route the serialisation through `scripts/cert_util.dumps`, which bakes the
round-trip in and is self-tested — but applying it means regenerating someone else's
certificate digests. Rewriting a digest without reading the pass is how a stale number
becomes a wrong one, and Pass 4392's taxonomy exists precisely because the two are
different failures.

**Offer, not an edit:** `scripts/cert_util.py` is in place and its selftest passes. If the
other track wants these repaired here, say so and it is a one-line change per file plus a
regeneration. Otherwise the diagnosis is recorded and the list is above.

## Pass 4440 — the corrupt blobs were committed that way

Three further failures are data-integrity rather than logic:

```
w33_pass3973_3980_check.py           binascii.Error: Excess padding not allowed
w33_pass3981_3988_schema_probe.py    zlib.error: Error -5 while decompressing data
w33_pass3983_orbital_central_fourier zlib.error: Error -5 while decompressing data
```

The obvious hypothesis was working-tree corruption — a line-ending rewrite, an editor pass,
something local. **It is not.** Each file is byte-identical to the commit that introduced
it:

| pass | introduced in | committed | working | identical |
|---|---|---:|---:|---|
| `w33_pass3973_3980_check` | `cce2d21bd` | 2048 B | 2048 B | yes |
| `w33_pass3981_3988_schema_probe` | `971a49369` | 1743 B | 1743 B | yes |
| `w33_pass3983_orbital_central_fourier` | `432db419d` | 5016 B | 5016 B | yes |

So there is nothing to recover: the embedded base64/zlib payloads were **truncated or
mis-encoded before the first commit**, and these passes have never run in this repository.
Git history is exhausted as an avenue, which is the useful half of a negative result — it
says stop looking there.

Note the sizes: 2048 and 1743 bytes are small for a pass carrying a compressed payload, and
2048 is suspiciously round. A payload cut at a power-of-two boundary is consistent with a
write that was truncated at source rather than damaged in transit.

## Evidence boundary

Pass 4439 diagnoses and repairs nothing; the root cause is inferred from the assertion sites
and the CLAUDE.md rule they violate, not from reading each pass's logic. Pass 4440 checks
the three files against the commit that *introduced* them, so it rules out post-commit
corruption and nothing else — it does not establish what the payloads were meant to contain.
