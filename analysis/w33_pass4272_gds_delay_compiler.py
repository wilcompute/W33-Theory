#!/usr/bin/env python3
"""Pure-Python GDSII delay-bank compiler for Pass 4272.

Consumes the frozen Pass-4148 branch schedule and the corrected Pass-4272
geometry contract.  It writes one GDS PATH per 205-um cell (dogleg or straight)
and keepout rectangles for the 16 ten-lane bank tiles.  Curves are tessellated
with the frozen number of line segments per quarter circle.

This is an open/public-rule geometry compiler, not proprietary foundry DRC.
"""
from __future__ import annotations
import argparse, hashlib, json, math, struct
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data/w33_pass4148_hybrid_stack_materialization.json'
CFG=ROOT/'data/w33_pass4272_gds_oriented_delay_compiler.json'

# GDSII record types / data types.
NO=0; I2=2; I4=3; R8=5; ASC=6
def rec(rt,dt,payload=b''):
    if len(payload)%2:payload+=b'\0'
    return struct.pack('>HBB',4+len(payload),rt,dt)+payload
def i2(*x):return struct.pack('>'+'h'*len(x),*x)
def i4(*x):return struct.pack('>'+'i'*len(x),*x)
def asc(s):return s.encode('ascii')
def real8(x):
    if x==0:return b'\0'*8
    sign=0
    if x<0:sign=0x80;x=-x
    e=64
    while x>=1:x/=16;e+=1
    while x<1/16:x*=16;e-=1
    m=int(round(x*(1<<56)))
    if m==(1<<56):m//=16;e+=1
    return bytes([sign|e])+m.to_bytes(7,'big')
def mm_to_db(x):return int(round(x*1_000_000)) # 1 nm DB unit

def arc(cx,cy,r,a0,a1,n):
    return [(cx+r*math.cos(a0+(a1-a0)*k/n),cy+r*math.sin(a0+(a1-a0)*k/n)) for k in range(1,n+1)]

def dogleg(x0,y,r,v,q,n):
    # Start heading east at baseline; four 90-degree bends.
    pts=[(x0,y)]
    pts += arc(x0,y+r,r,-math.pi/2,0,n)
    pts.append((x0+r,y+r+v))
    pts += arc(x0+2*r,y+r+v,r,math.pi,math.pi/2,n)
    pts.append((x0+2*r+q,y+v+2*r))
    pts += arc(x0+2*r+q,y+v+r,r,math.pi/2,0,n)
    pts.append((x0+3*r+q,y+r))
    pts += arc(x0+4*r+q,y+r,r,math.pi,3*math.pi/2,n)
    return pts

def path_element(layer,width_mm,pts):
    xy=[]
    for x,y in pts:xy.extend([mm_to_db(x),mm_to_db(y)])
    return b''.join([
        rec(0x09,NO),rec(0x0D,I2,i2(layer)),rec(0x0E,I2,i2(0)),
        rec(0x0F,I4,i4(mm_to_db(width_mm))),rec(0x10,I4,i4(*xy)),rec(0x11,NO)
    ])

def boundary(layer,x0,y0,x1,y1):
    xy=[mm_to_db(z) for p in [(x0,y0),(x1,y0),(x1,y1),(x0,y1),(x0,y0)] for z in p]
    return b''.join([rec(0x08,NO),rec(0x0D,I2,i2(layer)),rec(0x0E,I2,i2(0)),rec(0x10,I4,i4(*xy)),rec(0x11,NO)])

def begin_lib():
    date=(2026,8,8,2,0,0)*2
    return b''.join([
        rec(0x00,I2,i2(600)),rec(0x01,I2,i2(*date)),rec(0x02,ASC,asc('W33_DELAY')),
        rec(0x03,R8,real8(0.001)+real8(1e-9)),
        rec(0x05,I2,i2(*date)),rec(0x06,ASC,asc('DELAY_BANK'))
    ])
def end_lib():return rec(0x07,NO)+rec(0x04,NO)

