# Endpoints do Backend

## Endpoint 1: **POST /register_user**

- **Objetivo**: Registrar um novo usuário no sistema com nome, e-mail, senha, papel (role) e CPF.
- **Justificativa**: Permite o gerenciamento de usuários e o controle de acesso com base em papéis. Essencial para adicionar novos administradores, médicos ou pacientes ao sistema.
- **Status de Funcionamento**: `Falta Testar`
- **Roles**: `admin`
- **Requisições em**:
    - `UserRegistration.vue`

---

## Endpoint 2: **POST /consent-initial**

- **Objetivo**: Solicitar e registrar o consentimento inicial de um usuário após o registro.
- **Justificativa**: Atende ao requisito de consentimento explícito conforme a LGPD, garantindo que os usuários forneçam consentimento antes do uso completo do sistema.
- **Status de Funcionamento**: `Falta Testar`
- **Roles**: `Nenhum`
- **Requisições em**:
    - `ConsentUpdate.vue`

---

## Endpoint 3: **POST /login**

- **Objetivo**: Autenticar um usuário e fornecer um token JWT para acesso seguro ao sistema.
- **Justificativa**: Permite o controle de acesso com base na autenticação, garantindo que apenas usuários autenticados acessem funcionalidades protegidas.
- **Status de Funcionamento**: `OK`
- **Roles**: `Nenhum`
- **Requisições em**:
    - `Login.vue`
    
---

## Endpoint 4: **POST /logout**

- **Objetivo**: Invalidar o token de sessão atual.
- **Justificativa**: Permite o gerenciamento seguro de sessões e evita o uso indevido de tokens após o logout.
- **Status de Funcionamento**: `OK`
- **Roles**: `Nenhum`
- **Requisições em**:
    - `Sidebar.vue`
    
---

## Endpoint 5: **GET /user/me**

- **Objetivo**: Obter informações básicas sobre um usuário específico.
- **Justificativa**: Permite que administradores e médicos visualizem detalhes de usuários cadastrados para gerenciamento e controle.
- **Status de Funcionamento**: `Falta Testar`
- **Roles**: `Nenhum`
- **Requisições em**:
    - `UserProfile.vue`
    
---

## Endpoint 6: **PUT /user/me**

- **Objetivo**: Atualizar informações do usuário autenticado.
- **Justificativa**: Atende ao direito de correção de dados conforme a LGPD, permitindo que usuários atualizem seus dados.
- **Status de Funcionamento**: `Falta Testar`
- **Roles**: `paciente`, `admin`
- **Requisições em**:
    - `UserProfile.vue`
    - `UsersManagement.vue`
    
---

## Endpoint 7:  **GET /user/export**

- **Objetivo**: Exportar os dados do usuário autenticado.
- **Justificativa**: Atende ao direito de portabilidade de dados conforme a LGPD, permitindo que dados pessoais sejam exportados em formato padrão.
- **Status de Funcionamento**: `Falta Testar`
- **Roles**: `Nenhum`
- **Requisições em**:
    - `PersonalDataExport.vue`
    
---

## Endpoint 8: **POST /password-reset-request**

- **Objetivo**: Solicitar a recuperação de senha enviando um e-mail ao usuário.
- **Justificativa**: Fornece uma maneira segura para que usuários recuperem o acesso às suas contas em caso de perda de senha.
- **Status de Funcionamento**: `Falta Testar`
- **Roles**: `Nenhum`
- **Requisições em**:
    - `Login.vue`
    
---

## Endpoint 9: **POST /password-reset**

- **Objetivo**: Permitir a redefinição de senha após validação do token de recuperação.
- **Justificativa**: Garante a segurança e a usabilidade do sistema, permitindo que usuários redefinam suas senhas com um processo seguro.
- **Status de Funcionamento**: `Falta Testar`
- **Roles**: `Nenhum`
- **Requisições em**:
    - `ChangePassword.vue`
    
---

## Endpoint 10: **POST /register_patient**

