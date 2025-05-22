#!/usr/bin/env python3
import json
import sys
from pathlib import Path

def main():
    if len(sys.argv) < 4:
        print(f"Usage: {Path(sys.argv[0]).name} mid-tier.json heavys.json smgs.json [...] merged.json")
        sys.exit(1)

    *inputs, out_path = sys.argv[1:]
    merged = []
    for p in inputs:
        with open(p, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data, list):
                raise ValueError(f"{p} does not contain a top-level array")
            merged.extend(data)
    # Optional: dedupe by id
    # seen = set()
    # unique = []
    # for item in merged:
    #     if item['id'] not in seen:
    #         seen.add(item['id'])
    #         unique.append(item)
    # merged = unique

    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(merged, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
