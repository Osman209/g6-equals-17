/* fast_enumerate.c — the same enumeration as code/verify_degree3_kernels.py, in C.
 *
 * COVERS [P3, §2a] — an optional accelerator.  The Python script is the readable
 * definition of what is computed; this file exists because re-deriving the c = 6 and
 * c = 0 profiles in pure Python takes hours and here takes minutes.  Both write the same
 * data/degree3_kernels_c<c>.json.
 *
 *   cc -O2 -o fast_enumerate code/fast_enumerate.c
 *   ./fast_enumerate 12 > data/degree3_kernels_c12.json
 *   ./fast_enumerate 6  > data/degree3_kernels_c6.json
 *   ./fast_enumerate 0  > data/degree3_kernels_c0.json
 *
 * What it does, in the notation of [P3, §2a]:
 *   1. builds M = K12 + E - F for the given c;
 *   2. enumerates every triangle decomposition of M;
 *   3. keeps those with tau(G) = 5, i.e. with no four disjoint triangles partitioning the
 *      twelve cards (3+3+3+2 = 11 < 12, so no degree-two symbol can take part);
 *   4. reduces under Aut(M) by marking each orbit whole as it is first met;
 *   5. prints the representatives as a JSON list of lists of triangle indices, the
 *      triangles being C(12,3) in lexicographic order.
 *
 * A pair of capacity two can be served by its two triangles in either order, so the
 * search reaches such a decomposition once per order.  The orbit marking absorbs the
 * repeats, and the count of distinct decompositions is reported on stderr.
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define V 12
#define NPAIR 66
#define NTRI 220
#define HBITS 26
#define HSIZE (1u << HBITS)

static int PI[V][V], TIDX[V][V][V];
static int TRIv[NTRI][3], trA[NTRI], trB[NTRI], trC[NTRI], trV[NTRI], ntri = 0;
static int pairTri[NPAIR][64], pairTriN[NPAIR];
static signed char cap[NPAIR];
static int chosen[32], NT, NP;
static uint16_t *permTri;
static uint64_t *seen;
static long long paths = 0, distinct = 0, kernels = 0, reps = 0;
static int M[6][2] = {{0,1},{2,3},{4,5},{6,7},{8,9},{10,11}};
static FILE *OUT;

static uint64_t fnv(const uint16_t *a, int n) {
    uint64_t h = 1469598103934665603ULL;
    for (int i = 0; i < n; i++) { h ^= a[i]; h *= 1099511628211ULL; }
    return h ? h : 1;
}
static int mark(uint64_t h) {                  /* 1 if already present */
    uint32_t i = (uint32_t)(h >> (64 - HBITS));
    while (seen[i]) { if (seen[i] == h) return 1; i = (i + 1) & (HSIZE - 1); }
    seen[i] = h; return 0;
}
static void isort(uint16_t *a, int n) {
    for (int i = 1; i < n; i++) { uint16_t k = a[i]; int j = i - 1;
        while (j >= 0 && a[j] > k) { a[j+1] = a[j]; j--; } a[j+1] = k; }
}
/* four disjoint triangles covering all twelve cards */
static int part(int covered, int k, int start) {
    if (k == 4) return covered == 0xFFF;
    for (int i = start; i < NT; i++) { int m = trV[chosen[i]];
        if (!(m & covered) && part(covered | m, k + 1, i + 1)) return 1; }
    return 0;
}
static void emit(void) {
    uint16_t cur[32], img[32];
    for (int i = 0; i < NT; i++) cur[i] = (uint16_t)chosen[i];
    isort(cur, NT);
    if (mark(fnv(cur, NT))) return;            /* a repeated search path, or a known orbit */
    distinct++;
    if (part(0, 0, 0)) {                       /* tau(G) <= 4: not a kernel */
        for (int q = 0; q < NP; q++) { uint16_t *tb = permTri + (size_t)q * NTRI;
            for (int i = 0; i < NT; i++) img[i] = tb[cur[i]];
            isort(img, NT); if (!mark(fnv(img, NT))) distinct++; }
        return;
    }
    kernels++; reps++;
    fprintf(OUT, "%s[%d", reps == 1 ? "" : ", ", cur[0]);
    for (int i = 1; i < NT; i++) fprintf(OUT, ", %d", cur[i]);
    fprintf(OUT, "]");
    for (int q = 0; q < NP; q++) { uint16_t *tb = permTri + (size_t)q * NTRI;
        for (int i = 0; i < NT; i++) img[i] = tb[cur[i]];
        isort(img, NT); if (!mark(fnv(img, NT))) { distinct++; kernels++; } }
}
static void dfs(int left, int depth) {
    if (left == 0) { paths++; emit(); return; }
    int best = -1, bestn = 1 << 30;
    for (int p = 0; p < NPAIR; p++) if (cap[p] > 0) {
        int n = 0;
        for (int k = 0; k < pairTriN[p]; k++) { int i = pairTri[p][k];
            if (cap[trA[i]] > 0 && cap[trB[i]] > 0 && cap[trC[i]] > 0) n++; }
        if (n == 0) return;
        if (n < bestn) { bestn = n; best = p; if (n == 1) break; }
    }
    for (int k = 0; k < pairTriN[best]; k++) { int i = pairTri[best][k];
        if (cap[trA[i]] <= 0 || cap[trB[i]] <= 0 || cap[trC[i]] <= 0) continue;
        cap[trA[i]]--; cap[trB[i]]--; cap[trC[i]]--;
        chosen[depth] = i; dfs(left - 3, depth + 1);
        cap[trA[i]]++; cap[trB[i]]++; cap[trC[i]]++;
    }
}
static int nfp, nep, fperm[720][6], eperm[720][6], nF, nE, work[6];
static void genF(int k, int used) {
    if (k == nF) { memcpy(fperm[nfp++], work, sizeof(work)); return; }
    for (int i = 0; i < nF; i++) if (!(used >> i & 1)) { work[k] = i; genF(k+1, used | 1<<i); }
}
static void genE(int k, int used) {
    if (k == nE) { memcpy(eperm[nep++], work, sizeof(work)); return; }
    for (int i = 0; i < nE; i++) if (!(used >> i & 1)) { work[k] = nF+i; genE(k+1, used | 1<<i); }
}
int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: fast_enumerate <c in {0,6,12}>\n"); return 2; }
    int c = atoi(argv[1]);
    if (c != 0 && c != 6 && c != 12) { fprintf(stderr, "c must be 0, 6 or 12\n"); return 2; }
    OUT = stdout;
    int np = 0;
    for (int a = 0; a < V; a++) for (int b = a+1; b < V; b++) PI[a][b] = PI[b][a] = np++;
    for (int a = 0; a < V; a++) for (int b = a+1; b < V; b++) for (int d = b+1; d < V; d++) {
        TRIv[ntri][0]=a; TRIv[ntri][1]=b; TRIv[ntri][2]=d; TIDX[a][b][d]=ntri;
        trA[ntri]=PI[a][b]; trB[ntri]=PI[a][d]; trC[ntri]=PI[b][d];
        trV[ntri]=(1<<a)|(1<<b)|(1<<d); ntri++; }
    for (int p = 0; p < NPAIR; p++) pairTriN[p] = 0;
    for (int i = 0; i < ntri; i++) { int ps[3] = {trA[i], trB[i], trC[i]};
        for (int j = 0; j < 3; j++) pairTri[ps[j]][pairTriN[ps[j]]++] = i; }
    for (int p = 0; p < NPAIR; p++) cap[p] = 1;
    nF = c / 2; nE = 6 - nF;
    for (int i = 0; i < 6; i++) cap[PI[M[i][0]][M[i][1]]] = (i < nF) ? 0 : 2;
    int total = 0; for (int p = 0; p < NPAIR; p++) total += cap[p];
    NT = total / 3;
    if (nF) genF(0, 0); else nfp = 1;
    if (nE) genE(0, 0); else nep = 1;
    NP = nfp * nep * 64;
    permTri = malloc((size_t)NP * NTRI * sizeof(uint16_t));
    seen = calloc(HSIZE, sizeof(uint64_t));
    if (!permTri || !seen) { fprintf(stderr, "out of memory\n"); return 1; }
    int pn = 0;
    for (int f = 0; f < nfp; f++) for (int e = 0; e < nep; e++) for (int fl = 0; fl < 64; fl++) {
        int order[6], p[V];
        for (int k = 0; k < nF; k++) order[k] = fperm[f][k];
        for (int k = 0; k < nE; k++) order[nF+k] = eperm[e][k];
        for (int k = 0; k < 6; k++) { int A=M[k][0], B=M[k][1];
            int ta=M[order[k]][0], tb=M[order[k]][1];
            if (fl >> k & 1) { int t=ta; ta=tb; tb=t; }
            p[A]=ta; p[B]=tb; }
        for (int i = 0; i < ntri; i++) { int x=p[TRIv[i][0]], y=p[TRIv[i][1]], z=p[TRIv[i][2]], t;
            if (x>y) {t=x;x=y;y=t;} if (y>z) {t=y;y=z;z=t;} if (x>y) {t=x;x=y;y=t;}
            permTri[(size_t)pn*NTRI + i] = (uint16_t)TIDX[x][y][z]; }
        pn++;
    }
    fprintf(OUT, "[");
    dfs(total, 0);
    fprintf(OUT, "]\n");
    fprintf(stderr, "c=%d  |Aut(M)|=%d  search paths %lld  distinct decompositions %lld  "
                    "with tau(G)=5 %lld  kernels up to isomorphism %lld\n",
            c, NP, paths, distinct, kernels, reps);
    return 0;
}
