#include <bits/stdc++.h>
using namespace std;
struct Bits{uint64_t w[9];bool operator==(Bits const&o)const{for(int i=0;i<9;i++)if(w[i]!=o.w[i])return false;return true;}};
struct BH{size_t operator()(Bits const&b)const noexcept{uint64_t h=1469598103934665603ULL;for(int i=0;i<9;i++){h^=b.w[i];h*=1099511628211ULL;}return h;}};
inline bool disj(Bits const&a,Bits const&b){for(int i=0;i<9;i++)if(a.w[i]&b.w[i])return false;return true;}
inline Bits bor(Bits const&a,Bits const&b){Bits c;for(int i=0;i<9;i++)c.w[i]=a.w[i]|b.w[i];return c;}
vector<vector<Bits>> cand; uint64_t nodes=0,dead=0; vector<int> choice(9,-1); vector<char> usedc(9,0); bool found=false; chrono::steady_clock::time_point startt; double limitsec=550;
uint64_t traceh=1469598103934665603ULL;
bool dfs(int depth,Bits used){
 nodes++; if((nodes&((1<<20)-1))==0){double s=chrono::duration<double>(chrono::steady_clock::now()-startt).count();if(s>limitsec)return false;}
 if(depth==9){found=true;return true;}
 int best=-1; vector<int> bestids;
 for(int c=0;c<9;c++)if(!usedc[c]){
   vector<int> ids;ids.reserve(128);
   for(int i=0;i<(int)cand[c].size();i++)if(disj(used,cand[c][i]))ids.push_back(i);
   if(ids.empty()){dead++;return false;}
   if(best<0||ids.size()<bestids.size()){best=c;bestids.swap(ids);if(bestids.size()==1)break;}
 }
 usedc[best]=1;
 for(int id:bestids){traceh^=((uint64_t)best<<48)^((uint64_t)id<<16)^depth;traceh*=1099511628211ULL;choice[best]=id;if(dfs(depth+1,bor(used,cand[best][id])))return true;}
 choice[best]=-1;usedc[best]=0;return false;
}
int main(int argc,char**argv){if(argc<8){cerr<<"args reps actions orbit_t frame_label targets outcand outjson\n";return 2;}const int NO=327,NR=60,NG=25920,NF=540;
 vector<uint16_t>R(NO*NR),A((size_t)NG*NF);vector<int8_t>OT(NO*45),T(9*45);vector<uint8_t>FL(NF);
 auto rd=[&](const char*f,void*p,size_t n){FILE*x=fopen(f,"rb");if(!x){perror(f);exit(2);}if(fread(p,1,n,x)!=n){cerr<<"short "<<f<<"\n";exit(2);}fclose(x);};
 rd(argv[1],R.data(),R.size()*2);rd(argv[2],A.data(),A.size()*2);rd(argv[3],OT.data(),OT.size());rd(argv[4],FL.data(),FL.size());rd(argv[5],T.data(),T.size());
 unordered_map<string,int> target;for(int c=0;c<9;c++)target[string((char*)&T[c*45],45)]=c;
 vector<unordered_set<Bits,BH>> U(9);for(auto&u:U)u.reserve(16000);
 auto st=chrono::steady_clock::now();
 for(int j=0;j<NO;j++)for(int g=0;g<NG;g++){
   Bits b{};int8_t tv[45]{};auto*p=&A[(size_t)g*NF];
   for(int k=0;k<NR;k++){int im=p[R[j*NR+k]];b.w[im>>6]|=1ULL<<(im&63);tv[FL[im]]++;}
   auto it=target.find(string((char*)tv,45));if(it!=target.end())U[it->second].insert(b);
 }
 cand.resize(9);for(int c=0;c<9;c++){cand[c].assign(U[c].begin(),U[c].end());sort(cand[c].begin(),cand[c].end(),[](Bits const&a,Bits const&b){for(int i=8;i>=0;i--)if(a.w[i]!=b.w[i])return a.w[i]<b.w[i];return false;});cerr<<"c"<<c<<"="<<cand[c].size()<<"\n";}
 FILE*fo=fopen(argv[6],"wb");uint32_t magic=0x18350001;fwrite(&magic,4,1,fo);for(int c=0;c<9;c++){uint32_t n=cand[c].size();fwrite(&n,4,1,fo);fwrite(cand[c].data(),sizeof(Bits),n,fo);}fclose(fo);
 startt=chrono::steady_clock::now();Bits z{};bool ok=dfs(0,z);double sec=chrono::duration<double>(chrono::steady_clock::now()-startt).count();
 ofstream js(argv[7]);js<<"{\n  \"status\": \""<<(ok?"SAT":(sec>limitsec?"TIMEOUT":"UNSAT"))<<"\",\n  \"nodes\": "<<nodes<<",\n  \"dead_ends\": "<<dead<<",\n  \"seconds\": "<<setprecision(17)<<sec<<",\n  \"trace_fnv64\": \""<<hex<<setw(16)<<setfill('0')<<traceh<<dec<<"\",\n  \"candidate_counts\": [";for(int c=0;c<9;c++){if(c)js<<",";js<<cand[c].size();}js<<"]";
 if(ok){js<<",\n  \"covers\": [\n";for(int c=0;c<9;c++){js<<"    [";bool first=true;Bits const&b=cand[c][choice[c]];for(int f=0;f<NF;f++)if((b.w[f>>6]>>(f&63))&1ULL){if(!first)js<<",";first=false;js<<f;}js<<"]"<<(c==8?"\n":",\n");}js<<"  ]";}
 js<<"\n}\n";js.close();
 cout<<"{\"status\":\""<<(ok?"SAT":(sec>limitsec?"TIMEOUT":"UNSAT"))<<"\",\"nodes\":"<<nodes<<",\"seconds\":"<<sec<<"}\n";return ok?0:(sec>limitsec?124:10);
}
