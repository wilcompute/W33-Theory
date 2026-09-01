#!/usr/bin/env python3
"""Promote the 2026-09-01 all-five follow-up only from frozen PASS certificates.

Writes one TeX insert and one Markdown audit, appends the shared TeX frontier
manifest (thereby reaching all three manuscript front doors), updates the JSON
frontier reachability manifest, and inserts one card + nav link into root
index.html.  It fails closed if any required certificate is absent or not PASS.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
AN=ROOT/'analysis'


def load(name):
    p=DATA/name
    if not p.exists():raise FileNotFoundError(p)
    x=json.loads(p.read_text())
    if x.get('status')!='PASS':raise RuntimeError(f'{name}: {x.get("status")}')
    return x


def tf(x):return 'true' if x else 'false'
def pmatrix(rows):return '\\begin{pmatrix}'+r'\\'.join(' & '.join(map(str,row)) for row in rows)+'\\end{pmatrix}'


def main():
    atlas=load('PART_W33_20260901_GQ24_K44_E8_ATLAS.json')
    prim=load('PART_W33_20260901_K33_STEINBERG_PRIMITIVE.json')
    e6=load('PART_W33_20260901_E6_ODD_TRIANGLE_STEINBERG.json')
    pkt=load('PART_W33_20260901_PACKET_K33_GLOBALIZATION.json')
    m3=load('PART_W33_20260901_STEINBERG_M3_MATRIX_UNITS.json')
    b48=load('PART_W33_20260901_BINARY48_MEATAXE_ONLY.json')

    dark=e6['darkProjectorDirectHits']
    er=e6['relationsByIntersectionSize']
    orbit=pkt['packetStabilizer']['orbitSizes']
    cls=pkt['packet0IntersectionClassSizes']
    qmat=m3['K33PrimitiveQCoordinates']
    iso=b48['moduleIsomorphism']
    cf=b48['compositionFactorDimensions']
    homcf=b48['homBA']['compositionFactorDimensions']

    if dark:
        dark_sentence=('Among the three E6 even/odd triangle intersection relations, the relation(s) '
                       +', '.join(dark)+' have Steinberg Gram exactly proportional to the dark projector $S$.')
    else:
        dark_sentence=('None of the three coarse E6 even/odd triangle intersection relations has Steinberg Gram '
                       'proportional to $S$; this is a fail-closed no-go for that natural three-relation family, '
                       'not for all equivariant maps from the 120-point odd-triangle module.')

    table='; '.join(f'$|V\\cap U|={s}$: rank {er[s]["steinbergActualRank"]}' for s in ('0','1','2'))
    tex=f'''% Certificate-driven 2026-09-01 all-five follow-up.
\\subsection{{One $27\\times45$ atlas links $GQ(2,4)$, W33 octets, cubic incidence, and $E_8$ $D_4$ charts}}
\\label{{sec:20260901-gq24-e8-atlas}}

The same incidence matrix $I$ has row weight $5$, column weight $3$, and rank
$21$ over $\\mathbb Q$ and over $\\mathbb F_p$ for $p=2,3,5,7$.  Its $27$
rows are simultaneously points of $GQ(2,4)$, cubic-surface lines, W33
$K_{{4,4}}$-factorizations, and ten-$D_4$ partitions of the $240$ $E_8$ roots.
Its $45$ columns are simultaneously lines of $GQ(2,4)$, tritangent planes,
induced W33 $K_{{4,4}}$ octets, and orthogonal $D_4\\oplus D_4$ packets.  The
objectwise identities are
\\[
 II^T=5I_{{27}}+A_{{GQ(2,4)}},\\qquad I^TI=3I_{{45}}+A_{{GQ(4,2)}}.
\\]
An explicit coordinate permutation identifies this $I$ with the existing
$27$-line/$45$-tritangent cubic incidence matrix.

\\subsection{{The Schlaefli $K_{{3,3}}$ Gram selects one primitive Steinberg copy}}
\\label{{sec:20260901-steinberg-dark-frame}}

On the $3\\,\\mathrm{{St}}_{{81}}$ isotypic component the pulled-back
$K_{{3,3}}$ Gram obeys $K^2=8K$, so $Q=K/8$ is a primitive rank-$81$
projector.  If $P$ is the intrinsic $20_{{\\rm chart}}\\otimes15_{{\\rm W33}}$
Steinberg projector, then
\\[
 PQP=\\frac13P,\\qquad QPQ=\\frac13Q.
\\]
Normalizing the component of $Q$ in the complementary rank-$162$ sector gives
$R=\\frac32(E-P)Q(E-P)$ and $S=(E-P)-R$.  Exactly
\\[
 E=P\\oplus R\\oplus S,\\qquad
 \\operatorname{{rank}}P=\\operatorname{{rank}}R=\\operatorname{{rank}}S=81,
\\]
with $RQR=\\frac23R$ and $SQ=QS=0$.  Thus $S$ is an exact Steinberg-dark
complement for this finite incidence operator.  The squared multiplicity-space
overlap $1/3$ is representation theory, not a measured particle mixing angle.

\\subsection{{E6 odd triangles and the global packet/$K_{{3,3}}$ audit}}
\\label{{sec:20260901-e6-odd-global-k33}}

The $1080$ obstruction/C4 objects are explicitly the E6-sign-even triangles of
the double-six graph $H_{{36}}=\\operatorname{{SRG}}(36,20,10,12)$: the three
$K_{{3,3}}$ witnesses containing a C4 are the three $H_{{36}}$ edges of its
triangle.  The complementary $120$ sign-odd triangles are exactly the Steiner
trihedral-pair orbit.  For the three canonical even/odd incidence relations by
triangle-intersection size the Steinberg actual ranks are {table}.
{dark_sentence}

The separate $45\\times360$ packet/global-$K_{{3,3}}$ census is complete.  A
packet stabilizer has order $576$ and its orbit sizes on the global witness shell
are {orbit}.  For one packet the classes with zero, one, or two incident charts
inside a witness have sizes {cls['0']}, {cls['1']}, and {cls['2']} respectively.
The statement that an equivariant packet should canonically choose eight of the
$360$ global $K_{{3,3}}$s is therefore
\\texttt{{{tf(pkt['equivariantEightWitnessRefinementPossible'])}}} as a union of
stabilizer orbits.  This does not retract the local abstract quotient
$K_{{4,4}}\\to S_4/V_4\\simeq S_3\\to K_{{3,3}}$; it distinguishes that local
frame object from the global Schlaefli witness shell.

\\subsection{{The full rational Steinberg multiplicity algebra is explicit}}
\\label{{sec:20260901-steinberg-m3}}

Using $P,R,S$ as diagonal primitive idempotents and deterministic symmetric
orbital connectors, all nine rational matrix units $e_{{ij}}$ are constructed
and satisfy
\\[
 e_{{ij}}e_{{kl}}=\\delta_{{jk}}e_{{il}}.
\\]
Hence the entire finite-group multiplicity commutant is explicitly
$M_3(\\mathbb Q)$, not merely known abstractly from character multiplicity.
In those matrix-unit coordinates the geometric $K_{{3,3}}$ projector is
\\[
 [Q]_{{P,R,S}}={pmatrix(qmat)}.
\\]
The older deterministic $\\{-4,0,+4\\}$ orbital spectral frame is also
expressed in the same algebra.  These are multiplicity coordinates for three
isomorphic representations, not a physical generation or flavor matrix.

\\subsection{{Binary $48$: MeatAxe theorem separated from the Ext ceiling}}
\\label{{sec:20260901-binary48-meataxe}}

The canonical doubled-$D_4$ homology module and chamber
$\\operatorname{{im}}((LP-PL)\\bmod2)$ module are compared by aligned
$PSp(4,3)$ generators.  MeatAxe reports
$H_{{1,48}}\\cong\\Omega_{{48}}$ = \\texttt{{{tf(iso['H1_equals_Omega48'])}}}
and $A_{{24}}\\cong B_{{24}}$ = \\texttt{{{tf(iso['A24_equals_B24'])}}}.
Their composition-factor dimensions are
$H_{{1,48}}:{cf['H1_48']}$ and $\\Omega_{{48}}:{cf['Omega48']}$; the full
$576$-dimensional $\\operatorname{{Hom}}(B_{{24}},A_{{24}})$ MeatAxe factor
dimensions are {homcf}.  The independent splitting-equation certificate proves
$\\operatorname{{Ext}}^1(B_{{24}},A_{{24}})\\neq0$, so its dimension is at least
one.  Its exact dimension is deliberately left open because stock Cohomolo
refuses the full $576$-dimensional Hom module at its MDIM ceiling.

\\paragraph{{Evidence boundary.}}
Everything in this insert is finite incidence, finite-group representation,
modular-module, root-system, or exact linear-algebra evidence.  No spacetime,
particle, coupling, mass, laboratory threshold, or hardware dynamics follows
from the matching finite carriers without an additional explicit physical map.
'''
    (AN/'PASS20260901_all5_followup_insert.tex').write_text(tex)

    md=f'''# 2026-09-01 — all five follow-up fronts\n\n## Exact closures\n\n- **27×45 atlas:** one incidence matrix is simultaneously GQ(2,4), cubic 27/45, W33 K4,4-factor/octet, and E8 ten-D4/D4+D4 incidence.\n- **Steinberg frame:** `K^2=8K`; `Q=K/8` is primitive rank 81; `PQP=Q P Q=1/3`; `P,R,S` are orthogonal rank-81 projectors and `S Q=Q S=0`.\n- **E6 odd-triangle audit:** dark direct hits among intersection-size relations: `{dark}`; Steinberg actual ranks: `{ {s:er[s]['steinbergActualRank'] for s in ('0','1','2')} }`.\n- **Packet/global K3,3 audit:** packet-stabilizer orbit sizes `{orbit}`; equivariant eight-witness refinement possible: `{pkt['equivariantEightWitnessRefinementPossible']}`.\n- **Full M3(Q):** all nine rational matrix-unit identities verified; K3,3 projector coordinates `{qmat}`.\n- **Binary48:** H1 ≅ Omega48 = `{iso['H1_equals_Omega48']}`; A24 ≅ B24 = `{iso['A24_equals_B24']}`; Ext dimension remains open but is at least one from the explicit nonsplit extension.\n\n## Boundary\n\nThese are exact finite mathematical statements.  The 1/3 overlap, dark 81-space, and 3×3 multiplicity coordinates are not promoted as physical mixing angles, generations, fields, or dynamics.\n'''
    (AN/'2026-09-01_all5_followup.md').write_text(md)

    manifest=AN/'W33_CURRENT_FRONTIER_MANIFEST.tex'
    line=r'\\input{analysis/PASS20260901_all5_followup_insert}%'
    t=manifest.read_text()
    if line not in t:
        anchor=r'\\input{analysis/PASS20260901_five_front_execution_insert}%'
        if anchor not in t:raise RuntimeError('manifest anchor missing')
        t=t.replace(anchor,anchor+'\n'+line,1);manifest.write_text(t)

    jm=DATA/'w33_current_frontier_manifest_v1.json';j=json.loads(jm.read_text())
    req='analysis/PASS20260901_all5_followup_insert'
    if req not in j['required_ordered_inputs']:j['required_ordered_inputs'].append(req)
    jm.write_text(json.dumps(j,separators=(',',':'),sort_keys=True)+'\n')

    index=ROOT/'index.html';h=index.read_text();marker='<!-- 20260901-ALL5-STEINBERG-ATLAS -->'
    if marker not in h:
        nav='    <a href="#steinberg-all5-followup">Steinberg 81×3 atlas</a>\n'
        h=h.replace('  </nav>',nav+'  </nav>',1)
        dark_html=('one coarse E6 even/odd relation selects the dark projector'
                   if dark else 'the three coarse E6 even/odd relations do not by themselves select the dark projector')
        card=f'''  {marker}\n  <section class="card" id="steinberg-all5-followup">\n    <div class="status">PASS · 1 September 2026 · all-five follow-up</div>\n    <h2>One 27×45 atlas and an exact 81⊕81⊕81 Steinberg frame</h2>\n    <p>The same 27×45 incidence is now objectwise GQ(2,4), cubic line/tritangent, W33 K<sub>4,4</sub>-factor/octet, and E8 ten-D4 / D4⊕D4 incidence. Its rank is 21 over Q and mod 2,3,5,7.</p>\n    <div class="eq">K² = 8K; Q = K/8; rank Q = 81<br>PQP = (1/3)P; RQR = (2/3)R; SQ = QS = 0<br>E<sub>St</sub> = P ⊕ R ⊕ S, ranks 81 + 81 + 81</div>\n    <p>The entire multiplicity commutant is now explicit as nine rational matrix units for M<sub>3</sub>(Q). The E6 complementary 120 Steiner triangles were tested directly: {dark_html}. The packet stabilizer orbits on the 360 global K<sub>3,3</sub>s are {orbit}; an eight-witness equivariant refinement is {str(pkt['equivariantEightWitnessRefinementPossible']).lower()}.</p>\n    <p>Binary characteristic two was also separated cleanly from the Cohomolo size ceiling: MeatAxe says H1<sub>48</sub> ≅ Ω<sub>48</sub> is {str(iso['H1_equals_Omega48']).lower()}, while the independently proved nonsplit 24-by-24 extension gives Ext¹ ≠ 0 without guessing its exact dimension.</p>\n    <p class="boundary"><strong>Boundary:</strong> the 1/3 overlap and 3×3 coordinates are exact finite representation theory, not measured particle mixing, masses, couplings, or dynamics.</p>\n  </section>'''
        anchor='\n\n  <section class="card">'
        if anchor not in h:raise RuntimeError('root index card anchor missing')
        h=h.replace(anchor,'\n\n'+card+anchor,1);index.write_text(h)

    print(json.dumps({'status':'PASS','darkHits':dark,'packetOrbits':orbit,
                      'binaryIso':iso,'insert':'analysis/PASS20260901_all5_followup_insert.tex'},sort_keys=True))

if __name__=='__main__':main()
