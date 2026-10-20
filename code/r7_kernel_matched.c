/* COVERS [P7, Lemma 4]: matching number exactly 3, first route (nauty orbits of the matching,
   then an exhaustive search tree). Writes matched_n<n>_c<c>.log in the working directory and
   resumes from it. Needs nauty. Run through code/verify_g7_lower.py. */
/* Existence of a triangle decomposition of M = K_n + E - F with matching number exactly 3,
   by fixing the maximum matching first.

   If such a decomposition exists, it has 3 pairwise disjoint triangles M1, M2, M3 (on W, 9
   points), no 4 pairwise disjoint triangles, and so no triangle inside U = the other n - 9
   points. Up to Aut(M) the placement of {M1, M2, M3} is one of finitely many orbits; nauty
   picks one representative of each. For each representative the rest is searched
   exhaustively with those three triangles placed, triangles inside U forbidden, and every
   partial solution holding 4 disjoint triangles pruned.

   usage: matched n c      (F = first c/2 matching pairs, E = the rest)              */
#define MAXN 64
#include "nauty.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int N, C, cap[16][16], tri[48], nt;
static long long nodes, found;
static int Umask;

static int has_k_disjoint(int k, int used, int start){
  if(k==0) return 1;
  for(int i=start;i<nt;i++) if(!(tri[i]&used) && has_k_disjoint(k-1, used|tri[i], i+1)) return 1;
  return 0;
}
static void put(int a,int b,int x,int d){ cap[a][b]-=d;cap[b][a]-=d;cap[a][x]-=d;cap[x][a]-=d;cap[b][x]-=d;cap[x][b]-=d; }
static int okx(int a,int b,int x){ int m=(1<<a)|(1<<b)|(1<<x); return (m&Umask)!=m; }
static int firstsol[48], firstn;
static void dfs(void){
  nodes++;
  if(found) return;
  if(has_k_disjoint(4,0,0)) return;
  int ba=-1,bb=-1; long best=1<<30;
  for(int a=0;a<N;a++)for(int b=a+1;b<N;b++) if(cap[a][b]>0){
    int n=0; for(int x=0;x<N;x++) if(x!=a&&x!=b&&cap[a][x]>0&&cap[b][x]>0&&okx(a,b,x)) n++;
    long m = cap[a][b]==2 ? (long)n*(n-1)/2 : n;
    if(m<best){best=m;ba=a;bb=b;}
  }
  if(ba<0){ found++; memcpy(firstsol,tri,sizeof(int)*nt); firstn=nt; return; }
  if(best==0) return;
  int o[16],n=0; for(int x=0;x<N;x++) if(x!=ba&&x!=bb&&cap[ba][x]>0&&cap[bb][x]>0&&okx(ba,bb,x)) o[n++]=x;
  if(cap[ba][bb]==2){
    for(int i=0;i<n;i++)for(int j=i+1;j<n;j++){
      put(ba,bb,o[i],1); tri[nt++]=(1<<ba)|(1<<bb)|(1<<o[i]);
      if(cap[ba][o[j]]>0&&cap[bb][o[j]]>0){ put(ba,bb,o[j],1); tri[nt++]=(1<<ba)|(1<<bb)|(1<<o[j]); dfs(); nt--; put(ba,bb,o[j],-1); }
      nt--; put(ba,bb,o[i],-1);
    }
  } else for(int i=0;i<n;i++){ put(ba,bb,o[i],1); tri[nt++]=(1<<ba)|(1<<bb)|(1<<o[i]); dfs(); nt--; put(ba,bb,o[i],-1); }
}

static void initcap(void){
  for(int a=0;a<N;a++)for(int b=0;b<N;b++)cap[a][b]=(a!=b);
  for(int k=0;k<N/2;k++){int a=2*k,b=2*k+1,v=(2*k<C)?0:2; cap[a][b]=cap[b][a]=v;}
}
static int allowed(int t){ /* no unserved (F) pair inside */
  for(int a=0;a<N;a++) if(t>>a&1) for(int b=a+1;b<N;b++) if(t>>b&1) if(cap[a][b]==0) return 0;
  return 1;
}

