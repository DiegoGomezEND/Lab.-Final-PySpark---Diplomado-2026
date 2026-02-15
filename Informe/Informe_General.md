# **Análisis de la Dinámica Contractual del Estado Colombiano usando Datos Abiertos de SECOP II**

**Desarrollado por:** Diego Alejandro Gomez Cortes y Victor Hugo Díaz

### **Introducción**

SECOP II (Sistema Electrónico para la Contratación Pública) es la principal plataforma de transparencia y seguimiento de la contratación estatal en Colombia. A través de esta plataforma se registran los contratos públicos de entidades nacionales y territoriales, permitiendo el acceso abierto a información clave como valores contratados, tipos de contrato, entidades, proveedores y estados contractuales. El volumen, diversidad y naturaleza pública de estos datos convierten a SECOP II en una fuente estratégica para el análisis económico, administrativo y de política pública.

El análisis de los datos de SECOP II permite identificar patrones de contratación, concentración de recursos, comportamientos por territorio y modalidades contractuales, así como posibles riesgos o ineficiencias en el uso de los recursos públicos. Dado que la contratación estatal representa una porción significativa del gasto público, su estudio sistemático aporta valor tanto para la toma de decisiones institucionales como para el control ciudadano y el desarrollo de modelos analíticos y predictivos.

Desde una perspectiva de datos, SECOP II plantea retos propios de los entornos Big Data: grandes volúmenes de información, esquemas complejos, datos heterogéneos y actualizaciones constantes. Por esta razón, el uso de herramientas distribuidas como Apache Spark, Visual Studio Code, Java, JupyterLab y Docker resultan fundamentales para procesar, explorar y preparar estos datos de forma eficiente y escalable.

### **Objetivo del Análisis**

El objetivo de este trabajo es comprender el comportamiento de la contratación pública registrada en SECOP II, explorando sus principales características estructurales y económicas mediante técnicas de análisis de datos a gran escala. A partir de esta exploración, se busca sentar las bases para la construcción de análisis avanzados y modelos de Machine Learning que permitan extraer conocimiento útil sobre la dinámica contractual del Estado colombiano.

## Carga e ingesta de datos

En la fase de ingesta se consumieron datos abiertos de **SECOP II** a través de la API de **Datos Abiertos Colombia**, conservando registros con **fecha de firma** diligenciada. Posteriormente, la información se cargó en un entorno distribuido con **Apache Spark** (orquestado en contenedores con **Docker**) para garantizar reproducibilidad y escalabilidad.

Ya en Spark, se inspeccionó el esquema, se estandarizaron nombres de columnas y tipos de dato, y se seleccionaron variables relevantes para el análisis y el modelado. Finalmente, el conjunto resultante se almacenó en formato **Parquet**, optimizado para lectura eficiente y procesamiento distribuido en etapas posteriores.

**Evidencia**: `01_ingesta_resuelto.ipynb`


## **Análisis Exploratorio de Datos (EDA)**

En esta fase se realizó un análisis exploratorio sobre los contratos electrónicos de SECOP II con el fin de comprender la estructura del dataset, validar su calidad y caracterizar el comportamiento del valor contractual antes de pasar a la ingeniería de variables y al modelado. El EDA se enfocó en distribución del valor del contrato, concentración territorial, tipo de contrato, estado contractual y comportamiento temporal.

Primero, se verificó el periodo temporal efectivo a partir de la variable **fecha_de_firma** (filtrando registros con firma reportada). Los resultados muestran que la mayor parte de los contratos analizados se concentra hacia finales de 2025 y los primeros registros de 2026, lo que indica que el dataset representa procesos contractuales recientes dentro del periodo observado.

Luego, se calcularon estadísticas descriptivas de la variable objetivo **valor_del_contrato**. Se evidenció una distribución **altamente asimétrica**: la mayoría de contratos se ubica en rangos bajos y medios, mientras que una proporción menor corresponde a contratos de gran escala. Este patrón justifica el uso posterior de transformaciones (por ejemplo, logaritmo) y métricas robustas para evitar que los valores extremos dominen el ajuste del modelo.

A nivel territorial, se observó una concentración marcada de contratos en el **Distrito Capital de Bogotá**, seguido por **Antioquia** y **Valle del Cauca** dentro del top 10 por número de contratos (ver Figura 1). Este resultado respalda la necesidad de análisis regionales más detallados y de controles por territorio en etapas posteriores.


<img width="1157" height="465" alt="image" src="https://github.com/user-attachments/assets/b0f57285-8e74-47c2-b495-0bf131b51c7b" />


También se exploró la distribución por **tipo de contrato**, donde la modalidad de **Prestación de Servicios** domina el volumen de registros, seguida por otras modalidades administrativas y contratos de compra/suministro. En cuanto al **estado del contrato**, predominan contratos en ejecución y contratos con modificaciones, consistente con procesos contractuales activos.

Finalmente, se aplicó el método **IQR (Interquartile Range)** para detectar valores atípicos en **valor_del_contrato**, excluyendo previamente valores iguales o menores a cero. Se identificó aproximadamente un **15%** de contratos como outliers superiores. Estos casos no se interpretan como errores, sino como contratos de alta cuantía que impactan fuertemente la distribución; por ello, se consideran al momento de definir transformaciones y criterios de escalamiento para modelado.

El análisis temporal por año y mes evidenció picos de contratación hacia el cierre de 2025 y una disminución al inicio de 2026, coherente con dinámicas administrativas y ciclos presupuestales.

**Evidencia:** 02_exploracion_eda_resuelto.ipynb

## Feature Engineering y Construcción de Pipelines

En esta fase se prepararon los datos de **SECOP II** para su uso en modelos de *Machine Learning* con **Spark ML**, transformando variables categóricas en representaciones numéricas y consolidándolas en un vector de características reutilizable mediante **Pipelines**. El proceso se aplicó sobre una muestra de **100.000 contratos**, garantizando consistencia, escalabilidad y reproducibilidad en un entorno distribuido.

