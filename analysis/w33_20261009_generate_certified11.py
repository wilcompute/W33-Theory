"""Generalize Pass11786 independent exact Wick interval proof to corrected He10/11-state."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
p=R/'analysis/w33_pass11786_certified_spectral_transitions.py'
src=p.read_text()
changes=[
('DEGREES=(2,4,6,8)','DEGREES=(2,4,6,8,10)'),
('range(9)] for _ in range(9)','range(11)] for _ in range(11)'),
('ips=[1,3,5,7];ils=[2,4,6,8]','ips=[1,3,5,7,9];ils=[2,4,6,8,10]'),
('range(4)] for i in range(4)','range(5)] for i in range(5)'),
('for i in range(4):','for i in range(5):'),
('for j in range(4):','for j in range(5):'),
('for k in range(1,9)','for k in range(1,11)'),
("assert energy.hi<F('127.595533')","assert energy.hi<F('127.595507')"),
("ground_energy_upper_bound='127.595533'","ground_energy_upper_bound='127.595507'"),
("schema='w33.pass11786.v1'","schema='w33.20261009.certified11.v1'"),
("OUT=ROOT/'data/w33_pass11786_certified_spectral_transitions.json'","OUT=ROOT/'data/w33_20261009_certified11_wick.json'"),

]
for a,b in changes:
    assert a in src,repr(a)
    src=src.replace(a,b)
src=src.replace('the actual nine-state trial','the actual eleven-state trial')
out=R/'analysis/w33_20261009_certified11_wick.py'
out.write_text(src)
print(out)
