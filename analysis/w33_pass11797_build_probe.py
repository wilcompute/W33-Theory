"""Build the isolated probe against an installed orbifolder1.2.1 tree.

Only accelerates sector enumeration for exact unique field labels; all
gauge/space-group filters stay original. No external source is modified.
"""
from pathlib import Path
import argparse, subprocess, tempfile

OLD='RecursiveCounting(currentNumber, 0, MaxDigits[0], MaxDigits, vec_adjoining_Positions, SectorCouplings);'
NEW=r'''
    bool exact_names = true;
    vector<unsigned> exact_sectors;
    for (unsigned z=0; z<PreDifferentFields.size(); ++z) {
      unsigned count=0, sector=0;
      for (unsigned f=0; f<Fields.size(); ++f) {
        ostringstream label;
        label << Fields[f].Labels[Vacuum.use_Labels] << "_" << Fields[f].Numbers[Vacuum.use_Labels];
        if (Fields[f].Multiplet==LeftChiral && label.str()==PreDifferentFields[z]) {
          ++count; sector=Fields[f].GetInternalIndex()[0];
        }
      }
      if (count!=1) exact_names=false;
      exact_sectors.insert(exact_sectors.end(),PreNumbersOfFields[z],sector);
    }
    if (exact_names) SectorCouplings.push_back(exact_sectors);
    else RecursiveCounting(currentNumber, 0, MaxDigits[0], MaxDigits, vec_adjoining_Positions, SectorCouplings);
'''

def build(orb,output):
    source=orb/'src/orbifolder-1.2.1/src'; binary=orb/'build'
    cpp=source/'orbifolder/cyukawacouplings.cpp'
    text=cpp.read_text();assert text.count(OLD)==1
    include=sorted({str(p.parent) for p in source.rglob('*.hpp')}|
                   {str(source/'orbifolder'),str(orb/'sysroot/usr/include')})
    with tempfile.TemporaryDirectory(prefix='w33_11797_build_') as work:
        temporary=Path(work);patch=temporary/'cyukawacouplings_exact.cpp';patch.write_text(text.replace(OLD,NEW))
        obj=temporary/'couplings.o'
        prefix=['g++','-std=c++11','-Wno-deprecated-declarations','-O2',*['-I'+p for p in include]]
        subprocess.run(prefix+['-c',str(patch),'-o',str(obj)],check=True)
        objects=[str(p) for p in binary.glob('*.o') if p.name!='cyukawacouplings.cpp.o']
        subprocess.run(prefix+[str(Path(__file__).with_name('w33_pass11797_orbifolder_probe.cpp')),str(obj),*objects,
            '-L'+str(orb/'sysroot/usr/lib/x86_64-linux-gnu'),'-lgsl','-lgslcblas',
            '/usr/lib/x86_64-linux-gnu/libreadline.so.8','-o',str(output)],check=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--orb',type=Path,default=Path.home()/'orb')
    p.add_argument('--output',type=Path,default=Path('/tmp/w33_11797_fast_probe'))
    a=p.parse_args();build(a.orb,a.output)