### Selección de variables

Se seleccionaron variables con relevancia contractual y capacidad explicativa para capturar diferencias territoriales, administrativas y operativas entre los contratos:

- **Variables categóricas (features)**: `departamento`, `tipo_de_contrato`, `estado_contrato`  
  Estas variables fueron codificadas con transformaciones estándar de Spark ML (indexación y codificación *one-hot*), y posteriormente ensambladas en un único vector de entrada para los modelos.

- **Variable objetivo (label)**: `valor_del_contrato_num`  
  Esta variable representa el valor monetario del contrato y corresponde al **resultado a predecir**, por lo que **no se utiliza como feature** en el entrenamiento. Dado su comportamiento altamente asimétrico observado en el EDA, se trabajó con una transformación del objetivo (por ejemplo, `valor_del_contrato_log`) para estabilizar la escala durante el ajuste del modelo. En producción, las predicciones pueden reconvertirse a la escala original cuando se requiere interpretación monetaria.


---

## Limpieza de datos

Se aplicó una limpieza basada en la eliminación de valores nulos (*dropna*) únicamente en las variables utilizadas por el modelo, con el objetivo de asegurar consistencia en el entrenamiento y evitar fallas en el pipeline.

- Registros antes de limpieza: **100.000**
- Registros después de limpieza: **100.000**

En esta muestra, las variables seleccionadas no presentaron valores nulos, por lo que no fue necesario descartar registros ni aplicar imputaciones para continuar con el modelado.


---

### Codificación de variables categóricas

Las variables categóricas fueron transformadas usando:

1. **StringIndexer**: conversión de texto a índices numéricos
2. **OneHotEncoder**: transformación de índices a vectores binarios

**Categorías detectadas**

| Variable            | Categorías únicas |
|---------------------|------------------|
| departamento         | 34               |
| tipo_de_contrato     | 17               |
| estado_contrato      | 6                |

**Resultado del OneHotEncoding**

- Total de features categóricas generadas: **57**
- Features numéricas originales: **1**

**Total de features esperadas:** **58**


### Construcción del vector de features

Las variables numéricas y las categóricas codificadas fueron combinadas mediante **VectorAssembler**, generando un único vector:

- `features_raw`

**Validación del resultado**

- Dimensión esperada del vector: **58**
- Dimensión real del vector `features_raw`: **58**

Esto confirma que el proceso de codificación y ensamblaje se ejecutó correctamente.

---

### Construcción del Pipeline

El pipeline se construyó respetando el orden lógico de las transformaciones:

1. StringIndexer  
2. OneHotEncoder  
3. VectorAssembler  

**Resultado del pipeline**

- Total de stages: **7**
  - 3 StringIndexer
  - 3 OneHotEncoder
  - 1 VectorAssembler

El pipeline fue entrenado y aplicado exitosamente sobre el dataset limpio, garantizando reproducibilidad y consistencia en futuras ejecuciones.

### Análisis de varianza de features

Se realizó un análisis de varianza sobre el vector `features_raw` para identificar las dimensiones con mayor dispersión. Para evitar consumo excesivo de memoria, el cálculo se hizo sobre una muestra de **1.000 registros**, convirtiendo el vector de Spark a una matriz NumPy.

**Matriz evaluada:** (1000, 58)

**Top 5 features con mayor varianza (por índice del vector):**
- Feature 0: varianza = **3.5130**
- Feature 52: varianza = **0.2456**
- Feature 53: varianza = **0.2424**
- Feature 1: varianza = **0.2128**
- Feature 2: varianza = **0.0908**

En la práctica, esto indica que unas pocas dimensiones concentran la mayor parte de la variabilidad, lo cual respalda aplicar **normalización** y continuar con **reducción de dimensionalidad (PCA)** en la siguiente fase.

**Evidencia:** 03_feature_engineering_resuelto.ipynb

## Transformaciones Avanzadas

En esta fase se aplicaron transformaciones adicionales sobre el dataset ya construido en *Feature Engineering*, con el objetivo de mejorar la calidad de las variables de entrada, corregir diferencias de escala y preparar el espacio de características para el entrenamiento de modelos.

El punto de partida fue `secop_features.parquet`, que contiene el vector `features_raw` con **58** dimensiones, compuesto por **57 features categóricas** (OneHotEncoding) y **1 feature numérica**.

### ¿Por qué normalizar?

Al revisar los primeros registros de `features_raw`, se evidenció una disparidad clara en las escalas: la variable numérica (asociada al valor del contrato) puede estar en órdenes de millones, mientras que las variables categóricas codificadas toman valores binarios (0/1).  
Ejemplo observado en `features_raw`: `[4.5588e+06, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, ...]`

Esta diferencia de magnitudes puede afectar el entrenamiento, ya que las variables con valores grandes tienden a dominar el proceso de aprendizaje y dificultan la convergencia o la interpretación del modelo.

### Comparación antes y después de StandardScaler

Para corregir el problema de escalas, se aplicó **StandardScaler** sobre el vector `features_raw`, generando un nuevo vector normalizado denominado `features_scaled`. Con esto, las dimensiones quedan en una escala comparable, reduciendo el sesgo por magnitud y dejando el dataset listo para técnicas posteriores como reducción de dimensionalidad (por ejemplo, PCA) y entrenamiento de modelos.


### Estadísticas comparativas (muestra)

**Antes (`features_raw`):**
- Min: 0.00  
- Max: 24.27  
- Media: 0.34  
- Desviación estándar: 2.23  

**Después (`features_scaled`):**
- Min: 0.00  
- Max: 72.55  
- Media: 0.35  
- Desviación estándar: 1.57  

Estos valores corresponden a una muestra utilizada para comparar el comportamiento del vector antes y después del escalado. El escalado estandariza las magnitudes y deja el dataset en mejores condiciones para aplicar PCA y entrenar modelos de forma más estable.

