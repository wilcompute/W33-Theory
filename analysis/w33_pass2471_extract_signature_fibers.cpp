#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <unordered_map>
#include <unordered_set>
#include <vector>
using namespace std;
constexpr int NR=540,RW=9,NS=45;
struct Key{array<uint64_t,RW>w{};bool operator==(Key const&o)const{return w==o.w;}};
struct KHash{size_t operator()(Key const&k)const noexcept{uint64_t h=0x9e3779b97f4a7c15ULL;for(auto x:k.w){x^=x>>30;x*=0xbf58476d1ce4e5b9ULL;x^=x>>27;x*=0x94d049bb133111ebULL;x^=x>>31;h^=x+0x9e3779b97f4a7c15ULL+(h<<6)+(h>>2);}return h;}};
struct Sig{array<uint8_t,NS>a{};bool operator==(Sig const&o)const{return a==o.a;}};
struct SHash{size_t operator()(Sig const&s)const noexcept{uint64_t h=1469598103934665603ULL;for(auto x:s.a){h^=x;h*=1099511628211ULL;}return h;}};
Key transform(const Key&k,const vector<int>&g){Key y;for(int w=0;w<RW;w++){uint64_t x=k.w[w];while(x){int b=__builtin_ctzll(x);x&=x-1;int r=64*w+b;if(r<NR){int s=g[r];y.w[s/64]|=1ULL<<(s%64);}}}return y;}
Sig signature(const Key&k,const vector<int>&ko){Sig s;for(int w=0;w<RW;w++){uint64_t x=k.w[w];while(x){int b=__builtin_ctzll(x);x&=x-1;int r=64*w+b;if(r<NR)s.a[ko[r]]++;}}return s;}
int main(int argc,char**argv){if(argc!=6){cerr<<"input key reps targets outbin\n";return 2;}ifstream in(argv[1]);int nr,nc,ng,z;in>>nr>>nc>>ng;for(int i=0;i<nr*4;i++)in>>z;vector<vector<int>>gens(ng,vector<int>(NR));for(auto&g:gens)for(int&i:g)in>>i;ifstream ki(argv[2]);vector<int>ko(NR);for(int&i:ko)ki>>i;
 ifstream bin(argv[3],ios::binary);uint64_t m;bin.read((char*)&m,8);vector<Key>reps(m);vector<uint32_t>expected(m);for(size_t t=0;t<m;t++){for(int j=0;j<60;j++){uint16_t r;bin.read((char*)&r,2);reps[t].w[r/64]|=1ULL<<(r%64);}uint32_t st,hits;bin.read((char*)&expected[t],4);bin.read((char*)&st,4);bin.read((char*)&hits,4);}
 ifstream ti(argv[4]);int nt;ti>>nt;vector<Sig>targets(nt);unordered_map<Sig,int,SHash>tid;for(int i=0;i<nt;i++){for(int j=0;j<NS;j++){int x;ti>>x;targets[i].a[j]=x;}tid[targets[i]]=i;}vector<vector<Key>>fib(nt);
 for(size_t ri=0;ri<m;ri++){unordered_set<Key,KHash>seen;seen.reserve(expected[ri]*2);vector<Key>q{reps[ri]};seen.insert(reps[ri]);size_t head=0;while(head<q.size()){Key x=q[head++];auto it=tid.find(signature(x,ko));if(it!=tid.end())fib[it->second].push_back(x);for(auto&g:gens){Key y=transform(x,g);if(seen.insert(y).second)q.push_back(y);}}if(q.size()!=expected[ri])return 3;}
 ofstream out(argv[5],ios::binary);uint32_t ntt=nt;out.write((char*)&ntt,4);for(int i=0;i<nt;i++){uint64_t n=fib[i].size();out.write((char*)&n,8);for(auto&k:fib[i])out.write((char*)k.w.data(),RW*8);cerr<<i<<" "<<n<<"\n";}return 0;}
