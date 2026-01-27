import sys, subprocess, json
out = {'python': sys.executable}
try:
    out['pip_list'] = subprocess.check_output([sys.executable, '-m', 'pip', 'list', '--format=json']).decode()
except Exception as e:
    out['pip_list'] = 'ERROR: ' + repr(e)
for p in ['pandas','jsonschema','sage']:
    try:
        m = __import__(p)
        out[p] = {'found': True, 'version': getattr(m, '__version__', None)}
    except Exception as e:
        out[p] = {'found': False, 'error': repr(e)}
open('env_status.json','w').write(json.dumps(out, indent=2))
print('WROTE env_status.json')