## Configuración de PCA y selección del número de componentes

Esta etapa aplica **PCA (Análisis de Componentes Principales)** sobre el vector **`features_scaled`** para reducir dimensionalidad y dejar un espacio de features más manejable antes del entrenamiento.

- **Dimensión original del vector**: **58**
- **Número de componentes seleccionados (k)**: **30**
- **Salida del PCA**: **`features_pca`** (vector denso con 30 componentes)

La elección de **k = 30** se hizo probando valores y revisando la **varianza explicada acumulada**, buscando un equilibrio entre reducción y retención de señal.

**Varianza explicada acumulada (según el ajuste de PCA):**
- **Componente 10**: **23.47%**
- **Componente 20**: **41.33%**
- **Componente 30**: **58.84%**

En este dataset la varianza queda relativamente “repartida” entre componentes, algo común cuando hay muchas variables categóricas codificadas. Aunque no se alcanza un 80% de varianza explicada, **30 componentes** reducen la dimensionalidad de **58 → 30** (reducción de **48.3%**) manteniendo una porción relevante de información para modelado.


## Pipeline completo de transformaciones

Finalmente, se integraron las transformaciones en un **pipeline** para asegurar un flujo reproducible y consistente, tanto en entrenamiento como en etapas posteriores.

**Orden aplicado:**
1. **StandardScaler**
2. **PCA**

Este orden es clave, porque **PCA** es sensible a la escala: si no se normaliza antes, las variables con magnitudes mayores dominan la descomposición.

Como resultado, se generó el dataset final listo para modelado (**`secop_ml_ready.parquet`**), con:
- **`features_pca`**: vector reducido de características (**k = 30**)
- **`label`**: variable objetivo del modelo (**`valor_del_contrato_log`**)

Adicionalmente, el pipeline entrenado se dejó persistido para reutilizarlo en procesos futuros y mantener consistencia entre entrenamiento e inferencia.

---


## Modelos de Regresión

### Regresión lineal

Se construyó un modelo de **Regresión Lineal** en Spark ML con el objetivo de predecir el valor del contrato a partir del vector de características generado en las fases anteriores (Feature Engineering + PCA). El dataset utilizado corresponde al archivo `secop_ml_ready.parquet`, el cual contiene las variables transformadas y listas para modelado.

#### Estrategia de Train/Test Split

Se definió una partición **70% entrenamiento / 30% prueba**, utilizando una semilla fija para garantizar reproducibilidad.

**Resultados del split:**
- **Train:** 70,126 registros (70%)
- **Test:** 29,874 registros (30%)

Esta proporción es adecuada para un dataset de 100.000 registros, ya que permite entrenar con suficiente información sin perder capacidad de evaluación.


**Configuración del Modelo de Regresión Lineal**

Se configuró un modelo base de `LinearRegression` sin regularización, con los siguientes parámetros:

- `featuresCol`: `features`
- `labelCol`: `label`
- `maxIter`: 100
- `regParam`: 0.0
- `elasticNetParam`: 0.0

Este modelo sirve como **baseline**, permitiendo evaluar el comportamiento inicial antes de aplicar regularización en fases posteriores.

### Interpretación del R² del Modelo (Train)

El modelo se entrenó sobre el conjunto de entrenamiento, obteniendo las siguientes métricas:

- **R² (train): 0.7417**
- **RMSE (train): 0.94**

Dado que la variable objetivo se trabajó en **escala logarítmica** (`valor_del_contrato_log`), estas métricas se interpretan en esa misma escala. En términos prácticos, el R² sugiere que el modelo captura una parte importante de la variabilidad del **log del valor contractual** en entrenamiento, mientras que el RMSE indica el tamaño típico del error (también en log), lo que es coherente para un modelo lineal base en un problema con alta dispersión.

**Análisis de calidad de predicciones y errores**  
En el conjunto de prueba se revisaron las predicciones calculando:
- error absoluto  
- error porcentual  
- identificación de las predicciones con mayor error


**Hallazgos clave:**

1. Se observaron errores absolutos elevados en contratos de valores muy altos.
2. Los errores porcentuales superan el 100% en contratos pequeños, lo cual evidencia:
  - Alta dispersión en los valores
  - Dificultad del modelo lineal para capturar extremos
3. No se detectaron errores sistemáticos por duplicación o fallas de cálculo.

Estos resultados son coherentes con la naturaleza altamente asimétrica del valor de los contratos.

### Comparación Train vs Test (Overfitting)

Se evaluó el modelo sobre el conjunto de prueba:

**Métricas en Test:**
- **RMSE:** 0.9551  
- **MAE:** 0.4624  
- **R² (test): 0.7440**

**Comparación Train vs Test:**
- **R² Train:** 0.7417  
- **R² Test:** 0.7440  
- **Diferencia absoluta:** 0.0023  

No se evidencia **overfitting**, ya que el desempeño en test es prácticamente igual al de train. El modelo generaliza de forma consistente dentro de lo esperable para una regresión lineal base.

## Análisis de coeficientes del modelo

- **Intercepto:** 8.79  
- **Número de coeficientes:** 30 (corresponden a los **30 componentes PCA**, no a variables originales)

El intercepto representa el valor base estimado de la **variable objetivo en escala logarítmica** (`label = valor_del_contrato_log`) cuando el vector de componentes PCA toma valores cercanos a cero.  
Dado que las *features* provienen de **PCA**, los coeficientes no se interpretan como “efecto de una variable” específica, sino como la contribución de cada **componente principal** (combinaciones de las variables originales).

## Análisis de distribución de residuos

Se calculó el residuo como:

**residuo = label − prediction**

El histograma muestra que los residuos están **concentrados alrededor de 0**, lo que indica que el modelo captura razonablemente el comportamiento central. También se observan **colas y algunos valores extremos**, consistentes con la alta dispersión de los contratos: los errores tienden a aumentar cuando el contrato es atípico (muy alto o muy bajo) incluso trabajando en escala logarítmica.


