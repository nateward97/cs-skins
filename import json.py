import json
import csv

def flatten_json(json_data):
    flattened_data = {}
    for key, value in json_data.items():
        if isinstance(value, dict):
            flattened_sub_data = flatten_json(value)
            for sub_key, sub_value in flattened_sub_data.items():
                flattened_data[key + '.' + sub_key] = sub_value
        else:
            flattened_data[key] = value
    return flattened_data

def json_to_csv(json_file, csv_file):
    # Open the JSON file
    with open(json_file, 'r') as f:
        data = json.load(f)

    # Flatten the JSON data
    flattened_data = []
    flattened_item = flatten_json(data)
    flattened_data.append(flattened_item)

    # Extract the headers from the first item
    headers = flattened_data[0].keys()

    # Open the CSV file in write mode with UTF-8 encoding
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)

        # Write the header
        writer.writeheader()

        # Write the data
        writer.writerows(flattened_data)

# Example usage:
json_to_csv('data-steam.json', 'data-steam.csv')
