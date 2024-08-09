<?php

// Function to escape CSV fields
function escapeCsv($field) {
    if ($field === null || $field === "") {
        return '""';
    }
    $escapedField = str_replace('"', '""', strval($field)); // Escape double quotes by doubling them
    // Wrap the field in double quotes if it contains a comma, newline, or double quotes
    return "\"$escapedField\"";
}

// Function to clean unwanted characters from strings and trim spaces
function cleanString($str) {
    return trim(preg_replace('/[^\x20-\x7E]/', '', $str));
}

// Function to convert JSON to CSV, ignoring specified columns
function jsonToCsv($json) {
    // Access the 'data' array within the JSON
    $items = $json['data'];

    // Define CSV headers with only the necessary columns
    $csv = "Item Name,Lowest Sell Order\n";

    foreach ($items as $item) {
        $itemName = escapeCsv(cleanString($item['marketHashName']));
        $lowestSellOrder = escapeCsv($item['histogram']['lowestSellOrder']);

        // Build the CSV row, only including the necessary columns
        $csv .= "$itemName,$lowestSellOrder\n";
    }

    return $csv;
}

// Read JSON data from file
$jsonFile = 'data-steam.json';
if (!file_exists($jsonFile)) {
    die('Error: JSON file not found.');
}

$jsonData = file_get_contents($jsonFile);
if ($jsonData === false) {
    die('Error reading JSON file.');
}

$jsonArray = json_decode($jsonData, true);
if ($jsonArray === null) {
    die('Error parsing JSON file.');
}

$csvData = jsonToCsv($jsonArray);

// Write CSV to file
$outputFile = 'output_steam.csv';
if (file_put_contents($outputFile, $csvData) !== false) {
    echo 'CSV file has been created successfully.';
} else {
    echo 'Error writing CSV file.';
}

?>
