const fs = require('fs');
const path = require('path');

// This script removes the <head> and </head> tags from the built index.html file
console.log('Post-build: Removing <head> and </head> tags from index.html');

const indexPath = path.resolve(__dirname, 'build', 'index.html');

fs.readFile(indexPath, 'utf8', (err, data) => {
  if (err) {
    console.error('Error reading index.html:', err);
    process.exit(1);
  }

  // Remove only the <head> and </head> tags, preserving the content within
  const updatedData = data
    .replace(/<head>/i, '')
    .replace(/<\/head>/i, '');

  fs.writeFile(indexPath, updatedData, 'utf8', (err) => {
    if (err) {
      console.error('Error writing updated index.html:', err);
      process.exit(1);
    }
    console.log('Successfully removed <head> and </head> tags from index.html');
  });
});