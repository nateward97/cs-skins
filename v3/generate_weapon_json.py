import json
import os

def load_api_data(path):
    """
    Loads JSON data from a file, handling either a single JSON value or JSON Lines.
    """
    text = open(path, 'r', encoding='utf-8').read()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        items = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                items.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return items


def aggregate_variants(items):
    """
    Aggregates float ranges across variants for each base skin_id.
    Treats explicit [0.0, 0.0] ranges as missing, defaulting to full [0.0, 1.0].
    """
    grouped = {}
    for item in items:
        skin_id = item.get('skin_id') or item.get('id').split('_')[0]
        raw_min = item.get('min_float')
        raw_max = item.get('max_float')
        # Determine floats, treat None or placeholder zeros as full range
        try:
            has_values = raw_min is not None and raw_max is not None
            min_val = float(raw_min) if has_values else None
            max_val = float(raw_max) if has_values else None
        except (TypeError, ValueError):
            min_val = max_val = None
        if min_val is None or max_val is None or (min_val == 0.0 and max_val == 0.0):
            min_f, max_f = 0.0, 1.0
        else:
            min_f, max_f = min_val, max_val
        grouped.setdefault(skin_id, []).append({'item': item, 'min_f': min_f, 'max_f': max_f})

    aggregated = []
    for skin_id, variants in grouped.items():
        min_float = min(v['min_f'] for v in variants)
        max_float = max(v['max_f'] for v in variants)
        rep = variants[0]['item'].copy()
        rep['id'] = skin_id
        rep['min_float'] = min_float
        rep['max_float'] = max_float
        rep.pop('skin_id', None)
        aggregated.append(rep)
    return aggregated


def generate_weapon_files(api_json_path, output_dir):
    """
    Reads API JSON, aggregates variants with corrected float handling,
    groups by category, and writes per-category JSON files.
    """
    os.makedirs(output_dir, exist_ok=True)
    data = load_api_data(api_json_path)

    # Flatten items
    if isinstance(data, dict):
        all_items = []
        for val in data.values():
            if isinstance(val, dict) and ('contains' in val or 'items' in val):
                all_items.extend(val.get('contains', []) or val.get('items', []))
            else:
                all_items.append(val)
    elif isinstance(data, list):
        all_items = data
    else:
        raise ValueError("Unsupported API JSON structure.")

    # Aggregate float ranges with placeholder detection
    aggregated = aggregate_variants(all_items)

    # Group by category
    categories = {}
    for item in aggregated:
        cat_field = item.get('category') or item.get('type') or 'unknown'
        if isinstance(cat_field, dict):
            cat = cat_field.get('name', 'unknown').lower()
        else:
            cat = str(cat_field).lower()
        categories.setdefault(cat, []).append(item)

    # Write per-category files
    for category, items in categories.items():
        filename = f"{category.rstrip('s')}s.json"
        with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as f_out:
            json.dump(items, f_out, indent=4, ensure_ascii=False)
        print(f"Wrote {len(items)} items to {filename}")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description="Generate per-category weapon JSON files with corrected float handling."
    )
    parser.add_argument('api_json', help="Path to the API JSON file.")
    parser.add_argument('--out', default='.', help="Output directory for generated JSON files.")
    args = parser.parse_args()

    generate_weapon_files(args.api_json, args.out)
