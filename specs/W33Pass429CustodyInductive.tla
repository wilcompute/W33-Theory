---------------- MODULE W33Pass429CustodyInductive ----------------
EXTENDS Naturals, Sequences, FiniteSets, TLC

CONSTANTS Studies, Devices, Nonces, Roles, Keys, Payloads, Hash
CONSTANT StageType, StageRole, RoleKey, Context

VARIABLES chains, claims
vars == <<chains, claims>>

ChainOK(s, c) ==
  /\ Len(c) <= 8
  /\ \A i \in 1..Len(c):
       /\ c[i].type = StageType[i]
       /\ c[i].sequence = i-1
       /\ c[i].study = s
       /\ <<c[i].device,c[i].nonce>> = Context[s]
       /\ c[i].role = StageRole[i]
       /\ c[i].key = RoleKey[c[i].role]
       /\ c[i].claimEligible = FALSE
       /\ IF i=1 THEN c[i].predecessor = "GENESIS"
          ELSE /\ c[i].predecessor = Hash(c[i-1])
               /\ c[i].dependency = c[i-1].payload

DistinctRoleKeys == \A r1,r2 \in Roles: r1 # r2 => RoleKey[r1] # RoleKey[r2]
Complete(s) == s \in DOMAIN chains /\ Len(chains[s])=8
Safety ==
  /\ DistinctRoleKeys
  /\ \A s \in DOMAIN chains: ChainOK(s,chains[s])
  /\ claims \subseteq {s \in Studies: Complete(s)}

Init == chains = [s \in {} |-> <<>>] /\ claims = {}

Append(s,a) ==
  /\ s \in Studies
  /\ s \in DOMAIN chains
  /\ Len(chains[s]) < 8
  /\ LET i == Len(chains[s])+1 IN
       /\ a.type = StageType[i]
       /\ a.sequence = i-1
       /\ a.study = s
       /\ <<a.device,a.nonce>> = Context[s]
       /\ a.role = StageRole[i]
       /\ a.key = RoleKey[a.role]
       /\ a.claimEligible = FALSE
       /\ IF i=1 THEN a.predecessor = "GENESIS"
          ELSE /\ a.predecessor = Hash(chains[s][i-1])
               /\ a.dependency = chains[s][i-1].payload
  /\ chains' = [chains EXCEPT ![s] = Append(@,a)]
  /\ UNCHANGED claims

Finalize(s) ==
  /\ Complete(s)
  /\ claims' = claims \cup {s}
  /\ UNCHANGED chains

Next == (\E s \in Studies, a: Append(s,a)) \/ (\E s \in Studies: Finalize(s))
Spec == Init /\ [][Next]_vars

THEOREM TypeOK == Spec => []Safety
=============================================================================
