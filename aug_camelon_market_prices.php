<?php
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
    die("Connection failed: " . $conn->connect_error);
}

// Query to combine data from both tables
$sql = "
    SELECT item_name, 
           'STEAM' AS platform,  -- Platform name in uppercase for steam_output
           COALESCE(MIN(lowest_sell_order), 'N/A') AS price, 
           'steam_output' AS source,
           NULL AS total_count
    FROM steam_output 
    WHERE LOWER(item_name) LIKE '%aug | chameleon%' 
    GROUP BY item_name
    
    UNION ALL

    SELECT item_name, 
           platform,  -- Actual platform names from markets_output
           MIN(converted_price) AS price,
           'markets_output' AS source,
           SUM(count) AS total_count
    FROM markets_output
    WHERE LOWER(item_name) LIKE '%aug | chameleon%'
    GROUP BY item_name, platform, converted_price
    ORDER BY item_name ASC
";

// Execute query
$result = $conn->query($sql);

// Check for SQL errors
if ($conn->error) {
    echo "SQL Error: " . $conn->error;
    exit;
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AUG | Chameleon Data</title>
</head>
<body>
    <h1>AUG | Chameleon Data</h1>
    <table border="1">
        <tr>
            <th>Item Name</th>
            <th>Platform</th>
            <th>Price</th>
            <th>Source</th>
            <th>Total Count</th>
        </tr>

        <?php
        // Check if the query returned any results
        if ($result->num_rows > 0) {
            // Output data of each row
            while ($row = $result->fetch_assoc()) {
                echo "<tr>";
                echo "<td>" . htmlspecialchars($row["item_name"]) . "</td>";
                echo "<td>" . htmlspecialchars($row["platform"]) . "</td>";
                echo "<td>" . htmlspecialchars($row["price"]) . "</td>";
                echo "<td>" . htmlspecialchars($row["source"]) . "</td>";
                echo "<td>" . htmlspecialchars($row["total_count"]) . "</td>";
                echo "</tr>";
            }
        } else {
            echo "<tr><td colspan='5'>No results found</td></tr>";
        }
        ?>

    </table>
</body>
</html>

<?php
// Close the database connection
$conn->close();
?>
