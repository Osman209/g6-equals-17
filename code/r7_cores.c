/* COVERS [P7, Lemma 5], first route; with r = 6 and n = 8 it reproduces the 463 cores of
   [P3, §3]. Needs nauty. usage: r7_cores r n. Run through code/verify_g7_lower.py. */
/* Cores for the two-deletion branch, any r:  n = 3r - 11 points (the cards left after
   deleting the four cards of x and the four of y from a (3r-3)-card family).
   A core is a multiset of blocks (symbols, as sets of points) with
     - every block of size 1, 2 or 3; every point in exactly r blocks;
     - every pair of points in some block;
     - the 3-blocks (triangles) pairwise intersecting, each of multiplicity <= MMAX;
     - no r-3 blocks cover all points (tau(core) = r - 2);
     - the n points give n distinct cards.
   Triangles are enumerated as intersecting multisets; each is completed by one 2-block on
   every uncovered pair, then any further 2-blocks the room allows, then 1-blocks.
   Cores are reduced up to isomorphism with nauty (point-block incidence graph).
   usage: cores r          (r = 6 must reproduce the 463 cores of [P3, §3]) */
#define MAXN 64
#include "nauty.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int R, N, MMAX, NEEDCOV;
static int T[200], nT;            /* all triangles as bitmasks */
static int chosen[64], nch;       /* chosen triangles (with repeats) */
static int tdeg[16];
static long long leaves=0, raw=0;

/* ---- hash set of canonical graphs ---- */
#define HS (1<<22)
typedef struct { int n; setword g[MAXN]; } CG;
static CG *store; static int nstore; static int *htab;
static unsigned long long hashg(setword *g,int n){ unsigned long long h=1469598103934665603ULL; for(int i=0;i<n;i++){ h^=g[i]; h*=1099511628211ULL; } return h; }
static FILE *out;

static int blocks[80], nb;
static int popc(int x){ return __builtin_popcount(x); }

static int covers_k(int k, int cov, int start){
  if(cov==(1<<N)-1) return 1;
  if(k==0) return 0;
  for(int i=start;i<nb;i++) if(covers_k(k-1, cov|blocks[i], i+1)) return 1;
  return 0;
}

static void emit(void){
  /* distinct cards */
  int card[16];
  for(int p=0;p<N;p++){ card[p]=0; }
  /* compare cards as sorted block-index sets: card p = set of block indices containing p */
  for(int p=0;p<N;p++) for(int q=p+1;q<N;q++){
    int same=1; for(int i=0;i<nb;i++) if(((blocks[i]>>p)&1)!=((blocks[i]>>q)&1)){same=0;break;}
    if(same) return;
  }
  (void)card;
  if(covers_k(R-3,0,0)) return;   /* tau(core) <= r-3 */
  raw++;
  /* canonical form: vertices 0..N-1 points, N..N+nb-1 blocks */
  int n=N+nb, m=SETWORDSNEEDED(n);
  graph g[MAXN], cg[MAXN]; int lab[MAXN],ptn[MAXN],orb[MAXN];
  static DEFAULTOPTIONS_GRAPH(opt); statsblk st; opt.getcanon=TRUE; opt.defaultptn=FALSE;
  EMPTYGRAPH(g,m,n);
  for(int i=0;i<nb;i++) for(int p=0;p<N;p++) if(blocks[i]>>p&1) ADDONEEDGE(g,N+i,p,m);
  for(int i=0;i<n;i++){ lab[i]=i; ptn[i]=1; } ptn[N-1]=0; ptn[n-1]=0;
  densenauty(g,lab,ptn,orb,&opt,&st,m,n,cg);
  unsigned long long h=hashg(cg,n); int slot=h&(HS-1);
  while(htab[slot]>=0){ CG *c=&store[htab[slot]]; if(c->n==n && !memcmp(c->g,cg,sizeof(setword)*n)) return; slot=(slot+1)&(HS-1); }
  htab[slot]=nstore; store[nstore].n=n; memcpy(store[nstore].g,cg,sizeof(setword)*n); nstore++;
  /* write the core: block supports */
  fprintf(out,"[");
  for(int i=0;i<nb;i++){ fprintf(out,"%s[",i?",":""); int f=1; for(int p=0;p<N;p++) if(blocks[i]>>p&1){ fprintf(out,"%s%d",f?"":",",p); f=0;} fprintf(out,"]"); }
  fprintf(out,"]\n");
}

