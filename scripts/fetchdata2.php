<?php

// Function to fetch data from the API
function fetchData() {
    $apiKey = 'lrt8tPNhX8znmOdpTAh7Uihu5gePg8Mv';
    $appId = '730';
    $url = 'https://api.steamapihub.com/market-items/all?apiKey=' . $apiKey . '&appId=' . $appId;

    $response = file_get_contents($url);
    if ($response === FALSE) {
        echo 'Error fetching data';
        return null;
    }

    return json_decode($response, true);
}

// Function to write data to a JSON file
function writeToFile($data) {
    $jsonData = json_encode($data);
    file_put_contents('data-steam.json', $jsonData); // Changed filename to 'data-steam.json'
    echo 'Data written to file successfully';
}

// Initial fetch and write
$initialData = fetchData();
if ($initialData !== null) {
    writeToFile($initialData);
}

?>