/* canonical form of (M, {T1,T2,T3}) via nauty */
#define NV (16+8+3)
static setword canon_store[200000][NV*1]; static int ncanon;
static int canon(int T[3], graph *out){
  int n = N + N/2 + 3, m = SETWORDSNEEDED(n);
  graph g[NV*1]; int lab[NV], ptn[NV], orbits[NV];
  static DEFAULTOPTIONS_GRAPH(opt); statsblk st;
  opt.getcanon = TRUE; opt.defaultptn = FALSE;
  EMPTYGRAPH(g,m,n);
  for(int k=0;k<N/2;k++){ int v=N+k; ADDONEEDGE(g,v,2*k,m); ADDONEEDGE(g,v,2*k+1,m); }
  for(int i=0;i<3;i++){ int v=N+N/2+i; for(int a=0;a<N;a++) if(T[i]>>a&1) ADDONEEDGE(g,v,a,m); }
  /* colour classes: points | F-pair vertices | E-pair vertices | triangle vertices */
  int p=0;
  for(int a=0;a<N;a++){ lab[p]=a; ptn[p]=1; p++; } ptn[p-1]=0;
  int nf=C/2, ne=N/2-C/2;
  for(int k=0;k<nf;k++){ lab[p]=N+k; ptn[p]=1; p++; } if(nf) ptn[p-1]=0;
  for(int k=nf;k<N/2;k++){ lab[p]=N+k; ptn[p]=1; p++; } if(ne) ptn[p-1]=0;
  for(int i=0;i<3;i++){ lab[p]=N+N/2+i; ptn[p]=1; p++; } ptn[p-1]=0;
  densenauty(g,lab,ptn,orbits,&opt,&st,m,n,out);
  return n;
}

int main(int argc,char**argv){
  N=atoi(argv[1]); C=atoi(argv[2]);
  int START = argc>3 ? atoi(argv[3]) : 0, STEP = argc>4 ? atoi(argv[4]) : 1;
  char logname[64]; sprintf(logname,"matched_n%d_c%d.log",N,C);
  static char done[300000]; memset(done,0,sizeof done);
  { FILE *f=fopen(logname,"r"); if(f){ int k; long long nn; char w[16];
      while(fscanf(f,"%15s %d %lld",w,&k,&nn)==3) if(!strcmp(w,"done")) done[k]=1; fclose(f);} }
  FILE *lg=fopen(logname,"a");
  initcap();
  int T[600], nT=0;
  for(int t=0;t<(1<<N);t++) if(__builtin_popcount(t)==3 && allowed(t)) T[nT++]=t;
  long sets=0; ncanon=0;
  int n = N + N/2 + 3;
  long long totalnodes=0; int reps=0;
  for(int i=0;i<nT;i++) for(int j=i+1;j<nT;j++) if(!(T[i]&T[j])) for(int k=j+1;k<nT;k++) if(!(T[k]&(T[i]|T[j]))){
    sets++;
    int TT[3]={T[i],T[j],T[k]}; graph cg[NV];
    canon(TT,cg);
    int dup=0; for(int q=0;q<ncanon;q++) if(!memcmp(canon_store[q],cg,sizeof(setword)*n)){dup=1;break;}
    if(dup) continue;
    memcpy(canon_store[ncanon++],cg,sizeof(setword)*n);
    reps++;
    if(done[reps] || (reps % STEP) != START) continue;
    /* search with these three placed */
    initcap(); nt=0; found=0; nodes=0;
    int W=TT[0]|TT[1]|TT[2]; Umask=((1<<N)-1)&~W;
    int ok=1;
    for(int q=0;q<3;q++){ int a=-1,b=-1,x=-1; for(int v=0;v<N;v++) if(TT[q]>>v&1){ if(a<0)a=v; else if(b<0)b=v; else x=v; }
      if(cap[a][b]<1||cap[a][x]<1||cap[b][x]<1) ok=0; put(a,b,x,1); tri[nt++]=TT[q]; }
    if(ok) dfs();
    totalnodes+=nodes;
    if(!found){ fprintf(lg,"done %d %lld\n",reps,nodes); fflush(lg); }
    if(found){
      printf("RESULT FOUND a decomposition with matching number 3 (representative %d):", reps);
      for(int q=0;q<firstn;q++){ printf(" {"); for(int v=0;v<N;v++) if(firstsol[q]>>v&1) printf("%d,",v); printf("}"); }
      printf("\n"); return 0;
    }
  }
  printf("RESULT n=%d c=%d: %ld placements of 3 disjoint triangles, %d up to symmetry, %lld search nodes, NO decomposition with matching number 3 among the representatives searched by this process (start %d step %d)\n",
         N, C, sets, reps, totalnodes, START, STEP);
  return 0;
}
