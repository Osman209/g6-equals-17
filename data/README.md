# Data

| file | contents |
|---|---|
| `witness_17.json` | the seventeen-card witness of [P4], with the seventeen deletion five-covers |
| `eight_cores.jsonl` | the 463 canonical eight-card cores. One line per core: `supports` is the list of symbol supports as subsets of {0,...,7}, `multiplicity` is how many raw completions reduce to it |
| `degree3_kernels_c12.json`, `degree3_kernels_c6.json`, `degree3_kernels_c0.json` | the twelve-card kernels of maximum degree three, up to isomorphism: 2, 259 and 80 for the profiles (6,20), (3,22) and (0,24). Each entry is a list of triangle indices into C(12,3) in lexicographic order, a triangle being the three cards of one degree-three symbol. This is the second branch of [P3, §2a] |
| `eight_maximal.json` | the 10,144 maximal intersecting triple systems on eight points, step 1 of the reduction |
| `eight_triples_summary.json` | the seven orbit representatives with their triple-system counts and search nodes |
| `eight_triple_classes.jsonl` | the 129 symmetry classes, with multiplicities summing to 39,768 |
| `cnf/` | three CNF and DRAT pairs — cores 7, 239 and 342, the three hardest instances |

`eight_cores.jsonl` and `code/search_sixteen.py` are the two files the sixteen-card stage
rests on. Use these copies; do not reconstruct either from prose.
`code/verify_cnf_regeneration.py` checks the link between them.

The full certificate archive — 463 CNF files, 463 DRAT proofs, a solver log and a
checker log for each, and 463 verification markers, 2,318 files and 2.1 GB uncompressed —
is attached to the v1.0.1 release rather than committed here:

  https://github.com/Osman209/g6-equals-17/releases/tag/v1.0.1

The three pairs shipped in `cnf/` are the three hardest instances, and let a reader
reproduce the certification step without downloading the archive and without running a
solver.
