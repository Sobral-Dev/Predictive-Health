const fs = require('fs');
const path = require('path');

function removeSnapFiles(dir) {
  fs.readdir(dir, (err, files) => {
    if (err) throw err;
    for (const file of files) {
      const filePath = path.join(dir, file);
      fs.stat(filePath, (err, stat) => {
        if (err) throw err;
        if (stat.isDirectory()) {
          removeSnapFiles(filePath);
        } else if (file.endsWith('.snap')) {
          fs.unlink(filePath, (err) => {
            if (err) throw err;
            console.log(`Deleted ${filePath}`);
          });
        }
      });
    }
  });
}

const snapDirectories = ['./tests', './src']; 
snapDirectories.forEach(dir => removeSnapFiles(dir));
