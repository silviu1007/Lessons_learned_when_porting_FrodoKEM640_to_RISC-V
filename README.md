# FrodoKEM-640 RISC-V Assembly Optimizations

Hand-written RISC-V assembly kernels for FrodoKEM-640's two dominant matrix-multiply routines, cross-compiled to `rv64gc` and benchmarked under [QEMU](https://www.qemu.org/) user-mode emulation. Built on top of Microsoft's [FrodoKEM reference implementation](https://github.com/microsoft/PQCrypto-LWEKE).

> See [`master`](../../tree/master) for the project overview and how this branch relates to [`c_optimized_version_init`](../../tree/c_optimized_version_init).


## Table of Contents

- [1. Running the Code](#1-running-the-code)
- [2. Code Explanation](#2-code-explanation)
  * [2.1 Assembly Kernels](#21-assembly-kernels)
  * [2.2 Selecting a Configuration](#22-selecting-a-configuration)
  * [2.3 Benchmarking](#23-benchmarking)
  * [2.4 Figures](#24-figures)
- [3. Results](#3-results)

---

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

Each of the two multiply functions (`frodo_mul_add_as_plus_e` and `frodo_mul_add_sa_plus_e`) has its plain-C loop and its assembly call sitting right next to each other in the source, comment one, uncomment the other, to pick a configuration:

| Config | A·s uses | s'·A uses |
|---|---|---|
| `sw` | plain C loop | plain C loop |
| `asm1` | `inner_mul_row` | plain C loop |
| `asm2` | `inner_mul_row_v2` | plain C loop |
| `asm3` | plain C loop | `sa_mul_row` |
| `asm13` (accumulator + windowed) | `inner_mul_row` | `sa_mul_row` |
| `asm23` (paired-load + windowed, currently committed) | `inner_mul_row_v2` | `sa_mul_row` |

`build_frodo_riscv.sh` doesn't need to change to switch configs — it already links all three `.S` files regardless of which is called. Only:

1. edit the two calls in `frodo_macrify_testing.c` to match the row above, and
2. change `OUT="benchmarks/frodo640_..._$OPT"` in `build_frodo_riscv.sh` to the matching name,

then rerun the build script.

### 2.3 Benchmarking

**Source:** `FrodoKEM/benchmark_core.py`, `FrodoKEM/benchmark_O{level}.py`

Each `benchmark_O{level}.py` sets `OPT` and `OUTPUT_FILE`, then runs `benchmark_core.py`, which:

1. runs the `sw`, `asm13`, and `asm23` binaries 100 times each under `/usr/bin/time -v qemu-riscv64`,
2. parses KeyGen/Encaps/Decaps timing and peak RSS from the output, and
3. prints and writes (`results_O{level}.txt`) a mean/stdev/delta comparison table.

> **Warning:** always benchmark all three binaries for a given optimization level in the same invocation, as this script already does. Running them as separate invocations was found to introduce a drifting QEMU/host baseline between runs, which produced a false regression for `asm13` at `-O3` in an earlier pass of this work, it didn't hold up once all three were measured together.

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

**Headline result:** accumulator + windowed (`asm13`) beats paired-load + windowed (`asm23`) at every optimization level.

Worth knowing before changing the assembly further:

- **`S` is stored transposed (`Sᵀ`) in memory** — matters for correctness and for reasoning about stride costs in both kernels.
- Instruction-count claims in the thesis are grounded in `objdump -d` disassembly, not theoretical estimates — re-check with `objdump` if you modify the kernels.
- Strassen-style algorithmic restructuring was evaluated and found to give only a modest (~4.3%) net saving for this problem's fixed dimensions, not pursued further.
