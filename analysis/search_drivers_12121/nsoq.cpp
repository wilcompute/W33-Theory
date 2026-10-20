// non-SUSY orbifolder: full field dump of the standard config -- per field: multiplet, space-group element (k,m,n and
// lattice translation), representation, U(1) charges, q_sh (right-mover), oscillator contribution, and every
// left-mover weight; plus gauge factors (simple roots) and U(1) directions. Full precision.
#include <stdio.h>
#include <cstdlib>
#include <fstream>
#include <sstream>
#include "corbifold.h"
#include "corbifoldgroup.h"
#include "cprint.h"
#include "cfield.h"
#include "csector.h"
#include "coscillator.h"
using namespace std;
unsigned SELFDUALLATTICE;
static void vec(const CVector &v)
{
  for (unsigned x = 0; x < v.size(); ++x) { char b[64]; snprintf(b, 64, "%s%.12g", x ? "," : "", (double)v[x]); cout << b; }
}
int main(int argc, char *argv[])
{
  ifstream in(argv[1]);
  string prog = "";
  COrbifoldGroup G;
  if (!G.LoadOrbifoldGroup(in, prog)) { cout << "LOADFAIL" << endl; return 2; }
  COrbifold O(G);
  const SConfig &c = O.StandardConfig;
  const vector<CSector> &S = O.GetSectors();
  const CGaugeGroup &GG = c.SymmetryGroup.GaugeGroup;
  cout << "GAUGE " << GG.algebra << endl;
  for (unsigned f = 0; f < GG.factor.size(); ++f)
  {
    cout << "FACTOR " << f << " " << GG.factor[f].algebra;
    for (unsigned r = 0; r < GG.factor[f].simpleroots.size(); ++r)
    {
      cout << " |";
      for (unsigned x = 0; x < 16; ++x) { char b[64]; snprintf(b, 64, " %.12g", (double)GG.factor[f].simpleroots[r][x]); cout << b; }
    }
    cout << endl;
  }
  for (unsigned u = 0; u < GG.u1directions.size(); ++u)
  {
    cout << "U1 " << u << " |";
    for (unsigned x = 0; x < 16; ++x) { char b[64]; snprintf(b, 64, " %.12g", (double)GG.u1directions[u][x]); cout << b; }
    cout << endl;
  }
  for (unsigned i = 0; i < c.Fields.size(); ++i)
  {
    const CField &F = c.Fields[i];
    const CSpaceGroupElement &E = F.SGElement;
    cout << "FIELD " << i << " m=" << (int)F.Multiplet << " k=" << E.Get_k() << " mm=" << E.Get_m() << " n=" << E.Get_n() << " lat=";
    for (unsigned a = 0; a < 6; ++a) cout << (a ? "," : "") << E.Get_n(a).numerator() << "/" << E.Get_n(a).denominator();
    cout << " dim=";
    for (unsigned d = 0; d < F.Dimensions.size(); ++d) cout << (d ? "," : "") << F.Dimensions[d].Dimension << F.Dimensions[d].AdditionalLabel;
    cout << " q=";
    vec(F.U1Charges);
    cout << " qsh=";
    vec(F.q_sh);
    cout << " osc=";
    vec(F.OsciContribution);
    cout << " nlm=" << F.GetNumberOfLMWeights() << " nrm=" << F.GetNumberOfRMWeights(S) << " nosc=" << F.GetNumberOfOscillators(S) << endl;
    for (unsigned j = 0; j < F.GetNumberOfRMWeights(S); ++j) { cout << "R "; vec(F.GetRMWeight(j, S)); cout << endl; }
    for (unsigned j = 0; j < F.GetNumberOfOscillators(S); ++j)
    {
      const CModedOscillator &o = F.GetOscillator(j, S);
      cout << "O idx=" << o.GetIndex() << " type=" << (int)o.GetType() << " freq=" << o.GetFrequency() << " N=" << o.GetNumberOperator() << " lad=" << (int)o.GetLadderOperatorType() << endl;
    }
    for (unsigned j = 0; j < F.GetNumberOfLMWeights(); ++j)
    {
      cout << "W ";
      vec(F.GetLMWeight(j, S));
      cout << endl;
    }
  }
  cout << "END" << endl;
  return 0;
}
