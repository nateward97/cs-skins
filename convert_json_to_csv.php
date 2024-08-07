<?php
// Function to escape CSV fields
function escapeCsv($field) {
    return '"' . str_replace('"', '""', $field) . '"';
}

// Function to clean unwanted characters from strings and trim spaces
function cleanString($str) {
    // Remove or replace unwanted characters and trim spaces
    return trim(preg_replace('/[^\x20-\x7E]/', '', $str)); // Removes non-ASCII characters and trims spaces
}

// Function to convert JSON to CSV
function jsonToCsv($json) {
    $items = $json['data'];
    $csv = "Item,Platform,OrderType,ConvertedPrice,ConvertedCurrency,Count\n";

    $excludedPlatforms = ['BUFF163', 'MARKETCSGO', 'SKINBARON', 'DMARKET', 'CSMONEY', 'HALOSKINS', 'WHITEMARKET', 'WAXPEER', 'TRADEIT', 'CSGOEMPIRE'];

    foreach ($items as $itemName => $platforms) {
        $cleanedItemName = cleanString($itemName);
        foreach ($platforms as $platform => $details) {
            if (in_array($platform, $excludedPlatforms)) {
                continue; // Skip excluded platforms
            }
            if (isset($details['sellOrder'])) {
                $converted = $details['sellOrder']['converted'];
                $count = $details['sellOrder']['count'];

                // Properly quote and escape each field
                $csv .= escapeCsv($cleanedItemName) . ',' . escapeCsv($platform) . ',sellOrder,' . escapeCsv((string)$converted['price']) . ',' . escapeCsv($converted['currency']) . ',' . escapeCsv((string)$count) . "\n";
            }
        }
    }
    return $csv;
}

// Read JSON data from file
$data = file_get_contents('data.json');
if ($data === false) {
    die('Error reading JSON file');
}

$jsonData = json_decode($data, true);
if ($jsonData === null) {
    die('Error decoding JSON file');
}

$csvData = jsonToCsv($jsonData);

// Write CSV to file
if (file_put_contents('output.csv', $csvData) === false) {
    die('Error writing CSV file');
}

echo 'CSV file has been created successfully.';
?>