- **Objetivo**: Registrar um novo paciente no sistema com nome, idade, condições médicas, status de consentimento, CPF e Data de Nascimento.
- **Justificativa**: Permite o gerenciamento de pacientes com seus respectivos históricos médicos.
- **Status de Funcionamento**: `Falta Testar`
- **Roles**: `admin`, `medico`
- **Requisições em**:
    - `RegisterPatient.vue`
    
---

## Endpoint 11: **GET /patients/{id}/{role}**

- **Objetivo**: Obter dados completos de um paciente específico.
- **Justificativa**: Fornece acesso controlado a dados detalhados dos pacientes para médicos e administradores.
- **Status de Funcionamento**: `Falta Testar`
- **Roles**: `admin`, `medico`, `paciente`
- **Requisições em**:
    - `PatientDetails.vue`
    - `UserProfile.vue`
    
---

## Endpoint 12: **PUT /patients/{id}**

- **Objetivo**: Atualizar informações de um paciente específico.
- **Justificativa**: Atende ao direito de correção de dados clínicos conforme a LGPD, permitindo a atualização segura de informações de pacientes pelo médico que recebeu consentimento.
- **Status de Funcionamento**: `Falta Testar`
- **Roles**: `medico`
- **Requisições em**:
    - `PatientDetails.vue`
    
---

## Endpoint 13: **DELETE /patients/{id}**

- **Objetivo**: Anonimizar ou excluir logicamente os dados de um paciente específico.
- **Justificativa**: Atende ao direito de exclusão ou anonimização de dados conforme a LGPD, garantindo a proteção da privacidade do paciente.
- **Status de Funcionamento**: `Falta Testar`
- **Roles**: `admin`
- **Requisições em**:
    - `ShowPatients.vue`
    
---

## Endpoint 14: **POST /predict/diabetes**

- **Objetivo**: Fazer predição de risco de diabetes para um paciente.
- **Justificativa**: Atende à funcionalidade de suporte à decisão médica, fornecendo predições de risco de saúde personalizadas.
- **Status de Funcionamento**: `Falta Testar`
- **Roles**: `paciente`
- **Requisições em**:
    - `HealthPredictions.vue`
    
---

## Endpoint 15: **POST /predict/hypertension**

- **Objetivo**: Fazer predição de risco de hipertensão para um paciente.
- **Justificativa**: Atende à funcionalidade de suporte à decisão médica, fornecendo predições de risco de saúde personalizadas.
- **Status de Funcionamento**: `Falta Testar`
- **Roles**: `paciente`
- **Requisições em**:
    - `HealthPredictions.vue`
    
---

## Endpoint 16: **POST /predict/stroke**

- **Objetivo**: Fazer predição de risco de AVC para um paciente.
- **Justificativa**: Atende à funcionalidade de suporte à decisão médica, fornecendo predições de risco de saúde personalizadas.
- **Status de Funcionamento**: `Falta Testar`
- **Roles**: `paciente`
- **Requisições em**:
    - `HealthPredictions.vue`
    
---

## Endpoint 17: **GET /audit-log**

- **Objetivo**: Visualizar os logs de auditoria do sistema.
- **Justificativa**: Garante a transparência e a conformidade com a LGPD em relação ao registro e monitoramento de ações críticas no sistema.
- **Status de Funcionamento**: `Falta Testar`
- **Roles**: `admin`
- **Requisições em**:
    - ` AuditLogs.vue`
    
---

## Endpoint 18: **GET /patient/export**

- **Objetivo**: Exportar os dados do paciente autenticado.
- **Justificativa**: Atende ao direito de portabilidade de dados conforme a LGPD, permitindo que dados pessoais sejam exportados em formato padrão.
- **Status de Funcionamento**: `Falta Testar`
- **Roles**: `paciente`
- **Requisições em**:
    - `PersonalDataExport.vue`
    
---

## Endpoint 19: **POST /update-consent**

