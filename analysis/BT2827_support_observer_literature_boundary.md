# Pass 2827: Support Observer Literature Boundary

The Pass 2825--2827 result should be stated in standard finite-state testing language.

- A **preset distinguishing sequence** (PDS) is one fixed input word whose output trajectory identifies the initial state.
- An **adaptive distinguishing sequence** (ADS) chooses later inputs from earlier outputs; more generally, an all-word refinement asks whether bounded-depth experiments separate every state pair.
- Finite-state **observability** is reconstruction of the discrete state from input/output behavior.

These notions are standard in FSM testing and diagnosability; see, for example:

1. R. M. Hierons and U. C. Türker, “Distinguishing Sequences for Distributed Testing: Preset Distinguishing Sequences,” *The Computer Journal* 60 (2017), 110--125, DOI `10.1093/comjnl/bxw069`.
2. R. M. Hierons, G.-V. Jourdan, H. Ural, and H. Yenigün, “Using Adaptive Distinguishing Sequences in Checking Sequence Constructions,” SAC 2008, DOI `10.1145/1363686.1363850`.
3. E. De Santis and M. D. Di Benedetto, “Observability and diagnosability of finite state systems: a unifying framework,” *Automatica* 81 (2017), 115--122, DOI `10.1016/j.automatica.2017.02.042`.

The W33 claim is narrower and exact:

- the machine is a deterministic 81-state frame automaton;
- its input alphabet is the selected four-operation micro-ISA;
- its output is the four-bit binary support mask;
- exhaustive refinement has depth profile `16 -> 40 -> 78 -> 81`;
- the shortest preset support experiment has length six;
- exactly eight shortest preset words exist;
- the canonical experiment admits exactly 48 minimum eight-tap telemetry selectors.

No general complexity claim is made.  No equivalence is claimed between the W33 automaton and an arbitrary FSM class.  The cited literature supplies terminology and comparison only; every W33 count is produced by the repository verifier.
