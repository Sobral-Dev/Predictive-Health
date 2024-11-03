# Documentação do Projeto "Patient System"

## Visualização Hierárquica do Projeto

```plaintext
PatientSystem/
│
├── backend-PatientSystem/
│   ├── app.py
│   ├── auth.py
│   ├── config.py
│   ├── models.py
│   └── schemas.py
│
├── frontend-PatientSystem/
│   ├── .github/
│   ├── node_modules/
│   ├── src/
│   ├── tests/
│   ├── .gitattributes
│   ├── .gitignore
│   ├── .prettierrc.json
│   ├── .releaserc.json
│   ├── env.d.ts
│   ├── globalSetup.ts
│   ├── index.html
│   ├── install-setup.cjs
│   ├── package-lock.json
│   ├── package.json
│   ├── README.md
│   ├── setupTests.ts
│   ├── sonar-project.properties
│   ├── tsconfig.*
│   ├── vite.config.ts
│   ├── vitest.config.ts
│   └── webpack.config.js
│
├── health-predictive-dataset/
│   ├── diabetes_data.csv
│   ├── hypertension_data.csv
│   └── stroke_data.csv
│
└── models/
    ├── diabetes_model.pkl
    ├── hypertension_model.pkl
    └── stroke_model.pkl
```

---

## Diretório: **backend-PatientSystem/**

1. **`app.py`**:
   - **Objetivo**: Ponto de entrada principal da aplicação *Flask*. Define as rotas da API, configura a aplicação e inicializa o servidor.
   - **Justificativa**: Centraliza a configuração e registro de endpoints, garantindo organização e lógica clara das rotas e das dependências do projeto.

2. **`auth.py`**:
   - **Objetivo**: Gerenciar a lógica de autenticação e autorização, incluindo validação de papéis e tokens JWT.
   - **Justificativa**: Isolar a lógica de segurança melhora a clareza e permite reutilizar funções de autenticação e controle de acesso de forma eficiente.

3. **`config.py`**:
   - **Objetivo**: Armazenar as configurações do ambiente, como chaves de segurança, configurações do banco de dados e detalhes de servidores.
   - **Justificativa**: Centralizar as configurações facilita a manutenção, melhorando a segurança ao separar variáveis de ambiente sensíveis.

4. **`models.py`**:
   - **Objetivo**: Definir as tabelas do banco de dados, mapeando as classes do Python para tabelas SQL usando SQLAlchemy.
   - **Justificativa**: Organizar modelos de dados facilita a estruturação do banco de dados e o gerenciamento de entidades.

5. **`schemas.py`**:
   - **Objetivo**: Definir esquemas de validação de entrada de dados utilizando *Marshmallow*.
   - **Justificativa**: Separar a lógica de validação de dados permite reutilização e manutenção de padrões de dados de forma consistente.

---

## Diretório: **frontend-PatientSystem/**

1. **`src/`**:
   - **Objetivo**: Contém todo o código-fonte do projeto em Vue.js 3, incluindo componentes, layouts, páginas, e lógica de estado e navegação.
   - **Justificativa**: Centralizar a lógica da aplicação *frontend* melhora a organização e facilita o desenvolvimento com base em componentes.

2. **`tests/`**:
   - **Objetivo**: Diretório dedicado a testes de unidade, integração e ponta a ponta, garantindo a qualidade do código.
   - **Justificativa**: Manter a lógica de testes separada permite organizar e automatizar verificações de qualidade e funcionalidades.

3. **Arquivos de Configuração e Dependências**:
   - **Objetivo**: Configurar ferramentas de desenvolvimento, compiladores, transpiladores e pacotes de dependências.
   - **Justificativa**: Permitem configurar o ambiente de desenvolvimento, o que facilita a execução, o controle de qualidade e o build da aplicação *frontend*.

---

## Diretório: **health-predictive-dataset/**

1. **`diabetes_data.csv`**:
   - **Objetivo**: Contém o conjunto de dados usado para treinar o modelo de predição de diabetes.
   - **Justificativa**: Serve como base para o modelo de predição, armazenando dados essenciais para treinar o algoritmo e prever o risco de diabetes.

2. **`hypertension_data.csv`**:
   - **Objetivo**: Contém o conjunto de dados usado para treinar o modelo de predição de hipertensão.
   - **Justificativa**: Base para o modelo de predição de hipertensão, armazenando dados necessários para treinar o algoritmo de IA.

3. **`stroke_data.csv`**:
   - **Objetivo**: Contém o conjunto de dados usado para treinar o modelo de predição de AVC (acidente vascular cerebral).
   - **Justificativa**: Dados essenciais para treinar o modelo de predição de risco de AVC.

---

## Diretório: **models/**

1. **`diabetes_model.pkl`**:
   - **Objetivo**: Modelo de predição de diabetes treinado e salvo no formato *pickle*.
   - **Justificativa**: Permite carregar e reutilizar o modelo treinado para fazer predições de risco de diabetes no *backend*.

2. **`hypertension_model.pkl`**:
   - **Objetivo**: Modelo de predição de hipertensão treinado e salvo no formato *pickle*.
   - **Justificativa**: Carregar o modelo treinado para predições de risco de hipertensão, utilizando os endpoints do *backend*.

3. **`stroke_model.pkl`**:
   - **Objetivo**: Modelo de predição de AVC treinado e salvo no formato *pickle*.
   - **Justificativa**: Permite que o *backend* faça predições de risco de AVC com base nos dados fornecidos por pacientes.

---

# Justificativa Geral da Estrutura

A estrutura do projeto é organizada em diretórios específicos para **backend**, **frontend**, **conjuntos de dados** e **modelos treinados**. Cada parte do projeto possui sua lógica separada, o que facilita o desenvolvimento colaborativo e modular, além de permitir fácil manutenção e expansão.

- **Backend**: Gerencia a lógica de negócio, autenticação, controle de acesso e interação com o banco de dados e os modelos de IA.
- **Frontend**: Centraliza a interface do usuário, organizando componentes, páginas e lógica de navegação.
- **Conjuntos de Dados**: Armazena os dados necessários para treinar modelos de IA e fazer predições de saúde.
- **Modelos Treinados**: Contém os arquivos dos modelos que já foram treinados, prontos para serem utilizados pelo *backend*.