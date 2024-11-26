# Páginas da Interface Web

## 1. **Dashboard do Administrador**

- **Componente**: `AdminDashboard.vue`
- **Objetivo**: Apresentar uma visão geral das principais funcionalidades administrativas, incluindo gerenciamento de usuários, pacientes e auditoria.
- **Justificativa**: Centraliza as principais ações de controle e administração do sistema.
- **Endpoints Utilizados**:
  - **`GET /users` (HTTP `OK`)**: Fornece uma lista dos usuários registrados.
  - **`GET /patients` (HTTP `OK`)**: Lista todos os pacientes para uma visão geral.
- **Lógicas Condicionais Dinâmicas do HTML**:
  - **Nenhuma**

---

## 2. **Página de Histórico de Predições Anonimizada**

- **Componente**: `AdminPredictions.vue`
- **Objetivo**: Permitir que administradores visualizem todas as predições realizadas de forma anonimizada (sem dados sensíveis dos pacientes).
- **Justificativa**: 
- **Endpoints Utilizados**:
  - **`GET /admin/predictions` (HTTP `OK`)**: Fornece todos as predições persistidas no banco MongoDB, sem divulgar dados sensíveis dos pacientes.
- **Lógicas Condicionais Dinâmicas do HTML**:
  - **Nenhuma**

---

## 3. **Página de Logs de Auditoria**

- **Componente**: `AuditLogs.vue`
- **Objetivo**: Permitir que administradores visualizem todos os logs de auditoria registrados.
- **Justificativa**: Garante a conformidade com a LGPD em relação à transparência e rastreabilidade de ações.
- **Endpoints Utilizados**:
  - **`GET /audit-log` (HTTP `OK`)**: Fornece uma lista de ações realizadas para monitoramento e auditoria.
- **Lógicas Condicionais Dinâmicas do HTML**:
  - **Nenhuma**

---

## 4. **Página de Recuperação de Senha**

- **Componente**: `ChangePassword.vue`
- **Objetivo**: Permitir que um usuário recupere sua senha por meio de um link enviado para seu e-mail.
- **Justificativa**: Essencial para segurança e experiência do usuário, atendendo à necessidade de recuperação de acesso.
- **Endpoints Utilizados**:
  - **`PUT /user/change-password` (HTTP `OK`)**: Permite ao usuário autenticado que recorda sua senha atual a trocá-la sem necessidade do uso de um reset token.
  - **`POST /password-reset` (HTTP `OK`)**: Permite ao usuário autenticado trocar a senha fornecendo o reset token recebido por email.
- **Lógicas Condicionais Dinâmicas do HTML**:
  - **`v-if="!usingResetToken"`**: variável que permite que os inputs sejam dinâmicos, a depender se o usuário utilizará o reset token ou não.
  - **`<a :href="this.$router.push('/login').data.emailSender = true">`**: Redireciona o usuário para a tela onde há o envio do reset token, com a variável emailSender recebendo `true` para redirecionar ao formulário de requisição.

---

## 5. **Página de Atualização de Consentimento**

- **Componente**: `ConsentUpdate.vue`
- **Objetivo**: Permitir que médicos e administradores atualizem o status de consentimento de um paciente.
- **Justificativa**: Atende ao requisito de atualização de consentimento conforme LGPD.
- **Endpoints Utilizados**:
  - **`POST /update-consent` (HTTP `OK`)**: Atualiza o status de consentimento de um paciente.
  - **`GET /patients/consent/current` (HTTP `OK`)**: Obtém o status atual de consentimento do usuário autenticado.
  - **`POST /consent-initial` (HTTP `OK`)**: Permite o usuário dar o consentimento inicial, quando o consentimento ainda não foi aceito ou revogado.
- **Lógicas Condicionais Dinâmicas do HTML**:
  - **`$route.name === 'ConsentUpdate`**: A depender se é o primeiro acesso ou se já há um valor definido pelo usuário de aceito ou revogação do consentimento, alguns componentes do HTML podem serem omitidos, assim como o endpoint de mudança de consentimento alterar de `/consent-initial` para `update-consent`.

---

## 6. **Página de Listagem de Pacientes de um Médico**

