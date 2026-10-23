"""Independent cycle-level valid/ready software model for the optical phase-frame RTL.
The model is tested; the SV design and TB are source-reviewed, not simulated (tools unavailable).
"""
from dataclasses import dataclass
from pathlib import Path
import random
RTL=Path(__file__).resolve().parents[1]/"hardware/w33_linebus_phase_frame.sv"
TB=Path(__file__).resolve().parents[1]/"hardware/tb_w33_linebus_phase_frame.sv"
@dataclass
class Model:
    frame:int=0
    valid:bool=False
    mask:int=0
    out:int=0
    correction:int=0
    def tick(self,valid=False,mask=0,clear=False,ready=True,reset=False):
        if reset:
            self.frame=self.mask=self.out=self.correction=0
            self.valid=False
            return True
        accept=not self.valid or ready
        if accept:
            self.valid=bool(valid)
            if valid:
                self.frame=((0 if clear else self.frame)+mask.bit_count())%4
                self.mask=mask
                self.out=self.frame
                self.correction=(-self.frame)%4
        return accept

def test_all_state_mask_clear_combinations():
    for start in range(4):
        for mask in range(4):
            for clear in (False,True):
                m=Model(frame=start)
                assert m.tick(valid=True,mask=mask,clear=clear)
                target=((0 if clear else start)+mask.bit_count())%4
                assert m.valid and m.out==target and m.correction==(-target)%4

def test_backpressure_and_replacement():
    m=Model()
    assert m.tick(valid=True,mask=3)
    saved=(m.frame,m.mask,m.out,m.correction)
    for k in range(30):
        assert not m.tick(valid=True,mask=k%4,ready=False)
        assert saved==(m.frame,m.mask,m.out,m.correction)
    assert m.tick(valid=True,mask=2,ready=True)
    assert m.out==3 and m.mask==2

def test_reset_and_idle():
    m=Model()
    m.tick(valid=True,mask=1)
    for _ in range(5):m.tick(valid=False)
    assert m.frame==1 and not m.valid
    m.tick(reset=True)
    assert m.frame==0 and not m.valid

def test_random_handshake_reference():
    rng=random.Random(20261023)
    m=Model()
    count=0
    for _ in range(5000):
        v=bool(rng.getrandbits(1))
        mask=rng.randrange(4);ready=bool(rng.getrandbits(1))
        clear=bool(rng.randrange(13)==0);rst=bool(rng.randrange(177)==0)
        old=(m.frame,m.valid,m.mask,m.out,m.correction)
        accept=m.tick(valid=v,mask=mask,ready=ready,clear=clear,reset=rst)
        if rst:assert m.frame==0 and not m.valid
        elif not accept:assert old==(m.frame,m.valid,m.mask,m.out,m.correction)
        elif v:
            expected=((0 if clear else old[0])+mask.bit_count())%4
            assert m.out==expected and m.correction==(-expected)%4
            count+=1
    assert count>1000

def test_rtl_and_testbench_structural_contract():
    s=RTL.read_text(encoding="utf-8")
    tb=TB.read_text(encoding="utf-8")
    tokens=["always_ff","always_comb","cmd_ready = !result_valid || result_ready;",
            "frame_next = (cmd_clear ? 2'd0 : frame_reg) + popcount2;",
            "2'b11: popcount2 = 2'd2;",
            "result_correction <= 2'd0 - frame_next;"]
    assert all(t in s for t in tokens)
    assert "$fatal" in tb and "PASS w33_linebus_phase_frame" in tb