- **Objetivo**: Atualizar o status de consentimento de um usuário.
- **Justificativa**: Permite o controle explícito de consentimento conforme a LGPD, garantindo que o consentimento possa ser revogado ou fornecido conforme necessário.
- **Status de Funcionamento**: `Falta Testar`
- **Roles**: `Nenhum`
- **Requisições em**:
    - `ConsentUpdate.vue`
    
---

## Endpoint 20: **GET /patients**

- **Objetivo**: Obter a lista de todos os pacientes cadastrados. Administradores podem visualizar todos os pacientes (sem dados sensíveis) e os médicos podem visualizar os dados de seus pacientes.
- **Justificativa**: Permite visualizar todos os pacientes registrados no banco.
- **Status de Funcionamento**: `Falta Testar`
- **Roles**: `admin`, `medico`
- **Requisições em**:
    - `AdminDashboard.vue`
    - `ShowPatients.vue`
    
---

## Endpoint 21: **GET /users**

- **Objetivo**: Obter a lista de todos os usuários cadastrados. Apenas os Administradores podem visualizar todos os usuários (sem dados sensíveis).
- **Justificativa**: Permite visualizar todos os usuários registrados no banco.
- **Status de Funcionamento**: `Falta Testar`
- **Roles**: `admin`
- **Requisições em**:
    - `AdminDashboard.vue`
    - `UsersManagement.vue`
    
---

## Endpoint 22: **DELETE /users/{id}**

- **Objetivo**: Anonimizar ou excluir logicamente um usuário específico. Apenas o Administrador pode realizar essa operação.
- **Justificativa**: Atende ao direito de exclusão ou anonimização de dados conforme a LGPD, garantindo a proteção da privacidade do usuário.
- **Status de Funcionamento**: `Falta Testar`
- **Roles**: `admin`
- **Requisições em**:
    - `UsersManagement.vue`
    
---

## Endpoint 23: **PUT /user/change-password**

- **Objetivo**: Trocar a senha do usuário autenticado.
- **Justificativa**: .
- **Status de Funcionamento**: `Falta Testar`
- **Roles**: `Nenhum`
- **Requisições em**:
    - `ChangePassword.vue`
    
---

## Endpoint 24: **GET /patients/consent/current**

- **Objetivo**: Obter o estado atual de Consentimento do Usuário autenticado.
- **Justificativa**: Permite obrigar o usuário a conceder o consentimento inicial, além de fazer uma consulta rápida para qualquer alteração do status de consentimento, evitando qualquer infração do direito de aceite do usuário.
- **Status de Funcionamento**: `Falta Testar`
- **Roles**: `Nenhum`
- **Requisições em**:
    - `ConsentUpdate.vue`
    
---

## Endpoint 25: **POST /save-prediction**

- **Objetivo**: Salvar dados de predições realizadas por usuários no MongoDB.
- **Justificativa**: Permite que os médicos possam ter um histórico dos resultados obtidos pelos pacientes que acompanha (com o consentimento prévio), o que permite um acompanhamento mais detalhado do quadro clínico do paciente.
- **Status de Funcionamento**: `Falta Testar`
- **Roles**: `Nenhum`
- **Requisições em**:
    - `HealthPredictions.vue`
    
---

## Endpoint 26: **GET /user/predictions**

- **Objetivo**: Ver predições feitas pelo usuário autenticado.
- **Justificativa**: Permite que o próprio usuário possa visualizar o seu histórico de predições realizadas.
- **Status de Funcionamento**: `Falta Testar`
- **Roles**: `paciente`
- **Requisições em**:
    - `UserPredictions.vue`
    
---

## Endpoint 27: **POST /doctor-patient**

- **Objetivo**: Associar um médico a um paciente.
- **Justificativa**: Permite que um médico possa se associar a um paciente usuário para acompanhá-lo e ter acessos aos seus dados de predições com o consentimento prévio.
- **Status de Funcionamento**: `Falta Testar`
- **Roles**: `medico`
- **Requisições em**:
    - `PatientDetails.vue`
    
---

## Endpoint 28: **GET /doctor/{doctor_id}/patients**

