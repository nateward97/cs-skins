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
    Aggregates variants by skin_id, computing full wear list, float ranges, crates, and images.
    """
    grouped = {}
    for entry in items:
        # Determine base skin_id
        skin_id = entry.get('skin_id') or entry.get('id').split('_')[0]
        grouped.setdefault(skin_id, []).append(entry)

    aggregated = []
    for skin_id, variants in grouped.items():
        # Base properties from first variant
        base = variants[0]
        out = {
            'id': skin_id,
            'name': base.get('name'),
            'description': base.get('description', ''),
            'weapon': base.get('weapon')['name'] if isinstance(base.get('weapon'), dict) else base.get('weapon'),
            'category': (base.get('category')['name'].lower() if isinstance(base.get('category'), dict)
                         else base.get('category')).lower(),
            'pattern': base.get('pattern')['name'] if isinstance(base.get('pattern'), dict) else base.get('pattern'),
            'min_float': None,
            'max_float': None,
            'rarity': base.get('rarity')['name'] if isinstance(base.get('rarity'), dict) else base.get('rarity'),
            'stattrak': base.get('stattrak', False),
            'souvenir': base.get('souvenir', False),
            'paint_index': base.get('paint_index'),
            'wears': [],
            'crates': [],
            'collections': [],
            'image': {}
        }
        # Floats
        min_vals, max_vals = [], []
        for var in variants:
            # Floats
            try:
                min_f = float(var.get('min_float', 0))
                max_f = float(var.get('max_float', 0))
            except (TypeError, ValueError):
                min_f, max_f = 0.0, 1.0
            min_vals.append(min_f)
            max_vals.append(max_f)
            # Wear names and image mapping
            wear = var.get('wear', {}).get('name') if isinstance(var.get('wear'), dict) else None
            img_url = var.get('image')
            if wear and wear not in out['wears']:
                out['wears'].append(wear)
            if wear and img_url:
                out['image'][wear] = img_url
            # Crates
            for crate in var.get('crates', []):
                if crate not in out['crates']:
                    out['crates'].append(crate)
            # Collections
            for coll in var.get('collections', []):
                if coll not in out['collections']:
                    out['collections'].append(coll)
        out['min_float'] = min(min_vals) if min_vals else 0.0
        out['max_float'] = max(max_vals) if max_vals else 1.0
        aggregated.append(out)
    return aggregated


def generate_weapon_json(api_json_path, output_dir):
    """
    Processes raw API JSON and outputs per-category JSON files matching legacy format.
    """
    os.makedirs(output_dir, exist_ok=True)
    data = load_api_data(api_json_path)

    # Flatten source entries
    if isinstance(data, dict):
        entries = []
        for val in data.values():
            if isinstance(val, dict) and ('contains' in val or 'items' in val):
                entries.extend(val.get('contains', []) or val.get('items', []))
            else:
                entries.append(val)
    elif isinstance(data, list):
        entries = data
    else:
        raise ValueError("Unsupported API JSON structure.")

    # Aggregate
    skins = aggregate_variants(entries)

    # Group by category
    by_cat = {}
    for s in skins:
        cat = s['category']
        by_cat.setdefault(cat, []).append(s)

    # Write files
    for cat, items in by_cat.items():
        fname = f"{cat.rstrip('s')}s.json"
        with open(os.path.join(output_dir, fname), 'w', encoding='utf-8') as f:
            json.dump(items, f, indent=4, ensure_ascii=False, sort_keys=True)
        print(f"Wrote {len(items)} to {fname}")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description="Generate legacy-format per-category pistol JSON from API data."
    )
    parser.add_argument('api_json', help="Path to API JSON file.")
    parser.add_argument('--out', default='.', help="Output directory.")
    args = parser.parse_args()
    generate_weapon_json(args.api_json, args.out)