static int slack[16], extra[64][2], nextra;
static int pairs[200][2], npairs;
static void complete(int k){
  if(k==npairs){
    nb=0;
    for(int i=0;i<nch;i++) blocks[nb++]=chosen[i];
    /* forced 2-blocks */
    for(int a=0;a<N;a++) for(int b=a+1;b<N;b++){
      int cov=0; for(int i=0;i<nch;i++) if((chosen[i]>>a&1)&&(chosen[i]>>b&1)) cov=1;
      if(!cov) blocks[nb++]=(1<<a)|(1<<b);
    }
    for(int i=0;i<nextra;i++) blocks[nb++]=(1<<extra[i][0])|(1<<extra[i][1]);
    for(int p=0;p<N;p++) for(int s=0;s<slack[p];s++) blocks[nb++]=1<<p;
    emit(); return;
  }
  int a=pairs[k][0], b=pairs[k][1];
  complete(k+1);
  int added=0;
  while(slack[a]>0 && slack[b]>0){ slack[a]--; slack[b]--; extra[nextra][0]=a; extra[nextra][1]=b; nextra++; added++; complete(k+1); }
  for(int i=0;i<added;i++){ slack[a]++; slack[b]++; nextra--; }
}

static void leaf(void){
  for(int p=0;p<N;p++) if(tdeg[p]==0) return;
  int cov[16][16]; memset(cov,0,sizeof cov);
  for(int i=0;i<nch;i++) for(int a=0;a<N;a++) if(chosen[i]>>a&1) for(int b=0;b<N;b++) if(b!=a && (chosen[i]>>b&1)) cov[a][b]=1;
  for(int p=0;p<N;p++){ int unc=0; for(int q=0;q<N;q++) if(q!=p&&!cov[p][q]) unc++; slack[p]=R-tdeg[p]-unc; if(slack[p]<0) return; }
  leaves++;
  npairs=0; for(int a=0;a<N;a++) for(int b=a+1;b<N;b++) if(slack[a]>0&&slack[b]>0){ pairs[npairs][0]=a; pairs[npairs][1]=b; npairs++; }
  nextra=0; complete(0);
}

static void dfs(int i){
  if(i==nT){ leaf(); return; }
  dfs(i+1);
  int t=T[i];
  for(int j=0;j<nch;j++) if(!(chosen[j]&t)) return;
  int added=0;
  for(int m=1;m<=MMAX;m++){
    int bad=0; for(int p=0;p<N;p++) if((t>>p&1) && tdeg[p]+1>R) bad=1;
    if(bad) break;
    for(int p=0;p<N;p++) if(t>>p&1) tdeg[p]++;
    chosen[nch++]=t; added++;
    dfs(i+1);
  }
  for(int k=0;k<added;k++){ nch--; for(int p=0;p<N;p++) if(t>>p&1) tdeg[p]--; }
}

int main(int argc,char**argv){
  R=atoi(argv[1]); N=atoi(argv[2]); NEEDCOV=N-1;
  MMAX = R - (N-3+1)/2;               /* 2(R-m) >= N-3 */
  while(2*(R-MMAX) < N-3) MMAX--;
  store=malloc(sizeof(CG)*300000); htab=malloc(sizeof(int)*HS); memset(htab,-1,sizeof(int)*HS);
  char fn[64]; sprintf(fn,"cores_r%d_n%d.txt",R,N); out=fopen(fn,"w");
  for(int t=0;t<(1<<N);t++) if(popc(t)==3) T[nT++]=t;
  dfs(0);
  fclose(out);
  printf("RESULT r=%d n=%d multiplicity<=%d: triangle systems %lld, raw cores %lld, cores up to isomorphism %d (written to %s)\n",
         R,N,MMAX,leaves,raw,nstore,fn);
}