- **Objetivo**: Obter a lista de pacientes associados a um médico.
- **Justificativa**: Transparência das relações entre os usuários para os administradores, da mesma forma que aplica um regra de negócio onde o médico só pode visualizar dados pessoais de seus pacientes, dos quais deram consentimento prévio.
- **Status de Funcionamento**: `Falta Testar`
- **Roles**: `medico`, `admin`
- **Requisições em**:
    - `DoctorPatientList.vue`
    - `ShowPatients.vue`
    
---

## Endpoint 29: **GET /patient/doctors**

- **Objetivo**: Obter a lista de médicos associados a um paciente.
- **Justificativa**: Transparência das relações entre os usuários para os administradores, da mesma forma que aplica um regra de negócio onde o paciente só pode visualizar a sua lista de médicos associados.
- **Status de Funcionamento**: `Falta Testar`
- **Roles**: `paciente`
- **Requisições em**:
    - `UserProfile.vue`
    
---

## Endpoint 30: **GET /doctor/{doctor_id}/patient/{patient_id}/predictions**

- **Objetivo**: Ver histórico de predições de um paciente associado a um médico.
- **Justificativa**: Possiblita que o médico que acompanha um paciente em específico, com o consentimento dele, possa visualizar o seu histórico de predições para acompanhar o seu quadro clínico.
- **Status de Funcionamento**: `Falta Testar`
- **Roles**: `medico`
- **Requisições em**:
    - `PatientDetails.vue`
    
---

## Endpoint 31: **GET /doctor/{doctor_id}/predictions**

- **Objetivo**: Ver predições de todos os pacientes associado a um médico.
- **Justificativa**: Possibilita que o médico possa, com o consentimento dos usuários, visualizar o histórico de predições de todos os pacientes que ele acompanha.
- **Status de Funcionamento**: `Falta Testar`
- **Roles**: `medico`
- **Requisições em**:
    - `DoctorPredictions.vue`
    
---

## Endpoint 32: **GET /admin/predictions**

- **Objetivo**: Ver predições de todos os pacientes, por usuários Administradores, de maneira anonimizada.
- **Justificativa**: Possibilita que os usuários Administradores possam visualizar o histórico de predições de todos os pacientes cadastrados, respeitando seus dados sensíveis, permitindo assim que o administrador possa acompanhar o uso da aplicação sem expor dados que possam apontar para um paciente em específico, do qual tem o direito de ser o único a ter ciência de suas predições, além do médico que o acompanha, caso o consentimento seja dado.
- **Status de Funcionamento**: `Falta Testar`
- **Roles**: `admin`
- **Requisições em**:
    - `AdminPredictions.vue`
    
---

# Endpoint 33: ****

- **Objetivo**: 
- **Justificativa**: 
- **Status de Funcionamento**: `Falta Testar`
- **Roles**: ``
- **Requisições em**:
    - `None`
    
---

# Endpoint 34: ****

- **Objetivo**: 
- **Justificativa**: 
- **Status de Funcionamento**: `Falta Testar`
- **Roles**: ``
- **Requisições em**:
    - `None`
    
---

# Endpoint 35: ****

- **Objetivo**: 
- **Justificativa**: 
- **Status de Funcionamento**: `Falta Testar`
- **Roles**: ``
- **Requisições em**:
    - `None`
    
---

# Endpoint 36: ****

- **Objetivo**: 
- **Justificativa**: 
- **Status de Funcionamento**: `Falta Testar`
- **Roles**: ``
- **Requisições em**:
    - `None`
    
---

# Endpoint 37: ****

- **Objetivo**: 
- **Justificativa**: 
- **Status de Funcionamento**: `Falta Testar`
- **Roles**: ``
- **Requisições em**:
    - `None`
    
---

# Endpoint 38: ****

- **Objetivo**: 
- **Justificativa**: 
- **Status de Funcionamento**: `Falta Testar`
- **Roles**: ``
- **Requisições em**:
    - `None`
    
