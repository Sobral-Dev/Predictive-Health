# Tabelas do Banco de Dados PostgreSQL

---

## 1. **Tabela `User`**

- **Objetivo**: Armazenar informações dos usuários que têm acesso ao sistema, incluindo seus papéis e status de consentimento.
- **Justificativa**: Essencial para gerenciar autenticação, controle de acesso e recuperação de senhas, além de armazenar consentimentos dos usuários conforme a LGPD.

| Coluna         | Tipo           | Constraints                              | Descrição                                     |
| -------------- | -------------- | ---------------------------------------- | --------------------------------------------- |
| `id`           | `SERIAL`       | `PRIMARY KEY`                            | Identificador único do usuário.               |
| `name`         | `VARCHAR(50)`  | `NOT NULL`                               | Nome completo do usuário.                     |
| `email`        | `VARCHAR(120)` | `NOT NULL, UNIQUE`                       | E-mail único, utilizado para login.           |
| `password`     | `VARCHAR(128)` | `NOT NULL`                               | Hash da senha para autenticação.              |
| `role`         | `VARCHAR(20)`  | `NOT NULL, CHECK(role IN (...))`         | Papel do usuário (`admin`, `medico`, `paciente`, `deleted`). |
| `consent_status` | `BOOLEAN`    | `DEFAULT FALSE`                          | Indica se o usuário forneceu consentimento.   |
| `reset_token`  | `VARCHAR(120)` | `NULL`                                   | Token temporário para recuperação de senha.   |
| `created_at`   | `TIMESTAMP`    | `DEFAULT CURRENT_TIMESTAMP`              | Data e hora de criação do usuário.            |

**Constraints e Outros Detalhes**:
- **Chave Primária**: `id`
- **Restrições Únicas**: `email`
- **Verificação de Papel**: Utiliza o `CHECK` para garantir que apenas papéis válidos sejam atribuídos.

---

## 2. **Tabela `Patient`**

- **Objetivo**: Armazenar informações de pacientes, incluindo dados pessoais, condições médicas e status de consentimento.
- **Justificativa**: Essencial para gerenciar dados clínicos de pacientes e realizar predições de saúde, além de controlar o consentimento conforme LGPD.

| Coluna          | Tipo           | Constraints                             | Descrição                                     |
| --------------- | -------------- | --------------------------------------- | --------------------------------------------- |
| `id`            | `SERIAL`       | `PRIMARY KEY`                           | Identificador único do paciente.              |
| `name`          | `VARCHAR(50)`  | `NOT NULL`                              | Nome completo do paciente.                    |
| `age`           | `INT`          | `NULL`                                  | Idade do paciente.                            |
| `medical_conditions` | `TEXT`    | `NULL`                                  | Condições médicas do paciente.                |
| `consent_status`| `BOOLEAN`      | `DEFAULT FALSE`                         | Indica se o paciente forneceu consentimento.  |
| `created_at`    | `TIMESTAMP`    | `DEFAULT CURRENT_TIMESTAMP`             | Data e hora de criação do paciente.           |

**Constraints e Outros Detalhes**:
- **Chave Primária**: `id`
- **Consentimento**: O campo `consent_status` é usado para verificar se o paciente concordou em compartilhar seus dados.

---

## 3. **Tabela `AuditLog`**

- **Objetivo**: Armazenar logs de auditoria para monitorar ações críticas realizadas no sistema.
- **Justificativa**: Essencial para a conformidade com a LGPD, garantindo transparência e rastreabilidade de ações realizadas por usuários.

| Coluna      | Tipo         | Constraints                              | Descrição                                    |
| ----------- | ------------ | ---------------------------------------- | -------------------------------------------- |
| `id`        | `SERIAL`     | `PRIMARY KEY`                            | Identificador único do log de auditoria.     |
| `user_id`   | `INT`        | `NOT NULL, FOREIGN KEY REFERENCES "User"(id) ON DELETE CASCADE` | Referência ao usuário que realizou a ação. |
| `action`    | `VARCHAR(255)` | `NOT NULL`                             | Descrição da ação realizada.                 |
| `timestamp` | `TIMESTAMP`  | `DEFAULT CURRENT_TIMESTAMP`              | Data e hora da ação.                         |

**Constraints e Outros Detalhes**:
- **Chave Primária**: `id`
- **Chave Estrangeira**: `user_id` refere-se ao identificador do usuário.
- **Constraint ON DELETE CASCADE**: Garante que os logs de um usuário sejam removidos caso o usuário seja excluído.

---

## 4. **Tabela `RevokedToken`**

- **Objetivo**: Armazenar tokens JWT revogados para garantir que não sejam reutilizados.
- **Justificativa**: Essencial para gerenciar sessões de usuários e garantir que tokens revogados sejam bloqueados, atendendo aos requisitos de segurança.

| Coluna      | Tipo           | Constraints                              | Descrição                                     |
| ----------- | -------------- | ---------------------------------------- | --------------------------------------------- |
| `id`        | `SERIAL`       | `PRIMARY KEY`                            | Identificador único do token revogado.        |
| `jti`       | `VARCHAR(120)` | `NOT NULL`                               | Identificação única do token JWT.             |
| `created_at` | `TIMESTAMP`   | `DEFAULT CURRENT_TIMESTAMP`              | Data e hora da revogação do token.            |

**Constraints e Outros Detalhes**:
- **Chave Primária**: `id`
- **Armazenamento de Tokens**: Apenas tokens JWT que foram revogados são armazenados aqui, garantindo segurança.

---

## 5. **Tipos de Dados, Constraints e Detalhes Relevantes**

### **Tipos de Dados**:
- **SERIAL**: Tipo numérico utilizado para colunas de identificadores primários que auto-incrementam.
- **VARCHAR**: Define um campo de texto de tamanho limitado. Usado para nomes, e-mails, senhas e descrições curtas.
- **INT**: Armazena valores inteiros. Utilizado para idades e identificadores de usuários ou registros.
- **BOOLEAN**: Armazena valores lógicos (verdadeiro/falso). Utilizado para status de consentimento.
- **TIMESTAMP**: Armazena data e hora, utilizado para registrar o momento de criação de registros e ações.

### **Constraints Importantes**:
- **PRIMARY KEY**: Garante a unicidade dos registros dentro da tabela.
- **UNIQUE**: Garante que valores em colunas específicas sejam únicos (como e-mails).
- **FOREIGN KEY**: Mantém a integridade referencial entre tabelas (como em `user_id` na tabela `AuditLog`).
- **ON DELETE CASCADE**: Garante que, ao excluir um usuário, todos os logs associados sejam excluídos, mantendo a integridade.

---

# Justificativa Geral das Tabelas

Cada tabela foi projetada para atender aos seguintes requisitos:

1. **Gerenciamento Seguro de Usuários**: Controla papéis, autenticação e consentimento.
2. **Gerenciamento Completo de Pacientes**: Armazena dados clínicos e informações pessoais necessárias para predições de saúde.
3. **Transparência e Auditoria**: Garante que todas as ações sejam registradas e possam ser monitoradas.
4. **Controle de Sessão**: Mantém tokens revogados para evitar o uso indevido.