# Páginas da Interface Web

## 1. **Página de Login**

- **Objetivo**: Autenticar o usuário e conceder acesso ao sistema de acordo com seu papel (admin, médico, paciente).
- **Justificativa**: É a porta de entrada da aplicação, garantindo autenticação segura e gerenciamento de acesso.
- **Endpoints Utilizados**:
  - **`POST /login`**: Realiza a autenticação e retorna o token JWT.

## 2. **Página de Recuperação de Senha**

- **Objetivo**: Permitir que um usuário recupere sua senha por meio de um link enviado para seu e-mail.
- **Justificativa**: Essencial para segurança e experiência do usuário, atendendo à necessidade de recuperação de acesso.
- **Endpoints Utilizados**:
  - **`POST /password-reset-request`**: Envia um e-mail de recuperação de senha ao usuário.
  - **`POST /password-reset`**: Permite redefinir a senha após a validação do token de recuperação.

## 3. **Dashboard do Administrador**

- **Objetivo**: Apresentar uma visão geral das principais funcionalidades administrativas, incluindo gerenciamento de usuários, pacientes e auditoria.
- **Justificativa**: Centraliza as principais ações de controle e administração do sistema.
- **Endpoints Utilizados**:
  - **`GET /users/{id}`**: Exibe detalhes básicos do administrador.
  - **`GET /audit-log`**: Fornece uma lista de ações realizadas para o monitoramento.
  - **`GET /patients`**: Lista todos os pacientes para uma visão geral.

## 4. **Página de Gerenciamento de Usuários**

- **Objetivo**: CRUD completo para gerenciar usuários, permitindo que administradores criem, atualizem, visualizem e excluam usuários.
- **Justificativa**: Necessário para controle seguro de usuários e para a expansão e manutenção do sistema.
- **Endpoints Utilizados**:
  - **`POST /register`**: Cria um novo usuário.
  - **`GET /users/{id}`**: Exibe detalhes de um usuário específico.
  - **`PUT /users/{id}`**: Atualiza os dados de um usuário.
  - **`DELETE /users/{id}`**: Anonimiza ou desativa um usuário.

## 5. **Página de Cadastro de Usuários**

- **Objetivo**: Permitir a criação de novos usuários no sistema, definindo seu papel (admin, médico, paciente).
- **Justificativa**: Facilita o registro de novos usuários e a administração contínua.
- **Endpoints Utilizados**:
  - **`POST /register`**: Cria um novo usuário.

## 6. **Página de Perfil do Usuário**

- **Objetivo**: Permitir que cada usuário visualize e edite seus dados pessoais, como nome, e-mail, etc.
- **Justificativa**: Atende ao direito de correção de dados conforme LGPD.
- **Endpoints Utilizados**:
  - **`GET /user/me`**: Exibe os dados pessoais do usuário autenticado.
  - **`PUT /user/me`**: Atualiza os dados pessoais do usuário autenticado.

## 7. **Página de Cadastro de Pacientes**

- **Objetivo**: Permitir que médicos e administradores registrem novos pacientes no sistema.
- **Justificativa**: Atende à necessidade de registro de pacientes para futuras predições e gestão de dados clínicos.
- **Endpoints Utilizados**:
  - **`POST /patients`**: Cria um novo registro de paciente.

## 8. **Página de Listagem de Pacientes**

- **Objetivo**: Exibir uma lista completa de pacientes com funcionalidades para visualizar, editar e excluir os registros.
- **Justificativa**: Facilita o acesso centralizado e a manipulação de dados dos pacientes para médicos e administradores.
- **Endpoints Utilizados**:
  - **`GET /patients`**: Lista todos os pacientes.

## 9. **Página de Detalhes de Pacientes**

- **Objetivo**: Exibir os detalhes completos de um paciente específico, incluindo informações pessoais, condições médicas e consentimento.
- **Justificativa**: Fornece uma visão detalhada e individual dos pacientes para médicos e administradores.
- **Endpoints Utilizados**:
  - **`GET /patients/{id}`**: Exibe detalhes de um paciente específico.

## 10. **Página de Predição de Saúde (Diabetes, Hipertensão, AVC)**

- **Objetivo**: Criar formulários de predição de saúde para médicos, com base nos modelos de IA disponíveis.
- **Justificativa**: Atende à funcionalidade de predição de riscos de saúde para dar suporte à tomada de decisões médicas.
- **Endpoints Utilizados**:
  - **`POST /predict/diabetes`**: Prediz risco de diabetes para um paciente.
  - **`POST /predict/hypertension`**: Prediz risco de hipertensão para um paciente.
  - **`POST /predict/stroke`**: Prediz risco de AVC para um paciente.

## 11. **Página de Atualização de Consentimento**

- **Objetivo**: Permitir que médicos e administradores atualizem o status de consentimento de um paciente.
- **Justificativa**: Atende ao requisito de atualização de consentimento conforme LGPD.
- **Endpoints Utilizados**:
  - **`POST /patients/consent/{id}`**: Atualiza o status de consentimento de um paciente.

## 12. **Página de Exportação de Dados Pessoais**

- **Objetivo**: Permitir que usuários (pacientes) e médicos exportem seus dados pessoais e dados dos pacientes em formato JSON ou CSV.
- **Justificativa**: Atende ao direito de portabilidade de dados conforme LGPD.
- **Endpoints Utilizados**:
  - **`GET /patients/export/{id}`**: Exporta dados de um paciente específico.

## 13. **Página de Logs de Auditoria**

- **Objetivo**: Permitir que administradores visualizem todos os logs de auditoria registrados.
- **Justificativa**: Garante a conformidade com a LGPD em relação à transparência e rastreabilidade de ações.
- **Endpoints Utilizados**:
  - **`GET /audit-log`**: Fornece uma lista de ações realizadas para monitoramento e auditoria.