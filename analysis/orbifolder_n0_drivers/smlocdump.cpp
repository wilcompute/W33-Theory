// Pass 11910: dump the SM configuration of a (SUSY) orbifolder model: per field the SM label, twist k, lattice vector n,
// multiplet and dims. usage: smlocdump models.txt  (several models; prints MODEL n label, then F lines)
#include <stdio.h>
#include <cstdlib>
#include "cprompt.h"
#include "cspectrum.h"
#include "canalysemodel.h"
using namespace std;
unsigned SELFDUALLATTICE;
int main(int argc, char *argv[])
{
  ifstream in(argv[1]);
  ostringstream devnull;
  CPrint Quiet(Tstandard, &devnull);
  string prog = "";
  COrbifoldGroup G;
  int n = 0;
  while (G.LoadOrbifoldGroup(in, prog))
  {
    ++n;
    COrbifold O(G);
    vector<SConfig> cfg;
    bool bSM = true, bPS = false, bSU5 = false;
    CAnalyseModel A;
    A.AnalyseModel(O, O.StandardConfig, bSM, bPS, bSU5, cfg, Quiet, 3, false);
    cout << "MODEL " << n << " " << G.Label << " SM " << (bSM && !cfg.empty()) << endl;
    if (!bSM || cfg.empty()) continue;
    SConfig c = cfg[0];
    unsigned L = c.use_Labels;
    for (unsigned i = 0; i < c.Fields.size(); ++i)
    {
      const CField &F = c.Fields[i];
      const CSpaceGroupElement &g = F.SGElement;
      cout << "F " << F.Labels[L] << " k=" << g.Get_k() << " m=" << (int)F.Multiplet
           << " n=" << g.Get_n(0) << "," << g.Get_n(1) << "," << g.Get_n(2) << "," << g.Get_n(3) << "," << g.Get_n(4) << "," << g.Get_n(5)
           << " dim=";
      for (unsigned d = 0; d < F.Dimensions.size(); ++d) cout << (d ? "," : "") << F.Dimensions[d].Dimension << F.Dimensions[d].AdditionalLabel;
      cout << endl;
    }
  }
  return 0;
}
