#!/usr/bin/env python3
"""Certificate-driven publication integration for the 2026-09-01 all-five pass."""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'; AN=ROOT/'analysis'

def load(name):
    p=DATA/name
    if not p.exists(): raise FileNotFoundError(p)
    x=json.loads(p.read_text())
    if x.get('status')!='PASS': raise RuntimeError(f'{name}: {x.get("status")}')
    return x

def tf(v): return 'true' if v else 'false'

def main():
    atlas=load('PART_W33_20260901_GQ24_K44_E8_ATLAS.json')
    prim=load('PART_W33_20260901_K33_STEINBERG_PRIMITIVE.json')
    e6=load('PART_W33_20260901_E6_ODD_TRIANGLE_STEINBERG.json')
    pkt=load('PART_W33_20260901_PACKET_K33_GLOBALIZATION.json')
    m3=load('PART_W33_20260901_STEINBERG_M3_MATRIX_UNITS.json')
    b48=load('PART_W33_20260901_BINARY48_MEATAXE_ONLY.json')

    dark=e6['darkProjectorDirectHits']; er=e6['relationsByIntersectionSize']
    orbit=pkt['packetStabilizer']['orbitSizes']; classes=pkt['packet0IntersectionClassSizes']
    qcoords=m3['K33PrimitiveQCoordinates']; iso=b48['moduleIsomorphism']
    cf=b48['compositionFactorDimensions']; homcf=b48['homBA']['compositionFactorDimensions']
    rankline=', '.join(f'|V\\cap U|={s}: {er[s]["steinbergActualRank"]}' for s in ('0','1','2'))
    if dark:
        darktex='The intersection relation(s) '+', '.join(dark)+' select the dark projector $S$ up to scalar.'
    else:
        darktex=('None of the three coarse even/odd intersection relations is proportional to $S$; '
                 'this is a no-go only for this canonical three-relation family.')

    tex=f'''% Generated from frozen PASS certificates by integrate_20260901_all5_followup_v2.py.
\\subsection{{A single $27\\times45$ atlas for $GQ(2,4)$, W33, cubic incidence, and $E_8$}}
The same matrix $I$ has row weight $5$, column weight $3$, and rank $21$ over
$\\mathbb Q,\\mathbb F_2,\\mathbb F_3,\\mathbb F_5,\\mathbb F_7$.  Its rows are
simultaneously $GQ(2,4)$ points, cubic lines, W33 $K_{{4,4}}$ factorizations,
and ten-$D_4$ $E_8$ charts; its columns are $GQ(2,4)$ lines, tritangent planes,
W33 $K_{{4,4}}$ octets, and orthogonal $D_4\\oplus D_4$ packets.  Explicitly
\\[
 II^T=5I_{{27}}+A_{{GQ(2,4)}},\\qquad I^TI=3I_{{45}}+A_{{GQ(4,2)}}.
\\]
After explicit row and column permutations this is the existing cubic
$27$-line/$45$-tritangent incidence matrix.

\\subsection{{The $K_{{3,3}}$ Gram and an exact $81\\oplus81\\oplus81$ Steinberg frame}}
On the three-copy Steinberg isotypic block, $K^2=8K$, so $Q=K/8$ is a primitive
rank-$81$ projector.  With $P$ the intrinsic
$20_{{\\rm chart}}\\otimes15_{{\\rm W33}}$ copy,
\\[
 PQP=\\tfrac13P,\\qquad QPQ=\\tfrac13Q.
\\]
Defining $R=\\tfrac32(E-P)Q(E-P)$ and $S=(E-P)-R$ gives
\\[
 E=P\\oplus R\\oplus S,\\qquad
 \\operatorname{{rank}}P=\\operatorname{{rank}}R=\\operatorname{{rank}}S=81,
\\]
with $RQR=\\tfrac23R$ and $SQ=QS=0$.

\\subsection{{E6 odd triangles and the packet/global-$K_{{3,3}}$ census}}
The $1080$ obstruction/C4 carrier is explicitly the E6-sign-even triangle orbit
of $H_{{36}}=\\operatorname{{SRG}}(36,20,10,12)$; the complementary $120$
sign-odd triangles are the Steiner orbit.  The actual Steinberg ranks of the
three canonical even/odd incidence Grams are {rankline}.  {darktex}

For a fixed one of the $45$ packet/octet coordinates, its order-$576$
stabilizer has orbit sizes {orbit} on the $360$ global Schlaefli $K_{{3,3}}$
witnesses.  The intersection classes with zero, one, or two incident charts
have sizes {classes['0']}, {classes['1']}, {classes['2']}.  An equivariant
canonical eight-witness refinement is therefore
\\texttt{{{tf(pkt['equivariantEightWitnessRefinementPossible'])}}} as a union of
stabilizer orbits.  This does not retract the local abstract
$K_{{4,4}}\\to S_4/V_4\\simeq S_3\\to K_{{3,3}}$ quotient.

\\subsection{{The full rational Steinberg multiplicity algebra}}
The primitive diagonal frame $P,R,S$ plus deterministic orbital connectors
produces nine rational matrix units satisfying
\\[
 e_{{ij}}e_{{kl}}=\\delta_{{jk}}e_{{il}},
\\]
so the full multiplicity commutant is explicitly $M_3(\\mathbb Q)$.  The
geometric $K_{{3,3}}$ projector has matrix-unit coordinates
\\begin{{verbatim}}
{qcoords}
\\end{{verbatim}}
and the older $\\{-4,0,+4\\}$ orbital frame is expressed in the same algebra.
These are finite representation multiplicity coordinates, not a physical
flavor or generation matrix.

\\subsection{{Binary $48$: exact MeatAxe comparison, Ext dimension left open}}
Aligned $PSp(4,3)$ generators give
$H_{{1,48}}\\cong\\Omega_{{48}}$: \\texttt{{{tf(iso['H1_equals_Omega48'])}}},
and $A_{{24}}\\cong B_{{24}}$: \\texttt{{{tf(iso['A24_equals_B24'])}}}.
The composition-factor dimensions are $H_1:{cf['H1_48']}$ and
$\\Omega:{cf['Omega48']}$; the $576$-dimensional
$\\operatorname{{Hom}}(B_{{24}},A_{{24}})$ has MeatAxe factor dimensions
{homcf}.  The independent explicit nonsplitting equation proves
$\\operatorname{{Ext}}^1(B_{{24}},A_{{24}})\\neq0$, hence dimension at least
one.  Its exact dimension is not claimed because stock Cohomolo hits its MDIM
ceiling on the full Hom module.

\\paragraph{{Evidence boundary.}}
All statements here are exact finite incidence, root-system, representation,
modular-module, or linear-algebra results.  In particular the $1/3$ overlap,
dark $81$-space, and $3\\times3$ multiplicity coordinates are not by themselves
particle mixing, masses, couplings, fields, spacetime, or dynamics.
'''
    (AN/'PASS20260901_all5_followup_insert.tex').write_text(tex)

    md=f'''# 2026-09-01 all-five follow-up\n\n- 27×45 atlas: PASS.\n- Steinberg 81+81+81 frame: PASS.\n- E6 odd-triangle direct dark hits: `{dark}`; Steinberg ranks `{ {s:er[s]['steinbergActualRank'] for s in ('0','1','2')} }`.\n- Packet stabilizer K3,3 orbit sizes: `{orbit}`; equivariant 8-witness subset possible: `{pkt['equivariantEightWitnessRefinementPossible']}`.\n- Full rational M3 matrix-unit laws: `{m3['allNineRationalMatrixUnitLawsVerified']}`.\n- Binary H1_48 ~= Omega48: `{iso['H1_equals_Omega48']}`; A24 ~= B24: `{iso['A24_equals_B24']}`; Ext^1 dimension remains open but >=1.\n\nBoundary: exact finite mathematics only; no physical mixing/dynamics inferred.\n'''
    (AN/'2026-09-01_all5_followup.md').write_text(md)

    manifest=AN/'W33_CURRENT_FRONTIER_MANIFEST.tex'; t=manifest.read_text()
    line=r'\input{analysis/PASS20260901_all5_followup_insert}%'
    anchor=r'\input{analysis/PASS20260901_five_front_execution_insert}%'
    if line not in t:
        if anchor not in t: raise RuntimeError('manifest anchor missing')
        manifest.write_text(t.replace(anchor,anchor+'\n'+line,1))

    jp=DATA/'w33_current_frontier_manifest_v1.json'; j=json.loads(jp.read_text())
    req='analysis/PASS20260901_all5_followup_insert'
    if req not in j['required_ordered_inputs']: j['required_ordered_inputs'].append(req)
    jp.write_text(json.dumps(j,separators=(',',':'),sort_keys=True)+'\n')

    ip=ROOT/'index.html'; h=ip.read_text(); marker='<!-- 20260901-ALL5-STEINBERG-ATLAS -->'
    if marker not in h:
        h=h.replace('  </nav>','    <a href="#steinberg-all5-followup">Steinberg 81x3 atlas</a>\n  </nav>',1)
        darkhtml=('one canonical E6 relation selects the dark projector'
                  if dark else 'none of the three coarse E6 relations alone selects the dark projector')
        card=f'''  {marker}\n  <section class="card" id="steinberg-all5-followup">\n    <div class="status">PASS · 1 September 2026 · all-five follow-up</div>\n    <h2>One 27×45 atlas and an exact 81⊕81⊕81 Steinberg frame</h2>\n    <p>The same 27×45 incidence is objectwise GQ(2,4), cubic line/tritangent, W33 K<sub>4,4</sub>-factor/octet, and E8 ten-D4 / D4⊕D4 incidence; its rank is 21 over Q and mod 2,3,5,7.</p>\n    <div class="eq">K² = 8K; Q = K/8; rank Q = 81<br>PQP = (1/3)P; RQR = (2/3)R; SQ = QS = 0<br>E<sub>St</sub> = P ⊕ R ⊕ S, ranks 81 + 81 + 81</div>\n    <p>The full Steinberg multiplicity commutant is now explicit as nine rational matrix units for M<sub>3</sub>(Q). The complementary 120 E6/Steiner triangles were tested directly: {darkhtml}. Packet-stabilizer K<sub>3,3</sub> orbit sizes are {orbit}; a canonical equivariant eight-witness subset is {str(pkt['equivariantEightWitnessRefinementPossible']).lower()}.</p>\n    <p>In characteristic two, MeatAxe reports H1<sub>48</sub> ≅ Ω<sub>48</sub> = {str(iso['H1_equals_Omega48']).lower()}. The independently proved nonsplit extension gives Ext¹ ≠ 0, while its exact dimension remains open because the full 576-dimensional Hom exceeds stock Cohomolo's MDIM ceiling.</p>\n    <p class="boundary"><strong>Boundary:</strong> exact finite representation/incidence theory only; no measured mixing angle, mass, coupling, field, or dynamics is inferred.</p>\n  </section>'''
        anchor_html='\n\n  <section class="card">'
        if anchor_html not in h: raise RuntimeError('root index anchor missing')
        ip.write_text(h.replace(anchor_html,'\n\n'+card+anchor_html,1))

    print(json.dumps({'status':'PASS','darkHits':dark,'packetOrbits':orbit,'binaryIso':iso},sort_keys=True))

if __name__=='__main__': main()
