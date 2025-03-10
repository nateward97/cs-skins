<?php
header('Content-Type: application/json');

// Database credentials
$host = 'localhost';
$port = '3306';
$dbname = 'aigumniz_steam_price_data';
$username = 'aigumniz_steam_price_data';
$password = 'S%9EBMjyRV3W';

// Create connection
$conn = new mysqli($host, $username, $password, $dbname, $port);

// Check connection
if ($conn->connect_error) {
    die(json_encode(['error' => 'Connection failed: ' . $conn->connect_error]));
}

// Get the skin name from the URL parameter (sanitize the input)
$skinName = isset($_GET['skinName']) ? strtolower($conn->real_escape_string($_GET['skinName'])) : '';

// Check if skin name is provided
if (empty($skinName)) {
    echo json_encode(['error' => 'No skin name provided']);
    exit;
}

// SQL query to fetch prices for the given skin
$sql = "
    SELECT item_name, 
           'STEAM' AS platform,  -- Platform name in uppercase for steam_output
           COALESCE(MIN(lowest_sell_order), 'N/A') AS price, 
           'steam_output' AS source,
           NULL AS total_count
    FROM steam_output 
    WHERE LOWER(item_name) LIKE '%$skinName%' 
    GROUP BY item_name
    
    UNION ALL

    SELECT item_name, 
           platform,  -- Actual platform names from markets_output
           MIN(converted_price) AS price,
           'markets_output' AS source,
           SUM(count) AS total_count
    FROM markets_output
    WHERE LOWER(item_name) LIKE '%$skinName%'
    GROUP BY item_name, platform, converted_price
    ORDER BY item_name ASC
";

// Execute query
$result = $conn->query($sql);

// Initialize an empty array to hold the result
$data = [];

if ($result->num_rows > 0) {
    // Fetch each row and store it in the $data array
    while ($row = $result->fetch_assoc()) {
        $data[] = $row;
    }
} else {
    $data = ['message' => 'No data found for the provided skin'];
}

// Return the data in JSON format
echo json_encode($data);

// Close the database connection
$conn->close();
?>
