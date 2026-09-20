# Data

| file | contents |
|---|---|
| `witness_17.json` | the seventeen-card witness of [P4], with the seventeen deletion five-covers |
| `eight_cores.jsonl` | the 463 canonical eight-card cores. One line per core: `supports` is the list of symbol supports as subsets of {0,...,7}, `multiplicity` is how many raw completions reduce to it |
| `eight_maximal.json` | the 10,144 maximal intersecting triple systems on eight points, step 1 of the reduction |
| `eight_triples_summary.json` | the seven orbit representatives with their triple-system counts and search nodes |
| `eight_triple_classes.jsonl` | the 129 symmetry classes, with multiplicities summing to 39,768 |
| `cnf/` | three CNF and DRAT pairs — cores 7, 239 and 342, the three hardest instances |

`eight_cores.jsonl` and `code/search_sixteen.py` are the two files the sixteen-card stage
rests on. Use these copies; do not reconstruct either from prose.
`code/verify_cnf_regeneration.py` checks the link between them.

The full archive of all 463 CNF and DRAT pairs is about 4 GB and belongs in a release
asset or an archive record rather than in the repository. The three shipped here let a
reader reproduce the certification step without running a solver.
