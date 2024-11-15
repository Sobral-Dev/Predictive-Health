# Documentação do Modelo de Predição de Diabetes

Este documento descreve em detalhes as features utilizadas para treinar o modelo de predição de diabetes, incluindo a explicação de cada uma delas, a unidade de medida, o tipo de dado, e como cada feature contribui para os resultados do modelo. A relevância de cada feature para o risco e a probabilidade de diabetes é discutida, considerando a literatura médica e a análise de impacto no modelo.

---

## 1. Descrição Geral do Modelo

O modelo de predição de diabetes é baseado em um classificador de floresta aleatória (Random Forest Classifier). Ele utiliza um conjunto de features específicas de pacientes para prever a probabilidade e o risco de um diagnóstico de diabetes. Cada feature foi selecionada com base em sua associação documentada com o desenvolvimento de diabetes tipo 2.

### Objetivo do Modelo
O objetivo deste modelo é calcular o risco (positivo ou negativo) e a probabilidade associada de um indivíduo desenvolver diabetes, auxiliando profissionais de saúde em decisões preventivas e diagnósticas.

---

## 2. Descrição das Features

| Feature          | Descrição                                                                                   | Unidade         | Tipo de Dado | Impacto na Predição do Modelo |
|------------------|---------------------------------------------------------------------------------------------|-----------------|--------------|--------------------------------|
| **Age**          | Idade do paciente, um dos fatores de risco mais reconhecidos para o diabetes.              | Anos            | Numérico     | Altamente relevante devido ao aumento da resistência à insulina e declínio da função pancreática com o envelhecimento. |
| **BMI**          | Índice de Massa Corporal, que reflete a obesidade, outro fator de risco importante.        | kg/m²           | Numérico     | Fundamental, pois a obesidade é fortemente associada à resistência à insulina, aumentando o risco de diabetes. |
| **HighChol**     | Indicador de colesterol elevado, que influencia o metabolismo e a função cardiovascular.    | Booleano (0/1)  | Categórico   | Relevante; o colesterol alto frequentemente coexiste com a resistência à insulina, elevando o risco metabólico. |
| **HighBP**       | Indicador de hipertensão, condição que compartilha fatores de risco com o diabetes.        | Booleano (0/1)  | Categórico   | Importante, pois a hipertensão e o diabetes estão relacionados pela disfunção endotelial e resistência à insulina. |
| **PhysActivity** | Frequência de atividade física, que tem efeito preventivo contra o diabetes.               | Booleano (0/1)  | Categórico   | Impacto negativo: atividade física reduz o risco de diabetes, ajudando na manutenção da sensibilidade à insulina. |
| **GenHlth**      | Estado geral de saúde, autorrelatado pelos pacientes, refletindo possíveis comorbidades.   | Escala (1-5)    | Ordinal      | Moderado: indivíduos com baixa saúde autorreferida têm maior probabilidade de desenvolver diabetes. |
| **Smoker**       | Status de fumante, onde o tabagismo afeta o metabolismo e eleva o risco cardiovascular.    | Booleano (0/1)  | Categórico   | Relevante; o tabagismo está associado ao aumento da resistência à insulina e inflamação, elevando o risco de diabetes. |

---

## 3. Impacto de Cada Feature na Predição de Diabetes

Cada feature foi incluída no modelo com base na sua relação com o diabetes. Abaixo, detalhamos o impacto esperado de cada uma:

1. **Age**:  
   - **Impacto no Risco**: Com o envelhecimento, há um aumento gradual na resistência à insulina e diminuição na função pancreática, levando a um maior risco de diabetes.  
   - **Impacto na Probabilidade**: Um aumento na idade aumenta a probabilidade calculada de diabetes, especialmente após os 45 anos.

2. **BMI (Índice de Massa Corporal)**:  
   - **Impacto no Risco**: A obesidade é uma das principais causas do diabetes tipo 2, pois contribui para a resistência à insulina.  
   - **Impacto na Probabilidade**: Um BMI elevado aumenta significativamente a probabilidade predita de diabetes no modelo, especialmente para valores acima de 30 kg/m².

3. **HighChol (Colesterol Alto)**:  
   - **Impacto no Risco**: O colesterol alto está ligado à síndrome metabólica e à resistência à insulina, que são fatores de risco para o diabetes.  
   - **Impacto na Probabilidade**: Um paciente com colesterol alto verá uma ligeira elevação na probabilidade predita de diabetes.

4. **HighBP (Pressão Alta)**:  
   - **Impacto no Risco**: A hipertensão está associada à resistência à insulina e ao aumento do risco de diabetes.  
   - **Impacto na Probabilidade**: A presença de hipertensão tende a aumentar a probabilidade predita de diabetes, pois os fatores de risco das duas condições se sobrepõem.

5. **PhysActivity (Atividade Física)**:  
   - **Impacto no Risco**: A atividade física ajuda a manter a sensibilidade à insulina, sendo um fator protetor contra o diabetes.  
   - **Impacto na Probabilidade**: A falta de atividade física (valores baixos de PhysActivity) eleva a probabilidade predita de diabetes. A presença de atividade reduz a chance predita de desenvolver diabetes.

6. **GenHlth (Estado Geral de Saúde)**:  
   - **Impacto no Risco**: Indivíduos com baixo estado de saúde autorreferido (escala alta em GenHlth) tendem a ter maior risco de diabetes devido a possíveis comorbidades.  
   - **Impacto na Probabilidade**: Um estado de saúde pobre aumenta a probabilidade predita de diabetes, pois é provável que o indivíduo apresente outros fatores de risco não especificados.

7. **Smoker (Status de Fumante)**:  
   - **Impacto no Risco**: O tabagismo contribui para a resistência à insulina e inflamação crônica, aumentando o risco de diabetes.  
   - **Impacto na Probabilidade**: A presença do tabagismo eleva a probabilidade predita de diabetes, embora de forma menos acentuada em relação ao BMI e idade.

---

## 4. Justificativa para Inclusão das Features no Modelo de Diabetes

- **Age** e **BMI** são cruciais devido ao aumento documentado de diabetes com a idade e a forte correlação entre obesidade e diabetes.
- **HighChol** e **HighBP** foram incluídos por sua relação com a síndrome metabólica, que compartilha uma série de mecanismos patológicos com o diabetes.
- **PhysActivity** atua como um fator protetor e é inversamente relacionado ao diabetes, sendo relevante para prever um baixo risco.
- **GenHlth** permite uma visão ampla da saúde do paciente, capturando informações indiretas sobre o risco geral.
- **Smoker** foi incluído devido à relação com resistência à insulina, embora seu impacto seja mais moderado em relação a outras variáveis.

Essas features foram escolhidas tanto pela acessibilidade dos dados clínicos quanto pela sua robusta correlação com o diabetes em estudos populacionais. 