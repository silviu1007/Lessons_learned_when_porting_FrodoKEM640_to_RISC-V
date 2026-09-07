import subprocess
import re
import os
import statistics

BENCHMARKS_DIR = "./benchmarks"
OPT_LEVELS     = ["O0", "O1", "O2", "O3", "Os"]
N_RUNS         = 100

BINARIES = {
    "sw":   "frodo640_sw_{opt}",
    "v1v3": "frodo640_asm13_{opt}",
    "v2v3": "frodo640_asm23_{opt}",
}


def run_binary_once(binary):
    try:
        result = subprocess.run(
            ["/usr/bin/time", "-v", "qemu-riscv64", binary],
            capture_output=True, text=True, timeout=300
        )
        stdout = result.stdout
        stderr = result.stderr

        keygen = re.search(r"Key generation\s+\d+\s+[\d.]+\s+([\d.]+)", stdout)
        encaps = re.search(r"KEM encapsulate\s+\d+\s+[\d.]+\s+([\d.]+)", stdout)
        decaps = re.search(r"KEM decapsulate\s+\d+\s+[\d.]+\s+([\d.]+)", stdout)
        mem    = re.search(r"Maximum resident set size \(kbytes\):\s+(\d+)", stderr)

        if not all([keygen, encaps, decaps, mem]):
            return None

        return {
            "keygen_us": float(keygen.group(1)),
            "encaps_us": float(encaps.group(1)),
            "decaps_us": float(decaps.group(1)),
            "passed":    "Tests PASSED" in stdout,
            "peak_kb":   int(mem.group(1)),
        }

    except subprocess.TimeoutExpired:
        print("  timed out")
        return None
    except Exception as e:
        print(f"  error: {e}")
        return None


def run_binary_n_times(binary, n):
    results = []
    for i in range(n):
        print(f"    run {i+1}/{n}", end="\r", flush=True)
        r = run_binary_once(binary)
        if r is not None:
            results.append(r)
    print()
    return results


def summarise(results):
    if not results:
        return None

    def stats(key):
        vals = [r[key] for r in results]
        return statistics.mean(vals), statistics.stdev(vals) if len(vals) > 1 else 0.0

    km, ks = stats("keygen_us")
    em, es = stats("encaps_us")
    dm, ds = stats("decaps_us")
    mm, _  = stats("peak_kb")

    return {
        "keygen_mean": km, "keygen_sd": ks,
        "encaps_mean": em, "encaps_sd": es,
        "decaps_mean": dm, "decaps_sd": ds,
        "mem_mean":    mm,
        "passed":      all(r["passed"] for r in results),
        "n":           len(results),
    }


def delta_str(base, test):
    if base and test:
        return f"{(test - base) / base * 100:+.1f}%"
    return "N/A"


def mem_str(val):
    return f"{val:.0f}" if val is not None else "N/A"


# ── Run all three binaries per optimisation level ──────────────────────────────

all_results = {opt: {} for opt in OPT_LEVELS}

for opt in OPT_LEVELS:
    print(f"\n=== -{opt} ===")
    for label, pattern in BINARIES.items():
        binary = os.path.join(BENCHMARKS_DIR, pattern.format(opt=opt))
        print(f"  [{label}] running {N_RUNS} times...")
        summary = summarise(run_binary_n_times(binary, N_RUNS))
        all_results[opt][label] = summary
        if summary:
            status = "PASS" if summary["passed"] else "FAIL"
            print(f"  -> {status} ({summary['n']} runs)")


# ── Table 1: SW-only vs v1+v3 and v2+v3 ──────────────────────────────────────

SEP = "=" * 130

print(f"\n{SEP}")
print("  SW-ONLY BASELINE vs v1+v3 and v2+v3")
print(SEP)
print(f"{'Opt':<6} {'Op':<10}"
      f" {'SW mean':>12} {'SW sd':>10}"
      f" {'v1+v3 mean':>12} {'v1+v3 sd':>10} {'Δ vs SW':>10}"
      f" {'v2+v3 mean':>12} {'v2+v3 sd':>10} {'Δ vs SW':>10}"
      f" {'SW RSS':>8} {'v1+v3 RSS':>10} {'v2+v3 RSS':>10}")
