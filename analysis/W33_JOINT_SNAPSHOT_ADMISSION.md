# Joint admission for shared VM snapshots

The counter VM archive now has a bounded exact retention planner. It chooses
which pending snapshot requests fit together, then rechecks and publishes the
chosen batch. On an explicit three-request workload it retains two resumable
guests within a budget where a smallest-current-marginal greedy policy retains
only one. This is a scheduling decision backed by real archived state bytes.

## The experiment that changes the decision

Use the existing addition guest with initial counters (n,0), a common
`set-union-demo` session label, and fibre address (0,0,0). Offer snapshots with
n equal to 128, 254 and 255, each with utility one. Each counter has eight bits.

| Offered subset | Canonical archive payload bytes |
| --- | ---: |
| 128 | 2821 |
| 254 | 2821 |
| 255 | 2821 |
| 128 and 254 | 5350 |
| 128 and 255 | 5350 |
| 254 and 255 | 3850 |
| All three | 6379 |

At budget **3850**, the exact planner selects **254 and 255**. The explicitly
tested greedy comparator repeatedly chooses the smallest currently feasible
marginal cost, breaking ties by request id. It starts with 128 and cannot add
either remaining request. This refutes optimality of that policy on this
workload; it does not say that every greedy tie rule fails.

The reason is visible in the virtual hardware: 254 and 255 differ at the first
binary node but share the tail for 127. The 128 branch shares much less.
Individual lengths do not encode this relationship. Metadata and both fibre
tags remain part of every snapshot root; sharing data never licenses dropping
execution state. Both selected guests are resumed and run to halt through the
existing arithmetic receipt verifier.

## Prior ownership and the optimization object

`analysis/w33_shared_counter_archive.py` already owns collector-visible tails,
full recovery, and exact union-priced single publication (commit `8ecc185ef`).
`analysis/w33_adaptive_reversible_scheduler.py` already selects among modeled
reversible checkpoint strategies using an estimated deduplication ratio.
`analysis/w33_ladder_checkpoint_placement.py` owns the ladder placement adapter.
The present module schedules pending retention requests. It does not turn a
snapshot quote into a measured peak for an entire reversible execution, and it
does not replace the existing pebble or ladder strategy selectors.

This optimization object is established prior art, the **set-union knapsack
problem**: items have utility, each item requires a set of weighted elements,
and a shared element is charged once. See Goldschmidt, Nehme and Yu,
[Note: On the set-union knapsack problem, Naval Research Logistics 41 (1994),
833–842](https://doi.org/10.1002/1520-6750%28199410%2941%3A6%3C833%3A%3AAID-NAV3220410611%3E3.0.CO%3B2-Q).
No new optimization theorem or general efficient algorithm is claimed here.

For request indicators x_r, blob indicators y_b, utility u_r, blob weights w_b,
required closure C_r, and mandatory existing closure B, the integer formulation is

    maximize sum(u_r * x_r)
    subject to x_r <= y_b for every b in C_r
               y_b = 1 for every b in B
               sum(w_b * y_b) <= payload_budget
               x_r, y_b in {0,1}.

The reference implementation directly exhausts all subsets of at most sixteen
requests. Ties prefer fewer payload bytes, then lexicographic request ids.
It refuses larger inputs rather than presenting a heuristic as an optimum.
If existing strong retention alone exceeds budget, it returns infeasible and
releases nothing. This is optimal only for the supplied requests, utilities,
current mandatory roots and canonical payload metric.

## Executable control path

1. Workers call the existing `prepare` to produce immutable snapshot offers.
2. The owner supplies `Request(id, utility, snapshot)` records and a byte budget
   to `plan`. Every offer is validated, including offers eventually excluded.
3. The plan binds the request ids, utilities, content roots, registry root and
   budget through its problem digest. Its descriptor also records the selected
   ids, objective, payload cost and subset counts.
4. `admit` receives the authoritative budget again and recomputes the optimum.
   A changed request, registry, budget or plan is rejected before publication.
5. Chosen snapshots are published using the existing adapter into private
   staging stores. Only after the complete batch succeeds are the public stores
   updated. Failure on the second staged publication cannot leave the first
   guest partly admitted. Handles use the existing independent `resume` path.

This follows the validation-atomicity boundary of Continuity decision
`90df36a0-804f-4e55-ba8c-91281758521a`: owner operations are serialized;
allocation failure during final installation and process crashes are outside
the in-memory model. The plan is not an authorization token. Utility and the
meaning of distinct requests are supplied by the trusted caller. Distinct
fork requests may share an identical snapshot root; registry record overhead
is excluded, so this metric cannot price the total cost of those forks.

## Verification and limits

`analysis/w33_snapshot_admission_certificate.json` freezes every subset cost
above, the greedy comparison, the exact eight-subset search and recovered
outputs. Ten tests additionally use an independent materialization oracle:
for every subset of five requests, actually publish and collect its archive,
then compare the optimizer at every resulting budget boundary. Other tests
cover mandatory foreign roots, unretained garbage, stale plans, changed
utility, external budget binding, malformed excluded offers, corrupt content,
injected staging failure, tie rules, and the sixteen-request ceiling.

```sh
python analysis/w33_snapshot_admission_scheduler.py
python tests/test_w33_snapshot_admission_scheduler.py
```

Costs are canonical JSON blob payloads, excluding registry/index bytes, peak
scratch RAM, I/O, CPU and physical energy. Enumeration is exponential and
offer validation materializes temporary stores. Admission supplies neither
CPU fairness nor an end-to-end memory bound, eviction policy, durable commit,
physical quantum computation or an infinite collision-free hash namespace.
The broader requested history and recursive manuscript intake remains in
progress; this packet does not certify completion of that reading.

Five independent directions: integrate a certified larger-instance solver;
bound carry/borrow execution; add crash-safe publication; separate reusable
proofs from authority; compile verified retention lifetimes.
