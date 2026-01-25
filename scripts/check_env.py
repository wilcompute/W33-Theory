import sys
from importlib import util
packages = ['pandas','jsonschema','sage']
print('python:', sys.executable)
for p in packages:
    spec = util.find_spec(p)
    print(p, 'found' if spec else 'MISSING')
    if spec:
        m = __import__(p)
        v = getattr(m, '__version__', None)
        print('  version:', v)
