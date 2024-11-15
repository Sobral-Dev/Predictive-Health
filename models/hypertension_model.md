# Documentação do Modelo de Predição de Hipertensão

Este documento fornece uma visão técnica e científica das features utilizadas para treinar o modelo de predição de hipertensão, incluindo descrições, unidades de medida, tipos de dados e o impacto de cada feature na probabilidade de hipertensão. A justificativa para a inclusão de cada feature é baseada em estudos médicos e na análise de sua relevância para a predição de hipertensão.

---

## 1. Descrição Geral do Modelo

O modelo de predição de hipertensão utiliza um classificador de floresta aleatória (Random Forest Classifier), que avalia diferentes fatores de risco para prever a presença de hipertensão em indivíduos. 

### Objetivo do Modelo
O modelo é destinado a prever o risco e a probabilidade de hipertensão em pacientes, usando variáveis clínicas e comportamentais.

---

## 2. Descrição das Features

| Feature     | Descrição                                                                                              | Unidade        | Tipo de Dado | Impacto na Predição do Modelo |
|-------------|--------------------------------------------------------------------------------------------------------|----------------|--------------|--------------------------------|
| **age**     | Idade do paciente, fator de risco primário para hipertensão devido ao endurecimento arterial.          | Anos           | Numérico     | Altamente relevante; com o avanço da idade, o risco de hipertensão aumenta devido ao envelhecimento vascular. |
| **trestbps**| Pressão arterial em repouso, um indicador direto de hipertensão e disfunções cardiovasculares.         | mm Hg          | Numérico     | Extremamente relevante; valores elevados indicam predisposição direta à hipertensão. |
| **chol**    | Nível de colesterol, ligado ao acúmulo de placas nas artérias e ao risco cardiovascular.               | mg/dL          | Numérico     | Relevante; altos níveis de colesterol estão associados ao aumento da pressão arterial e risco cardiovascular. |
| **thalach** | Frequência cardíaca máxima, reflete a capacidade cardíaca e o sistema cardiovascular sob esforço.       | bpm            | Numérico     | Moderadamente relevante; valores baixos podem indicar disfunções cardiovasculares que contribuem para a hipertensão. |
| **exang**   | Indica a presença de angina induzida por exercício, associada a problemas coronarianos.                | Booleano (0/1) | Categórico   | Importante; a presença de angina pode indicar doenças cardíacas que aumentam o risco de hipertensão. |
| **oldpeak** | Depressão ST, um marcador eletrocardiográfico indicativo de isquemia ou doenças arteriais.             | mm             | Numérico     | Relevante; valores elevados sugerem problemas cardíacos, que estão ligados ao aumento da pressão arterial. |
| **cp**      | Tipo de dor no peito, refletindo diferentes tipos de problemas cardíacos e níveis de risco.            | Categórico (1-4)| Categórico  | Relevante; alguns tipos de dor no peito estão associados a doenças cardíacas que afetam a pressão arterial. |

---

## 3. Impacto de Cada Feature na Predição de Hipertensão

Cada feature foi selecionada pela sua importância na predição de hipertensão, conforme descrito a seguir:

1. **age**:
   - **Impacto no Risco**: A idade está fortemente correlacionada com a hipertensão, pois a elasticidade arterial diminui com o tempo, levando a maior resistência e pressão arterial.
   - **Impacto na Probabilidade**: O modelo atribui uma probabilidade maior de hipertensão conforme a idade aumenta, especialmente a partir dos 40 anos.

2. **trestbps (Pressão Arterial em Repouso)**:
   - **Impacto no Risco**: A pressão arterial elevada em repouso é um sinal direto de hipertensão e disfunção cardiovascular.
   - **Impacto na Probabilidade**: Este é um dos fatores mais importantes no modelo; valores altos em trestbps elevam drasticamente a probabilidade predita de hipertensão.

3. **chol (Colesterol)**:
   - **Impacto no Risco**: Níveis altos de colesterol levam ao acúmulo de placas nas artérias, dificultando o fluxo sanguíneo e aumentando a pressão.
   - **Impacto na Probabilidade**: Um nível elevado de colesterol aumenta a probabilidade de hipertensão, refletindo o risco cardiovascular.

4. **thalach (Frequência Cardíaca Máxima)**:
   - **Impacto no Risco**: A frequência cardíaca máxima reflete a saúde geral do sistema cardiovascular; valores baixos podem indicar problemas cardíacos.
   - **Impacto na Probabilidade**: Valores mais baixos de thalach aumentam a probabilidade de hipertensão, pois indicam possível disfunção cardiovascular.

5. **exang (Angina Induzida por Exercício)**:
   - **Impacto no Risco**: A presença de angina durante o exercício indica uma predisposição para problemas coronarianos, que estão associados à hipertensão.
   - **Impacto na Probabilidade**: Um valor positivo para exang aumenta a probabilidade de hipertensão, pois sugere problemas cardíacos.

6. **oldpeak (Depressão ST)**:
   - **Impacto no Risco**: A depressão ST é um marcador de isquemia; valores elevados indicam problemas arteriais que contribuem para a hipertensão.
   - **Impacto na Probabilidade**: Valores altos de oldpeak elevam a probabilidade de hipertensão no modelo.

7. **cp (Tipo de Dor no Peito)**:
   - **Impacto no Risco**: Diferentes tipos de dor no peito estão associados a diferentes condições cardíacas, algumas das quais são indicativas de hipertensão.
   - **Impacto na Probabilidade**: Certos tipos de dor (valores específicos de cp) aumentam a probabilidade de hipertensão devido à associação com doenças cardíacas.

---

## 4. Justificativa para Inclusão das Features no Modelo de Hipertensão

- **age** e **trestbps** foram incluídos por serem preditores diretos de hipertensão, devido ao efeito do envelhecimento vascular e pressão arterial elevada.
- **chol**, **thalach** e **exang** foram escolhidos com base em sua relação com a saúde cardiovascular, que influencia a probabilidade de hipertensão.
- **oldpeak** e **cp** oferecem informações complementares sobre o estado cardiovascular, permitindo que o modelo capture sinais indiretos de hipertensão.

Essas features foram escolhidas para maximizar a precisão do modelo, com base em evidências clínicas e na relação entre saúde cardiovascular e hipertensão.