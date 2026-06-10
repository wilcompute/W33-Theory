from pathlib import Path
root=Path(__file__).resolve().parents[1]
src=root/'analysis/BT719_selector_uniqueness_tex_insert.tex'
dst=root/'paper/sections/sec_bt719_selector_classification.tex'
pre=root/'paper/w33_preprint.tex'
line='\\input{sections/sec_bt719_selector_classification}'
dst.parent.mkdir(parents=True,exist_ok=True)
dst.write_text(src.read_text(),encoding='utf-8')
text=pre.read_text(encoding='utf-8')
if line not in text:
    marker='\\section{The TOE Singularity Theorem}'
    text=text.replace(marker,line+'\n\n'+marker,1)
    pre.write_text(text,encoding='utf-8')
print('BT719 integrated')
