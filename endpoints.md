# Endpoints do Backend

## 1. **POST /register**

- **Objetivo**: Registrar um novo usuário no sistema com nome, e-mail, senha e papel.
- **Justificativa**: Permite o gerenciamento de usuários e o controle de acesso com base em papéis. Essencial para adicionar novos administradores, médicos ou pacientes ao sistema.

## 2. **POST /consent-initial**

- **Objetivo**: Solicitar e registrar o consentimento inicial de um usuário após o registro.
- **Justificativa**: Atende ao requisito de consentimento explícito conforme a LGPD, garantindo que os usuários forneçam consentimento antes do uso completo do sistema.

## 3. **POST /login**

- **Objetivo**: Autenticar um usuário e fornecer um token JWT para acesso seguro ao sistema.
- **Justificativa**: Permite o controle de acesso com base na autenticação, garantindo que apenas usuários autenticados acessem funcionalidades protegidas.

## 4. **POST /logout**

- **Objetivo**: Invalidar o token de sessão atual.
- **Justificativa**: Permite o gerenciamento seguro de sessões e evita o uso indevido de tokens após o logout.

## 5. **GET /users/{id}**

- **Objetivo**: Obter informações básicas sobre um usuário específico.
- **Justificativa**: Permite que administradores e médicos visualizem detalhes de usuários cadastrados para gerenciamento e controle.

## 6. **PUT /users/{id}**

- **Objetivo**: Atualizar informações de um usuário específico.
- **Justificativa**: Atende ao direito de correção de dados conforme a LGPD, permitindo que administradores e médicos atualizem dados de outros usuários.

## 7. **POST /predict/diabetes**

- **Objetivo**: Fazer predição de risco de diabetes para um paciente.
- **Justificativa**: Atende à funcionalidade de suporte à decisão médica, fornecendo predições de risco de saúde personalizadas.

## 8. **POST /predict/hypertension**

- **Objetivo**: Fazer predição de risco de hipertensão para um paciente.
- **Justificativa**: Atende à funcionalidade de suporte à decisão médica, fornecendo predições de risco de saúde personalizadas.

## 9. **POST /predict/stroke**

- **Objetivo**: Fazer predição de risco de AVC para um paciente.
- **Justificativa**: Atende à funcionalidade de suporte à decisão médica, fornecendo predições de risco de saúde personalizadas.

## 10. **POST /patients**

- **Objetivo**: Criar um novo paciente com dados pessoais e condições médicas.
- **Justificativa**: Permite o registro de novos pacientes, essencial para gerenciar dados clínicos e fornecer predições de saúde.

## 11. **GET /patients/{id}**

- **Objetivo**: Obter dados completos de um paciente específico.
- **Justificativa**: Fornece acesso controlado a dados detalhados dos pacientes para médicos e administradores.

## 12. **PUT /patients/{id}**

- **Objetivo**: Atualizar informações de um paciente específico.
- **Justificativa**: Atende ao direito de correção de dados clínicos conforme a LGPD, permitindo a atualização segura de informações de pacientes.

## 13. **DELETE /patients/{id}**

- **Objetivo**: Anonimizar ou excluir logicamente os dados de um paciente específico.
- **Justificativa**: Atende ao direito de exclusão ou anonimização de dados conforme a LGPD, garantindo a proteção da privacidade do paciente.

## 14. **POST /consent**

- **Objetivo**: Atualizar o status de consentimento de um paciente.
- **Justificativa**: Permite o controle explícito de consentimento conforme a LGPD, garantindo que o consentimento possa ser revogado ou fornecido conforme necessário.

## 15. **GET /audit-log**

- **Objetivo**: Visualizar os logs de auditoria do sistema.
- **Justificativa**: Garante a transparência e a conformidade com a LGPD em relação ao registro e monitoramento de ações críticas no sistema.

## 16. **GET /patients/export/{id}**

- **Objetivo**: Exportar os dados de um paciente específico.
- **Justificativa**: Atende ao direito de portabilidade de dados conforme a LGPD, permitindo que dados pessoais sejam exportados em formato padrão.

## 17. **POST /password-reset-request**

- **Objetivo**: Solicitar a recuperação de senha enviando um e-mail ao usuário.
- **Justificativa**: Fornece uma maneira segura para que usuários recuperem o acesso às suas contas em caso de perda de senha.

## 18. **POST /password-reset**

- **Objetivo**: Permitir a redefinição de senha após validação do token de recuperação.
- **Justificativa**: Garante a segurança e a usabilidade do sistema, permitindo que usuários redefinam suas senhas com um processo seguro.

## 19. **GET /user/me**

- **Objetivo**: Obter dados pessoais do usuário autenticado.
- **Justificativa**: Permite que cada usuário visualize seus próprios dados, atendendo ao direito de acesso e correção de dados conforme a LGPD.

## 20. **PUT /user/me**

- **Objetivo**: Atualizar dados pessoais do usuário autenticado.
- **Justificativa**: Atende ao direito de correção de dados conforme a LGPD, permitindo que usuários atualizem suas informações pessoais.

## 21. **DELETE /users/{id}**

- **Objetivo**: Anonimizar ou excluir logicamente um usuário específico.
- **Justificativa**: Atende ao direito de exclusão ou anonimização de dados conforme a LGPD, garantindo a proteção da privacidade do usuário.

---

# Justificativa Geral dos Endpoints

Os **21 endpoints** cobrem todas as funcionalidades necessárias para:

- **Gerenciamento de usuários**: Criação, autenticação, recuperação de senha, atualização e anonimização.
- **Gerenciamento de pacientes**: Criação, atualização, visualização, anonimização e exportação de dados.
- **Controle de predições de saúde**: Predições de diabetes, hipertensão e AVC para suporte à tomada de decisões.
- **Conformidade com a LGPD**: Controle de consentimento, direito de correção, exclusão, portabilidade de dados e transparência por meio de auditoria.

Cada endpoint foi projetado para atender aos requisitos de segurança, controle de acesso e conformidade com a LGPD, além de fornecer suporte às funcionalidades essenciais do sistema.