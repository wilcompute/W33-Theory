#include <bits/stdc++.h>
using namespace std;
struct Bits { uint64_t w[9]; bool operator==(Bits const&o) const {for(int i=0;i<9;i++) if(w[i]!=o.w[i]) return false; return true;} };
struct BH { size_t operator()(Bits const&b) const noexcept { uint64_t h=1469598103934665603ULL; for(int i=0;i<9;i++){h^=b.w[i];h*=1099511628211ULL;} return (size_t)h;} };
int main(int argc,char**argv){
 if(argc<5){cerr<<"usage reps sizes actions out\n";return 2;}
 const int NO=327, NR=60, NG=25920, NF=540, BW=6;
 vector<uint16_t> reps(NO*NR), act((size_t)NG*NF); vector<uint32_t> osz(NO);
 auto rd=[&](const char*fn,void*p,size_t n){FILE*f=fopen(fn,"rb"); if(!f){perror(fn);exit(2);} if(fread(p,1,n,f)!=n){cerr<<"short "<<fn<<"\n";exit(2);} fclose(f);};
 rd(argv[1],reps.data(),reps.size()*2);rd(argv[2],osz.data(),osz.size()*4);rd(argv[3],act.data(),act.size()*2);
 uint64_t frameBases[NF][BW]{};
 for(int i=0;i<NO;i++)for(int k=0;k<NR;k++){int f=reps[i*NR+k];frameBases[f][i>>6]|=1ULL<<(i&63);}
 vector<uint32_t> cnt((size_t)NO*NO,0); vector<uint32_t> uniqueCounts(NO); vector<uint64_t> orbitHashes(NO);
 auto st=chrono::steady_clock::now();
 for(int j=0;j<NO;j++){
   unordered_set<Bits,BH> U; U.reserve(osz[j]*2+100);
   for(int g=0;g<NG;g++){
     Bits b{}; auto *pg=&act[(size_t)g*NF];
     for(int k=0;k<NR;k++){int im=pg[reps[j*NR+k]];b.w[im>>6]|=1ULL<<(im&63);} U.insert(b);
   }
   uniqueCounts[j]=U.size(); if(U.size()!=osz[j]){cerr<<"orbit size mismatch "<<j<<" "<<U.size()<<" "<<osz[j]<<"\n";return 3;}
   uint64_t hh=1469598103934665603ULL;
   for(auto const&b:U){
     for(int z=0;z<9;z++){hh^=b.w[z];hh*=1099511628211ULL;}
     uint64_t bad[BW]{};
     for(int wi=0;wi<9;wi++){uint64_t x=b.w[wi];while(x){int q=__builtin_ctzll(x);int f=(wi<<6)+q;x&=x-1;if(f>=NF)continue;for(int z=0;z<BW;z++)bad[z]|=frameBases[f][z];}}
     for(int z=0;z<BW;z++){uint64_t good=~bad[z]; if(z==BW-1) good&=((1ULL<<(NO-64*(BW-1)))-1); while(good){int q=__builtin_ctzll(good);good&=good-1;int i=(z<<6)+q;cnt[(size_t)i*NO+j]++;}}
   }
   orbitHashes[j]=hh;
   if(j%10==0){double sec=chrono::duration<double>(chrono::steady_clock::now()-st).count();cerr<<"j="<<j<<" sec="<<sec<<"\n";}
 }
 FILE*out=fopen(argv[4],"wb");uint32_t dims[2]={NO,NO};fwrite(dims,4,2,out);fwrite(cnt.data(),4,cnt.size(),out);fwrite(uniqueCounts.data(),4,NO,out);fwrite(orbitHashes.data(),8,NO,out);fclose(out);
 size_t nz=0;uint64_t total=0;for(auto x:cnt){if(x)nz++;total+=x;} double sec=chrono::duration<double>(chrono::steady_clock::now()-st).count();
 cout<<"{\"status\":\"PASS\",\"nonzero_cells\":"<<nz<<",\"ordered_disjoint_cover_hits\":"<<total<<",\"seconds\":"<<sec<<"}\n";
}
