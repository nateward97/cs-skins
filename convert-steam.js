const fs = require('fs');

// Function to escape CSV fields
function escapeCsv(field) {
    if (field === undefined || field === null) {
        return '""';
    }
    const escapedField = String(field).replace(/"/g, '""'); // Escape double quotes by doubling them
    // Wrap the field in double quotes if it contains a comma, newline, or double quotes
    return `"${escapedField}"`;
}

// Function to clean unwanted characters from strings and trim spaces
function cleanString(str) {
    return str.replace(/[^\x20-\x7E]/g, '').trim();
}

// Function to convert JSON to CSV
function jsonToCsv(json) {
    // Access the 'data' array within the JSON
    const items = json.data;

    // Define CSV headers
    let csv = "Item Name,App ID,Latest Price,Median Price,Average Price,Max Price,Min Price,Lowest Sell Order,Highest Buy Order,Buy Order Count,Sell Order Count,Last Updated\n";

    items.forEach(item => {
        const itemName = escapeCsv(cleanString(item.marketHashName));
        const appId = escapeCsv(item.appId);
        const latestPrice = escapeCsv(item.prices.latest);
        const medianPrice = escapeCsv(item.prices.median);
        const avgPrice = escapeCsv(item.prices.avg);
        const maxPrice = escapeCsv(item.prices.max);
        const minPrice = escapeCsv(item.prices.min);
        const lowestSellOrder = escapeCsv(item.histogram.lowestSellOrder);
        const highestBuyOrder = escapeCsv(item.histogram.highestBuyOrder);
        const buyOrderCount = escapeCsv(item.histogram.buyOrderCount);
        const sellOrderCount = escapeCsv(item.histogram.sellOrderCount);
        const updatedAt = escapeCsv(item.updatedAt);

        // Build the CSV row
        csv += `${itemName},${appId},${latestPrice},${medianPrice},${avgPrice},${maxPrice},${minPrice},${lowestSellOrder},${highestBuyOrder},${buyOrderCount},${sellOrderCount},${updatedAt}\n`;
    });

    return csv;
}

// Read JSON data from file
fs.readFile('data-steam.json', 'utf8', (err, data) => {
    if (err) {
        console.error('Error reading JSON file:', err);
        return;
    }

    let jsonData;
    try {
        jsonData = JSON.parse(data);
    } catch (parseErr) {
        console.error('Error parsing JSON file:', parseErr);
        return;
    }

    const csvData = jsonToCsv(jsonData);

    // Write CSV to file
    fs.writeFile('output_steam.csv', csvData, (err) => {
        if (err) {
            console.error('Error writing CSV file:', err);
        } else {
            console.log('CSV file has been created successfully.');
        }
    });
});
