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

// Query to get all variants of AUG | Chameleon, including normal, StatTrak, and Souvenir
$sql = "
    SELECT item_name, 
           COALESCE(MIN(lowest_sell_order), 'N/A') AS lowest_sell_order 
    FROM steam_output 
    WHERE LOWER(item_name) LIKE '%AUG | Chameleon%' 
    GROUP BY item_name 
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
    <title>AUG | Chameleon Accept Prices</title>
</head>
<body>
    <h1>AUG | Chameleon Acceptm Prices</h1>
    <table border="1">
        <tr>
            <th>Item Name</th>
            <th>Lowest Sell Order</th>
        </tr>

        <?php
        // Check if the query returned any results
        if ($result->num_rows > 0) {
            // Output data of each row
            while ($row = $result->fetch_assoc()) {
                echo "<tr>";
                echo "<td>" . htmlspecialchars($row["item_name"]) . "</td>";
                echo "<td>" . htmlspecialchars($row["lowest_sell_order"]) . "</td>";
                echo "</tr>";
            }
        } else {
            echo "<tr><td colspan='2'>No results found</td></tr>";
        }
        ?>

    </table>
</body>
</html>

<?php
// Close the database connection
$conn->close();
?>
