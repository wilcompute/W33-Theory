#include <bits/stdc++.h>
using namespace std; using U=uint64_t;
int main(int argc,char**argv){
 if(argc!=2){cerr<<"usage: worker syndromes.txt\n";return 2;}
 vector<U>s(240);ifstream in(argv[1]);if(!in)return 2;for(auto &x:s)in>>x;
 vector<U> l1=s,l2,l3;l2.reserve(28680);l3.reserve(2275280);
 for(int i=0;i<240;i++)for(int j=i+1;j<240;j++)l2.push_back(s[i]^s[j]);
 for(int i=0;i<240;i++)for(int j=i+1;j<240;j++)for(int k=j+1;k<240;k++)l3.push_back(s[i]^s[j]^s[k]);
 sort(l2.begin(),l2.end());vector<pair<U,int>>l2m;
 for(size_t i=0;i<l2.size();){size_t j=i+1;while(j<l2.size()&&l2[j]==l2[i])j++;l2m.push_back({l2[i],int(j-i)});i=j;}
 l2.clear();for(auto z:l2m)l2.push_back(z.first);
 auto prep=[](vector<U>&v){sort(v.begin(),v.end());v.erase(unique(v.begin(),v.end()),v.end());};prep(l1);prep(l3);
 cerr<<"lower unique "<<l1.size()<<" "<<l2.size()<<" "<<l3.size()<<"\n";
 size_t N=(size_t)240*239*238*237/24;vector<U>a(N);size_t q=0;
 for(int i=0;i<240;i++)for(int j=i+1;j<240;j++)for(int k=j+1;k<240;k++)for(int l=k+1;l<240;l++)a[q++]=s[i]^s[j]^s[k]^s[l];
 cerr<<"generated "<<q<<" sorting\n";sort(a.begin(),a.end());
 unsigned long long uniqueErr=0,ambErr=0,shadowErr[4]={0,0,0,0},synd=0,ambSynd=0;
 map<unsigned long long,unsigned long long>runSynd,runErr;map<pair<int,unsigned long long>,unsigned long long>pairJointSynd,pairJointErr;
 U zeroCount=0;size_t i=0;
 while(i<a.size()){
  size_t j=i+1;while(j<a.size()&&a[j]==a[i])j++;unsigned long long c=j-i;synd++;runSynd[c]++;runErr[c]+=c;
  U x=a[i];int lower=-1;if(x==0)lower=0;else if(binary_search(l1.begin(),l1.end(),x))lower=1;else if(binary_search(l2.begin(),l2.end(),x))lower=2;else if(binary_search(l3.begin(),l3.end(),x))lower=3;
  if(lower>=0){shadowErr[lower]+=c;if(lower==2){auto it=lower_bound(l2m.begin(),l2m.end(),make_pair(x,-1),[](auto a,auto b){return a.first<b.first;});int pc=it->second;pairJointSynd[{pc,c}]++;pairJointErr[{pc,c}]+=c;}}
  else if(c==1)uniqueErr++;else{ambErr+=c;ambSynd++;}
  if(x==0)zeroCount=c;i=j;
 }
 cout<<"{\n\"total_errors\":"<<a.size()<<",\n\"distinct_syndromes\":"<<synd<<",\n\"unique_minimum_errors\":"<<uniqueErr<<",\n\"ambiguous_minimum_errors\":"<<ambErr<<",\n\"ambiguous_minimum_syndromes\":"<<ambSynd<<",\n\"shadow_by_weight0\":"<<shadowErr[0]<<",\n\"shadow_by_weight1\":"<<shadowErr[1]<<",\n\"shadow_by_weight2\":"<<shadowErr[2]<<",\n\"shadow_by_weight3\":"<<shadowErr[3]<<",\n\"zero_syndrome_weight4\":"<<zeroCount<<",\n\"run_syndrome_hist\":{";
 bool first=true;for(auto[c,n]:runSynd){if(!first)cout<<",";first=false;cout<<"\""<<c<<"\":"<<n;}cout<<"},\n\"run_error_hist\":{";first=true;for(auto[c,n]:runErr){if(!first)cout<<",";first=false;cout<<"\""<<c<<"\":"<<n;}cout<<"},\n\"pair_shadow_joint_syndromes\":{";first=true;for(auto &kv:pairJointSynd){if(!first)cout<<",";first=false;cout<<"\"p"<<kv.first.first<<"_q"<<kv.first.second<<"\":"<<kv.second;}cout<<"},\n\"pair_shadow_joint_errors\":{";first=true;for(auto &kv:pairJointErr){if(!first)cout<<",";first=false;cout<<"\"p"<<kv.first.first<<"_q"<<kv.first.second<<"\":"<<kv.second;}cout<<"}\n}\n";
}
