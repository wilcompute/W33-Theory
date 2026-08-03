#include <bits/stdc++.h>
using namespace std;
struct ArrHash{size_t operator()(array<uint16_t,240> const&a) const noexcept {uint64_t h=1469598103934665603ULL;for(auto x:a){h^=x;h*=1099511628211ULL;}return h;}};
int main(int argc,char**argv){
 vector<array<uint16_t,240>> gens; const char* gp=argc>1?argv[1]:"data/w33_pass2560_edge_gens.txt"; const char* wp=argc>2?argv[2]:"data/w33_pass2560_singleton_witnesses263.json"; ifstream in(gp);
 while(in){array<uint16_t,240> g; int x; bool ok=1; for(int i=0;i<240;i++){if(!(in>>x)){ok=0;break;}g[i]=x;} if(ok)gens.push_back(g);}
 array<uint16_t,240> id; iota(id.begin(),id.end(),0);
 vector<array<uint16_t,240>> G{ id }; unordered_set<array<uint16_t,240>,ArrHash> seen;seen.reserve(60000);seen.insert(id);
 for(size_t h=0;h<G.size();h++)for(auto &g:gens){array<uint16_t,240> q;for(int i=0;i<240;i++)q[i]=g[G[h][i]];if(seen.insert(q).second)G.push_back(q);} cerr<<"G "<<G.size()<<"\n";
 ifstream jf(wp); string s((istreambuf_iterator<char>(jf)),istreambuf_iterator<char>()); vector<array<uint16_t,6>> W;
 size_t p=0; while((p=s.find("support",p))!=string::npos){p=s.find('[',p);array<uint16_t,6>a;for(int i=0;i<6;i++){while(p<s.size()&&!isdigit((unsigned char)s[p]))p++;int v=0;while(p<s.size()&&isdigit((unsigned char)s[p]))v=v*10+s[p++]-'0';a[i]=v;}sort(a.begin(),a.end());W.push_back(a);} cerr<<"W "<<W.size()<<"\n";
 map<array<uint16_t,6>,int> canon;
 int nonregular=0; for(auto &a:W){array<uint16_t,6> best;best.fill(65535);int stab=0;for(auto &g:G){array<uint16_t,6>b;for(int i=0;i<6;i++)b[i]=g[a[i]];sort(b.begin(),b.end());if(b==a)stab++;if(b<best)best=b;}if(stab!=1)nonregular++;canon[best]++;} cerr<<"nonregular "<<nonregular<<"\n";
 cout<<"orbits "<<canon.size()<<" lowerbound "<<canon.size()*G.size()<<"\n";map<int,int> mult;for(auto&[k,v]:canon)mult[v]++;for(auto [v,n]:mult)cout<<"sample_multiplicity "<<v<<" count "<<n<<"\n";
 ofstream out("data/w33_pass2560_orbit_reps263.rebuilt.txt");for(auto &[a,v]:canon){for(int i=0;i<6;i++)out<<a[i]<<(i==5?'\n':' ');} }
