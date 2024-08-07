const fs = require('fs');

// Function to escape CSV fields
const escapeCsv = (field) => `"${field.replace(/"/g, '""')}"`;

// Function to clean unwanted characters from strings and trim spaces
const cleanString = (str) => {
    // Remove or replace unwanted characters and trim spaces
    return str.replace(/[^\x20-\x7E]/g, '').trim(); // Removes non-ASCII characters and trims spaces
};

// Function to convert JSON to CSV
function jsonToCsv(json) {
    const items = json.data;
    let csv = 'Item,Platform,OrderType,ConvertedPrice,ConvertedCurrency,Count\n';

    const excludedPlatforms = new Set(['BUFF163', 'MARKETCSGO', 'SKINBARON', 'DMARKET', 'CSMONEY', 'HALOSKINS', 'WHITEMARKET', 'WAXPEER', 'TRADEIT', 'CSGOEMPIRE']);

    for (const [itemName, platforms] of Object.entries(items)) {
        const cleanedItemName = cleanString(itemName);
        for (const [platform, details] of Object.entries(platforms)) {
            if (excludedPlatforms.has(platform)) {
                continue; // Skip excluded platforms
            }
            if (details.sellOrder) {
                const converted = details.sellOrder.converted;
                const count = details.sellOrder.count;

                // Properly quote and escape each field
                csv += `${escapeCsv(cleanedItemName)},${escapeCsv(platform)},sellOrder,${escapeCsv(converted.price.toString())},${escapeCsv(converted.currency)},${escapeCsv(count.toString())}\n`;
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
