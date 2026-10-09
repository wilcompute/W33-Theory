// Replayable full benchmark metadata and explicitly requested legacy-rule couplings.
// Orbifolder1.2.1 owns the CFT implementation. Its random CouplingStrength is
// deliberately never exported as a physical string coefficient.
#include <stdio.h>
#include <cstdlib>
#include <sstream>
#include "cprompt.h"
#include "cspectrum.h"
#include "canalysemodel.h"
using namespace std;
unsigned SELFDUALLATTICE;
int main(int argc, char **argv) {
  if (argc != 3 && argc != 4) return 1;
  ifstream in(argv[1]); ostringstream quiet;
  CPrint print(Tstandard, &quiet); string program;
  COrbifoldGroup group;
  if (!group.LoadOrbifoldGroup(in, program)) return 2;
  COrbifold orb(group); vector<SConfig> configs;
  bool sm=true, ps=false, su5=false; CAnalyseModel analyser;
  analyser.AnalyseModel(orb, orb.StandardConfig, sm, ps, su5, configs, print, 3, false);
  if (!sm || configs.empty()) return 3;
  SConfig config=configs[0]; unsigned labels=config.use_Labels;
  // Isolated selection-rule adapter: GetDiscreteCharge reads this cached
  // contribution; gauge weights, constructing elements and actual oscillators
  // in orb.GetSectors() remain the original states. This is not an amplitude.
  if (argc == 4 && string(argv[3]) == "gamma-corrected")
    for (unsigned j=0;j<config.Fields.size();++j)
      if (!config.Fields[j].gamma_phases.empty())
        config.Fields[j].OsciContribution[1] += 6*config.Fields[j].gamma_phases[0];
  cout.precision(17);
  const auto &basis=config.SymmetryGroup.GaugeGroup.u1directions;
  for (unsigned a=0;a<basis.size();++a) {
    cout << "B " << a;
    for (unsigned j=0;j<basis[a].size();++j) cout << " " << basis[a][j];
    cout << endl;
  }
  // The existing all-weight and gamma drivers are separately frozen.
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
