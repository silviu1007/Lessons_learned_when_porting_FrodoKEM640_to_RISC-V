import subprocess
import time
import os
import re

BENCHMARKS_DIR = "./benchmarks"
OPT_LEVELS = ["O0", "O1", "O2", "O3", "Os"]

def run_binary(binary):
    try:
        start = time.time()
        proc = subprocess.run(
            ["/usr/bin/time", "-v", "qemu-riscv64", binary],
            capture_output=True,
            text=True,
            timeout=300
        )
        elapsed = time.time() - start
        output = proc.stdout
        stderr = proc.stderr

        keygen = re.search(r"Key generation\s+\d+\s+[\d.]+\s+([\d.]+)", output)
        encaps = re.search(r"KEM encapsulate\s+\d+\s+[\d.]+\s+([\d.]+)", output)
        decaps = re.search(r"KEM decapsulate\s+\d+\s+[\d.]+\s+([\d.]+)", output)
        passed = "Tests PASSED" in output
        mem    = re.search(r"Maximum resident set size \(kbytes\):\s+(\d+)", stderr)

        return {
            "keygen_us": float(keygen.group(1)) if keygen else None,
            "encaps_us": float(encaps.group(1)) if encaps else None,
            "decaps_us": float(decaps.group(1)) if decaps else None,
            "total_s":   elapsed,
            "passed":    passed,
            "peak_kb":   int(mem.group(1)) if mem else None
        }
    except subprocess.TimeoutExpired:
        return None
    except Exception as e:
        print(f"    ERROR: {e}")
        return None

ref_results     = {}
testing_results = {}

for opt in OPT_LEVELS:
    ref_bin     = os.path.abspath(os.path.join(BENCHMARKS_DIR, f"frodo640_{opt}"))
    testing_bin = os.path.abspath(os.path.join(BENCHMARKS_DIR, f"frodo640_testing_{opt}"))

    print(f"\n=== -{opt} ===")
    print(f"  [reference] running...")
    ref_results[opt] = run_binary(ref_bin)
    print(f"  [testing]   running...")
    testing_results[opt] = run_binary(testing_bin)

    r = ref_results[opt]
    t = testing_results[opt]
    status_r = "PASS" if r and r["passed"] else "FAIL"
    status_t = "PASS" if t and t["passed"] else "FAIL"
    print(f"  reference: {status_r}   testing: {status_t}")

print("\n" + "="*100)
print(f"{'Opt':<6} {'Operation':<12} {'Ref time':>12} {'Test time':>12} {'Time delta':>12} {'Ref RAM (KB)':>14} {'Test RAM (KB)':>14} {'RAM delta':>12}")
print("-"*100)

for opt in OPT_LEVELS:
    r = ref_results[opt]
    t = testing_results[opt]

    for op_name, r_key, t_key in [
        ("KeyGen",  "keygen_us", "keygen_us"),
        ("Encaps",  "encaps_us", "encaps_us"),
        ("Decaps",  "decaps_us", "decaps_us"),
    ]:
        r_time   = r[r_key]   if r and r[r_key]   else None
        t_time   = t[t_key]   if t and t[t_key]   else None
        r_mem    = r["peak_kb"] if r else None
        t_mem    = t["peak_kb"] if t else None

        time_delta = f"{((t_time - r_time)/r_time)*100:+.1f}%" if r_time and t_time else "N/A"
        ram_delta  = f"{t_mem - r_mem:+d} KB"                  if r_mem  and t_mem  else "N/A"

        r_time_str = f"{r_time:.1f} us" if r_time else "FAIL"
        t_time_str = f"{t_time:.1f} us" if t_time else "FAIL"
        r_mem_str  = f"{r_mem}"         if r_mem  else "N/A"
        t_mem_str  = f"{t_mem}"         if t_mem  else "N/A"

        print(f"{'-'+opt:<6} {op_name:<12} {r_time_str:>12} {t_time_str:>12} {time_delta:>12} {r_mem_str:>14} {t_mem_str:>14} {ram_delta:>12}")

    print()