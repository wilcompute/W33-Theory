from pathlib import Path
root=Path(__file__).resolve().parents[1]
fragment=(root/'analysis/PASS5028_5035_index_insert.html').read_text(encoding='utf-8')
for target in [root/'index.html',root/'docs/index.html']:
    text=target.read_text(encoding='utf-8')
    if 'pass5028-5035' not in text:
        target.write_text(text.replace('</body>',fragment+'\n</body>',1),encoding='utf-8')
