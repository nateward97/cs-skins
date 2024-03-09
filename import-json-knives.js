const fs = require('fs'); // Require the 'fs' module for file operations
const knives = require('./knives.json');
const apiHubRes = require('./cs2market.json');

function extractWear(name) {
  const wear = name.match(
    /(Factory New|Minimal Wear|Field-Tested|Well-Worn|Battle-Scarred)/,
  );
  return wear ? wear[0] : null;
}

function findImagesFor(name) {
  return apiHubRes.data
    .filter((item) => {
      return item.marketHashName.includes(name);
    })
    .map((item) => {
      return {
        [extractWear(item.marketHashName)]: item.image,
      };
    })
    .reduce((acc, curr) => {
      return { ...acc, ...curr };
    });
}

const res = knives.map((knives) => {
  return {
    ...knives,
    image: findImagesFor(knives.name),
  };
});

// Write the result to a new JSON file
fs.writeFile('result.json', JSON.stringify(res, null, 2), (err) => {
  if (err) {
    console.error('Error writing JSON file:', err);
  } else {
    console.log('JSON file has been saved as result.json');
  }
});
