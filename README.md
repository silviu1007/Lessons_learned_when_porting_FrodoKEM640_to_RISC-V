# FrodoKEM-640 on RISC-V

Bachelor's thesis project (Radboud University) porting **FrodoKEM-640** — a post-quantum key encapsulation mechanism based on Learning With Errors — to RISC-V, and replacing its two dominant matrix-multiply routines with hand-written assembly. Cross-compiled to `rv64gc` and benchmarked under [QEMU](https://www.qemu.org/) user-mode emulation. Built on top of Microsoft's [FrodoKEM reference implementation](https://github.com/microsoft/PQCrypto-LWEKE).

---

## Table of Contents

- [1. Running the Code](#1-running-the-code)
- [2. Code Explanation](#2-code-explanation)
  * [2.1 Assembly Kernels](#21-assembly-kernels)
  * [2.2 Selecting a Configuration](#22-selecting-a-configuration)
  * [2.3 Benchmarking](#23-benchmarking)
  * [2.4 Figures](#24-figures)
- [3. Results](#3-results)
- [4. Other Branches](#4-other-branches)



## 1. Running the Code

### Step 1 Set up the environment

```bash
sudo apt-get update
sudo apt-get install -y gcc-riscv64-linux-gnu qemu-user
```

### Step 2 Run the benchmarks

```bash
cd FrodoKEM
python3 benchmark_O2.py     # or benchmark_O0.py / O1 / O3 / Os
```

> **Note:** every configuration (`sw`, `asm1`, `asm2`, `asm3`, `asm13`, `asm23`) at every optimization level is already built and committed under `FrodoKEM/benchmarks/`. You don't need to build anything to reproduce the results, this runs each binary 100 times under `qemu-riscv64` and writes a comparison table to `results_O2.txt`.

### Step 3 (optional) Rebuild after changing the assembly

```bash
cd FrodoKEM
./build_frodo_riscv.sh
```

> **Warning:** which kernel actually gets used is not a build flag, it's controlled by which lines are commented out in `frodo_macrify_testing.c`. Read [2.2](#22-selecting-a-configuration) before rebuilding, or you'll just reproduce the config that's already committed.

---

## 2. Code Explanation

### 2.1 Assembly Kernels

**Source:** `FrodoKEM/src/`

| File | Function | Replaces | Strategy |
|---|---|---|---|
| `inner_mul.S` | `inner_mul_row` | A·s inner loop | **Accumulator**, holds all 8 output accumulators in `s0–s7` for the full 640-iteration loop. |
| `inner_mul_v2.S` | `inner_mul_row_v2` | A·s inner loop | **Paired-load**, loads two 16-bit values per `lwu`, halving load count vs. the naive version. |
| `sa_mul_row.S` | `sa_mul_row` | s'·A inner loop | **Windowed (W=8)**, processes output in windows of 8, refreshing which 8 values sit in `s0–s7` at each step. |

### 2.2 Selecting a Configuration

**Source:** `FrodoKEM/src/frodo_macrify_testing.c`

Each of the two multiply functions (`frodo_mul_add_as_plus_e` and `frodo_mul_add_sa_plus_e`) has its plain-C loop and its assembly call sitting right next to each other in the source, comment one, uncomment the other, to pick a configuration. `sw` (both plain C) is the baseline everything else is measured against:

| Config | A·s uses | s'·A uses |
|---|---|---|
| `sw` (C-only baseline) | plain C loop | plain C loop |
| `asm1` | `inner_mul_row` | plain C loop |
| `asm2` | `inner_mul_row_v2` | plain C loop |
| `asm3` | plain C loop | `sa_mul_row` |
| `asm13` (accumulator + windowed) | `inner_mul_row` | `sa_mul_row` |
| `asm23` (paired-load + windowed) | `inner_mul_row_v2` | `sa_mul_row` |

`build_frodo_riscv.sh` doesn't need to change to switch configs, it already links all three `.S` files regardless of which is called. Only:

1. edit the two calls in `frodo_macrify_testing.c` to match the row above, and
2. change `OUT="benchmarks/frodo640_..._$OPT"` in `build_frodo_riscv.sh` to the matching name,

then rerun the build script.

### 2.3 Benchmarking

**Source:** `FrodoKEM/benchmark_core.py`, `FrodoKEM/benchmark_O{level}.py`

Each `benchmark_O{level}.py` sets `OPT` and `OUTPUT_FILE`, then runs `benchmark_core.py`, which:

1. runs the `sw`, `asm13`, and `asm23` binaries 100 times each under `/usr/bin/time -v qemu-riscv64`,
2. parses KeyGen/Encaps/Decaps timing (in microseconds) and peak RSS from the output, and
3. prints and writes (`results_O{level}.txt`) a mean/stdev/delta comparison table.

> **Warning:** always benchmark all three binaries for a given optimization level in the same invocation, as this script already does. Running them as separate invocations introduced a drifting QEMU/host baseline between runs, which produced a false regression in an earlier pass of this work, it didn't hold up once all three were measured together.

To compare the individual `asm1`/`asm2`/`asm3` configs instead of the combined `asm13`/`asm23`, edit the `BINARIES` dict at the top of `benchmark_core.py`.

### 2.4 Figures

**Source:** `FrodoKEM/new_graphs/`

| Output file | What it shows |
|---|---|
| `fig6_1_accumulator_keygen_absolute.png` | KeyGen time, accumulator (`asm1`) vs. C-only baseline |
| `fig6_2_accumulator_keygen_percent.png` | Same comparison, as a percentage delta |
| `fig6_3` / `fig6_4` | Accumulator vs. paired-load, absolute and percentage |
| `fig6_5` / `fig6_6` | Windowed (`asm3`) Encaps/Decaps, absolute and percentage |
| `fig6_7` / `fig6_8` | Combined accumulator + windowed (`asm13`), absolute and percentage |
| `fig6_9_all_three_absolute.png` | All three individual kernels, absolute |
| `fig6_10_both_combinations_percent.png` | `asm13` vs. `asm23`, percentage delta |
| `fig6_11_pairedload_vs_accumulator_headtohead.png` | Direct head-to-head, `asm13` vs. `asm23` |

This is the current, authoritative figure set. `FrodoKEM/graphs/` and the loose top-level scripts (`plot_delta_h2h.py`, etc.) are earlier exploratory passes, superseded by `new_graphs/`. The `new_graphs` scripts currently read from hardcoded data arrays transcribed by hand from `results_*.txt`, worth automating if you regenerate these often.

---

## 3. Results

Numbers below are mean wall-clock time in microseconds, averaged over 100 runs under `qemu-riscv64`, taken directly from `results_O0.txt` through `results_Os.txt`.

### KeyGen: C-only baseline vs. best assembly config, by optimization level

| Opt level | SW mean (µs) | Best config (µs) | Improvement |
|---|---|---|---|
| `-O0` | 43,131 | 19,204 (`asm23`) | -55.5% |
| `-O1` | 11,318 | 7,351 (`asm13`) | -35.1% |
| `-O2` | 17,809 | 13,735 (`asm13`) | -22.9% |
| `-O3` | 14,658 | 13,669 (`asm13`) | -6.7% |
| `-Os` | 13,486 | 8,694 (`asm13`) | -35.5% |

KeyGen is where the assembly work pays off most consistently, a double-digit improvement over the C baseline at every optimization level, since this is the operation both targeted inner loops run inside.

### `asm13` (accumulator) vs. `asm23` (paired-load), head-to-head

| Opt level | KeyGen | Encaps | Decaps |
|---|---|---|---|
| `-O0` | `asm23` wins, +5.6% | `asm23` wins, +9.7% | `asm23` wins, +11.0% |
| `-O1` | `asm13` wins, +9.8% | `asm13` wins, +1.8% | `asm13` wins, +1.2% |
| `-O2` | `asm13` wins, +2.5% | `asm23` wins, +1.5% | `asm23` wins, +3.7% |
| `-O3` | `asm13` wins, +8.3% | `asm13` wins, +4.4% | `asm13` wins, +5.5% |
| `-Os` | `asm13` wins, +5.2% | `asm13` wins, +1.6% | `asm13` wins, +3.1% |

(percentages are how much slower the losing config was, relative to the winner)

There's no single universal winner here, which is worth being precise about rather than rounding it off: at `-O0` (no compiler optimization), paired-load (`asm23`) is faster across all three operations. Once any optimization flag is turned on, accumulator (`asm13`) takes the lead for KeyGen every time, and usually for Encaps/Decaps too, except at `-O2`, where paired-load stays ahead on Encaps and Decaps despite losing KeyGen. If you need a single default to build with going forward, `asm13` is the safer pick for anything compiled with `-O1` or higher, but re-run the benchmarks rather than assuming this holds if you change the kernels.

Also worth knowing before changing the assembly further:

- **`S` is stored transposed (`Sᵀ`) in memory**, matters for correctness and for reasoning about stride costs in both kernels.
- Instruction-count claims in the thesis are grounded in `objdump -d` disassembly, not theoretical estimates, re-check with `objdump` if you modify the kernels.
- Strassen-style algorithmic restructuring was evaluated and found to give only a modest (~4.3%) net saving for this problem's fixed dimensions.

---

## 4. Other Branches

`master` contains the full assembly work above. Two other branches exist, kept for reference rather than day-to-day use:

| Branch | Contains |
|---|---|
| `inner_mul_assembly` | The same snapshot as `master` at the point it was consolidated, full assembly work, benchmarking pipeline, and figures, unchanged. |
| `c_optimized_version_init` | An earlier, C-only branch. `frodo_mul_add_as_plus_e`'s inner loop is kept as a plain nested loop instead of calling assembly, with its own `build_frodo_riscv.sh` and `run_benchmark.py` comparing that plain-C build against a separately committed reference binary. This predates the assembly work rather than being a parallel optimization track, it covers the same ground as the `sw` config in [2.2](#22-selecting-a-configuration). |

Unless you specifically want to see how the C-only baseline looked before the assembly work started, there's no need to check out either branch, everything you need is on `master`.

## License
MIT-licensed, inherited from the original [FrodoKEM library](https://github.com/microsoft/PQCrypto-LWEKE) by the FrodoKEM team and Microsoft Research, see `LICENSE`.
