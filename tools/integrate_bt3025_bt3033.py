#!/usr/bin/env python3
"""Idempotently integrate Passes 3025--3033 into all four canonical front doors."""
from __future__ import annotations

import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SHARED='    \\input{analysis/BT3025_BT3033_belief_machine_insert}%\n'
BLUEPRINT_BEGIN='% BEGIN BT3025-BT3033 BELIEF MACHINE'
BLUEPRINT_END='% END BT3025-BT3033 BELIEF MACHINE'
BLUEPRINT_BLOCK=(f'\n{BLUEPRINT_BEGIN}\n'
                 '\\input{analysis/BT3025_BT3033_belief_machine_blueprint_insert}\n'
                 f'{BLUEPRINT_END}\n')
HTML_BEGIN='<!-- BEGIN BT3025-BT3033 BELIEF MACHINE -->'
HTML_END='<!-- END BT3025-BT3033 BELIEF MACHINE -->'


def replace_block(text,begin,end,block,anchor):
    if begin in text:
        start=text.index(begin)
        finish=text.index(end,start)+len(end)
        return text[:start]+block.strip('\n')+text[finish:]
    position=text.rfind(anchor)
    if position<0:
        raise RuntimeError(f'anchor {anchor!r} not found')
    return text[:position]+block+text[position:]


def integrate_wrapper(path):
    text=path.read_text()
    if SHARED.strip() not in text:
        matches=list(re.finditer(r'^    \\input\{analysis/[^}]+\}%\s*$',text,re.M))
        if not matches:
            raise RuntimeError(f'no theorem insert list in {path}')
        point=matches[-1].end()
        text=text[:point]+'\n'+SHARED.rstrip('\n')+text[point:]
    text=re.sub(r'(1821-)(\d+)( plus frame-Hoffman wrapper)',r'\g<1>3033\g<3>',text,count=1)
    path.write_text(text)


def main():
    integrate_wrapper(ROOT/'w33_paper.tex')
    integrate_wrapper(ROOT/'photonic_holonet.tex')

    blueprint=ROOT/'holonet_machine_blueprint.tex'
    text=blueprint.read_text()
    text=replace_block(text,BLUEPRINT_BEGIN,BLUEPRINT_END,BLUEPRINT_BLOCK,'\\end{document}')
    blueprint.write_text(text)

    html_path=ROOT/'docs'/'index.html'
    html=html_path.read_text()
    block=(ROOT/'analysis'/'BT3025_BT3033_belief_machine_index_insert.html').read_text().strip()
    html=replace_block(html,HTML_BEGIN,HTML_END,'\n'+block+'\n','</body>')
    html_path.write_text(html)
    print('BT3025-BT3033 four-front-door integration complete')


if __name__=='__main__':
    main()
