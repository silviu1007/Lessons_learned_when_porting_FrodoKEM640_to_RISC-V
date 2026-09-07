import re

SW_DUMP  = "benchmarks/sw_O3_full.txt"
ASM_DUMP = "benchmarks/asm13_O3_full.txt"

TARGETS = {
    "SW  frodo_mul_add_as_plus_e": (SW_DUMP,  "<frodo_mul_add_as_plus_e>:"),
    "SW  frodo_mul_add_sa_plus_e": (SW_DUMP,  "<frodo_mul_add_sa_plus_e>:"),
    "ASM inner_mul_row           ": (ASM_DUMP, "<inner_mul_row>:"),
    "ASM sa_mul_row              ": (ASM_DUMP, "<sa_mul_row>:"),
}

RV_REG = re.compile(r'\b(zero|ra|sp|gp|tp|t[0-6]|s[0-9]|s1[01]|a[0-7])\b')
ADDR_RE = re.compile(r'^\s*([0-9a-f]+):\s')

def extract_function(path, symbol):
    lines, inside = [], False
    with open(path) as f:
        for line in f:
            if symbol in line and not inside:  # first match only
                inside = True
            if inside:
                lines.append(line.rstrip())
                if inside and len(lines) > 2 and line.strip() == "":
                    break
    return lines

def get_addr(line):
    m = ADDR_RE.match(line)
    return int(m.group(1), 16) if m else None

def find_inner_loop(lines):
    """
    Find innermost loop by looking for backward branches —
    branches whose target address is LESS than the branch instruction address.
    """
    branch_re = re.compile(r'\b(bne|beq|blt|bge|bltu|bgeu|bnez|beqz|bnez)\b\s+\S+,?\s*\S*,?\s*([0-9a-f]+)\b')

    instr_lines = [(i, line) for i, line in enumerate(lines) if ADDR_RE.match(line)]

    backward_branches = []
    for i, line in instr_lines:
        m = branch_re.search(line)
        if m:
            branch_addr = get_addr(line)
            # target is last hex token before any '<' symbol
            toks = re.findall(r'\b([0-9a-f]+)\b', line.split(':',1)[-1])
            for tok in reversed(toks):
                try:
                    target = int(tok, 16)
                    if branch_addr is not None and target < branch_addr:
                        backward_branches.append((i, target, branch_addr))
                    break
                except ValueError:
                    continue

    if not backward_branches:
        print("  [DEBUG] No backward branches found. Branch lines seen:")
        for i, line in instr_lines:
            if re.search(r'\b(bne|beq|blt|bge|bltu|bgeu|bnez|beqz)\b', line):
                print("   ", line)
        return []

    # pick the last backward branch = innermost loop
    loop_end_idx, target_addr, branch_addr = backward_branches[-1]

    # find the line whose address matches target_addr
    start_idx = 0
    for i, line in instr_lines:
        addr = get_addr(line)
        if addr == target_addr:
            start_idx = i
            break

    return lines[start_idx : loop_end_idx + 1]

def analyse(label, path, symbol):
    print(f"\n{'='*60}")
    print(f"  {label.strip()}")
    print(f"{'='*60}")

    lines = extract_function(path, symbol)
    if not lines:
        print("  [NOT FOUND]")
        return
    print(f"  Total function lines : {len(lines)}")

    inner = find_inner_loop(lines)
    instrs = [l for l in inner if ADDR_RE.match(l)]

    print(f"  Inner loop lines     : {len(inner)}")
    print(f"  Instructions in loop : {len(instrs)}")

    all_regs = set()
    for l in instrs:
        all_regs.update(RV_REG.findall(l))
    all_regs.discard("zero")

    print(f"  Distinct registers   : {len(all_regs)}  ({', '.join(sorted(all_regs))})")
    print(f"    saved s*  : {sorted(r for r in all_regs if r.startswith('s'))}")
    print(f"    temp  t*  : {sorted(r for r in all_regs if r.startswith('t'))}")
    print(f"    args  a*  : {sorted(r for r in all_regs if r.startswith('a'))}")

    loads  = sum(1 for l in instrs if re.search(r'\b(lw|lhu|lh|lb|lwu)\b', l))
    stores = sum(1 for l in instrs if re.search(r'\b(sw|sh|sb)\b', l))
    muls   = sum(1 for l in instrs if re.search(r'\bmul\b', l))
    spills = sum(1 for l in instrs if re.search(r'\b(lw|sw)\b.*\(sp\)', l))

    print(f"  Loads  : {loads}  Stores : {stores}  Muls : {muls}  Spills(sp) : {spills}")

    print("\n  Inner loop listing:")
    for l in inner:
        print("   ", l)

for label, (path, sym) in TARGETS.items():
    analyse(label, path, sym)
print("\nDone.")