/* verify_rainbow.c — the two four-family matching lemmas of [P5, Lemmas 10 and 11].
 *
 * COVERS [P5, §4.1]: exhaustive check on 8, 9 and 10 vertices.  Called by
 * code/verify_rainbow_lemmas.py, which compiles it and checks the output.
 *
 *   Lemma 10. Three graphs with matchings of size four and a nonempty fourth graph
 *             have three disjoint edges taken from three distinct graphs.
 *   Lemma 11. The same for matching numbers (3, 3, 4, 4).
 *
 * WLOG each graph is exactly its matching (extra edges only add choices) and the fourth
 * graph of Lemma 10 is one edge.  The first size-four matching is fixed as
 * {01, 23, 45, 67}.  Lemma 10: every pair (P2, P3) of size-four matchings and every edge
 * f.  Lemma 11: if no rainbow triple exists, every edge of the two size-three matchings
 * is "safe" for the size-four pair (P, Q); so only the safe edges need to be searched.
 *
 *   cc -O2 -o verify_rainbow code/verify_rainbow.c && ./verify_rainbow 10
 * Prints one line per lemma; the counterexample counts must be zero.
 */
#include <stdio.h>
#include <stdlib.h>
static int n, NM; static unsigned M[20000][4];
static void gen(int k, unsigned used, unsigned *cur){
  if(k==4){ for(int i=0;i<4;i++) M[NM][i]=cur[i]; NM++; return; }
  for(int a=0;a<n;a++) if(!(used>>a&1)) for(int b=a+1;b<n;b++) if(!(used>>b&1)){
    unsigned e=(1u<<a)|(1u<<b); if(k>0 && e<=cur[k-1]) continue;
    cur[k]=e; gen(k+1,used|e,cur); }
}
static int two(const unsigned *X,int nx,const unsigned *Y,int ny,unsigned avoid){
  for(int i=0;i<nx;i++){ if(X[i]&avoid) continue;
    for(int j=0;j<ny;j++) if(!(Y[j]&avoid) && !(X[i]&Y[j])) return 1; }
  return 0;
}
static int rainbow(const unsigned *G[4],const int *sz){
  int idx[4][3]={{0,1,2},{0,1,3},{0,2,3},{1,2,3}};
  for(int c=0;c<4;c++){ int a=idx[c][0],b=idx[c][1],d=idx[c][2];
    if(!sz[a]||!sz[b]||!sz[d]) continue;
    for(int i=0;i<sz[a];i++) if(two(G[b],sz[b],G[d],sz[d],G[a][i])) return 1; }
  return 0;
}
int main(int argc,char**argv){
  n=atoi(argv[1]); unsigned cur[4]; NM=0; gen(0,0,cur);
  unsigned P1[4]={3,12,48,192};
  long long pairs=0,norb=0,bad4=0;
  for(int x=0;x<NM;x++) for(int y=0;y<NM;y++){
    const unsigned *G[4]={P1,M[x],M[y],0}; int sz[4]={4,4,4,0}; pairs++;
    if(rainbow(G,sz)) continue;
    norb++;
    for(int a=0;a<n;a++) for(int b=a+1;b<n;b++){ unsigned f=(1u<<a)|(1u<<b);
      unsigned F[1]={f}; G[3]=F; sz[3]=1;
      if(!rainbow(G,sz)) bad4++; }
  }
  printf("lemma4 n=%d matchings %d pairs %lld without-rainbow %lld counterexamples %lld\n",
         n,NM,pairs,norb,bad4);
  /* Lemma 11 */
  long long cfg=0,bad5=0;
  unsigned allE[64]; int nE=0;
  for(int a=0;a<n;a++) for(int b=a+1;b<n;b++) allE[nE++]=(1u<<a)|(1u<<b);
  for(int y=0;y<NM;y++){
    const unsigned *Q=M[y]; unsigned safe[64]; int ns=0;
    for(int i=0;i<nE;i++) if(!two(P1,4,Q,4,allE[i])) safe[ns++]=allE[i];
    unsigned T3[4000][3]; int nt=0;
    for(int i=0;i<ns;i++) for(int j=i+1;j<ns;j++) if(!(safe[i]&safe[j]))
      for(int k=j+1;k<ns;k++) if(!(safe[k]&(safe[i]|safe[j]))){
        T3[nt][0]=safe[i];T3[nt][1]=safe[j];T3[nt][2]=safe[k];nt++; }
    for(int i=0;i<nt;i++) for(int j=0;j<nt;j++){
      const unsigned *G[4]={T3[i],T3[j],P1,Q}; int sz[4]={3,3,4,4}; cfg++;
      if(!rainbow(G,sz)) bad5++; }
  }
  printf("lemma5 n=%d configurations-with-all-edges-safe %lld counterexamples %lld\n",n,cfg,bad5);
  return (bad4||bad5)?1:0;
}
