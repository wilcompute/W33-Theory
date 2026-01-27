import json, sys
from pathlib import Path
try:
    import jsonschema
except Exception as e:
    print('jsonschema import failed', repr(e))
    sys.exit(2)

def do(path, schema_path):
    d = json.loads(Path(path).read_text())
    s = json.loads(Path(schema_path).read_text())
    try:
        jsonschema.validate(instance=d, schema=s)
        print(f'VALID {path}')
    except Exception as e:
        print(f'INVALID {path}: {e}')
        raise

try:
    do('SUMMARY_RESULTS.json', 'schemas/summary_results.schema.json')
    do('NUMERIC_COMPARISONS.json', 'schemas/numeric_comparisons.schema.json')
    print('ALL VALID')
except Exception as e:
    sys.exit(1)
