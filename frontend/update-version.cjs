const fs = require('fs');

// Captura a nova versão a partir do argumento de linha de comando
const newVersion = process.argv[2];

if (!newVersion) {
  console.error('Nova versão não fornecida!');
  process.exit(1);
}

// Caminho para os arquivos package.json e package-lock.json
const packageJsonPath = './package.json';
const packageLockJsonPath = './package-lock.json';

// Função para atualizar a versão no arquivo JSON fornecido
const updateVersion = (filePath) => {
  const fileContent = fs.readFileSync(filePath, 'utf-8');
  const jsonContent = JSON.parse(fileContent);
  jsonContent.version = newVersion;
  fs.writeFileSync(filePath, JSON.stringify(jsonContent, null, 2));
};

// Atualiza a versão nos arquivos package.json e package-lock.json
updateVersion(packageJsonPath);
updateVersion(packageLockJsonPath);

console.log(`Versão atualizada para ${newVersion} em package.json e package-lock.json`);
