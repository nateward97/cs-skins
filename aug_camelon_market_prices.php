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

// Simplified query to get all variants of AUG | Chameleon without specific columns
$sql = "
    SELECT item_name, 
           platform, 
           SUM(count) AS total_count
    FROM markets_output
    WHERE LOWER(item_name) LIKE '%aug | chameleon%'
    GROUP BY item_name, platform
    ORDER BY item_name, platform
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
    <title>AUG | Chameleon Market Data</title>
</head>
<body>
    <h1>AUG | Chameleon Market Data</h1>
    <table border="1">
        <tr>
            <th>Item Name</th>
            <th>Platform</th>
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
                echo "<td>" . htmlspecialchars($row["total_count"]) . "</td>";
                echo "</tr>";
            }
        } else {
            echo "<tr><td colspan='3'>No results found</td></tr>";
        }
        ?>

    </table>
</body>
</html>

<?php
// Close the database connection
$conn->close();
?>
