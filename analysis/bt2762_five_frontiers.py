#!/usr/bin/env python3
"""Passes 2762-2766 exact release driver."""
import sys
import gzip
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from bt2762_core import *
from bt2762_group import *
from bt2762_isa import *
def main():
    checks = {}
    group = closure(GENERATORS)
    checks['sp43_order_51840'] = len(group) == 51840
    cx_fp = mm(mm(TRANSPOSE, CX_PF), TRANSPOSE)
    f_synth = mm(inv(F_F), F_P)
    checks['transpose_involution'] = mm(TRANSPOSE, TRANSPOSE) == I
    checks['transpose_multiplier_minus_one'] = mm(mm(tr(TRANSPOSE), J), TRANSPOSE) == tuple((tuple()-x % 3 for x in row)) for row in J))
    checks['transpose_outer'] = TRANSPOSE not in group
    checks['transpose_normalizes_generators'] = all((mm(mm(TRANSPOSE, g), TRANSPOSE) in group for g in GENERATORS))
    checks['transpose_reverses_cx'] = cx_fp == ((1, 0, 1, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 2, 0, 1))
    checks['local_fourier_synthesizes_reverse'] = mm(mm(f_synth, CX_PF), inv(f_synth)) == cx_fp
    geometry = build_geometry()
    points, _, lines, _, flags, _, edges, _, apartments, _ = geometry
    checks['w33_counts'] = [len(points), len(lines), len(flags), len(edges), len(apartments)] == [40, 40, 160, 240, 1620]
    classes = conjugacy_classes(group)
    checks['conjugacy_class_count_34'] = len(classes) == 34
    raw_rows = []
    for old_id, (rep, cls) in enumerate(classes):
        profiles = [cycle_profile(p) for p in action(rep, geometry)]
        raw_rows.append({'old_id': old_id, 'representative': rep, 'size': len(cls), 'centralizer_order': 51840 // len(cls), 'order': order(rep), 'trace_mod3': sum((rep[i][i] for i in range(4))) % 3, 'rank_g_minus_i': rank(msub(rep, I)), 'profiles': profiles})
    raw_rows.sort(key=lambda r: (r['order'], r['size'], r['profiles'], r['representative']))
    for i, row in enumerate(raw_rows, 1):
        row['class_id'] = i
    old_to_new = {r['old_id']: r['class_id'] for r in raw_rows}
    matrix_old = {g: old_id for old_id, (_, cls) in enumerate(classes) for g in cls}
    matrix_class = {g: old_to_new[old] for g, old in matrix_old.items()}
    projective_decoder = defaultdict(list)
    atlas_rows = []
    for row in raw_rows:
        g = row['representative']
        signature = tuple(row['profiles'])
        projective_decoder[str(signature)].append(row['class_id'])
        atlas_rows.append({'class_id': row['class_id'], 'representative': [list(x) for x in g], 'representative_sha256': hashlib.sha256(repr(g).encode()).hexdigest(), 'order': row['order'], 'size': row['size'], 'centralizer_order': row['centralizer_order'], 'trace_mod3': row['trace_mod3'], 'rank_g_minus_i': row['rank_g_minus_i'], 'point_cycles': profile_json(row['profiles'][0]), 'line_cycles': profile_json(row['profiles'][1]), 'flag_cycles': profile_json(row['profiles'][2]), 'edge_cycles': profile_json(row['profiles'][3]), 'apartment_cycles': profile_json(row['profiles'][4]), 'inverse_class': matrix_class[inv(g)], 'central_lift_class': matrix_class[mm(NEG_I, g)], 'transpose_class': matrix_class[mm(mm(TRANSPOSE, g), TRANSPOSE)]})
    checks['atlas_partition'] = sum((r['size'] for r in atlas_rows)) == 51840
    checks['projective_signature_count_15'] = len(projective_decoder) == 15
    checks['cx_and_reverse_same_class'] = matrix_class[CX_PF] == matrix_class[cx_fp]
    transpose_swaps = sorted(((r['class_id'], r['transpose_class']) for r in atlas_rows if r['class_id'] != r['transpose_class']))
    checks['transpose_swaps_20_classes'] = len(transpose_swaps) == 20
    centralizer = {g for g in group if mm(g, CX_PF) == mm(CX_PF, g)}
    center = {g for g in centralizer if all((mm(g, h) == mm(h, g) for h in centralizer))}
    derived = closure({commutator(a, b) for a in centralizer for b in centralizer})
    z6, z3 = find_center_generators(center)
    s3a, s3b, s3 = find_s3_complement(centralizer, center)
    checks['cx_centralizer_order_108'] = len(centralizer) == 108
    checks['centralizer_center_c6xc3'] = len(center) == 18 and len(closure((z6, z3))) == 18
    checks['centralizer_derived_c3'] = len(derived) == 3
    checks['centralizer_s3_complement'] = len(s3) == 6 and s3 & center == {I} and (len({mm(z, h) for z in center for h in s3}) == 108)
    checks['centralizer_order_census'] = Counter((order(g) for g in centralizer)) == {1: 1, 2: 7, 3: 26, 6: 74}
    pp, ll, _, _, _ = action(CX_PF, geometry)
    fixed_points = [i for i, j in enumerate(pp) if i == j]
    fixed_lines = [i for i, j in enumerate(ll) if i == j]
    axis = next((l for l in fixed_lines if set(fixed_points) == {geometry[1][p] for p in lines[l]}))
    external_lines = set(fixed_lines) - {axis}
    s3_line_actions = {h: action(h, geometry)[1] for h in s3}
    s3_external_perms = {tuple(sorted(((x, lh[x]) for x in external_lines))) for lh in s3_line_actions.values()}
    checks['s3_regular_on_six_line_fringe'] = len(s3_external_perms) == 6 and all((sum((1 for lh in s3_line_actions.values() if lh[x] == x)) == 1 for x in external_lines))
    line_point_ids = [set((geometry[1][p] for p in line)) for line in lines]
    axis_point_ids = line_point_ids[axis]
    attachments = {l: tuple(sorted(line_point_ids[l] & axis_point_ids)) for l in external_lines}
    pencils = defaultdict(list)
    for l, attached in attachments.items():
        pencils[attached].append(l)
    pencil_sets = sorted((set(v) for v in pencils.values()), key=lambda x: sorted(x))
    z3_line_action = action(z3, geometry)[1]
    checks['fringe_is_two_three_line_pencils'] = sorted((len(p) for p in pencil_sets)) == [3, 3] and all((len(k) == 1 for k in pencils))
    checks['central_c3_rotates_both_pencils'] = all(({z3_line_action[l] for l in pencil} == pencil and all((z3_line_action[l] != l for l in pencil)) for pencil in pencil_sets))
    sum_perm = tuple((3 * f + (t + f) % 3 for f in range(3) for t in range(3)))
    checks['physical_compiler_is_permutation'] = sorted(sum_perm) == list(range(9))
    checks['physical_compiler_order_three'] = all((sum_perm[sum_perm[sum_perm[i]]] == i for i in range(9)))
    checks['physical_compiler_matches_cx_basis'] = all((sum_perm[3 * f + t] == 3 * f + (t + f) % 3 for f in range(3) for t in range(3)))
    physical_compiler = {'logical_encoding': 'control=past mapped to frequency qutrit; target=future mapped to time qutrit', 'basis_index': '3*frequency + time', 'permutation': list(sum_perm), 'frequency_controlled_delays_bins': [0, 1, 2], 'qutrit_experimental_reference': {'paper': 'Imany et al., npj Quantum Information 5, 59 (2019)', 'doi': '10.1038/s41534-019-0173-8', 'time_bins': '3 ns wide, 6 ns center spacing', 'frequency_spacing': '380 GHz in the qutrit experiment', 'dispersion': '-2 ns/nm chirped fiber Bragg grating', 'wraparound_delay': '3 time bins = 18 ns', 'sum_computational_fidelity': '0.92 +/- 0.01', 'bell_output': '(|00>+|11>+|22>)/sqrt(3)', 'certified_eof': '>=1.19 +/- 0.12 ebits'}, 'boundary': "The published experiment certifies the physical gate principle and a qutrit implementation; it does not certify the Holonet's full fault-tolerant magic-injection stack."}
    checks['m36_grade_rom_8_24_4'] = Counter(MAGIC_GRADE_MAP) == {0: 8, 1: 24, 2: 4}
    opcodes = {'F_p': 0, 'F_f': 1, 'S_p': 2, 'S_f': 3, 'CX': 4, 'sigma5_Z': 5, 'D12_mirror': 6, 'M36_magic': 7}
    base_state = {'frame': (0, 0, 0, 0), 'mirror': (0, 0), 'magic_pending': False, 'magic_ray': 0, 'magic_consumed': 0, 'fault': False, 'retired': False}
    isa_ok = True
    for frame in itertools.product(range(3), repeat=4):
        st = dict(base_state)
        st['frame'] = frame
        for opcode in range(6):
            operands = (0, 1) if opcode in (4, 5) else (None,)
            for operand in operands:
                out = isa_step(st, opcode, operand)
                isa_ok &= all((0 <= x < 3 for x in out['frame']))
                isa_ok &= not out['fault'] and out['retired']
    d12 = [(r, s) for r in range(6) for s in range(2)]
    isa_ok &= len({d12_mul(a, b) for a in d12 for b in d12}) == 12
    isa_ok &= all((d12_mul(d12_mul(a, b), c) == d12_mul(a, d12_mul(b, c)) for a in d12 for b in d12 for c in d12))
    req = isa_step(base_state, 7, 35)
    ack = isa_step(req, 0, magic_ack=True)
    bad = isa_step(base_state, 7, 36)
    isa_ok &= req['magic_pending'] and (not req['retired'])
    isa_ok &= not ack['magic_pending'] and ack['magic_consumed'] == 1 and ack['retired']
    isa_ok &= bad['fault']
    checks['eight_opcode_isa_contract'] = isa_ok and len(opcodes) == 8
    program = [(0, None), (3, None), (4, 0), (5, 1), (6, (2, 1)), (7, 17)]
    st = dict(base_state)
    trace_rows = []
    for opcode, operand in program:
        st = isa_step(st, opcode, operand)
        trace_rows.append({'opcode': opcode, 'operand': operand, 'state': dict(st)})
        if opcode == 7:
            st = isa_step(st, 0, magic_ack=True)
            trace_rows.append({'event': 'magic_ack', 'state': dict(st)})
    checks['end_to_end_program_retires'] = st['magic_consumed'] == 1 and (not st['fault'])
    if not all(checks.values()):
        failed = [k for k, v in checks.items() if not v]
        raise AssertionError(f'failed checks: {failed}')
    out_root = Path(__file__).resolve().parents[1]
    atlas = {'schema': 'w33.sp43.geometric_gate_class_atlas.v1', 'group_order': len(group), 'class_count': len(atlas_rows), 'carrier_sizes': {'points': len(points), 'lines': len(lines), 'flags': len(flags), 'edges': len(edges), 'apartments': len(apartments)}, 'projective_signature_count': len(projective_decoder), 'projective_decoder': dict(projective_decoder), 'rows': atlas_rows}
    atlas_path = out_root / 'data' / 'PART_BT2764_SP43_GEOMETRIC_GATE_CLASS_ATLAS.json.gz'
    atlas_bytes = (json.dumps(atlas, indent=2, sort_keys=True) + '\n').encode('utf-8')
    atlas_path.write_bytes(gzip.compress(atlas_bytes, compresslevel=9, mtime=0))
    cert = {'schema': 'w33.bt2762_2766.five_frontiers.v1', 'checks': checks, 'transpose_direction_reversal': {'transpose': TRANSPOSE, 'cx_p_to_f': CX_PF, 'cx_f_to_p': cx_fp, 'local_fourier_conjugator': f_synth, 'identity': 'CX_f->p=(F_p F_f^-1) CX_p->f (F_p^-1 F_f)', 'cx_class': matrix_class[CX_PF], 'transpose_class_swaps': transpose_swaps}, 'centralizer': {'order': len(centralizer), 'structure': 'C6 x C3 x S3', 'center_order': len(center), 'derived_order': len(derived), 'order_census': dict(sorted(Counter((order(g) for g in centralizer)).items())), 'C6_generator': z6, 'C3_generator': z3, 'S3_order3_generator': s3a, 'S3_order2_generator': s3b, 'fixed_axis_line': axis, 'fixed_external_lines': sorted(external_lines), 'pencils_by_axis_point': {str(k[0]): sorted(v) for k, v in sorted(pencils.items())}, 'fringe_action': 'S3 regular on six external fixed lines; central C3 rotates both three-line pencils'}, 'atlas': {'path': str(atlas_path.relative_to(out_root)), 'sha256': hashlib.sha256(atlas_path.read_bytes()).hexdigest(), 'class_count': 34, 'projective_signature_count': 15}, 'physical_sum_compiler': physical_compiler, 'isa': {'opcodes': opcodes, 'cx_direction_operand': {'0': 'p->f', '1': 'f->p'}, 'z_register_operand': {'0': 'past', '1': 'future'}, 'mirror_operand': '(rotation mod 6, reflection bit), left multiplication in D12', 'magic_operand': 'ray index 0..35; retires only on external magic_ack', 'magic_grade_encoding': {'0': 'deep', '1': 'mid', '2': 'shallow'}, 'magic_grade_map_bt822_order': list(MAGIC_GRADE_MAP), 'program_trace': trace_rows}}
    cert_path = out_root / 'data' / 'PART_BT2762_BT2766_FIVE_FRONTIERS_results.json'
    cert_path.write_text(json.dumps(cert, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print(f'PASS {sum((bool(v) for v in checks.values()))}/{len(checks)} checks')
    print(f'group={len(group)} classes={len(atlas_rows)} apartments={len(apartments)}')
    print(f'centralizer={len(centralizer)} structure=C6xC3xS3')
    print(f"atlas_sha256={cert['atlas']['sha256']}")
    print(f'wrote {cert_path}')
    print(f'wrote {atlas_path}')
if __name__ == '__main__':
    main()
