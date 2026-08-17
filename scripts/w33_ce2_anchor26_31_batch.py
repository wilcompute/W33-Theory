"""Pass6089-6100 compatibility ledger — corrected by Pass6137-6144.

The historical file created one dictionary per anchor with `covered=50` and
`status=CLOSED`; it contained no CE2 rows, no coefficient evaluations, and no
group/action computation. These anchors remain open.
"""

bases=list(range(26,32))
ledger=[{
 'anchor':f'basis ({b},*)',
 'status':'OPEN__NO_ROWS_OR_ACTION_CERTIFICATE',
 'actual_rows_loaded':0,
 'orbit_action_constructed':False,
 'historical_covered_50':'WITHDRAWN_UNEVIDENCED',
} for b in bases]

print('=== CE2 Anchors 26-31 Corrected Status ===')
for x in ledger: print(x)
