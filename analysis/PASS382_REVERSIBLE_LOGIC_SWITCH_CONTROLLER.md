# Pass 382 — a 48-state reversible logic-switch controller

The LOAD_FLAG → FLIP_Q6_AXIS → LATCH_VERTEX word is most useful here as a
finite controller, not as a claim about a physical oscillator. This pass builds
an isolated reversible switching machine on

`Z/16 edge-step index × Z/3 phase`.

Its 48 states represent a sequencing register and one three-position operation
word. They do not carry actual flags, headers, Q6 edges, or routes.

## The switch machine

Let `T` be the controller tick. Its full transition table is generated in the
certificate, and its rule is:

~~~
T(edge, 0) = (edge, 1)               LOAD_FLAG → FLIP_Q6_AXIS
T(edge, 1) = (edge, 2)               FLIP_Q6_AXIS → LATCH_VERTEX
T(edge, 2) = (edge + 1 mod 16, 0)    LATCH_VERTEX → next LOAD_FLAG
~~~

So LOAD and FLIP are intra-edge logic switches, while LATCH is the switch that
advances the 16-step control register. GAP verifies all of the following:

- `T` is a bijection with an explicit two-sided inverse.
- `T` has exact order 48 and reaches every state from one start state.
- Each operation labels exactly 16 states; precisely 16 latch transitions
  advance the edge-step index.
- The one transition from `(15, 2)` to `(0, 0)` is a **controller-frame wrap**.
  It is not a Q6 path closure.

This gives a precise finite-state “oscillator” reading: a reversible 48-cycle
clock, not an assertion that a physical harmonic oscillator has been built or
identified. In particular, this controller does not identify a physical oscillator.

## The phase clock is not the sequencing clock

The same state set also has the free phase rotation

~~~
P(edge, phase) = (edge, phase + 1 mod 3).
~~~

`P` has order 3 and splits the controller into 16 three-state phase orbits. It
is a useful clock/relabeling action, but it is not the controller update `T`:
it agrees with `T` on the 32 LOAD and FLIP states and differs on exactly the 16
LATCH states. The two maps fail to commute on the 16 FLIP and 16 LATCH states:
a phase relabeling just before versus just after a latch gives a different edge
step. That is the logic-level reason a phase rotation cannot silently stand in
for a sequence advance.

## Fault-injection results

The certificate compares each injected map with the expected tick `T`.

| injected update | wrong expected transitions | reachable orbit size | exact residual syndrome |
|---|---:|---:|---|
| use `P` in place of `T` | 16, exactly the latches | 3 | 32 states at `0`, 16 at `45 mod 48` |
| stutter (`id`) | 48 | 1 | 48 states at `47 mod 48` |
| double tick (`T²`) | 48 | 24 | 48 states at `1 mod 48` |

These are finite control-state diagnostics. They show that the machine detects
these substitutions relative to its specified successor relation; they do not
claim fault tolerance, correction, timing performance, or a hardware device.

## Relation to the existing scheduler work

Pass 380 already proves the minimal **actual scheduler** phase refinement
`(tomotope_flag, phase_trit)` and leaves the header-orbit binding as an
explicitly separate compiler input. This pass does not bind a header, does not
attach a route to a controller state, and does not alter that boundary. It
isolates the reusable computing/logic-switch content: a reversible sequence
clock with a three-state phase clock that must not be confused with it.

## Reproduction

~~~
gap -q analysis/w33_pass382_reversible_logic_switch_controller.g
python3 -m pytest tests/test_pass382_gap_reversible_logic_switch_controller.py -q
~~~

- witness: `analysis/w33_pass382_reversible_logic_switch_controller.g`
- certificate: `data/w33_pass382_reversible_logic_switch_controller.json`
- regression: `tests/test_pass382_gap_reversible_logic_switch_controller.py`

Search signature: `48-cycle/16xC3/LOAD-FLIP-LATCH/reversible-logic-switch`.
