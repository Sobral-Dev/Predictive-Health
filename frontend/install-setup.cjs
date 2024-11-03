const { exec } = require('child_process');
const os = require('os');
const path = require('path');
const fs = require('fs');

const isWindows = os.platform() === 'win32';
const nodeVersion = 'v20.12.2';

function runCommand(command, callback) {
  exec(command, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error executing command: ${command}\n${error.message}`);
      if (callback) callback(error, stdout, stderr);
      return;
    }
    console.log(`Command executed successfully: ${command}\n${stdout}`);
    if (callback) callback(null, stdout, stderr);
  });
}

function handleDependencyConflicts(callback) {
  runCommand('npm install --force', (error, stdout, stderr) => {
    if (stderr.includes('ERESOLVE')) {
      console.log('Dependency conflict detected. Resolving conflicts...');
      
      // Extract the problematic package from the stderr
      const conflictMatches = stderr.match(/ERESOLVE unable to resolve dependency tree\n.*\n\s*dependency:\s*(\S+@\S+)/);
      if (conflictMatches && conflictMatches[1]) {
        const problematicPackage = conflictMatches[1];
        console.log(`Attempting to resolve conflict for ${problematicPackage}`);

        // Try to install the problematic package with the --legacy-peer-deps flag
        runCommand(`npm install ${problematicPackage} --legacy-peer-deps`, (installError, installStdout, installStderr) => {
          if (installError) {
            console.error(`Failed to resolve conflict for ${problematicPackage}\n${installError.message}`);
          } else {
            console.log(`Conflict resolved for ${problematicPackage}`);
            handleDependencyConflicts(callback);
          }
        });
      } else {
        console.error('Unable to identify the problematic package.');
      }
    } else {
      callback();
    }
  });
}

function removeNodeModulesAndPackageLock(callback) {
  const pathsToRemove = ['node_modules', 'package-lock.json'];
  let completed = 0;

  pathsToRemove.forEach((filePath) => {
    fs.rm(filePath, { recursive: true, force: true }, (err) => {
      if (err) {
        console.error(`Failed to remove ${filePath}: ${err.message}`);
        return;
      }
      console.log(`${filePath} removed successfully`);
      completed += 1;
      if (completed === pathsToRemove.length) {
        callback();
      }
    });
  });
}

function cleanNpmCache(callback) {
  runCommand('npm cache clean --force', () => {
    callback();
  });
}

function installAndUseNvmOnWindows(callback) {
  const nvmUrl = 'https://github.com/coreybutler/nvm-windows/releases/download/1.1.12/nvm-setup.exe';
  const nvmInstaller = path.join(os.tmpdir(), 'nvm-setup.exe');

  // Download nvm installer
  runCommand(`curl -o ${nvmInstaller} -L ${nvmUrl}`, () => {
    console.log('Downloaded nvm installer');

    // Run nvm installer
    runCommand(nvmInstaller, () => {
      console.log('NVM installed successfully');

      // Install Node.js version
      runCommand(`nvm install ${nodeVersion}`, () => {
        console.log(`Node.js ${nodeVersion} installed successfully`);
        runCommand(`nvm use ${nodeVersion}`, () => {
          console.log(`Using Node.js ${nodeVersion}`);
          callback();
        });
      });
    });
  });
}

function installAndUseNvmOnLinux(callback) {
  const nvmInstallScript = 'https://raw.githubusercontent.com/nvm-sh/nvm//v0.39.7/install.sh';

  // Ensure curl is installed before attempting to download nvm
  runCommand('sudo apt-get update', () => {
    runCommand('sudo apt-get install -y curl', (error) => {
      if (error) {
        console.error('Failed to install curl');
        return;
      }

      // Download and run nvm install script
      runCommand(`curl -o- ${nvmInstallScript} | bash`, () => {
        console.log('NVM installed successfully');

        // Source nvm script to make nvm command available
        runCommand(`source ~/.nvm/nvm.sh && nvm install ${nodeVersion} && nvm use ${nodeVersion}`, () => {
          console.log(`Node.js ${nodeVersion} installed and set to use`);
          callback();
        });
      });
    });
  });
}

function main() {
  if (isWindows) {
    console.log('Detected Windows OS');

    // Install rimraf globally if not installed
    runCommand('npm install -g rimraf', () => {
      installAndUseNvmOnWindows(() => {
        // Install npm-check-updates and update dependencies
        runCommand('npm install -g npm-check-updates', () => {
          runCommand('npx npm-check-updates -u', () => {
            // Handle dependency conflicts
            handleDependencyConflicts(() => {
              // Remove node_modules and package-lock.json using rimraf
              removeNodeModulesAndPackageLock(() => {
                // Clean npm cache
                cleanNpmCache(() => {
                  // Install project dependencies and run scripts
                  runCommand('npm install --force', () => {
                    runCommand('npm run format', () => {
                      console.log('Setup completed successfully');
                    });
                  });
                });
              });
            });
          });
        });
      });
    });
    
  } else {
    console.log('Detected Linux/Unix OS');

    installAndUseNvmOnLinux(() => {
      // Install npm-check-updates and update dependencies
      runCommand('npm install -g npm-check-updates', () => {
        runCommand('npx npm-check-updates -u', () => {
          // Handle dependency conflicts
          handleDependencyConflicts(() => {
            // Remove node_modules and package-lock.json
            removeNodeModulesAndPackageLock(() => {
              // Clean npm cache
              cleanNpmCache(() => {
                // Install project dependencies and run scripts
                runCommand('npm install --force', () => {
                  runCommand('npm run format', () => {
                    console.log('Setup completed successfully');
                  });
                });
              });
            });
          });
        });
      });
    });
  }
}

main();
