#include <bits/stdc++.h>
using namespace std;
struct T{uint64_t s; array<uint64_t,4> m;};
bool operator<(T const&a,T const&b){return a.s<b.s;}
int main(int argc,char**argv){int trials=argc>1?atoi(argv[1]):500;const char* path=argc>2?argv[2]:"data/w33_pass1848_syndrome_columns.txt";vector<uint64_t>c(240);ifstream in(path);for(auto&x:c)in>>x;
vector<uint64_t> q;q.reserve(134810340ULL);for(int i=0;i<240;i++)for(int j=i+1;j<240;j++){auto a=c[i]^c[j];for(int k=j+1;k<240;k++){auto b=a^c[k];for(int l=k+1;l<240;l++)q.push_back(b^c[l]);}}sort(q.begin(),q.end());q.erase(unique(q.begin(),q.end()),q.end());cerr<<"lower "<<q.size()<<"\n";
vector<T> tr;tr.reserve(2275280);for(int i=0;i<240;i++)for(int j=i+1;j<240;j++)for(int k=j+1;k<240;k++){T z{};z.s=c[i]^c[j]^c[k];z.m[i>>6]|=1ULL<<(i&63);z.m[j>>6]|=1ULL<<(j&63);z.m[k>>6]|=1ULL<<(k&63);tr.push_back(z);}sort(tr.begin(),tr.end());cerr<<"triples "<<tr.size()<<"\n";
mt19937_64 rng(93731);int tested=0,lower=0,coll=0,sing=0; cout<<"["; bool firstout=true;
for(int tt=0;tt<trials;tt++){array<int,6> e;unordered_set<int> u;while(u.size()<6)u.insert(rng()%240);copy(u.begin(),u.end(),e.begin());sort(e.begin(),e.end());uint64_t s=0;array<uint64_t,4> em{};for(int x:e){s^=c[x];em[x>>6]|=1ULL<<(x&63);}tested++;
 if(binary_search(q.begin(),q.end(),s)){lower++;continue;}
 bool other=false;array<uint64_t,4> found{};
 for(auto const&a:tr){uint64_t want=s^a.s;T lo{};lo.s=want;auto it=lower_bound(tr.begin(),tr.end(),lo);for(;it!=tr.end()&&it->s==want;++it){bool dis=1;for(int z=0;z<4;z++)if(a.m[z]&it->m[z]){dis=0;break;}if(!dis)continue;array<uint64_t,4> fm;for(int z=0;z<4;z++)fm[z]=a.m[z]|it->m[z];if(fm!=em){other=true;found=fm;break;}}if(other)break;}
 if(other){coll++;continue;}
 if(!firstout)cout<<",";firstout=false;cout<<"{\"support\":[";for(int z=0;z<6;z++){if(z)cout<<",";cout<<e[z];}cout<<"],\"syndrome\":"<<s<<"}";sing++;
}
cout<<"]\n";cerr<<"DONE tested "<<tested<<" lower "<<lower<<" coll "<<coll<<" singleton "<<sing<<"\n";return 0;}
