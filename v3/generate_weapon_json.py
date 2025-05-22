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


def aggregate_variants(items, image_lookup):
    """
    Aggregates variants by skin_id, collecting wear tiers, float ranges, crates,
    collections, and merging image maps from the lookup.
    """
    grouped = {}
    for entry in items:
        skin_id = entry.get('skin_id') or entry.get('id').split('_')[0]
        grouped.setdefault(skin_id, []).append(entry)

    aggregated = []
    for skin_id, variants in grouped.items():
        base = variants[0]
        out = {
            'id': skin_id,
            'name': base.get('name'),
            'description': base.get('description', ''),
            'weapon': base.get('weapon', {}).get('name') if isinstance(base.get('weapon'), dict) else base.get('weapon'),
            'category': (base.get('category', {}).get('name', 'unknown').lower()
                         if isinstance(base.get('category'), dict) else str(base.get('category')).lower()),
            'pattern': base.get('pattern', {}).get('name') if isinstance(base.get('pattern'), dict) else base.get('pattern'),
            'min_float': None,
            'max_float': None,
            'rarity': base.get('rarity', {}).get('name') if isinstance(base.get('rarity'), dict) else base.get('rarity'),
            'stattrak': base.get('stattrak', False),
            'souvenir': base.get('souvenir', False),
            'paint_index': base.get('paint_index'),
            'wears': [],
            'crates': [],
            'collections': [],
            'image': {}
        }
        min_vals, max_vals = [], []
        for var in variants:
            # Floats
            try:
                min_f = float(var.get('min_float', 0))
                max_f = float(var.get('max_float', 1))
            except (TypeError, ValueError):
                min_f, max_f = 0.0, 1.0
            min_vals.append(min_f)
            max_vals.append(max_f)

            # Wear tiers
            wear = var.get('wear', {}).get('name') if isinstance(var.get('wear'), dict) else None
            if wear and wear not in out['wears']:
                out['wears'].append(wear)

            # Crates and collections
            for crate in var.get('crates', []):
                if crate not in out['crates']:
                    out['crates'].append(crate)
            for coll in var.get('collections', []):
                if coll not in out['collections']:
                    out['collections'].append(coll)

            # Merge images from lookup
            variant_id = var.get('id')
            img_data = image_lookup.get(variant_id, {})
            img_map = img_data.get('image')
            if isinstance(img_map, dict):
                for w_name, url in img_map.items():
                    if w_name not in out['wears']:
                        out['wears'].append(w_name)
                    out['image'][w_name] = url

        out['min_float'] = min(min_vals) if min_vals else 0.0
        out['max_float'] = max(max_vals) if max_vals else 1.0
        aggregated.append(out)
    return aggregated


def generate_weapon_json(api_json_path, skin_api_path, output_dir):
    """
    Generates per-category JSON files by combining skin entries with a master image lookup.
    """
    os.makedirs(output_dir, exist_ok=True)
    entries = load_api_data(api_json_path)
    all_skins = load_api_data(skin_api_path)

    # Build image lookup: id -> full skin data
    if isinstance(all_skins, list):
        image_lookup = {item.get('id'): item for item in all_skins}
    else:
        image_lookup = all_skins

    # Flatten skin entries list or dict
    if isinstance(entries, dict):
        flat = []
        for v in entries.values():
            if isinstance(v, dict) and ('contains' in v or 'items' in v):
                flat.extend(v.get('contains', []) or v.get('items', []))
            else:
                flat.append(v)
        entries = flat

    # Aggregate and merge
    skins = aggregate_variants(entries, image_lookup)

    # Group by category and write
    by_cat = {}
    for s in skins:
        by_cat.setdefault(s['category'], []).append(s)

    for cat, items in by_cat.items():
        filepath = os.path.join(output_dir, f"{cat.rstrip('s')}s.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(items, f, indent=4, ensure_ascii=False, sort_keys=True)
        print(f"Wrote {len(items)} items to {filepath}")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description="Merge variant skin data with master images and output by category."
    )
    parser.add_argument('api_json', help="Path to the skin entries JSON file (api.json)")
    parser.add_argument('skin_api', help="Path to the master all-skins JSON file (all.json)")
    parser.add_argument('--out', default='.', help="Output directory for generated JSON files")
    args = parser.parse_args()
    generate_weapon_json(args.api_json, args.skin_api, args.out)
