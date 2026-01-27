JSON-safe helpers

Use `dump_json(obj, path_or_fileobj, **kwargs)` to write results with robust
serialization for Sage `Integer`, numpy types, Decimal and similar objects.

Example:

from utils.json_safe import dump_json

results = {'count': 42, 'sage_int': some_sage_integer}
dump_json(results, 'PART_XYZ_results.json', indent=2)
