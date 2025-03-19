_"**Prediction Health** é um sistema de gerenciamento de pacientes que permite o cadastro, acompanhamento e análise preditiva de **diabetes, hipertensão e AVC** para controle clínico de pacientes com condições de risco. Os pacientes podem visualizar seus dados médicos, atualizar informações e gerenciar permissões de acesso. Os médicos podem registrar e consultar históricos clínicos, além de acessar predições de seus pacientes para auxiliar no tratamento. O sistema também possibilita a exportação de registros médicos criptografados para profissionais autorizados pelo titular dos dados."_

<br>

# ↔️ Transferência de Dados

A **Lei Geral de Proteção de Dados (LGPD)** (Lei nº 13.709/2018) estabelece diretrizes rigorosas para a **transferência de dados pessoais**, principalmente quando esses dados são compartilhados entre diferentes sistemas ou terceiros. O objetivo é garantir que os dados pessoais dos titulares sejam tratados com segurança, transparência e dentro dos limites legais.

---

## O Que a LGPD Diz Sobre Transferência de Dados?

A transferência de dados ocorre quando informações pessoais de um titular são enviadas ou compartilhadas com terceiros. A LGPD distingue dois tipos principais:

### 1️⃣ Transferência Nacional
✅ Envolve o compartilhamento de dados dentro do Brasil.  
✅ Exemplo: Um hospital acessando os dados de um paciente armazenados no Prediction Health.  
✅ Deve seguir as diretrizes de **minimização de dados** e **consentimento informado**.  

### 2️⃣ Transferência Internacional
✅ Envolve o envio de dados para outros países.  
✅ Regulada pelo **Art. 33 da LGPD**, que exige salvaguardas, como:  
   - Consentimento explícito do titular.  
   - Avaliação se o país de destino tem proteção equivalente à LGPD.  
   - Cláusulas contratuais específicas que garantam segurança.  

---

## Artigos da LGPD Relacionados à Transferência de Dados:
📌 **Art. 33º** → Define as regras para transferência internacional de dados.  
📌 **Art. 7º, V** → Permite o compartilhamento de dados quando necessário para cumprir obrigações legais.  
📌 **Art. 46º** → Obriga a adoção de medidas técnicas e administrativas para garantir a segurança dos dados transferidos.  

---

## **Como é aplicado no Prediction Health?**

O Prediction Health manipula dados sensíveis de pacientes, incluindo **condições médicas** e **predições de saúde**, exigindo um controle rigoroso sobre qualquer transferência de dados. Para atender à LGPD, foram implementadas as seguintes medidas:

### ✅ 1. Consentimento Obrigatório para Acesso aos Dados
- Médicos e administradores só podem acessar os dados de um paciente **se houver consentimento ativo** para que os mesmos acessem.  
- O consentimento é registrado no banco de dados e pode ser revogado a qualquer momento.  

### ✅ 2. Logs de Auditoria para Transferências
- Qualquer compartilhamento ou exportação de dados gera um log no **MongoDB (audit_logs)**.  
- Isso garante rastreabilidade e conformidade com o **Art. 38º da LGPD**.  

### ✅ 3. Endpoint Seguro para Exportação de Dados
- Criado o endpoint `/export-patient-data`, que permite a médicos e administradores exportarem os dados dos pacientes **somente com consentimento prévio**.  
- Os dados são **mascarados** para proteger informações sensíveis.  
- A exportação só pode ser feita em **JSON criptografado**.  

### ✅ 4. Transferência Internacional (Caso Seja Necessário)
Atualmente, **não há necessidade de exportar dados para fora do Brasil**, então essa funcionalidade **não foi implementada**.