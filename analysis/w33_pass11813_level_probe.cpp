// Field dump + exact-coupling probe on orbifolder 1.2.1 internals (derived from Pass 11797's probe).
#include <stdio.h>
#include <cstdlib>
#include <sstream>
#include "cprompt.h"
#include "cspectrum.h"
#include "canalysemodel.h"
using namespace std;
unsigned SELFDUALLATTICE;
int main(int argc, char **argv) {
  if (argc < 3) return 1;
  ifstream in(argv[1]); ostringstream quiet;
  CPrint print(Tstandard, &quiet); string program;
  COrbifoldGroup group;
  if (!group.LoadOrbifoldGroup(in, program)) return 2;
  COrbifold orb(group); vector<SConfig> configs;
  bool sm=true, ps=false, su5=false; CAnalyseModel analyser;
  analyser.AnalyseModel(orb, orb.StandardConfig, sm, ps, su5, configs, print, 3, false);
  if (!sm || configs.empty()) return 3;
  SConfig config=configs[0]; unsigned labels=config.use_Labels;
  bool gamma = (argc >= 4 && string(argv[3]) == "gamma-corrected");
  if (gamma)
    for (unsigned j=0;j<config.Fields.size();++j)
      if (!config.Fields[j].gamma_phases.empty())
        config.Fields[j].OsciContribution[1] += 6*config.Fields[j].gamma_phases[0];
  cout.precision(17);
  const vector<CSector> &sectors = orb.GetSectors();
  for (unsigned j=0;j<config.Fields.size();++j) {
    const CField &f = config.Fields[j];
    if (f.Multiplet != LeftChiral) continue;
    cout << "F " << f.Labels[labels] << "_" << f.Numbers[labels];
    const vector<unsigned> &ii = f.GetInternalIndex();
    cout << " idx"; for (unsigned a=0;a<ii.size();++a) cout << " " << ii[a];
    cout << " dims"; for (unsigned a=0;a<f.Dimensions.size();++a) cout << " " << f.Dimensions[a].Dimension;
    cout << " u1"; for (unsigned a=0;a<f.U1Charges.GetSize();++a) cout << " " << f.U1Charges[a];
    cout << " qsh"; for (unsigned a=0;a<f.q_sh.GetSize();++a) cout << " " << f.q_sh[a];
    cout << " osc"; for (unsigned a=0;a<f.OsciContribution.GetSize();++a) cout << " " << f.OsciContribution[a];
    cout << " gam"; for (unsigned a=0;a<f.gamma_phases.size();++a) cout << " " << f.gamma_phases[a];
    cout << " nw " << f.GetNumberOfLMWeights() << " w";
    const CVector &w = f.GetLMWeight(0, sectors);
    for (unsigned a=0;a<w.GetSize();++a) cout << " " << w[a];
    cout << endl;
  }
  ifstream requests(argv[2]); string line;
  while (getline(requests,line)) {
    istringstream row(line); vector<string> names; string name;
    while (row>>name) names.push_back(name);
    if (names.empty()) continue;
    SConfig temporary=config;
    temporary.FieldCouplings.clear();
    orb.YukawaCouplings.AddCoupling(orb,temporary,names);
    cout << "CHECK " << temporary.FieldCouplings.size();
    for (unsigned j=0;j<names.size();++j) cout << " " << names[j];
    cout << endl;
  }
  return 0;
}
