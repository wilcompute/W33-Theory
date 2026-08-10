import json, zipfile, pathlib
ROOT = pathlib.Path('c:/Repos/Theory of Everything')
# find conj bundle with wildcard
cands = list(ROOT.glob('WE6_EVEN_to_PSp43_CONJUGACY_BUNDLE_v01*'))
print('cands',cands)
bundle = cands[0]
def load_json(bundle,name):
    if bundle.is_file():
        with zipfile.ZipFile(bundle) as z:
            return json.loads(z.read(name))
    else:
        return json.loads((bundle/name).read_text(encoding="utf-8"))
gens = load_json(bundle,'psp43_line_generators_6.json')['generators']
print('number generators', len(gens))
print('lengths', [len(g) for g in gens])
