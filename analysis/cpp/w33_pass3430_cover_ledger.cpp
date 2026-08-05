#include <algorithm>
#include <array>
#include <bitset>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <queue>
#include <stdexcept>
#include <string>
#include <tuple>
#include <unordered_map>
#include <unordered_set>
#include <vector>
using namespace std;

constexpr int NR=540, NC=240, COVER=60, RW=9;
struct Key { array<uint64_t,RW> w{}; bool operator==(Key const&o) const { return w==o.w; } };
struct Hash { size_t operator()(Key const&k) const noexcept { uint64_t h=0x9e3779b97f4a7c15ULL; for(uint64_t x:k.w){x^=x>>30;x*=0xbf58476d1ce4e5b9ULL;x^=x>>27;x*=0x94d049bb133111ebULL;x^=x>>31;h^=x+0x9e3779b97f4a7c15ULL+(h<<6)+(h>>2);} return size_t(h); } };
struct Geometry { array<array<uint16_t,4>,NR> rowcols{}; array<vector<uint16_t>,NC> colrows; vector<vector<uint16_t>> gens; };

static inline bool has(const Key&k,int r){return (k.w[r/64]>>(r%64))&1ULL;}
static vector<int> rows(const Key&k){vector<int>v;v.reserve(COVER);for(int r=0;r<NR;r++)if(has(k,r))v.push_back(r);return v;}
static bool key_less(const Key&a,const Key&b){for(int r=0;r<NR;r++){bool x=has(a,r),y=has(b,r);if(x!=y)return x>y;}return false;}
static Key transform(const Key&k,const vector<uint16_t>&g){Key y;for(int w=0;w<RW;w++){uint64_t x=k.w[w];while(x){int b=__builtin_ctzll(x);x&=x-1;int r=64*w+b;if(r<NR){int s=g[r];y.w[s/64]|=1ULL<<(s%64);}}}return y;}

static Geometry load_geometry(const string&path){
  ifstream in(path); if(!in) throw runtime_error("cannot open geometry");
  int nr,nc,ng;in>>nr>>nc>>ng;if(nr!=NR||nc!=NC||ng<=0)throw runtime_error("bad geometry header");
  Geometry g;g.gens.assign(ng,vector<uint16_t>(NR));
  for(int r=0;r<NR;r++)for(int j=0;j<4;j++){int c;in>>c;if(c<0||c>=NC)throw runtime_error("bad column");g.rowcols[r][j]=uint16_t(c);g.colrows[c].push_back(uint16_t(r));}
  for(auto&perm:g.gens)for(int r=0;r<NR;r++){int s;in>>s;if(s<0||s>=NR)throw runtime_error("bad permutation");perm[r]=uint16_t(s);}
  for(int c=0;c<NC;c++)if(g.colrows[c].size()!=9)throw runtime_error("column degree is not nine");
  return g;
}

struct Enumerator {
  Geometry const&g; bitset<NC> covered; vector<uint16_t> chosen; vector<Key> covers; uint64_t nodes=0;
  explicit Enumerator(Geometry const&gg):g(gg){covers.reserve(394200);}
  bool viable(int r) const {for(int j=0;j<4;j++)if(covered[g.rowcols[r][j]])return false;return true;}
  void add(int r){chosen.push_back(uint16_t(r));for(int j=0;j<4;j++)covered.set(g.rowcols[r][j]);}
  void remove(int r){for(int j=0;j<4;j++)covered.reset(g.rowcols[r][j]);chosen.pop_back();}
  void dfs(){
    nodes++;
    if(covered.count()==NC){if(chosen.size()!=COVER)throw runtime_error("wrong cover size");Key k;for(int r:chosen)k.w[r/64]|=1ULL<<(r%64);covers.push_back(k);return;}
    int best=-1,bestcount=1000;array<uint16_t,9> candidates{};int nbest=0;
    for(int c=0;c<NC;c++)if(!covered[c]){
      int count=0;array<uint16_t,9> local{};
      for(uint16_t r:g.colrows[c])if(viable(r))local[count++]=r;
      if(count==0)return;
      if(count<bestcount){best=c;bestcount=count;nbest=count;candidates=local;if(count==1)break;}
    }
    if(best<0)return;
    for(int z=0;z<nbest;z++){int r=candidates[z];add(r);dfs();remove(r);}
  }
  void run(){add(0);dfs();remove(0);sort(covers.begin(),covers.end(),key_less);if(covers.size()!=394200)throw runtime_error("fixed-frame count mismatch");}
};

