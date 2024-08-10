<?php
// Database credentials
$host = 'localhost';
$port = '3306';
$dbname = 'aigumniz_steam_price_data';
$username = 'aigumniz_steam_price_data';
$password = 'S%9EBMjyRV3W';

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Query to get AK-47 items
$sql = "SELECT item_name, latest_price, lowest_sell_order FROM steam_output WHERE item_name LIKE 'AK-47%'";
$result = $conn->query($sql);

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AK-47 Prices</title>
</head>
<body>
    <h1>AK-47 Prices</h1>
    <table border="1">
        <tr>
            <th>Item Name</th>
            <th>Latest Price</th>
            <th>Lowest Sell Order</th>
        </tr>

        <?php
        // Check if the query returned any results
        if ($result->num_rows > 0) {
            // Output data of each row
            while($row = $result->fetch_assoc()) {
                echo "<tr>";
                echo "<td>" . $row["item_name"] . "</td>";
                echo "<td>" . ($row["latest_price"] !== null ? $row["latest_price"] : "N/A") . "</td>";
                echo "<td>" . ($row["lowest_sell_order"] !== null ? $row["lowest_sell_order"] : "N/A") . "</td>";
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