- **Componente**: `DoctorPatientList.vue`
- **Objetivo**: Permitir que os médicos possam visualizar todos os pacientes nos quais ele está associado.
- **Justificativa**: 
- **Endpoints Utilizados**:
  - **`GET /doctor/${globalData.user_id}/patients` (HTTP `OK`)**: Fornece uma lista com todos os pacientes associados ao médico autenticado.
- **Lógicas Condicionais Dinâmicas do HTML**:
  - **`@click.prevent="this.$router.push(`/patients/${patient.id}`)`**: Ao clicar em qualquer paciente listado, o usuário médico consegue acessar as informações desse paciente sendo redirecionado para a página de detalhes dos pacientes (`PatientDetails.vue`).

---

## 7. **Página de Histórico de Predições para Médicos**

- **Componente**: `DoctorPredictions.vue`
- **Objetivo**: Permitir que os médicos possam visualizar todas as predições realizadas anteriormente pelos pacientes nos quais ele está associado.
- **Justificativa**: 
- **Endpoints Utilizados**:
  - **`GET /doctor/${globalData.user_id}/predictions` (HTTP `OK`)**: Fornece uma lista com todos as predições realizadas pelos pacientes associados ao médico autenticado.
- **Lógicas Condicionais Dinâmicas do HTML**:
  - **Nenhuma**

---

## 8. **Página de Predição de Saúde (Diabetes, Hipertensão, AVC)**

- **Componente**: `HealthPrediction.vue`
- **Objetivo**: Criar formulários de predição de saúde para médicos, com base nos modelos de IA disponíveis.
- **Justificativa**: Atende à funcionalidade de predição de riscos de saúde para dar suporte à tomada de decisões médicas.
- **Endpoints Utilizados**:
  - **`POST /predict/diabetes` (HTTP `OK`)**: Prediz risco de diabetes para um paciente.
  - **`POST /predict/hypertension` (HTTP `OK`)**: Prediz risco de hipertensão para um paciente.
  - **`POST /predict/stroke` (HTTP `OK`)**: Prediz risco de AVC para um paciente.
  - **`POST /save-prediction` (HTTP `OK`)**: Armazena no banco MongoDB as features e o resultado das predições realizadas assim que elas são terminadas.
- **Lógicas Condicionais Dinâmicas do HTML**:
  - **`<button class="choose-language" @click.prevent="english = !english"><i class="fa-solid fa-language">{{ !english ? 'PT-Br' : 'EN' }}</i></button>`**: Altera o idioma da página entre inglês e português.
  - **`<select v-model="selectedPrediction" @change="resetForm">
            <option disabled value="">Selecione uma condição...</option>
            <option value="diabetes">Diabetes</option>
            <option value="hypertension">Hipertensão</option>
            <option value="stroke">AVC</option>
          </select>`**: Input de Select que permite alterar entre os três tipos de predição. Ao escolher um dos valores, os inputs referentes àquela predição ficam visíveis no componente.

---

## 9. **Página de Login**

- **Componente**: `Login.vue`
- **Objetivo**: Autenticar o usuário e conceder acesso ao sistema de acordo com seu papel (admin, médico, paciente).
- **Justificativa**: É a porta de entrada da aplicação, garantindo autenticação segura e gerenciamento de acesso.
- **Endpoints Utilizados**:
  - **`POST /login` (HTTP `OK`)**: Realiza a autenticação e retorna o token JWT e dados necessários a serem armazenados para a sessão no `localStorage` e no `globalData`.
- **`POST /password-reset-request` (HTTP `OK`)**: Solicita a alteração de senha, enviando ao email do usuário um token que permite a alteração de forma segura. 
- **Lógicas Condicionais Dinâmicas do HTML**:
  - **Nenhuma**

---

## 10. **Página de Detalhes de Pacientes**