**Resultado visual:**

<img width="993" height="468" alt="image" src="https://github.com/user-attachments/assets/b7c78c19-cf7f-4e7e-8815-5346d0d7cb63" />



## Feature importance aproximado (componentes PCA)

Para identificar qué componentes influyen más, se ordenaron los coeficientes por **valor absoluto**.  
**Top 10 componentes más influyentes (|coef|):**

1. **PC3**  (coef = -1.225635)
2. **PC4**  (coef =  0.290171)
3. **PC1**  (coef = -0.118095)
4. **PC8**  (coef = -0.114240)
5. **PC5**  (coef = -0.087070)
6. **PC6**  (coef =  0.076073)
7. **PC17** (coef = -0.056776)
8. **PC21** (coef = -0.055518)
9. **PC30** (coef = -0.054747)
10. **PC28** (coef =  0.051529)

Estos resultados indican que **unas pocas componentes concentran la mayor parte del efecto lineal**, mientras que el resto aporta ajustes marginales. Al ser PCA, esto se entiende como influencia de **combinaciones lineales** de las variables originales, no de una variable individual.

--- 


## Regresión Logística para Clasificación de Riesgo Contractual

En esta fase se entrenó un modelo de **regresión logística** con el objetivo de **clasificar contratos del SECOP II** según su nivel de riesgo, a partir de las variables preparadas en las etapas previas del pipeline. A diferencia de la regresión lineal (enfoque de predicción continua), aquí se plantea un problema de **clasificación binaria**, donde el interés es estimar la probabilidad de que un contrato sea **alto riesgo**.

El dataset utilizado corresponde a `secop_features.parquet`, con **100.000** contratos y variables categóricas codificadas junto con variables numéricas listas para modelado.

**Notebook/Query:** `06_regresion_logistica.py`

### Creación de la variable objetivo binaria (`riesgo`)

Como el dataset original no incluye una variable explícita de riesgo, se construyó una variable objetivo binaria denominada `riesgo`, combinando dos criterios:

- **Riesgo financiero:** contratos cuyo **valor** supera el **percentil 90** del valor del contrato.
- **Riesgo operativo:** contratos con **duración definida** menor a **30 días** (cuando este dato está disponible).

El criterio financiero se aplicó a todos los contratos. El criterio operativo se aplicó únicamente cuando la duración estaba disponible; cuando no lo estaba, el contrato se clasificó solo con base en el criterio financiero para evitar excluir registros del análisis.

**Distribución final de la variable `riesgo`:**
- **Alto riesgo (1): 11.921 (11.9%)**
- **Bajo riesgo (0): 88.079 (88.1%)**
- **Total registros: 100.000**

Esta distribución refleja una **clase positiva minoritaria** (alto riesgo), por lo que en la evaluación del modelo se debe revisar el desempeño específicamente sobre esa clase y no depender únicamente de métricas globales.

### Análisis del balance de clases

Se analizó la distribución de la variable `riesgo` para evaluar el balance de clases antes de entrenar la regresión logística. Con base en el conteo del dataset, **88.079 contratos (88.1%)** corresponden a **bajo riesgo (0)** y **11.921 (11.9%)** a **alto riesgo (1)**, sobre un total de **100.000** registros.

Este resultado indica un desbalance moderado hacia la clase negativa. En la práctica, el modelo puede entrenarse como línea base, pero la evaluación debe centrarse en métricas que reflejen el desempeño sobre la clase positiva (alto riesgo) y, si el objetivo es priorizar detección, puede requerirse ajuste del umbral de decisión o técnicas de balanceo en etapas posteriores.

### Diferencia entre regresión logística y regresión lineal

La regresión logística se usa para **clasificación**, no para predicción de valores continuos. Estima la probabilidad de pertenecer a una clase (por ejemplo, `riesgo = 1`) aplicando una función sigmoide a la combinación lineal de las variables de entrada, produciendo un valor entre 0 y 1.

En este trabajo, la regresión lineal se utilizó para estimar el **valor del contrato**, mientras que la regresión logística se empleó para clasificar contratos según su **nivel de riesgo**, coherente con la naturaleza de cada objetivo.


**Configuración del modelo**

El modelo de regresión logística se configuró con los siguientes parámetros:

- `maxIter = 100`
- `regParam = 0.0`
- `threshold = 0.5`

Esta configuración corresponde a un modelo base sin regularización, utilizado como punto de referencia antes de introducir penalizaciones y ajustes más avanzados. El threshold de 0.5 se utilizó inicialmente como valor estándar, siendo posteriormente analizado y ajustado en los retos bonus.

**Interpretación de probabilidades**

El modelo genera una columna `probability` con la forma:

- `probability = [p(clase=0), p(clase=1)]`

Es decir, el **segundo valor** corresponde a la probabilidad de **alto riesgo (clase 1)**.  
Ejemplo: si `probability = [0.80, 0.20]`, entonces `p(alto_riesgo)=0.20` y, con `threshold=0.5`, el contrato se clasifica como **bajo riesgo (0)**.

**Evaluación del modelo con múltiples métricas**

Para evaluar el desempeño del modelo se utilizaron métricas apropiadas para clasificación binaria:

- **AUC-ROC:** `0.9431`
- **Accuracy:** `0.9652`
- **Precision (weighted):** `0.9652`
- **Recall (weighted):** `0.9652`
- **F1-Score (weighted):** `0.9630`

El valor de AUC-ROC indica una buena capacidad del modelo para discriminar entre contratos de alto y bajo riesgo, independientemente del threshold utilizado. Las métricas de precision y recall muestran un desempeño balanceado, lo que sugiere que el modelo logra identificar contratos riesgosos sin generar un número excesivo de falsas alarmas.

**Matriz de confusión**

Se construyó la matriz de confusión sobre el conjunto de prueba, obteniendo:

