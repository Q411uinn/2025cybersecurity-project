#!/usr/bin/env python3
import json, sys

if len(sys.argv) < 2:
    print("Usage: python3 constants_to_circom.py constants.json > ../circuits/constants.circom")
    sys.exit(1)

with open(sys.argv[1], 'r') as f:
    data = json.load(f)

# expected fields: field_prime (string or int), t, d, RF, RP, ROUND_CONSTANTS (list), MDS (list of lists)
p = data.get("field_prime")
t = data.get("t")
d = data.get("d")
RF = data.get("RF")
RP = data.get("RP")
RC = data.get("ROUND_CONSTANTS")  # flat list or nested
MDS = data.get("MDS")

if p is None or t is None or d is None or RF is None or RP is None or RC is None or MDS is None:
    print("Missing fields in constants.json. Required: field_prime, t, d, RF, RP, ROUND_CONSTANTS, MDS")
    sys.exit(2)

# flatten if necessary
flat_rc = []
if any(isinstance(x, list) for x in RC):
    for row in RC:
        flat_rc.extend(row)
else:
    flat_rc = RC

flat_mds = []
for row in MDS:
    flat_mds.extend(row)

out = []
out.append("pragma circom 2.1.6;\n")
out.append(f"var FIELD_PRIME = {p};\n")
out.append(f"var t_param = {t};\n")
out.append(f"var d_param = {d};\n")
out.append(f"var RF = {RF};\n")
out.append(f"var RP = {RP};\n")
out.append("\n// ROUND_CONSTANTS (flattened)\n")
out.append("var ROUND_CONSTANTS = [\n")
for i, v in enumerate(flat_rc):
    out.append(f"  {v}," + ("\n" if (i+1) % t == 0 else " "))
out.append("];\n\n")
out.append("// MDS (flattened row-major)\n")
out.append("var MDS = [\n")
for i, v in enumerate(flat_mds):
    out.append(f"  {v}," + ("\n" if (i+1) % t == 0 else " "))
out.append("];\n")

sys.stdout.write("".join(out))