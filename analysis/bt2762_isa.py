#!/usr/bin/env python3
"""Pure D12 and eight-opcode ISA semantics for Passes 2762-2766."""
from bt2762_core import *

def d12_mul(a, b):
    """Multiply r^a0 m^a1 by r^b0 m^b1 in D12 (|D12|=12)."""
    ar, am = a
    br, bm = b
    return ((ar + (-br if am else br)) % 6, am ^ bm)

def isa_step(state, opcode, operand=None, magic_ack=False):
    """Pure reference transition for the eight-opcode digital contract."""
    s = dict(state)
    xp, zp, xf, zf = s['frame']
    if s['magic_pending']:
        if magic_ack:
            s['magic_pending'] = False
            s['magic_consumed'] += 1
            s['retired'] = True
        else:
            s['retired'] = False
        return s
    s['retired'] = True
    if opcode == 0:
        xp, zp = (-zp % 3, xp)
    elif opcode == 1:
        xf, zf = (-zf % 3, xf)
    elif opcode == 2:
        zp = (zp + xp) % 3
    elif opcode == 3:
        zf = (zf + xf) % 3
    elif opcode == 4:
        direction = int(operand or 0)
        if direction == 0:
            zp, xf = ((zp - zf) % 3, (xf + xp) % 3)
        else:
            xp, zf = ((xp + xf) % 3, (zf - zp) % 3)
    elif opcode == 5:
        if int(operand or 0) == 0:
            zp = (zp + 1) % 3
        else:
            zf = (zf + 1) % 3
    elif opcode == 6:
        rot, refl = operand
        s['mirror'] = d12_mul((int(rot) % 6, int(bool(refl))), tuple(s['mirror']))
    elif opcode == 7:
        ray = int(operand)
        if not 0 <= ray < 36:
            s['fault'] = True
        else:
            s['magic_pending'] = True
            s['magic_ray'] = ray
            s['retired'] = False
    else:
        s['fault'] = True
    s['frame'] = (xp, zp, xf, zf)
    return s
