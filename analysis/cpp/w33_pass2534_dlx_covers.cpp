// Pass 2534 -- Algorithm X over the canonical 540x240 frame/edge incidence matrix.
//
// Self-contained: takes only M (from w33_pass1801_1805_common.build_geometry()),
// no dependency on the Pass-1511 representatives whose frame labelling could not be
// recovered (Passes 2511, 2517).
//
// Validation gate: the count of exact covers through frame 0 must reproduce Pass
// 1821's 394,200.  Anything else and the run is discarded.
//
//   argv[1] : M as "540 240" then one line per row listing its 4 column indices
//   argv[2] : "count" (default) or a path to dump the covers as 60-index lines

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <vector>
using namespace std;

static const int NR = 540, NC = 240, K = 4;

static int rowcols[NR][K];
static vector<int> colrows[NC];      // 9 rows each

static uint64_t covered[4];          // 240 columns -> 4 x 64
static bool     rowdead[NR];
static int      rowblock[NR];        // how many times this row is blocked
static int      chosen[64], depth = 0;
static long long solutions = 0, nodes = 0;
static FILE*    dump = nullptr;

static inline bool colcov(int c) { return covered[c >> 6] >> (c & 63) & 1ULL; }
static inline void setcol(int c)  { covered[c >> 6] |=  1ULL << (c & 63); }
static inline void clrcol(int c)  { covered[c >> 6] &= ~(1ULL << (c & 63)); }

static void select_row(int r, vector<int>& undo) {
    for (int k = 0; k < K; k++) {
        int c = rowcols[r][k];
        setcol(c);
        for (int r2 : colrows[c])
            if (!rowdead[r2]) { if (rowblock[r2]++ == 0) undo.push_back(r2); }
    }
}
static void unselect_row(int r, vector<int>& undo) {
    for (int k = 0; k < K; k++) {
        int c = rowcols[r][k];
        clrcol(c);
        for (int r2 : colrows[c]) rowblock[r2]--;
    }
    (void)undo;
}

static void search() {
    nodes++;
    // pick the uncovered column with fewest available rows
    int best = -1, bestn = 1 << 30;
    for (int c = 0; c < NC; c++) {
        if (colcov(c)) continue;
        int n = 0;
        for (int r : colrows[c]) if (rowblock[r] == 0 && !rowdead[r]) n++;
        if (n < bestn) { bestn = n; best = c; if (n == 0) break; }
    }
    if (best < 0) {                                  // every column covered
        solutions++;
        if (dump) {
            for (int i = 0; i < depth; i++) fprintf(dump, "%d%c", chosen[i], i + 1 == depth ? '\n' : ' ');
        }
        return;
    }
    if (bestn == 0) return;

    vector<int> cand;
    for (int r : colrows[best]) if (rowblock[r] == 0 && !rowdead[r]) cand.push_back(r);
    for (int r : cand) {
        chosen[depth++] = r;
        vector<int> undo;
        select_row(r, undo);
        search();
        unselect_row(r, undo);
        depth--;
    }
}

int main(int argc, char** argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s M.txt [dumpfile]\n", argv[0]); return 2; }
    FILE* f = fopen(argv[1], "r");
    if (!f) { fprintf(stderr, "cannot open %s\n", argv[1]); return 1; }
    int nr, nc;
    if (fscanf(f, "%d %d", &nr, &nc) != 2 || nr != NR || nc != NC) {
        fprintf(stderr, "expected 540 240, got %d %d\n", nr, nc); return 1; }
    for (int r = 0; r < NR; r++)
        for (int k = 0; k < K; k++) {
            if (fscanf(f, "%d", &rowcols[r][k]) != 1) { fprintf(stderr, "short read\n"); return 1; }
            colrows[rowcols[r][k]].push_back(r);
        }
    fclose(f);
    for (int c = 0; c < NC; c++)
        if ((int)colrows[c].size() != 9) { fprintf(stderr, "column %d has %zu rows, expected 9\n", c, colrows[c].size()); return 1; }
    printf("M: 540 x 240, row degree 4, column degree 9   OK\n");

    if (argc > 2 && strcmp(argv[2], "count") != 0) dump = fopen(argv[2], "w");

    // fix frame 0, as Pass 1821 does
    memset(covered, 0, sizeof(covered));
    memset(rowblock, 0, sizeof(rowblock));
    memset(rowdead, 0, sizeof(rowdead));
    chosen[depth++] = 0;
    vector<int> undo;
    select_row(0, undo);
    search();

    printf("covers through frame 0 : %lld   (Pass 1821: 394200)   match=%d\n",
           solutions, (int)(solutions == 394200));
    printf("search nodes           : %lld\n", nodes);
    printf("implied global count    : %lld * 540 / 60 = %lld\n",
           solutions, solutions * 540 / 60);
    if (dump) fclose(dump);
    return 0;
}
