"""Five extensions of W33_CARRY_TIMING_INFORMATION.md; no device calibration.

Finite probability masses use Fraction; entropy uses floating logarithms.
Reversible gate synthesis is structural, not a truth-table oracle.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import product
import json
from math import log2, log, isclose
from pathlib import Path

from w33_carry_timing_information import trace, trailing_ones
import w33_counter_zipper_microcode as micro
from w33_authenticated_counter_machine import BitStore, genesis
from w33_finite_control_unbounded_guest_hypervisor import FibreProductAddress
from w33_typed_universal_microvm import Instruction, Program


def entropy(masses):
    return -sum(float(p) * log2(float(p)) for p in masses if p)


def carry(x, radix):
    k = 0
    while x % radix == radix - 1:
        k += 1
        x //= radix
    return k


def digit_sum(x, radix):
    s = 0
    while x:
        x, d = divmod(x, radix)
        s += d
    return s


def radix_increment(x, radix):
    """Executable abstract digit zipper: scan, pivot, unwind, close, commit.

    Digits are classical radix symbols, not coherent qutrit hardware.
    """
    cursor, stack, result, ticks = x, [], [], 0
    while cursor % radix == radix - 1:
        cursor //= radix
        stack.append(0)
        ticks += 1
    cursor, pivot = divmod(cursor, radix)
    result = [pivot + 1]
    ticks += 1
    while stack:
        result.insert(0, stack.pop())
        ticks += 1
    value = sum(d * radix**j for j, d in enumerate(result)) + cursor * radix**len(result)
    return value, ticks + 2


def radix_witness():
    rows = []
    intervals = 0
    for b in (2, 3, 4, 5):
        for a in range(64):
            value, total = a, 0
            for length in range(1, 25):
                value, ticks = radix_increment(value, b)
                total += ticks
                assert value == a + length
                expected = 3*length + F(2, b-1)*(length+digit_sum(a,b)-digit_sum(value,b))
                assert total == expected
                intervals += 1
        for n in range(1, 5):
            for m in range(n):
                N, L, d = b**n, b**m, n-m
                counts, sums, forward, reverse = Counter(), Counter(), {}, {}
                for x in range(N):
                    z = tuple(2*carry(x+j,b)+3 for j in range(L))
                    sig = (x % L, carry(x//L,b))
                    assert forward.setdefault(sig,z) == z
                    assert reverse.setdefault(z,sig) == sig
                    counts[z] += 1
                    sums[sum(z)] += 1
                h = (1-b**(-d))*(b/(b-1)*log2(b)-log2(b-1))
                observed = entropy(F(c,N) for c in counts.values())
                assert isclose(observed,m*log2(b)+h,abs_tol=1e-12)
                assert isclose(entropy(F(c,N) for c in sums.values()),h,abs_tol=1e-12)
                rows.append(dict(radix=b,n=n,m=m,information_bits=observed,
                                 residual_input_entropy_bits=n*log2(b)-observed))
    return dict(intervals=intervals, partitions=rows, scope='Abstract classical radix zipper; binary authenticated backend unchanged')


def noisy_channel(n=3, m=1, layers=1):
    """Independent additive timing jitter: each layer is {-2:1/4,0:1/2,2:1/4} ticks.

    Unclipped signed measurement error, not execution time or calibrated noise.
    """
    noise = {0:F(1)}
    for _ in range(layers):
        nxt = defaultdict(F)
        for a,p in noise.items():
            for b,q in ((-2,F(1,4)),(0,F(1,2)),(2,F(1,4))):
                nxt[a+b] += p*q
        noise = dict(nxt)
    N,L = 1<<n,1<<m
    output, conditional = defaultdict(F), []
    for x in range(N):
        dist = defaultdict(F)
        z = trace(x,L)
        for errors in product(noise,repeat=L):
            p = F(1)
            for e in errors:
                p *= noise[e]
            dist[tuple(t+e for t,e in zip(z,errors))] += p
        assert sum(dist.values()) == 1
        conditional.append(entropy(dist.values()))
        for y,p in dist.items():
            output[y] += p/N
    assert sum(output.values()) == 1
    conditional_h = sum(conditional)/N
    assert isclose(conditional_h, L*entropy(noise.values()), abs_tol=1e-12)
    return dict(information_bits=entropy(output.values())-conditional_h,
                conditional_record_entropy_bits=conditional_h,
                total_record_entropy_bits=entropy(output.values()))


def noisy_witness():
    rows = []
    for m in (0,1,2):
        channels = [noisy_channel(3,m,layers) for layers in range(3)]
        values = [c['information_bits'] for c in channels]
        assert all(a+1e-12 >= b >= -1e-12 for a,b in zip(values,values[1:]))
        rows.append(dict(n=3,m=m,information_bits_by_jitter_layers=values, channels=channels))
    return dict(rows=rows, probabilities='exact rational', entropy='floating log2',
                noise='independent additive tick jitter {-2:1/4,0:1/2,2:1/4}, composed 0,1,2 times')


def valuation(x):
    assert x > 0
    return (x & -x).bit_length()-1


def backend_step(x, op):
    p = Program((Instruction(op,0,0,0 if op=='DECJZ' else None),),name='mixed-cost')
    mem = BitStore()
    state = genesis(p,mem,(x,0),session='mixed-cost')
    c = micro.start(p,state,FibreProductAddress(7,2,5))
    ticks = writes = 0
    while c.phase != 'DONE':
        receipt = micro.prove_tick(p,c,mem)
        c,nodes = micro.verify_tick(p,c,receipt)
        for node in nodes:
            mem.put(node)
        ticks += 1
        writes += len(nodes)
    return mem.decode(micro.committed(p,c).roots[0]),ticks,writes


def mixed_witness():
    cycles = []
    for k in range(17):
        x = (1<<k)-1
        y,ti,wi = backend_step(x,'INC')
        z,td,wd = backend_step(y,'DECJZ')
        assert z == x and ti+td == 4*k+6 and wi+wd == 4*k+1
        cycles.append(dict(k=k,ticks=ti+td,writes=wi+wd))
    paths = 0
    for start in range(8):
        for ops in product((-1,1),repeat=5):
            x,total,predicted = start,0,0
            for op in ops:
                y,t,_ = backend_step(x,'INC' if op==1 else 'DECJZ')
                if x==0 and op==-1:
                    predicted += 1
                else:
                    predicted += 3+2*valuation(max(x,y))
                total += t
                x = y
            assert total == predicted
            paths += 1
    return dict(cycles=cycles, mixed_paths=paths,
                law='T=zero_DEC_count+3*nonzero_moves+2*sum_edge_crossings(v2(upper_endpoint))',
                obstruction='A closed k-boundary cycle costs 4k+6; no state potential gives a uniform constant amortized cost for both operations')


def synthesize(n,m):
    """NOT/CNOT/Toffoli circuit, wires Y | record(r,k) | clean prefix ancillas.

    d=n-m, Y has n+1 bits, k uses bit_length(d) bits.
    Total oracle extends to invalid Y by capped trailing-zero count.
    """
    if not 0 <= m < n:
        raise ValueError('need 0 <= m < n')
    d=n-m
    r0=n+1
    a0=r0+m+d.bit_length()
    compute=[]
    # Temporarily complement the high d input bits, then form prefix ANDs.
    for j in range(d):
        compute.append(((),m+j))
    compute.append(((m,),a0))
    for j in range(1,d):
        compute.append(((a0+j-1,m+j),a0+j))
    copy=[((j,),r0+j) for j in range(m)]
    for j in range(1,d+1):
        for bit in range(valuation(j)+1):
            copy.append(((a0+j-1,),r0+m+bit))
    gates=compute+copy+list(reversed(compute))
    return gates, a0, d


def apply_gates(state,gates):
    for controls,target in gates:
        if all((state>>c)&1 for c in controls):
            state ^= 1<<target
    return state


def circuit_witness():
    rows=[]
    for n in range(1,8):
        for m in range(n):
            gates,a0,d=synthesize(n,m)
            record_bits=m+d.bit_length()
            for y in range(1<<(n+1)):
                high=(y>>m)&((1<<d)-1)
                k=valuation(high) if high else d
                oracle=(y% (1<<m)) | (k<<m)
                for r in range(1<<record_bits):
                    state=y|(r<<(n+1))
                    result=apply_gates(state,gates)
                    assert result == y|((r^oracle)<<(n+1))
                    assert apply_gates(result,list(reversed(gates))) == state
                if (1<<m)<=y<(1<<n)+(1<<m):
                    x=y-(1<<m)
                    assert oracle==(x%(1<<m))|(trailing_ones(x>>m)<<m)
            counts=Counter(len(c) for c,t in gates)
            assert counts[2]==2*(d-1)
            assert counts[1]==2+m+2*d-d.bit_count()
            assert counts[0]==2*d
            rows.append(dict(n=n,m=m,clean_ancillas=d,record_bits=record_bits,
                             not_gates=counts[0],cnot_gates=counts[1],toffoli_gates=counts[2]))
    gates,a0,d=synthesize(5,2)
    return dict(cases=rows, example_n5_m2_gates=gates,
                scope='Exact reversible classical gates, also basis-permutation unitaries; no device or optimality claim')


def physics_witness():
    """Published fitted work values, NOT raw measurements or Holonet calibration."""
    kb=1.380649e-23
    reported={'source':'https://www.sfu.ca/chaos/assets/papers/2014/prl14-reprint.pdf',
              'location':'Table I, page 4; Eq. (3)',
              'source_class':'published experimental fit; manually transcribed',
              'full_erasure_asymptotic_work_over_kBT':0.71,
              'no_erasure_asymptotic_work_over_kBT':0.05,
              'reported_uncertainty_each':0.03,
              'full_erasure_scale_time':1.39,'no_erasure_scale_time':1.48,
              'raw_trajectories_included':False}
    h=3.75
    return dict(published=reported,
                one_bit_theoretical_work_over_kBT=log(2),
                full_erasure_difference_in_reported_uncertainty_units=(0.71-log(2))/0.03,
                model_only=dict(temperature_kelvin=300,timing_entropy_bits=h,
                                unconditioned_erasure_bound_joules=kb*300*log(2)*h,
                                conditional_information_bound_joules=0),
                boundary='Measured fitted colloidal-trap work supports the one-bit reference only; no Holonet energy measurement, noise calibration, or transfer of finite-time coefficients')


def verify():
    return dict(schema='w33.computation-resource-frontiers.v1',status='PASS',
                radix=radix_witness(),noise=noisy_witness(),mixed=mixed_witness(),
                circuit=circuit_witness(),physics=physics_witness())


if __name__=='__main__':
    result=verify()
    Path(__file__).with_name('w33_computation_resource_frontiers_certificate.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':result['status'],'radix_intervals':result['radix']['intervals'],
                      'noise':result['noise']['rows'],'mixed_paths':result['mixed']['mixed_paths'],
                      'circuit_cases':len(result['circuit']['cases']),'physics':result['physics']},indent=2))
