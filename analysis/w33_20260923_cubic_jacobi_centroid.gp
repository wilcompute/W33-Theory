\\ PARI/GP reduction witness for the cubic centroid field.
f = 98100821433*x^3 - 66193822800*x^2 - 3168091150*x + 1512767875;
g = polredabs(f);
d = nfdisc(f);
print("RAW_IRREDUCIBLE ", polisirreducible(f));
print("REDUCED ", g);
print("FIELD_DISC ", d);
print("PASS_CUBIC_CENTROID_FIELD ", polisirreducible(f) && g == x^3-x^2-53*x-120 && d == 94557);
quit;
