// Pass 2511 -- the K8 criterion, executed in C++.
//
// Pass 2496: chi(H)=9 requires some cover whose disjointness link contains K8.
// Links are constant on PSp(4,3)-orbits, so at most 327 link types.
//
// Pass 2503 failed twice in Python (wrong generators, then a form-convention
// mismatch); Pass 2510 exported the correct 540-frame action from GAP.  Python
// then timed out on 8.47M cover generations, so this does the same work in C++.
//
// It VALIDATES against the frozen |link(canonical)| = 13648 before reporting
// anything new.
//
// Input  : data/w33_pass2510_frame_action.json  (1-based generators)
//          data/w33_pass2511_reps.txt           (327 lines of 60 frame indices)
// Output : link sizes and clique numbers per orbit, to stdout.

#include <cstdio>
#include <cstdint>
#include <cstring>
#include <vector>
#include <string>
#include <unordered_set>
#include <algorithm>
#include <functional>
#include <cctype>
#include <cstdlib>
using namespace std;

static const int NF = 540;        // frames
static const int W  = 9;          // 540 bits -> 9 * 64

struct Mask {
    uint64_t w[W];
    bool operator==(const Mask& o) const { return memcmp(w, o.w, sizeof(w)) == 0; }
};
struct MaskHash {
    size_t operator()(const Mask& m) const {
        size_t h = 1469598103934665603ULL;
        for (int i = 0; i < W; i++) { h ^= m.w[i]; h *= 1099511628211ULL; }
        return h;
    }
};
static inline void setbit(Mask& m, int b) { m.w[b >> 6] |= 1ULL << (b & 63); }
static inline bool disjoint(const Mask& a, const Mask& b) {
    for (int i = 0; i < W; i++) if (a.w[i] & b.w[i]) return false;
    return true;
}

int main(int argc, char** argv) {
    if (argc < 3) { fprintf(stderr, "usage: %s gens.txt reps.txt [maxorbits]\n", argv[0]); return 2; }
    int maxOrbits = (argc > 3) ? atoi(argv[3]) : 327;

    // --- generators: whitespace-separated, one permutation per line, 0-based ---
    vector<vector<int>> gens;
    { FILE* f = fopen(argv[1], "r");
      if (!f) { fprintf(stderr, "cannot open %s\n", argv[1]); return 1; }
      vector<int> cur; int x;
      char line[65536];
      while (fgets(line, sizeof(line), f)) {
          cur.clear(); char* p = line;
          while (sscanf(p, "%d", &x) == 1) {
              cur.push_back(x);
              while (*p && isspace((unsigned char)*p)) p++;
              while (*p && !isspace((unsigned char)*p)) p++;
          }
          if ((int)cur.size() == NF) gens.push_back(cur);
      }
      fclose(f); }
    printf("generators: %zu\n", gens.size());

    // --- close the permutation group ---
    vector<vector<int>> G;
    { vector<int> id(NF); for (int i = 0; i < NF; i++) id[i] = i;
      unordered_set<string> seen;
      auto key = [](const vector<int>& p) {
          return string((const char*)p.data(), p.size() * sizeof(int)); };
      G.push_back(id); seen.insert(key(id));
      for (size_t head = 0; head < G.size(); head++) {
          for (auto& g : gens) {
              vector<int> q(NF);
              for (int i = 0; i < NF; i++) q[i] = g[G[head][i]];
              if (seen.insert(key(q)).second) G.push_back(q);
          }
      } }
    printf("group order on frames: %zu\n", G.size());

    // --- orbit representatives ---
    vector<vector<int>> reps;
    { FILE* f = fopen(argv[2], "r");
      if (!f) { fprintf(stderr, "cannot open %s\n", argv[2]); return 1; }
      char line[65536];
      while (fgets(line, sizeof(line), f)) {
          vector<int> cur; int x; char* p = line;
          while (sscanf(p, "%d", &x) == 1) {
              cur.push_back(x);
              while (*p && isspace((unsigned char)*p)) p++;
              while (*p && !isspace((unsigned char)*p)) p++;
          }
          if (cur.size() == 60) reps.push_back(cur);
      }
      fclose(f); }
    printf("orbit representatives: %zu\n", reps.size());

    // --- all covers ---
    unordered_set<Mask, MaskHash> cset;
    cset.reserve(4000000);
    for (auto& r : reps)
        for (auto& g : G) {
            Mask m; memset(&m, 0, sizeof(m));
            for (int x : r) setbit(m, g[x]);
            cset.insert(m);
        }
    vector<Mask> covers(cset.begin(), cset.end());
    printf("covers: %zu   (frozen 3547800)   match=%d\n",
           covers.size(), (int)(covers.size() == 3547800));
    fflush(stdout);

    // --- per-orbit link size and clique number ---
    printf("\n%-6s %-12s %-10s %s\n", "orbit", "|link|", "clique", "K8?");
    for (int oi = 0; oi < (int)reps.size() && oi < maxOrbits; oi++) {
        Mask c; memset(&c, 0, sizeof(c));
        for (int x : reps[oi]) setbit(c, x);
        vector<Mask> link;
        for (auto& m : covers) if (disjoint(m, c)) link.push_back(m);

        // greedy-bounded exact clique on the link
        int n = (int)link.size();
        vector<vector<int>> adj(n);
        for (int i = 0; i < n; i++)
            for (int j = i + 1; j < n; j++)
                if (disjoint(link[i], link[j])) { adj[i].push_back(j); adj[j].push_back(i); }
        int best = 0;
        vector<int> cur;
        // simple branch and bound; the target is only 8, so this terminates fast
        function<void(vector<int>&)> expand = [&](vector<int>& cand) {
            if (cand.empty()) { best = max(best, (int)cur.size()); return; }
            if ((int)cur.size() + (int)cand.size() <= best) return;
            if (best >= 8) return;                 // we only need to know if K8 exists
            for (size_t k = 0; k < cand.size(); k++) {
                int v = cand[k];
                vector<int> nxt;
                for (size_t l = k + 1; l < cand.size(); l++) {
                    int u = cand[l];
                    if (binary_search(adj[v].begin(), adj[v].end(), u)) nxt.push_back(u);
                }
                cur.push_back(v);
                best = max(best, (int)cur.size());
                expand(nxt);
                cur.pop_back();
                if (best >= 8) return;
            }
        };
        for (int i = 0; i < n; i++) sort(adj[i].begin(), adj[i].end());
        vector<int> all(n); for (int i = 0; i < n; i++) all[i] = i;
        expand(all);
        printf("%-6d %-12d %-10d %s\n", oi, n, best, best >= 8 ? "YES" : "no");
        fflush(stdout);
    }
    return 0;
}
