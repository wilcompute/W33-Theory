#include <bits/stdc++.h>
using namespace std;
struct Key{array<uint64_t,3>w{};bool operator==(Key const&o)const{return w==o.w;}};
struct Hash{size_t operator()(Key const&k)const noexcept{uint64_t h=0x9e3779b97f4a7c15ULL;for(auto x:k.w){x^=x>>30;x*=0xbf58476d1ce4e5b9ULL;x^=x>>27;x*=0x94d049bb133111ebULL;x^=x>>31;h^=x+0x9e3779b97f4a7c15ULL+(h<<6)+(h>>2);}return h;}};
Key pack(const array<uint8_t,45>&a){Key k;for(int i=0;i<45;i++)k.w[i/16]|=(uint64_t(a[i])&15ULL)<<((i%16)*4);return k;}
int main(int argc,char**argv){if(argc<2)return 2;ifstream f(argv[1],ios::binary);uint32_t n,d;f.read((char*)&n,4);f.read((char*)&d,4);if(n!=720||d!=45)return 3;vector<array<uint8_t,45>>v(n);for(auto&a:v)f.read((char*)a.data(),45);array<uint8_t,45>cap;f.read((char*)cap.data(),45);
 vector<int> fit;for(int i=0;i<(int)n;i++){bool ok=1;for(int c=0;c<45;c++)if(v[i][c]>cap[c]){ok=0;break;}if(ok)fit.push_back(i);}cerr<<"fit="<<fit.size()<<"\n";
 unordered_set<Key,Hash> pairs;pairs.reserve(fit.size()*fit.size()/2);uint64_t pair_mult=0;
 array<uint8_t,45>s{};for(size_t aa=0;aa<fit.size();aa++)for(size_t bb=aa;bb<fit.size();bb++){int i=fit[aa],j=fit[bb];bool ok=1;for(int c=0;c<45;c++){int x=v[i][c]+v[j][c];if(x>cap[c]){ok=0;break;}s[c]=x;}if(ok){pair_mult++;pairs.insert(pack(s));}}
 cerr<<"pair_mult="<<pair_mult<<" pair_unique="<<pairs.size()<<"\n";
 uint64_t triples=0,lookups=0;array<uint8_t,45>t{},need{};bool found=0;array<int,5>wit{};
 for(size_t aa=0;aa<fit.size()&&!found;aa++){int i=fit[aa];for(size_t bb=aa;bb<fit.size()&&!found;bb++){int j=fit[bb];bool ok2=1;for(int c=0;c<45;c++)if(v[i][c]+v[j][c]>cap[c]){ok2=0;break;}if(!ok2)continue;for(size_t cc=bb;cc<fit.size();cc++){int k=fit[cc];bool ok=1;for(int c=0;c<45;c++){int x=v[i][c]+v[j][c]+v[k][c];if(x>cap[c]){ok=0;break;}t[c]=x;need[c]=cap[c]-x;}if(!ok)continue;triples++;lookups++;if(pairs.count(pack(need))){found=1;wit={i,j,k,-1,-1};break;}}}}
 vector<Key>ks(pairs.begin(),pairs.end());sort(ks.begin(),ks.end(),[](auto&a,auto&b){return a.w<b.w;});uint64_t h=1469598103934665603ULL;for(auto&k:ks)for(auto x:k.w){for(int b=0;b<8;b++){h^=(x>>(8*b))&255;h*=1099511628211ULL;}}
 cout<<"{\"status\":\""<<(found?"FOUND":"PASS")<<"\",\"fit_signatures\":"<<fit.size()<<",\"pair_multisets\":"<<pair_mult<<",\"unique_pair_sums\":"<<pairs.size()<<",\"admissible_triples\":"<<triples<<",\"lookups\":"<<lookups<<",\"completion_exists\":"<<(found?"true":"false")<<",\"pair_fnv64\":\""<<hex<<setw(16)<<setfill('0')<<h<<dec<<"\"}\n";return found?1:0;}
