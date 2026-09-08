# FrodoKEM-640 on RISC-V — C-only Baseline

> See [`master`](../../tree/master) for the full project and the assembly-optimized results. This branch is the plain-C baseline everything there gets measured against.

## What's here

FrodoKEM-640's two matrix-multiply routines (`frodo_mul_add_as_plus_e` and `frodo_mul_add_sa_plus_e`, in `FrodoKEM/src/frodo_macrify_testing.c`) are left as plain, portable C loops on this branch, no RISC-V assembly. It's an earlier snapshot from before the assembly work started, not a separate optimization track.

- `FrodoKEM/build_frodo_riscv.sh` — cross-compiles the plain-C build (`frodo640_testing_{OPT}`) for all five optimization levels.
- `FrodoKEM/run_benchmark.py` — benchmarks that build under `qemu-riscv64` against a pre-built reference binary (`frodo640_{OPT}`, committed directly, there's no script here that regenerates it).
- `FrodoKEM/benchmarks/` — all binaries already built, so you don't need to build anything to run the comparison.

## Running it

```bash
sudo apt-get install -y gcc-riscv64-linux-gnu qemu-user
cd FrodoKEM
python3 run_benchmark.py
```

This isn't expected to show much of a gap, it's the baseline. For the actual RISC-V assembly work and the thesis's benchmarked results, see [`master`](../../tree/master).
