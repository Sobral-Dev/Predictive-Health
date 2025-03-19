_"**Prediction Health** é um sistema de gerenciamento de pacientes que permite o cadastro, acompanhamento e análise preditiva de **diabetes, hipertensão e AVC** para controle clínico de pacientes com condições de risco. Os pacientes podem visualizar seus dados médicos, atualizar informações e gerenciar permissões de acesso. Os médicos podem registrar e consultar históricos clínicos, além de acessar predições de seus pacientes para auxiliar no tratamento. O sistema também possibilita a exportação de registros médicos criptografados para profissionais autorizados pelo titular dos dados."_

<br>

# ✍️ Consentimento Inicial

A **Lei Geral de Proteção de Dados (LGPD)** (Lei nº 13.709/2018) trata o consentimento inicial como **uma das bases legais** para o tratamento de dados pessoais, mas exige que ele seja obtido de forma clara, específica e informada.  

## O Que a LGPD Diz Sobre o Consentimento Inicial?
1. **Deve ser fornecido de forma livre, informada e inequívoca**  
   - O usuário precisa saber **quais dados** estão sendo coletados e **para qual finalidade**.  
   - O consentimento **não pode ser forçado** ou embutido em termos longos e confusos.  

2. **Deve estar associado a uma finalidade específica**  
   - O consentimento não pode ser **genérico** ("concordo com tudo").  
   - Ele deve ser **vinculado a um propósito claro**, como uso para predição de saúde.  

3. **O titular dos dados deve poder revogar o consentimento a qualquer momento**  
   - O usuário deve ter **controle total** sobre seus dados e a opção de **revogar o consentimento** facilmente.  

4. **Se houver mudança na finalidade do tratamento, um novo consentimento é necessário**  
   - Se os dados forem utilizados para uma **nova finalidade**, a empresa **precisa coletar um novo consentimento** do usuário.  

5. **Consentimentos devem ser registrados e armazenados para auditoria**  
   - A empresa precisa **guardar evidências** de que o consentimento foi dado, incluindo:  
     - **Versão do termo aceito**  
     - **Data e hora do aceite**  
     - **Status atual (ativo ou revogado)**  

---

## Artigos da LGPD Que Falam Sobre o Consentimento:
✅ **Art. 5º, XII** → Define consentimento como uma "manifestação livre, informada e inequívoca".  
✅ **Art. 7º, I** → Diz que o tratamento de dados pode ser feito com **consentimento do titular**.  
✅ **Art. 8º, § 1º** → Exige que o consentimento seja dado **por escrito ou outro meio que demonstre a manifestação de vontade do titular**.  
✅ **Art. 8º, § 5º** → O titular pode **revogar o consentimento a qualquer momento**.  

---

## Como é aplicado no Predictive Health?
1. Foi criado a **collection `ConsentTerm`**, que armazena os termos e suas versões.  
2. Foi criado também a **collection `UserConsent`**, que registra quais consentimentos foram dados por cada usuário.  
3. É dada a garantia que **o usuário possa revogar** qualquer consentimento a qualquer momento pelo sistema. Assim como o **direito de arrependimento de um consentimento**, podendo mudar o consentimento de um termo no qual já tinha declinado ou consentido.  
4. É mantido um **histórico de versões**, garantindo que **se um consentimento foi dado antes da revogação, os dados coletados antes continuam válidos**.  
5. **Se um novo termo for lançado**, é verificado se ele é **mandatório** e, caso seja, o usuário é obrigado a **aceitá-lo ou revogá-lo** antes de continuar a usar o sistema. Caso recuse, fica impedindo de usar o sistema até que o consentimento seja aceito.
