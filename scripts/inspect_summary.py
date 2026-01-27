import json, pathlib
p=pathlib.Path('SUMMARY_RESULTS.json')
if not p.exists():
    print('MISSING')
else:
    d=json.loads(p.read_text())
    print('top_keys:', list(d.keys())[:10])
    print('has_total:', 'total_part_json_files' in d)
    if 'total_part_json_files' in d:
        print('total_part_json_files=', d['total_part_json_files'])
    print('has_summaries:', 'summaries' in d)
    if 'summaries' in d:
        print('summaries_len=', len(d['summaries']))
    # show a small snippet of collected_files count
    print('collected_files=', len(d.get('collected_files',[])))
