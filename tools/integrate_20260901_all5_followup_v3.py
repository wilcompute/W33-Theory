#!/usr/bin/env python3
"""Brace-safe certificate-driven publication integrator for 2026-09-01 all-five pass."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/'data'; AN=ROOT/'analysis'

def load(name):
    p=DATA/name
    if not p.exists(): raise FileNotFoundError(p)
    x=json.loads(p.read_text())
    if x.get('status')!='PASS': raise RuntimeError('%s: %s'%(name,x.get('status')))
    return x

def main():
    load('PART_W33_20260901_GQ24_K44_E8_ATLAS.json')
    load('PART_W33_20260901_K33_STEINBERG_PRIMITIVE.json')
    e6=load('PART_W33_20260901_E6_ODD_TRIANGLE_STEINBERG.json')
    pkt=load('PART_W33_20260901_PACKET_K33_GLOBALIZATION.json')
    m3=load('PART_W33_20260901_STEINBERG_M3_MATRIX_UNITS.json')
    b48=load('PART_W33_20260901_BINARY48_MEATAXE_ONLY.json')
    dark=e6['darkProjectorDirectHits']; er=e6['relationsByIntersectionSize']
    orbit=pkt['packetStabilizer']['orbitSizes']; cls=pkt['packet0IntersectionClassSizes']
    iso=b48['moduleIsomorphism']; cf=b48['compositionFactorDimensions']
    homcf=b48['homBA']['compositionFactorDimensions']; q=m3['K33PrimitiveQCoordinates']
    tex=r'''%% Generated from frozen PASS certificates.
\subsection{One $27\times45$ atlas and the $81\oplus81\oplus81$ Steinberg frame}
The same $27\times45$ matrix is, objectwise, the incidence matrix for
$GQ(2,4)$ points/lines, cubic lines/tritangents, W33 $K_{4,4}$
factorizations/octets, and $E_8$ ten-$D_4$ charts/$D_4\oplus D_4$ packets.
It has row weight $5$, column weight $3$, and rank $21$ over
$\mathbb Q,\mathbb F_2,\mathbb F_3,\mathbb F_5,\mathbb F_7$, with
\[
 II^T=5I_{27}+A_{GQ(2,4)},\qquad I^TI=3I_{45}+A_{GQ(4,2)}.
\]
On the three-copy Steinberg block the Schlaefli $K_{3,3}$ Gram satisfies
$K^2=8K$.  Thus $Q=K/8$ is primitive of rank $81$.  With $P$ the intrinsic
$20_{\rm chart}\otimes15_{\rm W33}$ copy,
\[
 PQP=\tfrac13P,\qquad QPQ=\tfrac13Q.
\]
Writing $R=\tfrac32(E-P)Q(E-P)$ and $S=(E-P)-R$ gives
\[
 E=P\oplus R\oplus S,\quad \operatorname{rank}(P,R,S)=(81,81,81),
 \quad RQR=\tfrac23R,\quad SQ=QS=0.
\]

\subsection{E6 odd-triangle and packet/global-$K_{3,3}$ no-go audits}
The $1080$ obstruction objects are exactly the E6-sign-even triangles of
$H_{36}=\operatorname{SRG}(36,20,10,12)$; the complementary $120$ sign-odd
triangles are the Steiner orbit.  For intersection sizes $0,1,2$, the three
canonical even/odd incidence Grams have Steinberg actual ranks respectively
%s, %s, %s.  Direct dark-projector hits: \texttt{%s}.

For a fixed packet, its order-$576$ stabilizer has orbit sizes %s on the
$360$ global Schlaefli $K_{3,3}$ witnesses.  The classes meeting its three
incident charts in $0,1,2$ vertices have sizes %s,%s,%s.  A canonical
equivariant eight-witness refinement is \texttt{%s}; hence the local abstract
$K_{4,4}\to S_4/V_4\simeq S_3\to K_{3,3}$ quotient is not an eight-element
subfamily of the distinct global witness shell.

\subsection{Explicit $M_3(\mathbb Q)$ multiplicity algebra}
The primitive frame $P,R,S$ plus deterministic orbital connectors yields all
nine rational matrix units $e_{ij}$ and verifies
\[
 e_{ij}e_{kl}=\delta_{jk}e_{il}.
\]
Thus the complete Steinberg multiplicity commutant is explicit as
$M_3(\mathbb Q)$.  The geometric $K_{3,3}$ projector has matrix-unit
coordinates \texttt{%s}.  The older $\{-4,0,+4\}$ orbital spectral frame is
expressed in the same coordinates.  These are representation multiplicity
coordinates, not a physical flavor/generation matrix.

\subsection{Binary $48$: MeatAxe comparison without guessing Ext}
MeatAxe gives $H_{1,48}\cong\Omega_{48}$ = \texttt{%s} and
$A_{24}\cong B_{24}$ = \texttt{%s}.  Their factor-dimension multisets are
$H_1:%s$ and $\Omega:%s$; the $576$-dimensional
$\operatorname{Hom}(B_{24},A_{24})$ has factor dimensions %s.  The independent
splitting-equation certificate proves $\operatorname{Ext}^1(B_{24},A_{24})\ne0$,
so its dimension is at least one; the exact value remains open because stock
Cohomolo hits its MDIM ceiling on the full Hom module.

\paragraph{Boundary.}
These are exact finite incidence, root-system, representation, modular-module,
and linear-algebra statements.  The $1/3$ overlap, dark $81$-space, and
$3\times3$ coordinates are not by themselves particle mixing, masses,
couplings, fields, spacetime, or dynamics.
'''%(er['0']['steinbergActualRank'],er['1']['steinbergActualRank'],er['2']['steinbergActualRank'],dark,
      orbit,cls['0'],cls['1'],cls['2'],pkt['equivariantEightWitnessRefinementPossible'],q,
      iso['H1_equals_Omega48'],iso['A24_equals_B24'],cf['H1_48'],cf['Omega48'],homcf)
    (AN/'PASS20260901_all5_followup_insert.tex').write_text(tex)
    md='''# 2026-09-01 all-five follow-up\n\n- Unified 27x45 GQ/cubic/W33/E8 atlas: PASS.\n- Exact Steinberg 81+81+81 frame: PASS.\n- E6 odd-triangle Steinberg ranks: %s; direct dark hits: %s.\n- Packet/global K3,3 stabilizer orbits: %s; equivariant 8-subset: %s.\n- Full rational M3 matrix units: %s.\n- Binary H1_48 ~= Omega48: %s; A24 ~= B24: %s; Ext dimension open but >=1.\n\nBoundary: exact finite mathematics only.\n'''%([er[s]['steinbergActualRank'] for s in ('0','1','2')],dark,orbit,pkt['equivariantEightWitnessRefinementPossible'],m3['allNineRationalMatrixUnitLawsVerified'],iso['H1_equals_Omega48'],iso['A24_equals_B24'])
    (AN/'2026-09-01_all5_followup.md').write_text(md)

    manifest=AN/'W33_CURRENT_FRONTIER_MANIFEST.tex'; t=manifest.read_text()
    line='\\input{analysis/PASS20260901_all5_followup_insert}%'
    anchor='\\input{analysis/PASS20260901_five_front_execution_insert}%'
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
        card='''  %s
  <section class="card" id="steinberg-all5-followup">
    <div class="status">PASS · 1 September 2026 · all-five follow-up</div>
    <h2>One 27×45 atlas and an exact 81⊕81⊕81 Steinberg frame</h2>
    <p>The same 27×45 incidence is objectwise GQ(2,4), cubic line/tritangent, W33 K<sub>4,4</sub>-factor/octet, and E8 ten-D4 / D4⊕D4 incidence; its rank is 21 over Q and mod 2,3,5,7.</p>
    <div class="eq">K² = 8K; Q = K/8; rank Q = 81<br>PQP = (1/3)P; RQR = (2/3)R; SQ = QS = 0<br>E<sub>St</sub> = P ⊕ R ⊕ S, ranks 81 + 81 + 81</div>
    <p>Full rational M<sub>3</sub>(Q) matrix units are explicit. The three coarse E6 even/odd relations have Steinberg ranks %s. Packet-stabilizer K<sub>3,3</sub> orbit sizes are %s, so an equivariant eight-witness refinement is %s.</p>
    <p>Binary H1<sub>48</sub> ≅ Ω<sub>48</sub> is %s. The nonsplit extension proves Ext¹ ≠ 0; its exact dimension remains open.</p>
    <p class="boundary"><strong>Boundary:</strong> exact finite representation/incidence theory only; no measured mixing angle, mass, coupling, field, or dynamics is inferred.</p>
  </section>'''%(marker,[er[s]['steinbergActualRank'] for s in ('0','1','2')],orbit,str(pkt['equivariantEightWitnessRefinementPossible']).lower(),str(iso['H1_equals_Omega48']).lower())
        anchor_html='\n\n  <section class="card">'
        if anchor_html not in h: raise RuntimeError('root index anchor missing')
        ip.write_text(h.replace(anchor_html,'\n\n'+card+anchor_html,1))
    print(json.dumps({'status':'PASS','darkHits':dark,'packetOrbits':orbit,'binaryIso':iso},sort_keys=True))

if __name__=='__main__': main()