def validate_stream(buf):
    i=0;records=0;last=None
    while i<len(buf):
        if i+4>len(buf):raise ValueError('truncated GDS record')
        n,rt,dt=struct.unpack('>HBB',buf[i:i+4])
        if n<4 or n%2 or i+n>len(buf):raise ValueError('invalid GDS record length')
        last=rt;i+=n;records+=1
    if i!=len(buf) or last!=0x04:raise ValueError('stream does not end at ENDLIB')
    return records

def compile_layout(src,cfg):
    r=cfg['corrected_cell']['bend_radius_mm'];v=cfg['corrected_cell']['vertical_straight_leg_mm']
    q=cfg['corrected_cell']['top_straight_mm'];xp=cfg['corrected_cell']['x_pitch_mm']
    pitch=cfg['banking']['lane_pitch_mm'];tw=cfg['banking']['tile_width_mm'];th=cfg['banking']['tile_height_mm']
    gx=cfg['banking']['tile_gap_x_mm'];gy=cfg['banking']['tile_gap_y_mm'];keep=cfg['banking']['perimeter_keepout_mm']
    width=cfg['corrected_cell']['waveguide_width_um']/1000
    nseg=cfg['corrected_cell']['arc_segments_per_quarter_for_gds']
    layers=cfg['open_drc_contract']['layers']
    buf=bytearray(begin_lib());routes=[];doglegs=0;straight=0;maxpts=0
    for b,branch in enumerate(src['branch_layers']):
        seen=set()
        for ell,layer in enumerate(branch):
            delay=8-ell
            for point,line in layer:
                seen.add(point)
                bank=point//10;lane=point%10;tile=b*4+bank;col=tile%6;row=tile//6
                tx=keep+col*(tw+gx);ty=keep+row*(th+gy);y=ty+(lane+0.5)*pitch
                for j in range(8):
                    x0=tx+j*xp
                    if j<delay:
                        pts=dogleg(x0,y,r,v,q,nseg);doglegs+=1
                    else:
                        pts=[(x0,y),(x0+xp,y)];straight+=1
                    maxpts=max(maxpts,len(pts));buf.extend(path_element(layers['waveguide_core'],width,pts))
                routes.append({'branch':b,'point':point,'line':line,'layer':ell,'delay_slots':delay,'tile':tile,'bank':bank,'lane':lane})
        assert seen==set(range(40))
    # Keepout rectangles are placed on a dedicated non-fabrication layer.
    for tile in range(16):
        col=tile%6;row=tile//6;tx=keep+col*(tw+gx);ty=keep+row*(th+gy)
        buf.extend(boundary(layers['keepout'],tx,ty,tx+tw,ty+th))
    buf.extend(end_lib())
    assert len(routes)==160 and doglegs==919 and straight==361 and maxpts<200
    return bytes(buf),routes,{'doglegs':doglegs,'straight_cells':straight,'max_path_vertices_per_cell':maxpts,'gds_records':validate_stream(buf)}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='build/w33_delay_bank_4272.gds');ap.add_argument('--summary',default='build/w33_delay_bank_4272_summary.json');args=ap.parse_args()
    src=json.loads(SRC.read_text());cfg=json.loads(CFG.read_text())
    assert src['semantic_sha256']==cfg['source_schedule_sha256']
    assert cfg['corrected_cell']['x_pitch_mm']>=4*cfg['corrected_cell']['bend_radius_mm']
    gds,routes,stats=compile_layout(src,cfg)
    out=ROOT/args.out;summary=ROOT/args.summary;out.parent.mkdir(parents=True,exist_ok=True);summary.parent.mkdir(parents=True,exist_ok=True)
    out.write_bytes(gds)
    payload={
      'schema':'w33.pass4272.gds_compile_result.v1',
      'gds_sha256':hashlib.sha256(gds).hexdigest(),
      'gds_bytes':len(gds),
      'route_count':len(routes),
      'delay_units':sum(r['delay_slots'] for r in routes),
      'stats':stats,
      'bbox_mm':cfg['banking']['overall_bbox_mm'],
      'open_drc_checks':cfg['open_drc_contract']['checks_pass'],
      'boundary':cfg['boundary'],
    }
    assert payload['delay_units']==919 and all(payload['open_drc_checks'].values())
    summary.write_text(json.dumps(payload,sort_keys=True,indent=2)+'\n')
    print(json.dumps(payload,sort_keys=True))
if __name__=='__main__':main()
