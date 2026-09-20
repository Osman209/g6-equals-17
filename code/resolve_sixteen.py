"""Retry UNKNOWN cores in parallel; never convert a budget exhaustion to UNSAT.

COVERS [P3, §5] — rerun of any core left UNKNOWN by a conflict budget. A budget exhaustion is never an exclusion.
"""
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor,as_completed
import json,time,argparse
from search_sixteen import build,audit,Solver
ROOT=Path(__file__).resolve().parents[1]

def work(task):
 i,S,budget,name=task;start=time.monotonic();cnf,nv,data,meta=build(S)
 with Solver(name=name,bootstrap_with=cnf) as solver:
  if budget:solver.conf_budget(budget);ans=solver.solve_limited()
  else:ans=solver.solve()
  r=dict(core=i,status='UNSAT' if ans is False else 'SAT' if ans else 'UNKNOWN',seconds=round(time.monotonic()-start,3),solver=name,stats=solver.accum_stats(),**meta)
  if ans:r['cards']=audit(S,solver.get_model(),data,True)
 return r
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--budget',type=int,default=100000);p.add_argument('--workers',type=int,default=4);p.add_argument('--solver',default='cadical195');p.add_argument('--input',default='sat_results_cadical195_0.jsonl');p.add_argument('--output',default='sat_retry.jsonl');a=p.parse_args()
 rows=[json.loads(l) for l in (ROOT/'data'/'eight_cores.jsonl').read_text().splitlines()]
 results=[json.loads(l) for l in (ROOT/'results'/a.input).read_text().splitlines()]
 todo=[r['core'] for r in results if r['status']=='UNKNOWN']
 print('RETRYING',len(todo),flush=True)
 with ProcessPoolExecutor(max_workers=a.workers) as pool,(ROOT/'results'/a.output).open('w') as f:
  jobs=[pool.submit(work,(i,rows[i]['supports'],a.budget,a.solver)) for i in todo]
  for job in as_completed(jobs):
   r=job.result();f.write(json.dumps(r)+'\n');f.flush();print({k:v for k,v in r.items() if k!='cards'},flush=True)
