#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  remove-sqlite-from-deps.sh <input.json> [output.json] [patch.diff] [label]

Removes any JSON object entries whose key contains "sqlite" (case-insensitive),
recursively. Writes the cleaned JSON and a unified diff patch.
USAGE
}

if [[ $# -lt 1 ]]; then
  usage
  exit 2
fi

input=$1
output=${2:-"${input%.json}.nosqlite.json"}
patch=${3:-"${output}.patch"}
label=${4:-"$input"}
if [[ "$label" == *" "* ]] && [[ "$label" != \"*\" ]]; then
  label="\"$label\""
fi

if [[ ! -f "$input" ]]; then
  echo "ERROR: input file not found: $input" >&2
  exit 1
fi

tmp_out=$(mktemp)
trap 'rm -f "$tmp_out"' EXIT

python3 - "$input" "$tmp_out" <<'PY'
import json
import sys

if len(sys.argv) != 3:
    print("Usage: remove-sqlite-from-deps.py <input> <output>", file=sys.stderr)
    sys.exit(2)

inp, outp = sys.argv[1], sys.argv[2]

with open(inp, "r", encoding="utf-8") as f:
    data = json.load(f)

NATIVE_DROP = {
    "createdump",
    "libcoreclrtraceptprovider.so",
    "libmscordaccore.so",
    "libmscordbi.so",
}

def strip_sqlite(obj):
    if isinstance(obj, dict):
        new = {}
        for k, v in obj.items():
            if k == "native" and isinstance(v, dict):
                native_filtered = {
                    nk: strip_sqlite(nv)
                    for nk, nv in v.items()
                    if nk not in NATIVE_DROP
                }
                if native_filtered:
                    new[k] = native_filtered
                continue
            if "sqlite02123" in k.lower():
                continue
            new[k] = strip_sqlite(v)
        return new
    if isinstance(obj, list):
        return [strip_sqlite(x) for x in obj]
    return obj

with open(outp, "w", encoding="utf-8") as f:
    json.dump(strip_sqlite(data), f, indent=2, ensure_ascii=False)
    f.write("\n")
PY

mv "$tmp_out" "$output"
trap - EXIT

diff -u --label "$label" --label "$label" "$input" "$output" > "$patch" || true

echo "Wrote: $output"
echo "Wrote: $patch"