- **Componente**: `PatientDetails.vue`
- **Objetivo**: Exibir os detalhes completos de um paciente específico, incluindo informações pessoais, condições médicas e consentimento.
- **Justificativa**: Fornece uma visão detalhada e individual dos pacientes para médicos e administradores.
- **Endpoints Utilizados**:
  - **`GET /patients/${this.$route.params.id}/${globalData.user_role}` (HTTP `OK`)**: Exibe detalhes de um paciente específico.
  - **`POST /doctor-patient` (HTTP ``)**: Permite o médico requisitar uma associação a um paciente, para poder acompanhar seu histórico de predições e acompanhar seu quadro médico.
  - **`PUT /patients/{patientId}` (HTTP `OK`)**: Atualiza os dados do paciente pelo médico consentido que o acompanha.
  - **`GET /doctor/${globalData.user_id}/patient/${this.$route.params.id}/predictions` (HTTP `OK`)**: Obtém o histórico de predições do paciente acompanhado pelo médico autenticado e que recebeu consentimento para tal. 
- **Lógicas Condicionais Dinâmicas do HTML**:
  - **` {{ !editPatient ? `<span>` : `<input type="text" @placeholder="${patient.name}" v-model="${updateValues.name}">`}}`**: lógica para transformar o elemento HTML de forma dinâmica, caso o usuário médico queira editar informações de seu paciente.

---

## 11. **Página de Exportação de Dados Pessoais**

- **Componente**: `PersonalDataExport.vue`
- **Objetivo**: Permitir que usuários exportem seus dados pessoais e médicos em formato JSON ou CSV.
- **Justificativa**: Atende ao direito de portabilidade de dados conforme LGPD.
- **Endpoints Utilizados**:
  - **`GET /user/export` (HTTP `OK`)**: Exporta dados do usuário autenticado.
  - **`GET /patient/export` (HTTP `OK`)**: Exporta dados do paciente autenticado.
- **Lógicas Condicionais Dinâmicas do HTML**:
  - **`this.gd.user_role === 'paciente'`**: Condicional para aparecer a `<section>` de classe `checkbox-section`.
  - **`v-if="this.gd.user_role === 'paciente' ? 
            userData !== false || patientData !== false : 
            this.gd.user_id !== null" `**: Condicional para os botões de exportação em CSV e JSON.

---

## 12. **Página de Cadastro de Pacientes**

- **Componente**: `RegisterPatient.vue`
- **Objetivo**: Permitir que médicos e administradores registrem novos pacientes no sistema.
- **Justificativa**: Atende à necessidade de registro de pacientes para futuras predições e gestão de dados clínicos.
- **Endpoints Utilizados**:
  - **`POST /register_patient` (HTTP `OK`)**: Cria um novo registro de paciente.
- **Lógicas Condicionais Dinâmicas do HTML**:
  - **Nenhuma**

---

## 13. **Página de Listagem de Pacientes**

- **Componente**: `ShowPatients.vue`
- **Objetivo**: Exibir uma lista completa de pacientes com funcionalidades para visualizar, editar e excluir os registros.
- **Justificativa**: Facilita o acesso centralizado e a manipulação de dados dos pacientes para médicos e administradores.
- **Endpoints Utilizados**:
  - **`GET /patients` (HTTP `OK`)**: Lista todos os pacientes.
  - **`DELETE /patients/${patientId}` (HTTP `OK`)**: Permite fazer a remoção lógica do registro de um paciente (Anonimização).
- **Lógicas Condicionais Dinâmicas do HTML**:
  - **Nenhuma**

---

## 14. **Página de Histórico de Predições para Pacientes**

- **Componente**: `UserPredictions.vue`
- **Objetivo**: Permitir que os pacientes possam visualizar todas as predições realizadas anteriormente por ele mesmo.
- **Justificativa**: 
- **Endpoints Utilizados**:
  - **`GET /user/predictions` (HTTP `OK`)**: Fornece uma lista com todos as predições realizadas anteriormente pelo paciente.
- **Lógicas Condicionais Dinâmicas do HTML**:
  - **Nenhuma**

---

## 15. **Página de Perfil do Usuário**

- **Componente**: `UserProfile.vue`
- **Objetivo**: Permitir que cada usuário visualize e edite seus dados pessoais, como nome, e-mail, etc.
- **Justificativa**: Atende ao direito de correção de dados conforme LGPD.
- **Endpoints Utilizados**:
  - **`GET /user/me` (HTTP `OK`)**: Exibe os dados pessoais do usuário autenticado.
