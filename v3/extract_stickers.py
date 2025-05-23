import json

# Load the original data
with open('all.json', 'r', encoding='utf-8') as infile:
    data = json.load(infile)

# Filter only keys that start with 'sticker-'
stickers = {k: v for k, v in data.items() if k.startswith('sticker-')}

# Save the stickers to a new file
with open('stickers.json', 'w', encoding='utf-8') as outfile:
    json.dump(stickers, outfile, indent=2, ensure_ascii=False)

print(f"Extracted {len(stickers)} stickers to stickers.json")
