const fs = require('fs');

// Read the transformed JSON data from the file
const transformedData = require('./transformed.json');

function convertJson(json) {
    const convertedJson = {};

    json.forEach(item => {
        const id = `sticker-${item.id}`;
        convertedJson[id] = {
            id: id,
            name: item.name,
            description: item.description,
            variant: item.variant,
            rarity: item.rarity,
            image: item.image,
            letter: item.letter,
            "buff-id": item["buff-id"],
            "buff-stickersearch-id": item["buff-stickersearch-id"]
        };
    });

    return convertedJson;
}

const convertedJson = convertJson(transformedData);

fs.writeFile('converted.json', JSON.stringify(convertedJson, null, 2), (err) => {
    if (err) throw err;
    console.log('Converted JSON data has been saved to converted.json');
});
