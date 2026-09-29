# Run records

| file | contents |
|---|---|
| `sat_results_cadical195_0.jsonl` | the budgeted pass over all 463 cores: 460 UNSAT, 3 UNKNOWN |
| `sat_retry*.jsonl` | the retry chain. Cores 7, 239 and 342 were rerun without a conflict budget and proved UNSAT |
| `sat_retry_input*.jsonl` | the UNKNOWN inputs each retry round was given |
| `certificate_summary.jsonl` | one line per core, 0 to 462, with the DRAT verification result and timing |
| `drat_batch_result.txt` | the batch console tally |
| `hard_cores.json` | the three instances that first hit the budget |
| `completion_summary.json`, `release_summary.json` | aggregate summaries |
| `g11_results.jsonl.gz` | the per-instance record of the eleven-card degree-three search: 5,373 lines, one per instance, all UNSAT |
| `search_record.json` | the solver output that produced the seventeen-card witness, with symbols indexed from 0 |

An UNKNOWN is never an exclusion. A core is only closed by an UNSAT answer that carries a
checked DRAT proof.

`degree3_kernels_check.txt` is the recorded run of `code/verify_degree3_kernels.py --witness`:
the three profiles of [P3, §2a], their 341 kernels, the exhaustive extension test on each,
and the location of the [P4] witness kernel inside the enumeration.

`p5_checks.txt` is the recorded run of the six [P5] scripts, with
`verify_local_graphs.py` in its `--full` form.
