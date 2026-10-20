/* COVERS [P7, Lemma 4 and §4.3]: plain exhaustive search, two uses -- matching number at most 2
   in all three profiles, and the c = 14 profile in full. Calibration: n = 12, c = 12 and 6 with nu = 4
   give 69,120 and 558,672, the counts of [P3, §2a]. Run through code/verify_g7_lower.py. */
/* Exhaustive count of labelled triangle decompositions of M = K_n + E - F (F = first c/2
   matching pairs, E = the other matching pairs, served twice) with no NU pairwise disjoint
   triangles. A capacity-two pair takes both of its triangles in one branching step, so each
   decomposition is counted once.  usage: exact n c nu */
#include <stdio.h>
#include <stdlib.h>
static int N, cap[16][16], tri[40], nt, NU;
static long long found=0, nodes=0;
static int has_k_disjoint(int k, int used, int start){
  if(k==0) return 1;
  for(int i=start;i<nt;i++) if(!(tri[i]&used) && has_k_disjoint(k-1, used|tri[i], i+1)) return 1;
  return 0;
}
static void put(int a,int b,int x,int d){ cap[a][b]-=d;cap[b][a]-=d;cap[a][x]-=d;cap[x][a]-=d;cap[b][x]-=d;cap[x][b]-=d; }
static void dfs(void){
  nodes++;
  if(NU && has_k_disjoint(NU,0,0)) return;
  int ba=-1,bb=-1; long best=1<<30;
  for(int a=0;a<N;a++)for(int b=a+1;b<N;b++) if(cap[a][b]>0){
    int n=0; for(int x=0;x<N;x++) if(x!=a&&x!=b&&cap[a][x]>0&&cap[b][x]>0) n++;
    long m = cap[a][b]==2 ? (long)n*(n-1)/2 : n;
    if(m<best){best=m;ba=a;bb=b;}
  }
  if(ba<0){found++; return;}
  if(best==0) return;
  int o[16],n=0; for(int x=0;x<N;x++) if(x!=ba&&x!=bb&&cap[ba][x]>0&&cap[bb][x]>0) o[n++]=x;
  if(cap[ba][bb]==2){
    for(int i=0;i<n;i++)for(int j=i+1;j<n;j++){
      put(ba,bb,o[i],1); tri[nt++]=(1<<ba)|(1<<bb)|(1<<o[i]);
      if(cap[ba][o[j]]>0&&cap[bb][o[j]]>0){ put(ba,bb,o[j],1); tri[nt++]=(1<<ba)|(1<<bb)|(1<<o[j]); dfs(); nt--; put(ba,bb,o[j],-1); }
      nt--; put(ba,bb,o[i],-1);
    }
  } else for(int i=0;i<n;i++){ put(ba,bb,o[i],1); tri[nt++]=(1<<ba)|(1<<bb)|(1<<o[i]); dfs(); nt--; put(ba,bb,o[i],-1); }
}
int main(int argc,char**argv){
  N=atoi(argv[1]); int c=atoi(argv[2]); NU=atoi(argv[3]);
  for(int a=0;a<N;a++)for(int b=0;b<N;b++)cap[a][b]=(a!=b);
  for(int k=0;k<N/2;k++){int a=2*k,b=2*k+1,v=(2*k<c)?0:2; cap[a][b]=cap[b][a]=v;}
  dfs();
  printf("RESULT n=%d c=%d no %d disjoint triangles: %lld decompositions (%lld search nodes)\n",N,c,NU,found,nodes);
}
