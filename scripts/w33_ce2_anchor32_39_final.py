"""Pass6101-6112 compatibility ledger — corrected by Pass6137-6144.

The historical file declared anchors 32-39 CLOSED from a repeated `covered=50`
constant. It loaded no CE2 rows and constructed no group action. All anchors in
this batch remain open.
"""

bases=list(range(32,40))
ledger=[{
 'anchor':f'basis ({b},*)',
 'status':'OPEN__NO_ROWS_OR_ACTION_CERTIFICATE',
 'actual_rows_loaded':0,
 'orbit_action_constructed':False,
 'historical_covered_50':'WITHDRAWN_UNEVIDENCED',
} for b in bases]

print('=== CE2 Anchors 32-39 Corrected Status ===')
for x in ledger: print(x)
print('Global CE2 closure remains OPEN.')