- **`PUT /user/me` (HTTP `OK`)**: Atualiza os dados pessoais do usuário autenticado.
  - **`GET /patients/${globalData.user_id}/paciente` (HTTP `OK`)**: Recebe os dados de histórico de paciente do usuário autenticado.
  - **`GET /patient/doctors` (HTTP `OK`)**: Lista os médicos associados ao paciente autenticado.
  - **`GET /doctor/${globalData.user_id}/patients` (HTTP `OK`)**: Listar todos os pacientes associados ao médico autenticado.
- **Lógicas Condicionais Dinâmicas do HTML**:
  - **` <section class="profile-section" v-if="patient && this.gd.user_role === 'paciente'">
`**: Caso o usuário autenticado seja um paciente, essa seção da página que mostra os dados de perfil do paciente é renderizado.

---

## 16. **Página de Cadastro de Usuários**

- **Componente**: `UserRegistration.vue`
- **Objetivo**: Permitir a criação de novos usuários no sistema, definindo seu papel (admin, médico, paciente).
- **Justificativa**: Facilita o registro de novos usuários e a administração contínua.
- **Endpoints Utilizados**:
  - **`POST /register_user` (HTTP `OK`)**: Cria um novo usuário.
- **Lógicas Condicionais Dinâmicas do HTML**:
  - **Nenhuma**

---

## 17. **Página de Gerenciamento de Usuários**

- **Componente**: `UsersManagement.vue`
- **Objetivo**: CRUD completo para gerenciar usuários, permitindo que administradores criem, atualizem, visualizem e excluam usuários.
- **Justificativa**: Necessário para controle seguro de usuários e para a expansão e manutenção do sistema.
- **Endpoints Utilizados**:
  - **`GET /users` (HTTP `OK`)**: Lista os usuários registrados no sistema.
  - **`PUT /user/me` (HTTP `OK`)**: Atualiza os dados de um usuário.
  - **`DELETE /users/${userId}` (HTTP `OK`)**: Anonimiza ou desativa um usuário.
- **Lógicas Condicionais Dinâmicas do HTML**:
  - **Nenhuma**

---

## 18. ****

- **Componente**: ``
- **Objetivo**: 
- **Justificativa**: 
- **Endpoints Utilizados**:
  - **`GET /`**: 
- **Lógicas Condicionais Dinâmicas do HTML**:
  - **Nenhuma**

---

## 19. ****

- **Componente**: ``
- **Objetivo**: 
- **Justificativa**: 
- **Endpoints Utilizados**:
  - **`GET /`**: 
- **Lógicas Condicionais Dinâmicas do HTML**:
  - **Nenhuma**

---

## 20. ****

- **Componente**: ``
- **Objetivo**: 
- **Justificativa**: 
- **Endpoints Utilizados**:
  - **`GET /`**: 
- **Lógicas Condicionais Dinâmicas do HTML**:
  - **Nenhuma**

---

## 21. ****

- **Componente**: ``
- **Objetivo**: 
- **Justificativa**: 
- **Endpoints Utilizados**:
  - **`GET /`**: 
- **Lógicas Condicionais Dinâmicas do HTML**:
  - **Nenhuma**

---

## 22. ****

- **Componente**: ``
- **Objetivo**: 
- **Justificativa**: 
- **Endpoints Utilizados**:
  - **`GET /`**: 
- **Lógicas Condicionais Dinâmicas do HTML**:
  - **Nenhuma**

---

## 23. ****

- **Componente**: ``
- **Objetivo**: 
- **Justificativa**: 
- **Endpoints Utilizados**:
  - **`GET /`**: 
- **Lógicas Condicionais Dinâmicas do HTML**:
  - **Nenhuma**

---

## 24. ****

- **Componente**: ``
- **Objetivo**: 
- **Justificativa**: 
- **Endpoints Utilizados**:
  - **`GET /`**: 
- **Lógicas Condicionais Dinâmicas do HTML**:
  - **Nenhuma**

---

## 25. ****

- **Componente**: ``
- **Objetivo**: 
- **Justificativa**: 
- **Endpoints Utilizados**:
  - **`GET /`**: 
- **Lógicas Condicionais Dinâmicas do HTML**:
  - **Nenhuma**