- **True Positives (TP)**: 2.587  
- **True Negatives (TN)**: 26.204  
- **False Positives (FP)**: 89  
- **False Negatives (FN)**: 950  
- **Total evaluado**: 29.830  

En este caso, el error más crítico son los **falsos negativos (FN)**, porque representan contratos de **alto riesgo** clasificados como **bajo riesgo**. Con estos resultados, el modelo mantiene una **precisión alta** cuando predice “alto riesgo” (pocos FP), pero deja escapar una parte relevante de casos realmente riesgosos (FN).

**Ajuste del threshold de clasificación**

Se evaluó el desempeño del modelo utilizando diferentes valores de threshold. Al aumentar el threshold a 0.7, se obtuvo:

- Accuracy: **0.950**
- Recall: **0.950**

Este resultado confirma el trade-off entre precisión y sensibilidad. Un threshold más alto hace al modelo más conservador, reduciendo la detección de contratos riesgosos. Dado el objetivo del análisis, se concluye que no es conveniente utilizar un threshold elevado y que valores cercanos o inferiores a 0.5 son más adecuados para priorizar la detección de riesgo.

**Curva ROC**

Se construyó la curva ROC para visualizar el trade-off entre la tasa de verdaderos positivos (TPR) y la tasa de falsos positivos (FPR) a lo largo de distintos thresholds. La curva se encuentra claramente por encima de la línea de clasificación aleatoria, confirmando la capacidad discriminatoria del modelo.

<img width="736" height="505" alt="image" src="https://github.com/user-attachments/assets/6782ae8d-db55-4461-bffb-6874a5759a04" />


La curva ROC muestra que el modelo discrimina muy bien entre contratos de **alto** y **bajo riesgo**. El **AUC = 0.943** indica un desempeño claramente superior al azar (0.5) y cercano a un clasificador excelente: el modelo tiende a asignar probabilidades más altas a los contratos de alto riesgo. Al estar la curva por encima de la diagonal, es posible lograr **alta detección (TPR)** con un **nivel moderado de falsas alarmas (FPR)**, ajustando el *threshold* según el objetivo (por ejemplo, priorizar *recall* si es más costoso dejar pasar contratos riesgosos).


## Regularización L1, L2 y ElasticNet

En esta fase se evaluó el efecto de la regularización sobre el modelo de regresión lineal entrenado con **componentes PCA**. La intención fue comprobar si introducir penalización **L2 (Ridge)**, **L1 (Lasso)** o una combinación **ElasticNet** mejora la estabilidad del modelo y su desempeño en datos no vistos, manteniendo el mismo pipeline de variables ya transformadas.

**Dataset utilizado:** `secop_ml_ready.parquet`  
**Variables para modelado:** `features = features_pca` y `label = valor_del_contrato_log` (escala log).  
**Partición:** 70% entrenamiento / 30% prueba (**Train: 70,170** | **Test: 29,830**, semilla 42).

### Motivación (por qué regularizar)
Aunque el baseline ya permite una primera aproximación, la regularización ayuda a **controlar la magnitud de los coeficientes** y a reducir sensibilidad a variaciones del dataset. En un escenario con variables transformadas (PCA), esto se traduce en un modelo potencialmente más **robusto** y con mejor capacidad de generalización al comparar métricas en test.

### Configuración de evaluación
La comparación entre configuraciones se hizo con **RMSE** como métrica principal, calculado sobre el conjunto de prueba. Dado que la variable objetivo está en **log**, el RMSE se interpreta en esa escala (no en pesos), por lo que sirve para comparar modelos de forma consistente dentro del mismo enfoque.

**Métrica utilizada:** `rmse`


**Experimento con Múltiples Regularizaciones**

Se entrenaron 18 modelos variando:

**regParam (λ):**

- 0.0  
- 1.0  
- 10.0  
- 100.0  
- 1000.0  
- 10000.0  

**elasticNetParam (α):**

- 0.0 → Ridge  
- 0.5 → ElasticNet  
- 1.0 → Lasso  

Total modelos entrenados: 18  

**Resultados del Experimento**

Modelo sin regularización (λ = 0.0):
- RMSE Train: 0.94
- RMSE Test: 0.96

Ridge (α = 0.0, λ = 1.0):
- RMSE Test: 1.12

ElasticNet (α = 0.5, λ = 1.0):
- RMSE Test: 1.29

Lasso (α = 1.0, λ = 1.0):
- RMSE Test: 1.47

A medida que λ aumenta, el RMSE en test también aumenta, lo que sugiere pérdida de capacidad predictiva (underfitting). El menor RMSE se obtuvo con λ = 0.0; en este caso, la regularización no mejoró el desempeño del modelo.

**Comparación de Overfitting**

Brecha aproximada:

Gap = RMSE_Test − RMSE_Train
Gap ≈ 947,902,345.85

La brecha se mantiene prácticamente constante en todas las configuraciones.

Interpretación:

- No se observa reducción significativa del overfitting mediante regularización.
- El modelo basado en PCA ya presenta estabilidad estructural.
- Incrementar λ solo aumenta el error sin reducir la brecha train-test.

**Modelo Final**

Se seleccionó como mejor modelo:

- regParam = 0.0  
- elasticNetParam = 0.0  

Resultados finales:

- RMSE Train: 0.94
- RMSE Test: 0.96

Modelo guardado en: /opt/spark-data/raw/regularized_model

**Efecto de λ en Lasso**

Se evaluó cómo cambia la **sparsity** (cantidad de coeficientes llevados a cero) al aumentar **λ (regParam)** en **Lasso (L1)**, usando un modelo entrenado sobre **30 componentes PCA**.

**Resultados (coeficientes en 0 / 30 | RMSE test):**
- λ = 0.01 → 8/30 coeficientes en 0 | RMSE test: 0.96  
- λ = 0.10 → 25/30 coeficientes en 0 | RMSE test: 1.00  
- λ = 1.00 → 29/30 coeficientes en 0 | RMSE test: 1.47  
- λ = 10.00 → 30/30 coeficientes en 0 | RMSE test: 1.88  
- λ = 100.00 → 30/30 coeficientes en 0 | RMSE test: 1.88  
- λ = 1000.00 → 30/30 coeficientes en 0 | RMSE test: 1.88  

