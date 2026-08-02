#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <set>
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;
struct K{array<uint64_t,3>w{};bool operator==(K const&o)const{return w==o.w;}bool operator<(K const&o)const{return w<o.w;}};
struct H{size_t operator()(K const&k)const noexcept{uint64_t h=0x9e3779b97f4a7c15ULL;for(auto x:k.w){x^=x>>30;x*=0xbf58476d1ce4e5b9ULL;x^=x>>27;x*=0x94d049bb133111ebULL;x^=x>>31;h^=x+0x9e3779b97f4a7c15ULL+(h<<6)+(h>>2);}return h;}};
K pack(array<int,45> const&a){K k;for(int i=0;i<45;i++)k.w[i/16]|=(uint64_t)a[i]<<(4*(i%16));return k;}
array<int,45> unpack(K const&k){array<int,45>a{};for(int i=0;i<45;i++)a[i]=(k.w[i/16]>>(4*(i%16)))&15;return a;}
int main(int argc,char**argv){
 if(argc!=2){cerr<<"usage: trade_search global_signatures720.json\n";return 2;}
 ifstream in(argv[1]);string s((istreambuf_iterator<char>(in)),{});vector<array<int,45>>V;vector<int>C;size_t p=0;
 while((p=s.find("\"count\":",p))!=string::npos){p+=8;C.push_back(stoi(s.substr(p)));p=s.find("\"vector\":[",p)+10;array<int,45>a{};for(int j=0;j<45;j++){a[j]=stoi(s.substr(p));p=s.find(j==44?']':',',p)+1;}V.push_back(a);}if(V.size()!=720)return 2;
 vector<int> old={90,206,290,99,373,415,554,610,640};array<bool,720>isold{};for(int x:old)isold[x]=1;vector<int>out;for(int i=0;i<720;i++)if(!isold[i])out.push_back(i);
 unordered_map<K,vector<pair<uint16_t,uint16_t>>,H>M;M.reserve(300000);for(int ii=0;ii<(int)out.size();ii++){int a=out[ii];for(int jj=ii+1;jj<(int)out.size();jj++){int b=out[jj];array<int,45>z{};for(int q=0;q<45;q++)z[q]=V[a][q]+V[b][q];M[pack(z)].push_back({a,b});}}
 set<array<int,9>> T2,T3,T4;
 auto make_tuple=[&](vector<int> rem,vector<int> add){vector<int>x;for(int z:old)if(find(rem.begin(),rem.end(),z)==rem.end())x.push_back(z);x.insert(x.end(),add.begin(),add.end());sort(x.begin(),x.end());if(x.size()!=9||unique(x.begin(),x.end())!=x.end())return array<int,9>{};array<int,9>a{};copy(x.begin(),x.end(),a.begin());return a;};
 for(int i=0;i<9;i++)for(int j=i+1;j<9;j++){array<int,45>t{};for(int q=0;q<45;q++)t[q]=V[old[i]][q]+V[old[j]][q];auto it=M.find(pack(t));if(it!=M.end())for(auto [a,b]:it->second){auto z=make_tuple({old[i],old[j]},{a,b});if(z[8])T2.insert(z);}}
 for(int i=0;i<9;i++)for(int j=i+1;j<9;j++)for(int k=j+1;k<9;k++){array<int,45>t{};for(int q=0;q<45;q++)t[q]=V[old[i]][q]+V[old[j]][q]+V[old[k]][q];for(int c:out){array<int,45>d{};bool ok=1;for(int q=0;q<45;q++){d[q]=t[q]-V[c][q];if(d[q]<0||d[q]>8){ok=0;break;}}if(!ok)continue;auto it=M.find(pack(d));if(it==M.end())continue;for(auto [a,b]:it->second){if(c==a||c==b)continue;auto z=make_tuple({old[i],old[j],old[k]},{a,b,c});if(z[8])T3.insert(z);}}}
 for(int i=0;i<9;i++)for(int j=i+1;j<9;j++)for(int k=j+1;k<9;k++)for(int l=k+1;l<9;l++){array<int,45>t{};for(int q=0;q<45;q++)t[q]=V[old[i]][q]+V[old[j]][q]+V[old[k]][q]+V[old[l]][q];for(auto const& [key,L]:M){auto a0=unpack(key);array<int,45>d{};bool ok=1;for(int q=0;q<45;q++){d[q]=t[q]-a0[q];if(d[q]<0||d[q]>8){ok=0;break;}}if(!ok)continue;K kd=pack(d);if(kd<key)continue;auto it=M.find(kd);if(it==M.end())continue;for(auto u:L)for(auto v:it->second){if(u.first==v.first||u.first==v.second||u.second==v.first||u.second==v.second)continue;auto z=make_tuple({old[i],old[j],old[k],old[l]},{u.first,u.second,v.first,v.second});if(z[8])T4.insert(z);}}}
 cout<<"{\"pair_trade_tuples\":[";bool f=1;for(auto&t:T2){if(!f)cout<<",";f=0;cout<<"[";for(int i=0;i<9;i++){if(i)cout<<",";cout<<t[i];}cout<<"]";}cout<<"],\"triple_trade_tuples\":[";f=1;for(auto&t:T3){if(!f)cout<<",";f=0;cout<<"[";for(int i=0;i<9;i++){if(i)cout<<",";cout<<t[i];}cout<<"]";}cout<<"],\"quad_trade_tuples\":[";f=1;for(auto&t:T4){if(!f)cout<<",";f=0;cout<<"[";for(int i=0;i<9;i++){if(i)cout<<",";cout<<t[i];}cout<<"]";}cout<<"]}\n";
 cerr<<"counts "<<T2.size()<<" "<<T3.size()<<" "<<T4.size()<<"\n";
}
