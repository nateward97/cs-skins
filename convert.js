const fs = require('fs');

// Function to convert JSON to CSV
function jsonToCsv(json) {
    const items = json.data;
    let csv = 'Item,Platform,OrderType,ConvertedPrice,ConvertedCurrency,Count\n';

    const excludedPlatforms = new Set(['BUFF163', 'MARKETCSGO', 'SKINBARON', 'DMARKET', 'CSMONEY', 'HALOSKINS', 'WHITEMARKET', 'WAXPEER', 'TRADEIT', 'CSGOEMPIRE']);

    for (const [itemName, platforms] of Object.entries(items)) {
        for (const [platform, details] of Object.entries(platforms)) {
            if (excludedPlatforms.has(platform)) {
                continue; // Skip excluded platforms
            }
            if (details.sellOrder) {
                const converted = details.sellOrder.converted;
                const count = details.sellOrder.count;

                csv += `${itemName},${platform},sellOrder,${converted.price},${converted.currency},${count}\n`;
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
