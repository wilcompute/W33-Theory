"""verdict of a specdump output file: 'SM' (an NU1 line = SM spectrum printed), 'noSM' (loaded, no SM), 'load failure' (anything
else: empty, or only warnings such as 'Orbifold group ill-defined').  Shell exit codes from the batch loops are not used."""
def sdclass(path):
    t = open(path, errors='ignore').read()
    if any(l.startswith('NU1 ') for l in t.split('\n')):
        return 'SM'
    if t.strip().startswith('noSM') or '\nnoSM' in t:
        return 'noSM'
    return 'load failure'
