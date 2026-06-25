# BT1803 W(E6) orbit-classification handoff
# Load GRAPE/nauty in GAP, construct the Schlaefli graph SRG(27,16,10,8),
# compute Aut(Schlaefli) (expected order 51840 = W(E6)), then compute orbits
# on 18-subsets of the 45 tritangent support lines containing the BT1795 image.
#
# BT1795 image support indices:
BT1795Image := [5,7,10,12,15,18,20,22,29,30,34,36,37,38,40,41,42,44];
#
# Required outputs:
#   Size(AutSchlaefli);
#   Orbit(AutSchlaefliOnTritangents, BT1795Image, OnSets);
#   Stabilizer(AutSchlaefliOnTritangents, BT1795Image, OnSets);
#   Orbit representatives grouped by old/new count and double-six syndrome ranks.
#
# This file is a handoff stub: fill SchlaefliGraph and TritangentAction using
# GAP/GRAPE or a nauty-exported graph from analysis/bt1794_schlafli_e6_lift.py.