print(SEP)

for opt in OPT_LEVELS:
    sw   = all_results[opt].get("sw")
    v1v3 = all_results[opt].get("v1v3")
    v2v3 = all_results[opt].get("v2v3")

    for op_name, mk, sk in [
        ("KeyGen", "keygen_mean", "keygen_sd"),
        ("Encaps", "encaps_mean", "encaps_sd"),
        ("Decaps", "decaps_mean", "decaps_sd"),
    ]:
        sw_m   = sw[mk]   if sw   else None
        v1_m   = v1v3[mk] if v1v3 else None
        v2_m   = v2v3[mk] if v2v3 else None
        sw_s   = sw[sk]   if sw   else None
        v1_s   = v1v3[sk] if v1v3 else None
        v2_s   = v2v3[sk] if v2v3 else None

        print(
            f"{'-'+opt:<6} {op_name:<10}"
            f" {f'{sw_m:.1f}' if sw_m else 'N/A':>12}"
            f" {f'±{sw_s:.1f}' if sw_s else 'N/A':>10}"
            f" {f'{v1_m:.1f}' if v1_m else 'N/A':>12}"
            f" {f'±{v1_s:.1f}' if v1_s else 'N/A':>10}"
            f" {delta_str(sw_m, v1_m):>10}"
            f" {f'{v2_m:.1f}' if v2_m else 'N/A':>12}"
            f" {f'±{v2_s:.1f}' if v2_s else 'N/A':>10}"
            f" {delta_str(sw_m, v2_m):>10}"
            f" {mem_str(sw['mem_mean'] if sw else None):>8}"
            f" {mem_str(v1v3['mem_mean'] if v1v3 else None):>10}"
            f" {mem_str(v2v3['mem_mean'] if v2v3 else None):>10}"
        )
    print()


# ── Table 2: v1+v3 vs v2+v3 head-to-head ─────────────────────────────────────

print(f"\n{SEP}")
print("  HEAD-TO-HEAD: v1+v3 vs v2+v3  (positive Δ = v2+v3 is slower)")
print(SEP)
print(f"{'Opt':<6} {'Op':<10}"
      f" {'v1+v3 mean':>12} {'v1+v3 sd':>10}"
      f" {'v2+v3 mean':>12} {'v2+v3 sd':>10}"
      f" {'Δ (v2 vs v1)':>14}"
      f" {'RSS delta':>10}")
print(SEP)

for opt in OPT_LEVELS:
    v1v3 = all_results[opt].get("v1v3")
    v2v3 = all_results[opt].get("v2v3")

    for op_name, mk, sk in [
        ("KeyGen", "keygen_mean", "keygen_sd"),
        ("Encaps", "encaps_mean", "encaps_sd"),
        ("Decaps", "decaps_mean", "decaps_sd"),
    ]:
        v1_m = v1v3[mk] if v1v3 else None
        v2_m = v2v3[mk] if v2v3 else None
        v1_s = v1v3[sk] if v1v3 else None
        v2_s = v2v3[sk] if v2v3 else None

        rss_v1 = v1v3["mem_mean"] if v1v3 else None
        rss_v2 = v2v3["mem_mean"] if v2v3 else None
        rss_d  = f"{rss_v2 - rss_v1:+.0f}" if rss_v1 and rss_v2 else "N/A"

        print(
            f"{'-'+opt:<6} {op_name:<10}"
            f" {f'{v1_m:.1f}' if v1_m else 'N/A':>12}"
            f" {f'±{v1_s:.1f}' if v1_s else 'N/A':>10}"
            f" {f'{v2_m:.1f}' if v2_m else 'N/A':>12}"
            f" {f'±{v2_s:.1f}' if v2_s else 'N/A':>10}"
            f" {delta_str(v1_m, v2_m):>14}"
            f" {rss_d:>10}"
        )
    print()

print(SEP)
print("Done.")