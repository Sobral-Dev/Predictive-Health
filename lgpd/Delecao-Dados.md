_"**Prediction Health** é um sistema de gerenciamento de pacientes que permite o cadastro, acompanhamento e análise preditiva de **diabetes, hipertensão e AVC** para controle clínico de pacientes com condições de risco. Os pacientes podem visualizar seus dados médicos, atualizar informações e gerenciar permissões de acesso. Os médicos podem registrar e consultar históricos clínicos, além de acessar predições de seus pacientes para auxiliar no tratamento. O sistema também possibilita a exportação de registros médicos criptografados para profissionais autorizados pelo titular dos dados."_

<br>

# 🗑 Deleção de Dados (Direito à Exclusão / Direito ao Esquecimento)

A **Lei Geral de Proteção de Dados (LGPD)** (Lei nº 13.709/2018) garante ao titular dos dados o **direito de solicitar a exclusão ou anonimização de seus dados pessoais** quando eles não forem mais necessários para a finalidade original do tratamento.

---

## O Que a LGPD Diz Sobre a Deleção de Dados?
A exclusão de dados deve ocorrer nos seguintes casos, conforme o **Art. 18, VI da LGPD**:

✅ **O dado não é mais necessário** para a finalidade para a qual foi coletado.  
✅ **O titular revogou o consentimento** e não há outra base legal para manter os dados.  
✅ **O tratamento de dados foi realizado de forma irregular**.  
✅ **A exclusão é necessária para cumprir obrigações legais ou regulatórias**.  

🚨 **Exceção**: A deleção **não** é obrigatória se houver necessidade de manter os dados por razões legais (ex.: registros fiscais, dados médicos exigidos por regulamentações). Nesse caso, os dados podem ser **anonimizados** em vez de excluídos.

---

## Artigos da LGPD Relacionados à Deleção de Dados:
📌 **Art. 18º, VI** → Garante ao titular o direito de solicitar a exclusão de seus dados pessoais.  
📌 **Art. 16º** → Permite que dados sejam retidos **somente se houver base legal** para tal.  
📌 **Art. 46º** → Obriga a adoção de medidas de segurança para garantir que a exclusão ocorra de forma correta e irreversível.  

---

## Como é Aplicado no Prediction Health?

O **Prediction Health** garante que os usuários tenham o direito de solicitar a exclusão de seus dados, de forma **segura, auditável e conforme a LGPD**.  

### ✅ 1. Permitir que o Usuário Exclua a Própria Conta
- Criado o endpoint `/delete-my-account`, permitindo que **pacientes deletem suas próprias contas**.  
- Antes da exclusão, o sistema **verifica se há necessidade de manter alguns dados por obrigações legais**.  
- Se necessário, os dados são **anonimizados ao invés de deletados**.  

---

### ✅ 2. Anonimização em Caso de Retenção Obrigatória
- Se a exclusão de um usuário não for possível por questões legais, **os dados são anonimizados** em vez de excluídos.  
- O nome e o CPF são substituídos por identificadores aleatórios.  

---

### ✅ 3. Logs de Auditoria para Rastreabilidade
- Qualquer exclusão ou anonimização de dados gera um **registro nos logs de auditoria**.  
- Isso garante conformidade com a **LGPD (Art. 38º)** e rastreabilidade das ações realizadas.  

---

### ✅ 4. Revogação de Consentimento Automática
- Quando um usuário exclui sua conta, **todos os consentimentos ativos são automaticamente revogados**.  
- Se um usuário tentar acessar o sistema sem consentimentos válidos, ele será bloqueado.  
- A UI do Vue.js foi atualizada para **exibir um aviso claro** sobre os efeitos da revogação.  