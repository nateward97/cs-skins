<?php
// Database configuration
$servername = "localhost:3306";
$username = "aigumniz_andy";
$password = "S%9EBMjyRV3W";
$dbname = "aigumniz_cspricedata";

// Create a connection to the database
$conn = new mysqli($servername, $username, $password, $dbname);

// Check the connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Path to the CSV file
$csvFile = '/path/to/your/output.csv';

// Open the CSV file
if (($handle = fopen($csvFile, 'r')) !== FALSE) {
    // Skip the first line (header)
    fgetcsv($handle, 1000, ",");

    // Prepare the SQL statement
    $stmt = $conn->prepare("INSERT INTO datatable (Item, Platform, OrderType, ConvertedPrice, ConvertedCurrency, Count) VALUES (?, ?, ?, ?, ?, ?)");
    $stmt->bind_param("sssssi", $item, $platform, $orderType, $convertedPrice, $convertedCurrency, $count);

    // Read each line from the CSV file
    while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
        // Assign the CSV columns to variables
        $item = $data[0];
        $platform = $data[1];
        $orderType = $data[2];
        $convertedPrice = $data[3];
        $convertedCurrency = $data[4];
        $count = $data[5];

        // Execute the prepared statement
        $stmt->execute();
    }

    // Close the CSV file
    fclose($handle);

    echo "CSV file has been imported successfully.";
} else {
    echo "Error opening the CSV file.";
}

// Close the database connection
$conn->close();
?>
