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
    $items = $json; // In this case, the JSON is an array of items directly.
    $csv = "Item Name,App ID,Latest Price,Median Price,Average Price,Max Price,Min Price,Lowest Sell Order,Highest Buy Order,Buy Order Count,Sell Order Count,Last Updated\n";

    foreach ($items as $item) {
        $itemName = cleanString($item['marketHashName']);
        $appId = escapeCsv($item['appId']);
        $latestPrice = escapeCsv((string)$item['prices']['latest']);
        $medianPrice = escapeCsv((string)$item['prices']['median']);
        $avgPrice = escapeCsv((string)$item['prices']['avg']);
        $maxPrice = escapeCsv((string)$item['prices']['max']);
        $minPrice = escapeCsv((string)$item['prices']['min']);
        $lowestSellOrder = escapeCsv((string)$item['histogram']['lowestSellOrder']);
        $highestBuyOrder = escapeCsv((string)$item['histogram']['highestBuyOrder']);
        $buyOrderCount = escapeCsv((string)$item['histogram']['buyOrderCount']);
        $sellOrderCount = escapeCsv((string)$item['histogram']['sellOrderCount']);
        $updatedAt = escapeCsv($item['updatedAt']);

        // Build the CSV row
        $csv .= "$itemName,$appId,$latestPrice,$medianPrice,$avgPrice,$maxPrice,$minPrice,$lowestSellOrder,$highestBuyOrder,$buyOrderCount,$sellOrderCount,$updatedAt\n";
    }

    return $csv;
}

// Read JSON data from file
$data = file_get_contents('data-steam.json');
if ($data === false) {
    die('Error reading JSON file');
}

$jsonData = json_decode($data, true);
if ($jsonData === null) {
    die('Error decoding JSON file');
}

$csvData = jsonToCsv($jsonData);

// Write CSV to file
if (file_put_contents('output_steam.csv', $csvData) === false) {
    die('Error writing CSV file');
}

echo 'CSV file has been created successfully.';
?>