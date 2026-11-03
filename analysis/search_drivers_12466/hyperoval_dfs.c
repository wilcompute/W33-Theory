/* 12525: an independent exhaustive search for hyperovals of W(3,q), sharing no solver code with CP-SAT or CaDiCaL.
   Input file: n_points n_lines q ; then each line's q+1 point ids; then n_cases, each case: k fixed lines, then m banned lines.
   Search: every point is on 0 or 2 chosen lines.  Take a point on exactly 1 chosen line with the fewest available lines; branch on the
   one further line (earlier candidates become banned in later branches, so each solution is visited exactly once).
   Prune: W - chosen >= size of a greedy set of pairwise non-collinear once-covered points, since each needs its own new line; and the Mantel count below.
   Output per case: solutions counted by weight, and nodes.  usage: hyperoval_dfs file W first last */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAXP 2400
#define MAXQ 14
static int np, nl, q, W;
static int L[MAXP][MAXQ], TH[MAXP][MAXQ];
static int thn[MAXP];
static signed char cov[MAXP];
static int banned[MAXP], chosen[MAXP], nchosen;
static unsigned char *col;
static long long sols[MAXP], nodes;
#define COL(a,b) col[(a)*np+(b)]

static int line_ok(int l) {
    if (chosen[l] || banned[l]) return 0;
    for (int i = 0; i <= q; i++) if (cov[L[l][i]] >= 2) return 0;
    return 1;
}
static void add_line(int l) { chosen[l] = 1; nchosen++; for (int i = 0; i <= q; i++) cov[L[l][i]]++; }
static void del_line(int l) { chosen[l] = 0; nchosen--; for (int i = 0; i <= q; i++) cov[L[l][i]]--; }

static void dfs(void) {
    nodes++;
    int best = -1, bestc = 1 << 30, once = 0;
    static int oncep[MAXP];
    int local[MAXP];
    (void)local;
    for (int p = 0; p < np; p++) if (cov[p] == 1) {
        int c = 0;
        for (int k = 0; k <= q; k++) if (line_ok(TH[p][k])) c++;
        if (c == 0) return;
        oncep[once++] = p;
        if (c < bestc) { bestc = c; best = p; }
    }
    if (once == 0) { sols[nchosen]++; return; }
    int rem = W - nchosen;
    if (rem <= 0) return;
    /* greedy pairwise non-collinear once-points: each needs a distinct new line */
    int ind[256], ni = 0;
    for (int i = 0; i < once && ni <= rem; i++) {
        int p = oncep[i], ok = 1;
        for (int j = 0; j < ni; j++) if (COL(p, ind[j])) { ok = 0; break; }
        if (ok) ind[ni++] = p;
    }
    if (ni > rem) return;
    if (once > rem * (q + 1)) return;
    /* Let a further lines complete the set.  Their a(q+1) incidences: `once` fill once-covered points, and the rest are on points covered
       by exactly two of the new lines.  The new lines meet pairwise in at most one point and have no triangles (GQ), so by Mantel they have
       at most a^2/4 meeting pairs.  Hence a(q+1) - once <= a^2/2, and a(q+1) - once is even.  Keep only a <= rem satisfying this. */
    {
        int feasible = 0;
        for (int a = ni; a <= rem && !feasible; a++) {
            int d = a * (q + 1) - once;
            if (d < 0 || (d & 1)) continue;
            if (2 * d > a * a) continue;
            if (((nchosen + a) & 1)) continue;      /* even sets have even weight */
            feasible = 1;
        }
        if (!feasible) return;
    }
    int cand[MAXQ], nc = 0;
    for (int k = 0; k <= q; k++) if (line_ok(TH[best][k])) cand[nc++] = TH[best][k];
    for (int i = 0; i < nc; i++) {
        add_line(cand[i]);
        dfs();
        del_line(cand[i]);
        banned[cand[i]]++;
    }
    for (int i = 0; i < nc; i++) banned[cand[i]]--;
}

int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "r"); W = atoi(argv[2]);
    int first = atoi(argv[3]), last = atoi(argv[4]);
    if (fscanf(f, "%d %d %d", &np, &nl, &q) != 3) return 1;
    for (int j = 0; j < nl; j++) for (int i = 0; i <= q; i++) {
        if (fscanf(f, "%d", &L[j][i]) != 1) return 1;
        TH[L[j][i]][thn[L[j][i]]++] = j;
    }
    col = calloc((size_t)np * np, 1);
    for (int j = 0; j < nl; j++) for (int a = 0; a <= q; a++) for (int b = 0; b <= q; b++) if (a != b) COL(L[j][a], L[j][b]) = 1;
    int ncase; if (fscanf(f, "%d", &ncase) != 1) return 1;
    long long totalsol = 0;
    for (int c = 0; c < ncase; c++) {
        int k, m; static int fx[MAXP], bn[MAXP];
        if (fscanf(f, "%d", &k) != 1) return 1;
        for (int i = 0; i < k; i++) if (fscanf(f, "%d", &fx[i]) != 1) return 1;
        if (fscanf(f, "%d", &m) != 1) return 1;
        for (int i = 0; i < m; i++) if (fscanf(f, "%d", &bn[i]) != 1) return 1;
        if (c < first || c >= last) continue;
        memset(cov, 0, sizeof(cov)); memset(chosen, 0, sizeof(chosen)); memset(banned, 0, sizeof(banned)); memset(sols, 0, sizeof(sols)); nodes = 0; nchosen = 0;
        for (int i = 0; i < m; i++) banned[bn[i]] = 1;
        for (int i = 0; i < k; i++) add_line(fx[i]);
        dfs();
        printf("case %d nodes %lld sols", c, nodes);
        for (int w = 0; w < MAXP; w++) if (sols[w]) { printf(" %d:%lld", w, sols[w]); totalsol += sols[w]; }
        printf("\n"); fflush(stdout);
    }
    printf("DONE total_solutions %lld\n", totalsol);
    return 0;
}
