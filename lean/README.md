# Lean checks

Two finite lemmas of the $g(6)$ papers stated and proved in Lean 4, with no Mathlib.

| file | statement | time | expected |
|---|---|---|---|
| `K7.lean` | [P1, Lemma 2], the $K_7$ lemma | about 4 min | proved |
| `Petals.lean` | [P2, Lemma 3], the petal statement on eleven points | about 20 min | proved |

Each file is written by a short generator, `gen_k7.py` and `gen_petals.py`. The generator
is the source: it fixes the numbering of edges or triples, and anyone can read from it
what the Lean statement says.

## What the proofs rest on

The proofs use `bv_decide`. It turns the goal into a SAT problem, runs the CaDiCaL solver,
and checks the solver's LRAT certificate with a checker that is itself proved correct in
Lean. The solver is therefore not trusted. What is trusted is listed by `#print axioms`
at the end of each file:

```text
[propext, Classical.choice, Lean.ofReduceBool, Quot.sound]
```

The first, second and fourth are Lean's standard axioms. `Lean.ofReduceBool` means the
certificate check runs as compiled code rather than inside the kernel, so the Lean
compiler is trusted as well. This is weaker than a kernel-only proof, and much stronger
than trusting a SAT solver's answer.

The Lean statement is a statement about bit-vectors. Whether it says the same thing as the
lemma in the paper is a matter of reading: the generator and the comment at the top of
each file give the encoding.

## Controls

A proof of a statement that can never fail proves nothing, so each file has a false
variant that must fail.

- `python3 gen_k7.py --control` writes `K7_control.lean`, which asks the matching to meet
  all four covers. `bv_decide` reports a counterexample.
- `python3 gen_petals.py 11 7 Petals_ctl7` writes the petal statement with seven triples
  at the centre instead of six. `bv_decide` reports a counterexample. (It calls the
  counterexample "potentially spurious" because it treats each `S y` as a free variable;
  that abstraction is sound for the proof, and the counterexample is a real one.)

## Running

Install Lean through elan and use the toolchain in `lean-toolchain`. No `lake` project is
needed; each file is checked on its own.

```bash
python3 gen_k7.py
lean K7.lean
python3 gen_petals.py 11 6 Petals
lean Petals.lean
```

If `Petals.lean` stops with a stack overflow, give it a larger stack (on Linux):

```bash
ulimit -s unlimited
lean --tstack=4000000 Petals.lean
```

The theorem names are `k7_lemma` and `petals_11_6`. Lean prints a few "unused variable"
warnings for `Petals.lean`: some hypotheses are not needed for the contradiction. These
are warnings, not errors.
