"""Pass6113-6124 global CE2 ledger — corrected by Pass6137-6144.

A global closure can be claimed only from evidenced sectors. This verifier is
fail-closed: it reports the number of explicitly loaded/evidenced orbit rows and
never converts unlabeled placeholders into closed sectors.
"""

# Current live evidence after corrections.
# Anchor 22 producer retains 3 imported witnesses; anchor23 retains 5 seed rows.
# Anchors24-25 contain analogy hypotheses only; anchors26-39 contain no rows.
evidence={
 22:{'actual_rows_loaded':3,'status':'OPEN'},
 23:{'actual_rows_loaded':5,'status':'OPEN'},
 24:{'actual_rows_loaded':0,'status':'OPEN'},
 25:{'actual_rows_loaded':0,'status':'OPEN'},
}
for b in range(26,40): evidence[b]={'actual_rows_loaded':0,'status':'OPEN'}

coverage_denominator=20  # explicitly tracked basis sectors 20..39
closed=[b for b,x in evidence.items() if x['status']=='CLOSED']
actual_rows_loaded=sum(x['actual_rows_loaded'] for x in evidence.values())

print('=== CE2 Global Evidence Ledger — Fail Closed ===')
print('tracked basis sectors: 20..39')
print('coverage_denominator:',coverage_denominator)
print('evidenced closed sectors:',len(closed))
print('actual_rows_loaded:',actual_rows_loaded)
print('closed labels:',closed)
print('GLOBAL STATUS: OPEN / NOT VERIFIED COMPLETE')

assert len(closed) < coverage_denominator
assert actual_rows_loaded == 8
