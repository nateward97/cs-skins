const fs = require('fs');

// Load the full dataset from the single JSON file
fs.readFile('old-skins.json', 'utf8', (err, data) => {
    if (err) {
        console.error("Error reading the JSON file:", err);
        return;
    }

    const jsonData = JSON.parse(data);
    const rifles = {};

    // Separate skins from collections (assuming collections are in a specific key like 'collection-sets')
    const skins = {};
    const collections = {};

    // Iterate through the JSON to separate skins and collections
    for (const key in jsonData) {
        if (key.startsWith("collection-set")) {
            collections[key] = jsonData[key]; // Collect collections data
        } else {
            skins[key] = jsonData[key]; // Collect skin data
        }
    }

    // Iterate through each skin and filter rifles
    for (const skinId in skins) {
        const skin = skins[skinId];

        // Check if the category is "Rifles"
        if (skin.category && skin.category.name === "Rifles") {
            const baseId = skin.skin_id; // Use the base skin_id to group the wears

            // If this is the first time we're encountering this skin, initialize the entry
            if (!rifles[baseId]) {
                rifles[baseId] = {
                    id: baseId,
                    name: skin.name.split(' (')[0], // Remove wear from the name
                    description: skin.description,
                    weapon: skin.weapon.name,
                    category: "rifle",
                    pattern: skin.pattern.name,
                    min_float: skin.min_float,
                    max_float: skin.max_float,
                    rarity: skin.rarity.name,
                    stattrak: false, // Default to false, will check later
                    souvenir: false, // Default to false, will check later
                    paint_index: skin.paint_index,
                    wears: [],
                    crates: [], // Initialize crates array
                    collections: [], // Initialize collections array
                    image: {},
                };
            }

            // Add wear and corresponding image if not already present
            if (!rifles[baseId].wears.includes(skin.wear.name)) {
                rifles[baseId].wears.push(skin.wear.name);
            }
            rifles[baseId].image[skin.wear.name] = skin.image;

            // Check if StatTrak or Souvenir is true for any variant
            if (skin.stattrak) {
                rifles[baseId].stattrak = true;
            }
            if (skin.souvenir) {
                rifles[baseId].souvenir = true;
            }

            // Add buff and stattrak IDs for each wear state (if available)
            if (skin[`buff-id-${skin.wear.name.toLowerCase().replace(/ /g, '-')}`]) {
                rifles[baseId][`buff-id-${skin.wear.name.toLowerCase().replace(/ /g, '-')}`] = skin[`buff-id-${skin.wear.name.toLowerCase().replace(/ /g, '-')}`];
            }

            if (skin[`stattrak-id-${skin.wear.name.toLowerCase().replace(/ /g, '-')}`]) {
                rifles[baseId][`stattrak-id-${skin.wear.name.toLowerCase().replace(/ /g, '-')}`] = skin[`stattrak-id-${skin.wear.name.toLowerCase().replace(/ /g, '-')}`];
            }

            // Check the collections to find which collection contains this skin
            for (const collectionKey in collections) {
                const collection = collections[collectionKey];

                // Check if the skin is in this collection
                if (collection.contains.some(item => item.id === baseId)) {
                    // If the collection has crates, add the crate information
                    if (collection.crates && collection.crates.length > 0) {
                        collection.crates.forEach(crate => {
                            // Avoid duplicate crates
                            if (!rifles[baseId].crates.some(existingCrate => existingCrate.id === crate.id)) {
                                rifles[baseId].crates.push({
                                    id: crate.id,
                                    name: crate.name,
                                    image: crate.image
                                });
                            }
                        });
                    }

                    // If the collection has no crates, add the collection itself
                    if (collection.crates.length === 0) {
                        // Avoid duplicate collections
                        if (!rifles[baseId].collections.some(existingCollection => existingCollection.id === collection.id)) {
                            rifles[baseId].collections.push({
                                id: collection.id,
                                name: collection.name,
                                image: collection.image
                            });
                        }
                    }
                }
            }
        }
    }

    // Convert the rifles object into an array for saving as JSON
    const rifleArray = Object.values(rifles);

    // Write the merged rifle skins to a new rifles.json file
    fs.writeFile('rifles2.json', JSON.stringify(rifleArray, null, 4), (err) => {
        if (err) {
            console.error("Error writing the file:", err);
            return;
        }

        console.log(`Extracted and merged ${rifleArray.length} rifle skins with collections and crates.`);
    });
});
