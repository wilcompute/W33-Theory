#!/usr/bin/env python3
"""Idempotently patch photonic_holonet.tex with the BT893--BT898 Yukawa/profile correction.

This targets the Photonic Holonet paper, not a standalone transvection paper.
The word transvection remains valid as an internal Standard-Model-spine theorem;
the paper identity and guard target are the holonet architecture.
"""
from __future__ import annotations
from pathlib import Path

TARGET=Path("photonic_holonet.tex")

OLD_FLAVOR="""The grading $R$ and its conjugation $C$ together generate the
\\textbf{flavor group $S_3$} ($\\langle R,C\\rangle$, order $6$,
non-abelian --- the minimal non-abelian flavor symmetry of BSM
model-building), under which the matter shell decomposes as
$\\mathbb{C}[27]=6\\cdot\\mathbf{1}\\oplus3\\cdot\\mathbf{1'}\\oplus
9\\cdot\\mathbf{2}$, the standard doublet appearing $q^2=9$ times.
And the flavor--gauge relationship is exact:"""

NEW_FLAVOR="""The grading $R$ and its conjugation $C$ together generate the
\\textbf{flavor group $S_3$} ($\\langle R,C\\rangle$, order $6$,
non-abelian --- the minimal non-abelian flavor symmetry of BSM
model-building), under which the matter shell decomposes as
$\\mathbb{C}[27]=6\\cdot\\mathbf{1}\\oplus3\\cdot\\mathbf{1'}\\oplus
9\\cdot\\mathbf{2}$, the standard doublet appearing $q^2=9$ times.
The newest Yukawa correction (BT893--BT898) sharpens the texture
boundary: for a Higgs of grade $g_H$ the generation-pair support is
not a pure cyclic shift but the shifted reflection
\\[
Y_{g_H}[a,b]=1\\quad\\Longleftrightarrow\\quad b\\equiv -a-g_H\\pmod3,
\\]
so the three Higgs-grade skeletons are exactly the three reflections
of $D_3\\cong S_3$.  Consequently $Y_{g_H}Y_{g_H}^T=I_3$: the
three-grade skeleton is support-complete but angle-blind.  The
physical CKM/PMNS and mass hierarchy layer must live in the
within-grade $q^2=9$ profile degrees of freedom, precisely the same
$9\\cdot\\mathbf2$ flavor multiplicity.  In that profile layer the
substrate-native Cabibbo plane is $(\\Phi_3,q)=(13,3)$, giving
$\\sin\\theta=q/\\sqrt{\\Phi_3^2+q^2}=3/\\sqrt{178}$, while the Koide
condition is the equal-norm split between the $S_3$ singlet and
standard-doublet components of the signed square-root mass vector.
And the flavor--gauge relationship is exact:"""

OLD_ETHOS="""the tomotope's framing was corrected from ``non-polytopal maniplex''
to ``uniform polytope with non-polytopal minimal covers'' when the
literature was read precisely; and the ``$\\mathbb{Z}_3$ Berry phase
as a discrete second Chern class'' was corrected (BT871) --- the
uniform Berry $2$-cochain is a coboundary over $\\mathbb{F}_3$, so the
physical $\\mathbb{Z}_3$ is the order-$3$ action on the Steinberg
register, not a curvature class."""

NEW_ETHOS="""the tomotope's framing was corrected from ``non-polytopal maniplex''
to ``uniform polytope with non-polytopal minimal covers'' when the
literature was read precisely; the ``$\\mathbb{Z}_3$ Berry phase
as a discrete second Chern class'' was corrected (BT871) --- the
uniform Berry $2$-cochain is a coboundary over $\\mathbb{F}_3$, so the
physical $\\mathbb{Z}_3$ is the order-$3$ action on the Steinberg
register, not a curvature class; and the Yukawa texture wording was
corrected (BT893--BT898) from a misleading circulant/support-shift
reading to a shifted-reflection $S_3$ skeleton whose numerical angles
live only in the within-grade $q^2=9$ profile layer."""

OLD_LEDGER="""flavor group $S_3$ ($\\mathbb{C}[27]=6{\\cdot}1{+}3{\\cdot}1'{+}9{\\cdot}2$) & bt879\\\\"""
NEW_LEDGER=OLD_LEDGER+"""
Yukawa reflection/profile layer (shifted reflections, $q^2=9$ profiles, Koide bridge) & bt893--bt898\\\\"""

def replace_once(text:str,old:str,new:str,name:str)->str:
    if new in text:
        return text
    if old not in text:
        raise SystemExit(f"BT899 patch failed: missing anchor {name}")
    return text.replace(old,new,1)

def main()->None:
    text=TARGET.read_text(encoding="utf-8")
    text=replace_once(text,OLD_FLAVOR,NEW_FLAVOR,"flavor paragraph")
    text=replace_once(text,OLD_ETHOS,NEW_ETHOS,"ethos correction paragraph")
    text=replace_once(text,OLD_LEDGER,NEW_LEDGER,"verification ledger")
    TARGET.write_text(text,encoding="utf-8")
    print("BT897--BT899 photonic_holonet.tex patch applied/idempotent")

if __name__=="__main__": main()
