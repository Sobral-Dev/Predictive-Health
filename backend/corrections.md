### 3. **Associação entre Usuário e Paciente**
   - **Erro**: A lógica para acessar os detalhes do paciente usando o ID do usuário ainda não está completamente implementada.
   - **Solução**:
     - Implementar uma relação no banco de dados que associa cada `User` a um `Patient`, quando aplicável.
     - Atualizar a lógica de login para armazenar o ID do paciente correspondente no local storage ou em uma variável Vue que possa ser acessada por outros componentes.

---

### 5. **Controle de Acesso e Segurança**
   - **Erro**: Falta uma lógica para impedir que usuários sem permissão acessem seções restritas.
   - **Solução**: Implementar um sistema de controle de acesso usando o Vue.js `EventBus` ou Vuex para gerenciar o estado global, incluindo o role do usuário. Além disso, podemos utilizar `beforeEnter` guards no Vue Router para proteger rotas restritas.

---

### 6. **Deletar Usuário**
   - **Erro**: A função de deletar usuários não funciona, enquanto deletar pacientes funciona.
   - **Solução**: Revisar o endpoint de exclusão de usuário no backend para garantir que a lógica esteja correta e que o usuário seja corretamente anonimizado ou removido. Pode ser necessário verificar permissões ou o fluxo de requisição no frontend.

---

### 8. **Predições de Saúde**
   - **Erro**: Os métodos de predição não estão funcionando, e o frontend só tem campos para Diabetes.
   - **Solução**:
     - Corrigir os problemas no backend que estão impedindo que as predições sejam executadas.
     - Implementar um formulário dinâmico no frontend que ajusta os campos necessários com base na condição de saúde selecionada (Diabetes, Hipertensão, ou AVC).