A medida que **λ aumenta**, Lasso **fuerza más coeficientes a cero** (termina anulando el modelo cuando λ ≥ 10, dejando **30/30** en cero). En paralelo, el **RMSE en test empeora**, por lo que en este experimento la regularización fuerte no aporta y conviene mantener **λ bajo** si se busca conservar capacidad predictiva.

#### Visualización del efecto de λ

Efecto de λ en la sparsity (Lasso):

<img width="826" height="514" alt="image" src="https://github.com/user-attachments/assets/3c9faffa-9530-44f1-860f-18e79a731c60" />



Efecto de λ en el error del modelo:

<img width="598" height="346" alt="image" src="https://github.com/user-attachments/assets/41e0faa3-739e-4190-8dc1-b511c2e71dc2" />


Las dos gráficas muestran un patrón coherente: a medida que aumenta **λ (regParam)** en Lasso, el modelo aplica una penalización más fuerte, lo que se refleja en **más coeficientes llevados a cero** y, al mismo tiempo, en un **cambio progresivo del RMSE en test** hasta llegar a una zona donde el comportamiento se vuelve **estable**. En conjunto, esto confirma que **λ controla directamente el nivel de simplicidad del modelo** (sparsity) y permite observar con claridad el **trade-off** entre regularización y desempeño, facilitando la selección de un valor de λ acorde al objetivo del análisis.

## **Optimizacion de Hiperparametros**

### **Validacion Cruzada**

En esta fase se aplicó **validación cruzada K-Fold** para obtener una estimación más robusta del desempeño del modelo, reduciendo la dependencia de una sola partición train/test. El flujo consiste en dividir el conjunto de entrenamiento en **K folds** y entrenar el modelo K veces, usando en cada iteración **K−1 folds para entrenar** y **1 fold para validar**, promediando la métrica para estabilizar la evaluación. El dataset utilizado fue `secop_ml_ready.parquet`, con partición **80% entrenamiento / 20% prueba** (semilla 42), obteniendo **Train: 80,068** y **Test: 19,932** registros.

Para la búsqueda se construyó un **ParamGrid** con **36 combinaciones**, variando `regParam` (0.01, 0.1, 1.0), `elasticNetParam` (0.0, 0.5, 1.0), `maxIter` (50, 100) y `fitIntercept` (True, False). Con **K=5 folds**, esto implicó entrenar **180 modelos** en total (36 × 5), evaluando cada configuración con **RMSE** como métrica principal.

El mejor modelo seleccionado por Cross-Validation correspondió a una configuración tipo **Ridge** (`elasticNetParam = 0.0`) con regularización suave (`regParam = 0.01`). En los resultados del notebook, el **mejor RMSE en validación cruzada fue 0.95**, y al evaluar esa configuración sobre el conjunto de prueba se obtuvo un **RMSE en test de 0.94**, lo que indica un desempeño consistente fuera de muestra (teniendo en cuenta que el objetivo está en escala logarítmica).

Adicionalmente, se probó el efecto del número de folds con **K = 3, 5 y 10**. El **mejor RMSE se mantuvo estable (0.95)** en los tres casos, mientras que el **tiempo total** aumentó con K (**21.7s**, **35.3s** y **68.6s**, respectivamente), reflejando el trade-off esperado entre robustez de validación y costo computacional.

## Optimización de Hiperparámetros

Se optimizaron hiperparámetros del modelo de **Regresión Lineal con regularización** usando el dataset `secop_ml_ready.parquet`, donde la variable objetivo corresponde a `valor_del_contrato_log` (por eso el **RMSE se interpreta en la escala log** del label). Para garantizar reproducibilidad, se mantuvo un **split 80/20** con **semilla 42**, obteniendo **80,068 registros en train** y **19,932 en test**.

Se ejecutó un **Grid Search con Validación Cruzada (K=3)** explorando combinaciones de `regParam` (0.01, 0.1, 1.0), `elasticNetParam` (0.0, 0.5, 1.0) y variaciones de configuración del estimador. El mejor modelo encontrado fue **regParam = 0.01**, **elasticNetParam = 0.0 (Ridge/L2)**, **maxIter = 50** y **fitIntercept = True**, con un **RMSE promedio en Cross-Validation ≈ 0.94** y un **RMSE en test ≈ 0.94**. El tiempo total de ejecución de esta búsqueda fue de **27.07 s**.

En paralelo, se aplicó **TrainValidationSplit** con **trainRatio = 0.8** para comparar desempeño y costo computacional. Esta estrategia encontró exactamente la misma configuración óptima (**regParam = 0.01**, **elasticNetParam = 0.0**, **maxIter = 50**, **fitIntercept = True**) y obtuvo el mismo **RMSE en test ≈ 0.94**, con un tiempo de ejecución menor de **8.03 s**, lo que sugiere consistencia del óptimo bajo ambos enfoques.

Finalmente, se realizó un refinamiento local alrededor de la mejor región (incluyendo valores cercanos como **regParam = 0.005, 0.01, 0.02** y `elasticNetParam` en **0.0, 0.25, 0.5**), sin observar mejoras sobre el **RMSE ≈ 0.94**. Con base en esto, se seleccionó como estrategia final **Grid Search + CV** y se guardó el modelo óptimo en `/opt/spark-data/raw/tuned_model`, junto con los hiperparámetros en `/opt/spark-data/raw/hiperparametros_optimos.json`.


# **MLOps y Produccion**

## **MLflow Tracking**

En este reto se configuró la conexión con el servidor de MLflow utilizando la URI `http://mlflow:5000`, lo que permitió centralizar el registro de experimentos en un servidor dedicado y no en archivos locales. Se creó el experimento `secop_prediccion`, donde se almacenan todos los runs relacionados con el modelo de predicción de contratos. Esto garantiza trazabilidad, organización y comparabilidad entre diferentes entrenamientos del modelo.

