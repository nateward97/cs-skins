const fs = require('fs');

// Function to convert JSON to CSV
function jsonToCsv(json) {
    const items = json.data;
    let csv = 'Item,Platform,OrderType,ConvertedPrice,ConvertedCurrency,Count,UpdatedAt\n';

    for (const [itemName, platforms] of Object.entries(items)) {
        for (const [platform, details] of Object.entries(platforms)) {
            for (const orderType of ['sellOrder', 'buyOrder']) {
                if (details[orderType]) {
                    const converted = details[orderType].converted;
                    const count = details[orderType].count;
                    const updatedAt = details.updatedAt;

                    csv += `${itemName},${platform},${orderType},${converted.price},${converted.currency},${count},${updatedAt}\n`;
                }
            }
        }
    }
    return csv;
}

// Read JSON data from file
fs.readFile('data.json', 'utf8', (err, data) => {
    if (err) {
        console.error('Error reading JSON file:', err);
        return;
    }
    const jsonData = JSON.parse(data);
    const csvData = jsonToCsv(jsonData);

    // Write CSV to file
    fs.writeFileSync('output.csv', csvData);

    console.log('CSV file has been created successfully.');
});