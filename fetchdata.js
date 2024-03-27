const axios = require('axios');
const fs = require('fs');
const cron = require('node-cron');

// Function to fetch data from the API
async function fetchData() {
    try {
        const response = await axios.get('https://api.steamapihub.com/market-places/all?apiKey=lrt8tPNhX8znmOdpTAh7Uihu5gePg8Mv&appId=730');
        return response.data;
    } catch (error) {
        console.error('Error fetching data:', error);
        return null;
    }
}

// Function to write data to a JSON file
function writeToFile(data) {
    const jsonData = JSON.stringify(data, null, 2); // Indent with 2 spaces
    fs.writeFile('data.json', jsonData, (err) => {
        if (err) {
            console.error('Error writing to file:', err);
        } else {
            console.log('Data written to file successfully');
        }
    });
}

// Schedule the fetch operation every 30 minutes
cron.schedule('*/30 * * * *', async () => {
    console.log('Fetching data...');
    const data = await fetchData();
    if (data) {
        writeToFile(data);
    }
});

// Initial fetch and write
(async () => {
    const initialData = await fetchData();
    if (initialData) {
        writeToFile(initialData);
    }
})();
