# Estrutura Hierárquica do Projeto Backend

```plaintext
backend-PatientSystem/
│
├── app.py
├── auth.py
├── config.py
├── models.py
└── schemas.py
```

## Documentação do Diretório `backend-PatientSystem`

## 1. **Arquivo: `app.py`**

- **Objetivo**: Este é o ponto de entrada principal da aplicação *Flask*. Ele é responsável por definir e registrar todos os endpoints (rotas) do sistema, bem como configurar a aplicação e inicializar o servidor.
- **Justificativa**: Centraliza a lógica de rotas e a configuração do *Flask*, mantendo a estrutura do projeto organizada e clara. Isso facilita a separação de responsabilidades entre diferentes funcionalidades e módulos.

- **Principais Funções**:
  - Configuração do *Flask* e instâncias de dependências (JWT, SQLAlchemy, etc.).
  - Registro e definição de todos os endpoints da API RESTful.
  - Inicialização dos modelos de IA (carregamento em memória).
  - Definição de callbacks de controle de sessão e manuseio de erros.

## 2. **Arquivo: `auth.py`**

- **Objetivo**: Centralizar toda a lógica de autenticação e controle de autorização. Contém funções e decoradores para validar permissões dos usuários, autenticar credenciais e gerenciar sessões.
- **Justificativa**: Isolar a lógica de autenticação e controle de acesso melhora a segurança e facilita a manutenção. Isso permite que a lógica de autenticação seja reutilizada de forma clara e eficiente em múltiplos pontos do projeto.

- **Principais Funções**:
  - Verificação de papéis e permissões usando decoradores.
  - Validação de credenciais de login e verificação de hashes de senha.
  - Funções de auditoria (registros de ações) e revogação de tokens de sessão.

## 3. **Arquivo: `config.py`**

- **Objetivo**: Armazenar todas as configurações de ambiente da aplicação, incluindo detalhes de conexão com o banco de dados, chave de segurança JWT, configurações de e-mail e outras variáveis importantes.
- **Justificativa**: Centralizar as configurações em um arquivo separado permite que ajustes sejam feitos facilmente, sem impactar o código principal. Isso também ajuda a manter informações sensíveis, como senhas e chaves secretas, fora do código-fonte.

- **Principais Configurações**:
  - Variáveis de ambiente para o banco de dados PostgreSQL.
  - Chave secreta para JWT e configuração de expiração de tokens.
  - Configurações do servidor de e-mail para recuperação de senha.

## 4. **Arquivo: `models.py`**

- **Objetivo**: Definir os modelos de dados utilizados no banco de dados relacional PostgreSQL. Cada classe em `models.py` representa uma tabela no banco de dados e suas respectivas colunas e relações.
- **Justificativa**: Centralizar as definições dos modelos permite manter uma estrutura clara e organizada das entidades e suas relações, seguindo as práticas do ORM (Object Relational Mapping) com SQLAlchemy.

- **Principais Modelos**:
  - **`User`**: Armazena informações de usuários, incluindo seus papéis e status de consentimento.
  - **`Patient`**: Armazena dados dos pacientes e suas informações clínicas.
  - **`AuditLog`**: Armazena logs de auditoria, vinculados a ações críticas realizadas por usuários.
  - **`RevokedToken`**: Armazena tokens JWT revogados para controle seguro de sessões.

## 5. **Arquivo: `schemas.py`**

- **Objetivo**: Definir esquemas de validação de dados de entrada usando *Marshmallow*. Esses esquemas garantem que os dados enviados para o *backend* estejam no formato e nos padrões corretos.
- **Justificativa**: Isolar a validação de dados permite que a lógica de validação seja reutilizada em diferentes partes do sistema, garantindo consistência e clareza na verificação de entradas de usuários.

- **Principais Esquemas**:
  - **`UserSchema`**: Valida as informações de criação e atualização de usuários, como nome, e-mail, senha e papel.
  - **`ConsentSchema`**: Valida o status de consentimento de usuários e pacientes.