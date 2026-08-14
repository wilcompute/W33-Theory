// Pass5215: orbit-complete q=3 radius-seven provenance census.
// Inputs:
//   /tmp/w33_pass5176_q3_graph.txt from Pass5176 exporter
//   /tmp/w33_pass5215_q3_stab.txt from Pass5215 stabilizer exporter
// The 16 projective collineations fixing apartment 0 reduce connected six-sets
// to 734,414 orbit representatives. Every connected seven-set containing 0 has
// a connected six-set parent containing 0, hence every stabilizer orbit occurs
// among one-vertex extensions of those representatives. We test all 64,439,500
// such extensions at the max-vote -> max-singleton provenance stage.
#include <algorithm>
#include <array>
#include <atomic>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <unordered_set>
#include <utility>
#include <vector>
using namespace std;
static vector<vector<int>> adjv,stab;
static vector<array<int,6>> charts;
static vector<vector<pair<int,int>>> ach;
static int leadarr[8]={0,8,16,1,32,2,4,0};
static int syn(int m){return (((m>>0&1)^(m>>1&1)^(m>>3&1)))|((((m>>0&1)^(m>>2&1)^(m>>4&1)))<<1)|((((m>>1&1)^(m>>2&1)^(m>>5&1)))<<2);}
static uint64_t packv(vector<int> v){sort(v.begin(),v.end());uint64_t k=0;int j=0;for(int x:v)if(x)k|=(uint64_t)x<<(11*j++);return k;}
static vector<int> unpack(uint64_t k,int size){vector<int>v={0};for(int i=0;i<size-1;i++)v.push_back((k>>(11*i))&2047);sort(v.begin(),v.end());return v;}
static uint64_t canon(const vector<int>&V){uint64_t best=~0ULL;for(auto&P:stab){vector<int>w;w.reserve(V.size());for(int x:V)w.push_back(P[x]);best=min(best,packv(w));}return best;}
static bool subset(const vector<int>&X,const vector<int>&E){for(int x:X)if(!binary_search(E.begin(),E.end(),x))return false;return true;}
static vector<int> provenanceStage(const vector<int>&E){
    int touched[32],masks[32],nt=0;
    auto addmask=[&](int ci,int bit){for(int i=0;i<nt;i++)if(touched[i]==ci){masks[i]^=bit;return;}touched[nt]=ci;masks[nt]=bit;nt++;};
    for(int a:E)for(auto [ci,p]:ach[a])addmask(ci,1<<p);
    int cand[96],votes[96],sing[96],nc=0;
    auto addvote=[&](int a,bool s){for(int i=0;i<nc;i++)if(cand[i]==a){votes[i]++;sing[i]+=s;return;}cand[nc]=a;votes[nc]=1;sing[nc]=s;nc++;};
    for(int i=0;i<nt;i++){int m=masks[i],lm=leadarr[syn(m)];if(!lm)continue;int p=__builtin_ctz((unsigned)lm);addvote(charts[touched[i]][p],__builtin_popcount((unsigned)m)==1&&((m>>p)&1));}
    if(!nc)return{};int mv=0;for(int i=0;i<nc;i++)mv=max(mv,votes[i]);int ms=0;for(int i=0;i<nc;i++)if(votes[i]==mv)ms=max(ms,sing[i]);
    vector<int>F;for(int i=0;i<nc;i++)if(votes[i]==mv&&sing[i]==ms)F.push_back(cand[i]);sort(F.begin(),F.end());return F;
}
int main(int argc,char**argv){
    string gp=argc>1?argv[1]:"/tmp/w33_pass5176_q3_graph.txt";
    string sp=argc>2?argv[2]:"/tmp/w33_pass5215_q3_stab.txt";
    ifstream f(gp);int n,nc;if(!(f>>n>>nc))return 2;adjv.assign(n,{});for(auto&v:adjv){v.resize(20);for(int&x:v)f>>x;sort(v.begin(),v.end());}
    charts.resize(nc);ach.assign(n,{});for(int ci=0;ci<nc;ci++)for(int p=0;p<6;p++){f>>charts[ci][p];ach[charts[ci][p]].push_back({ci,p});}
    ifstream sf(sp);int gs,nn;sf>>gs>>nn;stab.assign(gs,vector<int>(nn));for(auto&P:stab)for(int&x:P)sf>>x;if(n!=1620||nc!=1080||gs!=16||nn!=1620)return 3;for(auto&P:stab)if(P[0]!=0)return 4;
    unordered_set<uint64_t>cur,nxt;cur.insert(0);vector<size_t>cnt(7);cnt[1]=1;
    const size_t expected[7]={0,1,5,57,1043,25929,734414};
    for(int size=1;size<6;size++){
        nxt.clear();nxt.reserve(max<size_t>(100,cur.size()*3));
        for(uint64_t key:cur){auto V=unpack(key,size);vector<int>C;for(int v:V)for(int u:adjv[v])C.push_back(u);sort(C.begin(),C.end());C.erase(unique(C.begin(),C.end()),C.end());for(int u:C){if(binary_search(V.begin(),V.end(),u))continue;auto W=V;W.push_back(u);nxt.insert(canon(W));}}
        cur.swap(nxt);cnt[size+1]=cur.size();if(cnt[size+1]!=expected[size+1]){cerr<<"orbit count mismatch\n";return 5;}
    }
    // Freeze the exact representative order used by the development runner.
    vector<uint64_t> reps(cur.begin(),cur.end());
    // Size-six provenance stage itself is already true-only on every orbit rep.
    for(uint64_t key:reps){auto V=unpack(key,6);auto F=provenanceStage(V);if(F.empty()||!subset(F,V))return 6;}
    long long ext=0;atomic<int>bad(0);
#ifdef _OPENMP
#pragma omp parallel for schedule(dynamic,256) reduction(+:ext)
#endif
    for(long long ii=0;ii<(long long)reps.size();ii++){
        if(bad.load())continue;auto V=unpack(reps[(size_t)ii],6);
        vector<int>C;for(int v:V)for(int u:adjv[v])C.push_back(u);sort(C.begin(),C.end());C.erase(unique(C.begin(),C.end()),C.end());
        for(int u:C){if(binary_search(V.begin(),V.end(),u))continue;auto E=V;E.push_back(u);sort(E.begin(),E.end());auto F=provenanceStage(E);ext++;if(F.empty()||!subset(F,E)){bad.store(1);break;}}
    }
    if(bad)return 7;
    if(ext!=64439500){cerr<<"extension count "<<ext<<" expected 64439500\n";return 8;}
    cout<<"{\"status\":\"PASS\",\"stabilizer\":16,\"orbit_counts\":[1,5,57,1043,25929,734414],\"weight7_extensions_tested\":64439500,\"false_provenance_stage\":0}\n";
    return 0;
}