**Registro del Modelo Baseline**

Se entrenó un modelo base de regresión lineal sin regularización (`regParam=0.0`, `elasticNetParam=0.0`) utilizando como variable objetivo el **logaritmo del valor del contrato**, con el fin de estabilizar la varianza y reducir el impacto de valores extremos.

Las métricas obtenidas fueron:

- **RMSE:** 0.89  
- **MAE:** 0.46  
- **R²:** 0.73  

Estas métricas están calculadas en **escala logarítmica**, lo que implica que los errores representan diferencias relativas y no absolutas en pesos colombianos. El modelo fue almacenado como artefacto dentro del run, permitiendo su posterior consulta o descarga desde la interfaz de MLflow.

**Registro de Múltiples Modelos (Ridge, Lasso y ElasticNet)**

Se entrenaron tres modelos adicionales con diferentes tipos de regularización: Ridge (L2), Lasso (L1) y ElasticNet (L1 + L2), todos con `regParam=0.1`. Cada run registró parámetros, métricas (RMSE, MAE y R²) y el modelo entrenado como artefacto.

🔹 **Ridge**
- **RMSE:** 0.89  
- **MAE:** 0.46  
- **R²:** 0.7385  

🔹**Lasso**
- **RMSE:** 0.92  
- **MAE:** 0.50 
- **R²:** 0.7209 

 🔹 **ElasticNet**
- **RMSE:** 0.91 
- **MAE:** 0.48 
- **R²:** 0.7312 

Se observó que el modelo Ridge obtuvo el mejor desempeño general en términos de RMSE y R², aunque las diferencias entre modelos fueron moderadas.


**Exploración y Comparación en MLflow UI**

Se utilizó la interfaz web de MLflow para comparar los runs lado a lado, ordenar por RMSE y analizar las diferencias en parámetros y métricas. Se observó que el modelo Ridge presentó el menor RMSE (≈ 1.45), consolidándose como la mejor alternativa dentro de los experimentos evaluados.

<img width="1600" height="596" alt="image" src="https://github.com/user-attachments/assets/8c50b8b1-cc03-4f86-a5e4-b0e986b90a3f" />



## **Registro de Artefactos Personalizados**

Se creó un nuevo run donde, además de registrar el modelo y métricas, se agregó un reporte en texto con los resultados y un gráfico de **predicciones vs valores reales en escala logarítmica**. Este gráfico permitió visualizar el comportamiento del modelo respecto a la línea de predicción perfecta y evidenciar la tendencia del modelo a concentrarse alrededor de la media.

Estos archivos fueron almacenados como artefactos dentro de MLflow, permitiendo su visualización directa desde la interfaz.

<img width="558" height="553" alt="image" src="https://github.com/user-attachments/assets/72253475-8111-4c72-ba0b-c8e344b54eb9" />



## **Model Registry**

El ciclo completo de gestión de modelos utilizando el **Model Registry de MLflow**, con el objetivo de versionar, promover y consumir modelos de forma controlada. Se logro, configurando la conexión al servidor de MLflow y se definió el nombre del modelo como `secop_prediccion_contratos` y se estableció el entorno para registrar versiones oficiales del modelo de predicción del valor de contratos SECOP.

En el primer paso se entrenó y registró la versión 1 (baseline) sin regularización, almacenando métricas y registrándola directamente en el Registry. Luego se entrenó la versión 2 con regularización (ElasticNet), comparando su RMSE frente al baseline. Tras la evaluación, se determinó que la versión 1 presentó un mejor desempeño, por lo que fue promovida a **Production**, mientras que la versión 2 fue archivada. Este proceso permitió aplicar correctamente el ciclo de vida: `None → Staging → Production → Archived`.  
 
<img width="1600" height="439" alt="image" src="https://github.com/user-attachments/assets/dae1fcbe-e23c-4eb4-b9fb-056a31908170" />


Posteriormente se agregó metadata y descripción formal al modelo en producción, incluyendo versión, RMSE validado, dataset utilizado, tipo de features (PCA), autor y fecha. Esto garantiza trazabilidad, documentación técnica y gobernanza del modelo dentro del Registry.  
 
<img width="738" height="803" alt="image" src="https://github.com/user-attachments/assets/7270abf3-fe8c-431d-8986-919ef1874b6b" />


Finalmente, se cargó el modelo directamente desde el Registry utilizando la URI lógica: "models:/secop_prediccion_contratos/Production", se verificó su correcto funcionamiento realizando predicciones sobre el conjunto de prueba. El RMSE obtenido coincidió exactamente con el registrado durante el entrenamiento, confirmando reproducibilidad, control de versiones y correcta gestión del ciclo de vida del modelo.

---

## Inferencia en Producción

En esta sección se simuló un flujo típico de **MLOps** para generar **predicciones batch** en un entorno controlado. El objetivo es representar cómo se ejecutaría el modelo en producción: cargar un modelo versionado desde **MLflow Model Registry**, recibir datos nuevos, aplicar el modelo a gran escala y dejar resultados listos para consumo por otros equipos o sistemas. Este enfoque permite trazabilidad (qué modelo produjo qué predicción), repetibilidad y control de versiones, elementos clave cuando el modelo evoluciona en el tiempo.

La inferencia se planteó como **Batch Inference**, ya que el caso consiste en correr predicciones sobre un volumen grande de contratos. A diferencia del entrenamiento, aquí el foco no está en ajustar parámetros sino en **operacionalizar el modelo**: cargarlo desde `models:/{nombre_modelo}/Production`, lo cual es preferible a usar una ruta local porque desacopla el despliegue del entorno, facilita rollback (volver a una versión previa) y estandariza el “modelo oficial” que está activo en producción. Si no existe un modelo en el stage *Production*, el sistema debería manejarlo con control de errores y fallback (por ejemplo, cargar *Staging* o abortar el proceso dejando un log de alerta).

