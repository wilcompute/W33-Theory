---------------- MODULE W33Pass424Custody ----------------
EXTENDS Naturals, Sequences, FiniteSets
CONSTANTS ArtifactTypes, Roles, Study, Device, Nonce
VARIABLES chain, keysDistinct, claimEligible
TypeOK == chain \in Seq([type: ArtifactTypes, seq: Nat, study: {Study}, device: {Device}, nonce: {Nonce}, predecessor: STRING, role: Roles])
Ordered == \A i \in 1..Len(chain): chain[i].seq = i-1
ContextBound == \A i \in 1..Len(chain): /\ chain[i].study=Study /\ chain[i].device=Device /\ chain[i].nonce=Nonce
HashChained == \A i \in 2..Len(chain): chain[i].predecessor = Hash(chain[i-1])
ClaimSafe == claimEligible => Len(chain)=Cardinality(ArtifactTypes)
Invariant == TypeOK /\ Ordered /\ ContextBound /\ HashChained /\ keysDistinct /\ ClaimSafe
Init == chain=<<>> /\ keysDistinct /\ ~claimEligible
Next == \/ HonestAppend \/ AdversarialCandidate
Spec == Init /\ [][Next]_<<chain,keysDistinct,claimEligible>>
THEOREM Spec => []Invariant
================================================================
