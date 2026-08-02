#include <bits/stdc++.h>
using namespace std;constexpr int RW=9,EW=4,NO=45;
struct Bits{array<uint64_t,RW>w{};};struct EBits{array<uint64_t,EW>w{};};
int nf,ne,no,ns;vector<array<int,4>> fe;vector<int> keyv;vector<Bits> edgeMask,conflictMask,octMask;vector<EBits> fbits;vector<array<uint8_t,NO>> targets;vector<int> sol;vector<Bits> answers;uint64_t nodes;
inline bool used(const EBits&u,int e){return(u.w[e>>6]>>(e&63))&1ULL;}inline int pc(const Bits&a,const Bits&b){int n=0;for(int i=0;i<RW;i++)n+=__builtin_popcountll(a.w[i]&b.w[i]);return n;}inline Bits sub(const Bits&a,const Bits&b){Bits c;for(int i=0;i<RW;i++)c.w[i]=a.w[i]&~b.w[i];return c;}inline EBits uni(const EBits&a,const EBits&b){EBits c;for(int i=0;i<EW;i++)c.w[i]=a.w[i]|b.w[i];return c;}inline bool disjoint(const Bits&a,const Bits&b){for(int i=0;i<RW;i++)if(a.w[i]&b.w[i])return false;return true;}
void dfs(Bits avail,EBits covered,array<uint8_t,NO>&rem){
 nodes++;if(sol.size()==60){for(auto x:rem)if(x)return;Bits m;for(int r:sol)m.w[r>>6]|=1ULL<<(r&63);answers.push_back(m);return;}
 for(int o=0;o<NO;o++)if(rem[o]&&pc(avail,octMask[o])<rem[o])return;
 int best=-1,bn=999;for(int e=0;e<ne;e++)if(!used(covered,e)){int n=0;for(int w=0;w<RW;w++){uint64_t x=avail.w[w]&edgeMask[e].w[w];while(x){int b=__builtin_ctzll(x);x&=x-1;int r=w*64+b;if(r<nf&&rem[keyv[r]])n++;}}if(n<bn){bn=n;best=e;if(n<=1)break;}}
 if(best<0||bn==0)return;
 for(int wi=0;wi<RW;wi++){uint64_t x=avail.w[wi]&edgeMask[best].w[wi];while(x){int b=__builtin_ctzll(x);x&=x-1;int r=wi*64+b;if(r>=nf||!rem[keyv[r]])continue;int o=keyv[r];sol.push_back(r);Bits na=sub(avail,conflictMask[r]);EBits nc=uni(covered,fbits[r]);rem[o]--;if(!rem[o])na=sub(na,octMask[o]);dfs(na,nc,rem);rem[o]++;sol.pop_back();}}
}
vector<Bits> enumerate_fiber(int sid,uint64_t&count_nodes){answers.clear();sol.clear();nodes=0;Bits avail;for(int r=0;r<nf;r++)if(targets[sid][keyv[r]])avail.w[r>>6]|=1ULL<<(r&63);EBits covered;auto rem=targets[sid];dfs(avail,covered,rem);count_nodes=nodes;return answers;}
int main(int argc,char**argv){if(argc<2)return 2;ifstream in(argv[1]);in>>nf>>ne>>no>>ns;assert(nf==540&&ne==240&&no==45&&ns==9);fe.resize(nf);keyv.resize(nf);edgeMask.assign(ne,{});conflictMask.assign(nf,{});octMask.assign(no,{});fbits.assign(nf,{});
 for(int r=0;r<nf;r++){for(int j=0;j<4;j++){int e;in>>e;fe[r][j]=e;edgeMask[e].w[r>>6]|=1ULL<<(r&63);fbits[r].w[e>>6]|=1ULL<<(e&63);}in>>keyv[r];octMask[keyv[r]].w[r>>6]|=1ULL<<(r&63);}targets.resize(ns);for(auto&t:targets)for(int o=0;o<no;o++){int z;in>>z;t[o]=z;}for(int r=0;r<nf;r++)for(int e:fe[r])for(int w=0;w<RW;w++)conflictMask[r].w[w]|=edgeMask[e].w[w];
 uint64_t n1,n8;auto a=enumerate_fiber(1,n1);auto b=enumerate_fiber(8,n8);uint64_t compat=0;for(auto&x:a)for(auto&y:b)compat+=disjoint(x,y);cout<<"{\"fiber1_covers\":"<<a.size()<<",\"fiber8_covers\":"<<b.size()<<",\"fiber1_nodes\":"<<n1<<",\"fiber8_nodes\":"<<n8<<",\"disjoint_pairs\":"<<compat<<"}\n";return compat?1:0;}
