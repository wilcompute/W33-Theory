#include <bits/stdc++.h>
using namespace std;
struct Bits{uint64_t w[9]; bool operator==(Bits const&o)const{for(int i=0;i<9;i++)if(w[i]!=o.w[i])return false;return true;}};
struct H{size_t operator()(Bits const&b)const noexcept{uint64_t h=1469598103934665603ULL;for(int i=0;i<9;i++){h^=b.w[i];h*=1099511628211ULL;}return h;}};
static bool lessb(Bits const&a,Bits const&b){for(int i=8;i>=0;i--){if(a.w[i]!=b.w[i])return a.w[i]<b.w[i];}return false;}
int main(int argc,char**argv){const int NO=327,NR=60,NG=25920,NF=540;if(argc!=5)return 2;vector<uint16_t>R(NO*NR),A((size_t)NG*NF),O(NF);auto rd=[&](const char*f,void*p,size_t n){FILE*x=fopen(f,"rb");if(!x){perror(f);exit(2);}if(fread(p,1,n,x)!=n){cerr<<"short\n";exit(2);}fclose(x);};rd(argv[1],R.data(),R.size()*2);rd(argv[2],A.data(),A.size()*2);rd(argv[3],O.data(),O.size()*2);
 auto canon=[&](const uint16_t*cov){Bits best{};for(int i=0;i<9;i++)best.w[i]=~0ULL;best.w[8]&=((1ULL<<(NF-512))-1);for(int g=0;g<NG;g++){Bits b{};auto*p=&A[(size_t)g*NF];for(int k=0;k<NR;k++){int x=p[cov[k]];b.w[x>>6]|=1ULL<<(x&63);}if(lessb(b,best))best=b;}return best;};
 unordered_map<Bits,int,H> mp;mp.reserve(NO*2);vector<Bits>C(NO);auto st=chrono::steady_clock::now();for(int i=0;i<NO;i++){C[i]=canon(&R[i*NR]);if(mp.count(C[i])){cerr<<"duplicate canon\n";return 3;}mp[C[i]]=i;if(i%20==0)cerr<<"base "<<i<<"\n";}
 vector<int> out(NO,-1);for(int i=0;i<NO;i++){uint16_t cov[NR];for(int k=0;k<NR;k++)cov[k]=O[R[i*NR+k]];Bits c=canon(cov);auto it=mp.find(c);if(it==mp.end()){cerr<<"missing outer "<<i<<"\n";return 4;}out[i]=it->second;}
 for(int i=0;i<NO;i++)if(out[out[i]]!=i){cerr<<"not involution\n";return 5;}
 FILE*f=fopen(argv[4],"wb");for(int x:out){uint16_t q=x;fwrite(&q,2,1,f);}fclose(f);int fix=0;for(int i=0;i<NO;i++)fix+=out[i]==i;double sec=chrono::duration<double>(chrono::steady_clock::now()-st).count();cout<<"{\"fixed_orbits\":"<<fix<<",\"transposed_pairs\":"<<(NO-fix)/2<<",\"seconds\":"<<sec<<"}\n";
}
