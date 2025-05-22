import json
import os

def generate_weapon_files(api_json_path, output_dir):
    """
    Reads the API JSON, flattens all weapons from nested collections, groups by 'category', 
    and writes separate JSON files for each category.

    Args:
        api_json_path (str): Path to the API JSON file (nested collections format).
        output_dir (str): Directory where generated JSON files will be saved.
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Load API data
    with open(api_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Flatten items: support either top-level list or dict of collections with 'contains'
    all_items = []
    if isinstance(data, list):
        all_items = data
    elif isinstance(data, dict):
        for coll in data.values():
            # Each collection may list skins under 'contains'
            skins = coll.get('contains', [])
            all_items.extend(skins)
    else:
        raise ValueError("Unsupported API JSON structure; expected list or dict.")

    # Group by category
    categories = {}
    for item in all_items:
        cat = item.get('category', 'unknown')
        categories.setdefault(cat, []).append(item)

    # Write per-category files
    for category, items in categories.items():
        # pluralize filename: e.g. 'pistol' -> 'pistols.json'
        filename = os.path.join(output_dir, f"{category.rstrip('s')}s.json")
        with open(filename, 'w', encoding='utf-8') as out:
            json.dump(items, out, indent=4, ensure_ascii=False)
        print(f"Wrote {len(items)} items to {filename}")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate per-category weapon JSON files from nested API data"
    )
    parser.add_argument(
        'api_json', help="Path to the API JSON file containing collections"
    )
    parser.add_argument(
        '--out', default='.', help="Output directory for generated JSON files"
    )
    args = parser.parse_args()

    generate_weapon_files(args.api_json, args.out)
