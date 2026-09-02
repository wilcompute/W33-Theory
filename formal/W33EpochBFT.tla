----------------------------- MODULE W33EpochBFT -----------------------------
EXTENDS Naturals, FiniteSets, Sequences

CONSTANT Validators, Values, Quorum
ASSUME Validators # {} /\ Values # {} /\ Quorum \in Nat

VARIABLES view, votes, prepared, committed
vars == <<view, votes, prepared, committed>>

VoteKey(v, ph) == <<view, ph, v>>
SignerSet(ph, x) == {v \in Validators : votes[VoteKey(v, ph)] = x}
HasQC(ph, x) == Cardinality(SignerSet(ph, x)) >= Quorum

TypeOK ==
  /\ view \in Nat
  /\ votes \in [ [Nat, {"PREPARE", "COMMIT"}, Validators] -> (Values \cup {"NONE"}) ]
  /\ prepared \in SUBSET Values
  /\ committed \in SUBSET Values

Init ==
  /\ view = 0
  /\ votes = [k \in [Nat, {"PREPARE", "COMMIT"}, Validators] |-> "NONE"]
  /\ prepared = {}
  /\ committed = {}

HonestVote(v, ph, x) ==
  /\ v \in Validators
  /\ x \in Values
  /\ votes[VoteKey(v, ph)] = "NONE"
  /\ ph = "PREPARE" \/ x \in prepared
  /\ votes' = [votes EXCEPT ![VoteKey(v, ph)] = x]
  /\ UNCHANGED <<view, prepared, committed>>

FormPrepareQC(x) ==
  /\ x \in Values
  /\ HasQC("PREPARE", x)
  /\ prepared' = prepared \cup {x}
  /\ UNCHANGED <<view, votes, committed>>

FormCommitQC(x) ==
  /\ x \in prepared
  /\ HasQC("COMMIT", x)
  /\ committed' = committed \cup {x}
  /\ UNCHANGED <<view, votes, prepared>>

Timeout ==
  /\ view' = view + 1
  /\ UNCHANGED <<votes, prepared, committed>>

Next ==
  \/ \E v \in Validators, ph \in {"PREPARE", "COMMIT"}, x \in Values : HonestVote(v, ph, x)
  \/ \E x \in Values : FormPrepareQC(x)
  \/ \E x \in Values : FormCommitQC(x)
  \/ Timeout

Safety == Cardinality(committed) <= 1

Spec == Init /\ [][Next]_vars

=============================================================================
\* Model-check with five validators, two values and Quorum=4.  This abstraction
\* intentionally models only one height.  The executable Python adversarial
\* fuzzer covers durable votes, crashes/restarts, view rotation and one Byzantine
\* signer.  Production liveness/network timing remain outside this small model.
