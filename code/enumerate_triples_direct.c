/* COVERS [P3, §3] steps 1-3 by a second route: the 129 classes of triple systems,
   enumerated directly from the definition, with no maximal families and no orbits.
   Run through code/verify_cores_direct.py, which compiles it with cc.

   Enumerates ALL labelled multisets of triples on the 8 card indices with
   - multiplicity <= 3 per triple,
   - triples pairwise intersecting,
   - every card in >= 1 triple,
   - slack(v) = 6 - deg3(v) - #(pairs at v covered by no triple) >= 0,
   and keeps exactly one labelled representative per isomorphism class (the one equal
   to its own canonical form under the full symmetric group S8, computed by trying every
   permutation consistent with a point invariant). No maximal families, no orbits.
   Output: one line per class, the sorted triple masks.                                */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int T[56], nT = 0;
static int chosen[64], nch = 0;   /* triple masks, with repeats, in nondecreasing order */
static int deg[8];
static long leaves = 0, classes = 0;
static int perms[40320][8], nperm = 0;

static int popc(int x){ return __builtin_popcount(x); }

static void genperms(int *a, int k){
    if (k == 8){ memcpy(perms[nperm++], a, sizeof(int)*8); return; }
    for (int i = k; i < 8; i++){
        int t=a[k];a[k]=a[i];a[i]=t; genperms(a,k+1); t=a[k];a[k]=a[i];a[i]=t;
    }
}
static int cmpint(const void*a,const void*b){ return *(int*)a - *(int*)b; }

static int permmask(int m, const int *p){ int r=0; for(int v=0;v<8;v++) if(m>>v&1) r|=1<<p[v]; return r; }

/* is the current labelled object equal to its canonical form? canonical form = lexicographically
   smallest sorted mask list over permutations p (old point v -> new point p[v]) that send points
   with larger invariant to smaller labels. Any isomorphism respects the invariant, so the minimum
   over this restricted set is an isomorphism invariant and is attained by exactly the canonical
   labelled objects. */
static int is_canonical(void){
    long inv[8];
    int covered[8][8]; memset(covered,0,sizeof covered);
    for(int i=0;i<nch;i++) for(int a=0;a<8;a++) if(chosen[i]>>a&1) for(int b=0;b<8;b++) if(b!=a && (chosen[i]>>b&1)) covered[a][b]=1;
    for(int v=0;v<8;v++){
        long s=deg[v]*1000000L;
        int unc=0; for(int w=0;w<8;w++) if(w!=v && !covered[v][w]) unc++;
        s+=unc*10000L;
        /* sum of degrees of co-points over triples through v (with multiplicity) */
        long co=0; for(int i=0;i<nch;i++) if(chosen[i]>>v&1) for(int w=0;w<8;w++) if(w!=v && (chosen[i]>>w&1)) co+=deg[w];
        s+=co;
        inv[v]=s;
    }
    /* identity must be allowed: labels already sorted by decreasing invariant */
    for(int a=0;a<7;a++) if(inv[a]<inv[a+1]) return 0;
    int cur[64]; memcpy(cur,chosen,sizeof(int)*nch);
    int buf[64];
    /* allowed permutations = those permuting labels inside blocks of equal invariant */
    int blk[8]; int nb=0; for(int a=0;a<8;a++){ if(a==0||inv[a]!=inv[a-1]) nb++; blk[a]=nb-1; }
    for(int k=0;k<nperm;k++){
        const int *p=perms[k]; int ok=1;
        for(int a=0;a<8;a++) if(blk[p[a]]!=blk[a]){ok=0;break;}
        if(!ok) continue;
        for(int i=0;i<nch;i++) buf[i]=permmask(cur[i],p);
        qsort(buf,nch,sizeof(int),cmpint);
        for(int i=0;i<nch;i++){ if(buf[i]<cur[i]) return 0; if(buf[i]>cur[i]) break; }
    }
    return 1;
}

static void leaf(void){
    for(int v=0;v<8;v++) if(!deg[v]) return;
    int cov=0; /* bitset of 28 pairs */
    int covered[8][8]; memset(covered,0,sizeof covered);
    for(int i=0;i<nch;i++) for(int a=0;a<8;a++) if(chosen[i]>>a&1) for(int b=0;b<8;b++) if(chosen[i]>>b&1) covered[a][b]=1;
    for(int v=0;v<8;v++){ int unc=0; for(int w=0;w<8;w++) if(w!=v && !covered[v][w]) unc++; if(6-deg[v]-unc<0) return; }
    (void)cov;
    leaves++;
    if(!is_canonical()) return;
    classes++;
    for(int i=0;i<nch;i++) printf("%d%c",chosen[i], i+1<nch?' ':'\n');
}

static void dfs(int i){
    if(i==nT){ leaf(); return; }
    dfs(i+1);                          /* multiplicity 0 */
    int t=T[i];
    for(int j=0;j<nch;j++) if(!(chosen[j]&t)) return;   /* must meet every chosen triple */
    int added=0;
    for(int m=1;m<=3;m++){
        int bad=0; for(int v=0;v<8;v++) if(t>>v&1){ if(deg[v]+1>6) bad=1; }
        if(bad) break;
        for(int v=0;v<8;v++) if(t>>v&1) deg[v]++;
        chosen[nch++]=t; added++;
        dfs(i+1);
    }
    for(int k=0;k<added;k++){ nch--; for(int v=0;v<8;v++) if(t>>v&1) deg[v]--; }
}

int main(void){
    for(int m=0;m<256;m++) if(popc(m)==3) T[nT++]=m;      /* ascending, so chosen stays sorted */
    int a[8]={0,1,2,3,4,5,6,7}; genperms(a,0);
    dfs(0);
    fprintf(stderr,"LEAVES %ld CLASSES %ld\n",leaves,classes);
    return 0;
}
