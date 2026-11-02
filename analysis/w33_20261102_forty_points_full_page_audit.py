"""Complete page-by-page text audit of the local 215-page Forty Points PDF."""
import re,hashlib,json
from pathlib import Path
import fitz
ROOT=Path(__file__).resolve().parents[1]
pdf=ROOT/'papers/forty_points/main.pdf'
doc=fitz.open(pdf)
assert len(doc)==215
rows=[]
full=[]
for i in range(len(doc)):
 p=doc.load_page(i)
 txt=p.get_text('text',sort=True)
 assert txt.strip(),f'empty page {i+1}'
 full.append(txt)
 lines=[x.strip() for x in txt.splitlines() if x.strip()]
 rows.append({'page':i+1,'chars':len(txt),'sha256':hashlib.sha256(txt.encode('utf-8')).hexdigest(),
    'top_lines':lines[:4],
    'theorem_mentions':len(re.findall(r'\\bTheorem\\s+\\d',txt)),
    'status_refuted':len(re.findall(r'\\bREFUTED\\b',txt)),
    'status_open':len(re.findall(r'\\bOPEN\\b',txt))})
text='\n'.join(full)
result={'schema':'w33.20261102.forty_points_complete_pdf_page_audit.v1',
 'status':'ALL_215_PAGES_EXTRACTED_AND_INDEXED',
 'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),
 'pdf_byte_size':pdf.stat().st_size,
 'page_count':len(rows),'nonempty_pages':sum(bool(x['chars']) for x in rows),
 'total_extracted_characters':sum(x['chars'] for x in rows),
 'combined_normalized_text_sha256':hashlib.sha256(text.encode('utf-8')).hexdigest(),
 'theorem_mentions':sum(x['theorem_mentions'] for x in rows),
 'explicit_refuted_markers':sum(x['status_refuted'] for x in rows),
 'explicit_open_markers':sum(x['status_open'] for x in rows),
 'pages':rows,
 'scope':'Every PDF page extracted and indexed; textual coverage is NOT a proof that each claim or printed equation was independently checked, nor a visual check of every figure.'}
out=ROOT/'data/w33_20261102_forty_points_complete_page_audit.json'
out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('PAPER_AUDIT',result['status'],'CHARS',result['total_extracted_characters'],'SHA',result['pdf_sha256'],flush=True)
print('READ_COVERAGE',len(doc),'pages; last three:',repr([x['top_lines'][:2] for x in rows[-3:]]).encode('ascii','backslashreplace').decode('ascii'),flush=True)
