----------------------------- MODULE W33EpochBFT -----------------------------
EXTENDS Naturals, FiniteSets, Sequences

CONSTANT Validators, Values, Quorum, Byzantine, MaxView
ASSUME /\ Validators # {}
       /\ Values # {}
       /\ Quorum \in Nat
       /\ Byzantine \subseteq Validators
       /\ Cardinality(Byzantine) <= 1
       /\ MaxView \in Nat

ViewSet == 0..MaxView
Honest == Validators \ Byzantine

VARIABLES view, votes, prepared, committed, lock
vars == <<view, votes, prepared, committed, lock>>

VoteKey(v, ph) == <<view, ph, v>>
SignerSet(ph, x) == {v \in Validators : votes[VoteKey(v, ph)] = x}
HasQC(ph, x) == Cardinality(SignerSet(ph, x)) >= Quorum

TypeOK ==
  /\ view \in ViewSet
  /\ votes \in [ [ViewSet, {"PREPARE", "COMMIT"}, Validators] -> (Values \cup {"NONE"}) ]
  /\ prepared \in SUBSET Values
  /\ committed \in SUBSET Values
  /\ lock \in (Values \cup {"NONE"})

Init ==
  /\ view = 0
  /\ votes = [k \in [ViewSet, {"PREPARE", "COMMIT"}, Validators] |-> "NONE"]
  /\ prepared = {}
  /\ committed = {}
  /\ lock = "NONE"

Vote(v, ph, x) ==
  /\ v \in Validators
  /\ x \in Values
  /\ votes[VoteKey(v, ph)] = "NONE"
  /\ IF v \in Byzantine
        THEN TRUE
        ELSE /\ (ph = "PREPARE" => (lock = "NONE" \/ lock = x))
             /\ (ph = "COMMIT" => x \in prepared)
  /\ votes' = [votes EXCEPT ![VoteKey(v, ph)] = x]
  /\ UNCHANGED <<view, prepared, committed, lock>>

FormPrepareQC(x) ==
  /\ x \in Values
  /\ HasQC("PREPARE", x)
  /\ (lock = "NONE" \/ lock = x)
  /\ prepared' = prepared \cup {x}
  /\ lock' = x
  /\ UNCHANGED <<view, votes, committed>>

FormCommitQC(x) ==
  /\ x \in prepared
  /\ HasQC("COMMIT", x)
  /\ committed' = committed \cup {x}
  /\ UNCHANGED <<view, votes, prepared, lock>>

Timeout ==
  /\ view < MaxView
  /\ view' = view + 1
  /\ UNCHANGED <<votes, prepared, committed, lock>>

Next ==
  \/ \E v \in Validators, ph \in {"PREPARE", "COMMIT"}, x \in Values : Vote(v, ph, x)
  \/ \E x \in Values : FormPrepareQC(x)
  \/ \E x \in Values : FormCommitQC(x)
  \/ Timeout

Safety == Cardinality(committed) <= 1
LockSafety == lock # "NONE" => prepared \subseteq {lock}
TypeInvariant == TypeOK

Spec == Init /\ [][Next]_vars

=============================================================================
\* Finite one-height safety abstraction for TLC. Five validators, quorum four,
\* two competing values, one explicitly Byzantine validator, and bounded views
\* are supplied by W33EpochBFT.cfg.  Honest PREPARE votes obey a persistent
\* prepare lock; the Byzantine validator may vote arbitrarily once per phase/view.
\* The executable Python fuzzer separately exercises durable implementation
\* snapshots, crashes/restarts, timeout certificates and signature validation.
\* Neither artifact claims production-network liveness under arbitrary delay.
