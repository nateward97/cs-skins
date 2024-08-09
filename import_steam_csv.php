<?php
// Database credentials
$host = 'localhost'; // Your database host
$port = '3306';      // Your database port
$dbname = 'aigumniz_steam_price_data'; // Your database name
$username = 'aigumniz_steam_price_data'; // Your database username
$password = 'S%9EBMjyRV3W'; // Your database password

// Database connection
try {
    // Create a DSN (Data Source Name) string
    $dsn = "mysql:host=$host;port=$port;dbname=$dbname;charset=utf8";
    $pdo = new PDO($dsn, $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die("Database connection failed: " . $e->getMessage());
}

// Path to the CSV file
$csvFile = 'output_steam.csv'; // Ensure this is the correct path to your CSV file

// Table name in the database where data will be inserted
$tableName = 'steam_output'; // Your table name

// Open the CSV file for reading
if (($handle = fopen($csvFile, 'r')) !== false) {
    // Skip the header row
    fgetcsv($handle);

    // Prepare the SQL statement for inserting data
    $stmt = $pdo->prepare("
        INSERT INTO $tableName (item_name, lowest_sell_order)
        VALUES (:item_name, :lowest_sell_order)
    ");

    // Loop through the CSV rows
    while (($data = fgetcsv($handle, 1000, ',')) !== false) {
        // Bind the CSV data to the SQL statement
        $stmt->bindParam(':item_name', $data[0]);
        $stmt->bindParam(':lowest_sell_order', $data[1]);

        // Execute the statement
        $stmt->execute();
    }

    // Close the CSV file
    fclose($handle);

    echo "Data has been successfully imported into the database.";
} else {
    echo "Error opening the CSV file.";
}
?>
