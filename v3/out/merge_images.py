import json
import os

def load_json(path):
    """Loads JSON array or dict from a file"""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def merge_variant_images(entry_data_path, all_skins_path, output_path):
    """
    Reads aggregated pistols.json (list of variant entries) and the full skins dump (id -> variant entries),
    builds wear->image map for each base skin, and writes merged output.
    """
    # Load aggregated entries (list of variant skins)
    base_skins = load_json(entry_data_path)
    # Load all skins dump; can be dict or list
    all_skins = load_json(all_skins_path)
    # Normalize all_skins to dict id->entry
    if isinstance(all_skins, list):
        all_lookup = {item['id']: item for item in all_skins}
    else:
        all_lookup = all_skins

    # Build mapping: base_skin_id -> {wear_name: image_url}
    image_maps = {}
    for var_id, var_entry in all_lookup.items():
        # variant id like skin-xxx_y[_st]
        parts = var_id.split('_')
        base_id = parts[0]
        # wear name from var_entry['wear']['name']
        wear = var_entry.get('wear', {}).get('name')
        url = var_entry.get('image')
        if wear and url:
            image_maps.setdefault(base_id, {})[wear] = url

    # Merge into base_skins
    missing = []
    for skin in base_skins:
        # Determine base_id: use skin_id field if present, otherwise strip suffix
        base_id = skin.get('skin_id') or skin.get('id', '').split('_')[0]
        imap = image_maps.get(base_id)
        if imap:
            skin['image'] = imap
        else:
            missing.append(base_id)

    applied = len(base_skins) - len(missing)
    print(f"Applied image maps to {applied}/{len(base_skins)} skins.")
    if missing:
        uniq = sorted(set(missing))
        print(f"Warning: no image data for skins: {', '.join(uniq[:10])}...")

    # Write merged output
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(base_skins, f, indent=4, ensure_ascii=False, sort_keys=True)
    print(f"Wrote merged file: {output_path}")


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description="Merge wear->image maps into aggregated pistols JSON using full skins dump.")
    p.add_argument('base_json', help="Path to aggregated pistols.json (variant skins)")
    p.add_argument('all_skins', help="Path to full skins dump JSON (all variants)")
    p.add_argument('out', help="Output path for merged pistols.json")
    args = p.parse_args()
    merge_variant_images(args.base_json, args.all_skins, args.out)