static void write_fixed(const string&path,const vector<Key>&covers){ofstream out(path,ios::binary);uint64_t n=covers.size();out.write((char*)&n,8);for(auto const&k:covers){auto rs=rows(k);if(rs.size()!=COVER)throw runtime_error("bad key");for(int r:rs){uint16_t u=r;out.write((char*)&u,2);}}}
static vector<Key> read_fixed(const string&path){ifstream in(path,ios::binary);if(!in)throw runtime_error("cannot open fixed cover binary");uint64_t n;in.read((char*)&n,8);vector<Key> out(n);for(Key&k:out)for(int j=0;j<COVER;j++){uint16_t r;in.read((char*)&r,2);if(r>=NR)throw runtime_error("bad row in binary");k.w[r/64]|=1ULL<<(r%64);}return out;}

struct OrbitRecord {int orbit_size,stabilizer,sample_hits;vector<int> representative;};
static vector<OrbitRecord> reduce_orbits(const Geometry&g,const vector<Key>&sample){
  unordered_map<Key,uint8_t,Hash> mark;mark.reserve(2*sample.size());for(auto const&k:sample)mark.emplace(k,0);
  vector<OrbitRecord> records;records.reserve(327);uint64_t marked=0,total=0;
  for(auto const&seed:sample){auto it0=mark.find(seed);if(it0==mark.end()||it0->second)continue;
    unordered_set<Key,Hash> seen;seen.reserve(30000);vector<Key> queue;queue.reserve(30000);queue.push_back(seed);seen.insert(seed);size_t head=0;int hits=0;Key canonical=seed;
    while(head<queue.size()){
      Key x=queue[head++];if(key_less(x,canonical))canonical=x;
      if(has(x,0)){auto it=mark.find(x);if(it!=mark.end()&&!it->second){it->second=1;marked++;hits++;}}
      for(auto const&gen:g.gens){Key y=transform(x,gen);if(seen.insert(y).second)queue.push_back(y);}
    }
    int os=int(queue.size());if(25920%os)throw runtime_error("orbit does not divide group order");int st=25920/os;total+=os;
    records.push_back({os,st,hits,rows(canonical)});
  }
  if(marked!=sample.size())throw runtime_error("not all fixed-frame covers marked");
  if(records.size()!=327)throw runtime_error("orbit count mismatch");
  if(total!=3547800)throw runtime_error("global cover count mismatch");
  sort(records.begin(),records.end(),[](auto const&a,auto const&b){if(a.stabilizer!=b.stabilizer)return a.stabilizer<b.stabilizer;return a.representative<b.representative;});
  unordered_map<int,int> hist;for(auto const&r:records)hist[r.stabilizer]++;
  if(hist[2]!=228||hist[4]!=84||hist[8]!=15)throw runtime_error("stabilizer histogram mismatch");
  return records;
}

static void write_json(const string&path,const vector<OrbitRecord>&records,uint64_t fixed_count,uint64_t nodes){
  ofstream out(path);out<<"{\n  \"schema\": \"w33.pass3430_3433.canonical_cover_representatives.v1\",\n  \"status\": \"PASS_327_CANONICAL_REPRESENTATIVE_LEDGER\",\n";
  out<<"  \"fixed_frame_covers\": "<<fixed_count<<",\n  \"algorithm_x_nodes\": "<<nodes<<",\n  \"group_order\": 25920,\n  \"global_covers\": 3547800,\n  \"orbits\": [\n";
  for(size_t i=0;i<records.size();i++){auto const&r=records[i];if(i)out<<",\n";out<<"    {\"orbit_size\":"<<r.orbit_size<<",\"stabilizer_order\":"<<r.stabilizer<<",\"sample_hits\":"<<r.sample_hits<<",\"representative\":[";for(size_t j=0;j<r.representative.size();j++){if(j)out<<",";out<<r.representative[j];}out<<"]}";}
  out<<"\n  ],\n  \"boundary\": \"Representatives are canonical only in the live Pass-1801 frame labeling. Switch components require the separately checked legal-switch artifact.\"\n}\n";
}

int main(int argc,char**argv){
  try{
    if(argc!=4){cerr<<"usage: ledger GEOMETRY FIXED.bin LEDGER.json\n";return 2;}
    Geometry geometry=load_geometry(argv[1]);vector<Key> fixed;uint64_t nodes=0;
    if(filesystem::exists(argv[2])) fixed=read_fixed(argv[2]);
    else {Enumerator e(geometry);e.run();nodes=e.nodes;fixed=move(e.covers);write_fixed(argv[2],fixed);}
    if(fixed.size()!=394200)throw runtime_error("fixed binary count mismatch");
    auto records=reduce_orbits(geometry,fixed);write_json(argv[3],records,fixed.size(),nodes);
    cout<<"PASS_327_CANONICAL_REPRESENTATIVE_LEDGER fixed="<<fixed.size()<<" orbits="<<records.size()<<"\n";
    return 0;
  }catch(exception const&e){cerr<<"FAIL: "<<e.what()<<"\n";return 1;}
}
