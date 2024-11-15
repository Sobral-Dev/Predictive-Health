| Coluna                 | Descrição                                                         | Tipo     | Exemplo |
|------------------------|-----------------------------------------------------------------|----------|---------|
| age                    | Idade do paciente.                                              | float64  | 57.0    |
| sex                    | Sexo do paciente (0 = Feminino, 1 = Masculino).                 | float64  | 1.0     |
| cp                     | Tipo de dor no peito (0 = Assintomático, 1-3 = Tipos variados de angina). | int64    | 3       |
| trestbps               | Pressão arterial em repouso (em mmHg).                          | int64    | 145     |
| chol                   | Nível de colesterol sérico (em mg/dl).                          | int64    | 233     |
| fbs                    | Glicemia de jejum (> 120 mg/dl, 0 = Não, 1 = Sim).              | int64    | 1       |
| restecg                | Resultados do eletrocardiograma em repouso (0 = Normal, 1-2 = Anormalidades detectadas). | int64 | 0       |
| thalach                | Frequência cardíaca máxima alcançada (valor numérico).          | int64    | 150     |
| exang                  | Indica se o paciente apresenta angina induzida por exercício (0 = Não, 1 = Sim). | int64 | 0       |
| oldpeak                | Depressão do segmento ST induzida por exercício em relação ao repouso. | float64 | 2.3     |
| slope                  | Inclinação do segmento ST durante o exercício (0 = Descendente, 1 = Plano, 2 = Ascendente). | int64 | 0       |
| ca                     | Número de vasos sanguíneos principais (0-4) coloridos por fluoroscopia. | int64    | 0       |
| thal                   | Resultado do exame de talassemia (0 = Normal, 1-2 = Defeituoso). | int64    | 1       |
| target                 | Indica se o paciente tem hipertensão (0 = Não, 1 = Sim).         | int64    | 1       |