Para simular datos nuevos, se cargó el parquet procesado y se preparó el esquema para que coincida con lo que el modelo espera, eliminando la columna objetivo (label). En un escenario real, estos datos podrían llegar desde una base de datos transaccional, archivos en un data lake (S3/HDFS), una API, o incluso un stream; en todos los casos, la idea es que el modelo reciba únicamente las **features** requeridas y que el pipeline valide el esquema antes de ejecutar predicciones.

Las predicciones se generaron usando `model.transform()` y se agregó un `prediction_timestamp`. Este timestamp es importante para trazabilidad, auditoría y monitoreo, ya que permite reconstruir cuándo se produjo cada predicción y asociarla con la versión del modelo y el lote de datos. Además del timestamp, en producción suele ser útil guardar metadatos como `model_version`, `batch_id`, `source_system`, `data_date` y un identificador único del contrato.

Luego se incluyó un bloque de **monitoreo básico** para verificar que las predicciones sean razonables: estadísticas descriptivas (mínimo, máximo, promedio, desviación estándar), detección de valores negativos si el contexto no los permite, y conteos por rangos para detectar colas extremas. Este monitoreo es una primera capa para identificar anomalías y es el punto de partida para detectar **data drift**, comparando la distribución actual de features y/o predicciones contra la distribución histórica del entrenamiento. Si las predicciones empiezan a desviarse de lo esperado, lo correcto sería activar alertas, revisar la calidad de datos, y evaluar reentrenamiento o ajuste de umbrales según el caso.

Finalmente, se guardaron los resultados en formatos consumibles. El formato **Parquet** es el más adecuado para analítica interna y consumo en Spark por eficiencia y compresión; mientras que **CSV** es útil para consumo externo, validaciones rápidas o reportes que se abren en herramientas como Excel (aunque es menos eficiente). Para un dashboard interno normalmente se prioriza Parquet o una tabla en un motor analítico; para un reporte gerencial suele ser CSV o una tabla resumida; y para input de otro sistema suele preferirse Parquet o una tabla con esquema fijo (dependiendo del integrador).

En cuanto a automatización, este flujo se puede programar de forma periódica (por ejemplo diario o bajo demanda según la llegada de lotes). Un orquestador como Airflow permite calendarización, dependencias, reintentos, logging y alertas. El monitoreo debería incluir comparación de métricas en el tiempo, chequeos de drift y umbrales de alarma. El reentrenamiento se dispara cuando el desempeño cae, el drift es persistente o cambian reglas de negocio. Las alertas típicas se basan en cambios abruptos de distribución, aumento de valores extremos, incremento sostenido de error (si se cuenta con verdad terreno posterior), o fallas de esquema/datos.

En resumen, esta sección replica el ciclo mínimo de inferencia en producción: **cargar modelo versionado**, **preparar datos nuevos**, **predecir a escala**, **monitorear resultados**, **persistir outputs**, y **diseñar la automatización** para operación continua.


---
## Conclusiones Finales

A lo largo del taller se construyó un flujo completo y reproducible para analizar y modelar contratos electrónicos de SECOP II, desde la ingesta y depuración hasta el despliegue en un escenario de “producción”. El trabajo no se limitó a entrenar modelos: se estandarizó un entorno de ejecución (Docker + Spark), se consolidó un dataset curado en Parquet y se dejó un pipeline de Machine Learning escalable que permite repetir el proceso con nuevos cortes de datos sin rehacer cada paso manualmente.

En la fase exploratoria quedó claro que el valor contractual es una variable de alta dispersión y con asimetría marcada (muchos contratos de valores relativamente bajos y una fracción pequeña de contratos con montos muy altos). Ese comportamiento justificó decisiones técnicas posteriores del pipeline: limpieza de registros inconsistentes, tratamiento de nulos, y el uso de transformaciones que estabilizan la escala de la variable objetivo (incluyendo el uso de una versión transformada del valor para mejorar el ajuste y la estabilidad del entrenamiento). A nivel descriptivo, también se identificaron patrones estructurales útiles para interpretación: concentración territorial y diferencias claras por modalidad y estado contractual, que ayudan a contextualizar cualquier salida predictiva y a evitar interpretaciones “ciegas” del modelo.

En términos de modelado, el valor principal del trabajo fue pasar de un enfoque básico a uno robusto. Se implementaron pipelines con feature engineering (codificación de categorías y ensamblado de variables), escalamiento y reducción de dimensionalidad (PCA) para dejar un conjunto de features consistente y entrenable de manera distribuida. Sobre esa base se entrenaron modelos de regresión y clasificación, se evaluaron con métricas acordes al objetivo (errores para regresión y desempeño discriminativo para clasificación), y se controló el riesgo de sobreajuste comparando comportamiento entre entrenamiento y prueba. La regularización y el ajuste de hiperparámetros se trabajaron como parte del método (no como “reto aislado”): se exploró cómo cambian los errores al ajustar penalizaciones y se formalizó la selección del mejor enfoque mediante validación cruzada, priorizando generalización por encima de resultados “bonitos” solo en entrenamiento.

Finalmente, el componente MLOps cerró el ciclo de vida del modelo. Se registraron experimentos y resultados en MLflow, se dejaron versiones trazables en el Model Registry y se planteó el uso de stages (Staging/Production) como control práctico antes de exponer un modelo como definitivo. Con esto, el notebook de inferencia en producción no queda como demostración teórica: representa un patrón realista para cargar el modelo por nombre y etapa, generar predicciones batch, agregar metadatos (timestamp) y guardar salidas en formatos consumibles (Parquet/CSV). En conjunto, el entregable final no es solo “un modelo”, sino un sistema reproducible y escalable que deja bases sólidas para monitoreo, retraining y mejoras futuras con nuevas variables o nuevas ventanas de datos.






