# **Análisis de la Dinámica Contractual del Estado Colombiano usando Datos Abiertos de SECOP II**

**Desarrollado por:** Diego Alejandro Gomez Cortes

### **Introducción**

SECOP II (Sistema Electrónico para la Contratación Pública) es la principal plataforma de transparencia y seguimiento de la contratación estatal en Colombia. A través de esta plataforma se registran los contratos públicos de entidades nacionales y territoriales, permitiendo el acceso abierto a información clave como valores contratados, tipos de contrato, entidades, proveedores y estados contractuales. El volumen, diversidad y naturaleza pública de estos datos convierten a SECOP II en una fuente estratégica para el análisis económico, administrativo y de política pública.

El análisis de los datos de SECOP II permite identificar patrones de contratación, concentración de recursos, comportamientos por territorio y modalidades contractuales, así como posibles riesgos o ineficiencias en el uso de los recursos públicos. Dado que la contratación estatal representa una porción significativa del gasto público, su estudio sistemático aporta valor tanto para la toma de decisiones institucionales como para el control ciudadano y el desarrollo de modelos analíticos y predictivos.

Desde una perspectiva de datos, SECOP II plantea retos propios de los entornos Big Data: grandes volúmenes de información, esquemas complejos, datos heterogéneos y actualizaciones constantes. Por esta razón, el uso de herramientas distribuidas como Apache Spark, Visual Studio Code, Java, JupyterLab y Docker resultan fundamentales para procesar, explorar y preparar estos datos de forma eficiente y escalable.

### **Objetivo del Análisis**

El objetivo de este trabajo es comprender el comportamiento de la contratación pública registrada en SECOP II, explorando sus principales características estructurales y económicas mediante técnicas de análisis de datos a gran escala. A partir de esta exploración, se busca sentar las bases para la construcción de análisis avanzados y modelos de Machine Learning que permitan extraer conocimiento útil sobre la dinámica contractual del Estado colombiano.

## **Cargue de los Datos**

En una primera fase, se tuvo en cuenta la construccion de entornos de trabajos adecuados para el tratamiento de los datos del Secop para asi mismos tratar con diferentes entornos que nos ayudaran asu analisis y gracias a esto se realizó la ingesta de datos directamente desde la API de Datos Abiertos Colombia, seleccionando los contratos más recientes que cuentan con fecha de firma registrada. Posteriormente, la información fue cargada en un entorno distribuido con Apache Spark, donde se exploró su esquema y se normalizaron los nombres de las columnas para garantizar consistencia técnica.

Asi mismo se seleccionaron las variables clave relevantes para el análisis y modelado, y el conjunto de datos resultante fue almacenado en formato Parquet optimizado. Este proceso permitió disponer de una base de datos estructurada, eficiente y lista para análisis exploratorio y etapas posteriores de Machine Learning distribuido.

Query: **01_ingesta_resuelto.ipynb**

## **Análisis Exploratorio de Datos (EDA)**

En esta fase se realizó un análisis exploratorio sobre los contratos electrónicos del SECOP II con el objetivo de comprender la estructura del dataset, la distribución de los valores contractuales y los patrones principales por territorio, tipo y estado del contrato. Este análisis permite validar la calidad de los datos y preparar el terreno para la construcción de variables y modelos de Machine Learning distribuido.

Inicialmente se validó el **periodo temporal efectivo** de los datos analizados a partir de la columna `fecha_de_firma`. Los resultados muestran que los contratos incluidos corresponden principalmente al último trimestre de 2025 y los primeros registros de 2026, confirmando que el dataset representa contratos efectivamente firmados y no simples registros administrativos pendientes.

Posteriormente se calcularon **estadísticas descriptivas generales** y específicas para la variable objetivo `valor_del_contrato`. Se identificó una distribución altamente asimétrica, donde la mayoría de los contratos se concentran en rangos bajos y medios, mientras que una fracción menor representa contratos de muy alto valor. El análisis por rangos permitió cuantificar esta concentración y evidenciar la existencia de contratos de alto impacto presupuestal.

En el análisis territorial se observó una fuerte concentración de contratos en grandes centros administrativos como Bogotá, Antioquia y Valle del Cauca, tanto en número de contratos como en valor total adjudicado. Este comportamiento refleja la centralización de la contratación pública y justifica el uso de análisis regionales más detallados en fases posteriores.

![Distribución de contratos por departamento](../Imagenes/Imagen1.png)

Tambien se exploró la distribución por **tipo de contrato**, donde la modalidad de **Prestación de Servicios** domina ampliamente el volumen de contratos, seguida por modalidades administrativas específicas y contratos de compra y suministro. En cuanto al **estado del contrato**, la mayoría se encuentran en ejecución o han sufrido modificaciones, lo cual es consistente con procesos contractuales activos y dinámicos.

Aparte se aplicó el método **IQR (Interquartile Range)** para la detección de outliers en el valor del contrato, excluyendo previamente valores iguales o menores a cero. El análisis identificó aproximadamente un 15% de contratos como valores atípicos superiores, los cuales no representan errores, sino contratos de gran escala con alto impacto presupuestal. Este resultado confirma la necesidad de aplicar transformaciones y técnicas de escalamiento en las siguientes fases del pipeline de Machine Learning.

El estudio temporal por año y mes evidenció picos claros de contratación hacia finales de 2025, con una disminución marcada al inicio de 2026, lo cual coincide con ciclos fiscales y administrativos propios de la contratación pública en Colombia.

Query: **02_exploracion_eda_resuelto.ipynb**

## Feature Engineering y Construcción de Pipelines

En esta fase se prepararon los datos del **SECOP II** para su uso en modelos de *Machine Learning* utilizando **Spark ML**. A partir del dataset explorado en la fase de EDA, se transformaron variables categóricas y numéricas en un **vector de características numéricas (`features_raw`)**, requisito fundamental para entrenar algoritmos de aprendizaje automático. El proceso se aplicó sobre **100.000 contratos**, garantizando consistencia, escalabilidad y reutilización mediante el uso de **Pipelines**.

### Selección de variables

**Variables categóricas**

Se seleccionaron variables con alto poder explicativo y relevancia contractual:

- `departamento`
- `tipo_de_contrato`
- `estado_contrato`

Estas variables permiten capturar diferencias territoriales, administrativas y operativas entre los contratos registrados en SECOP II.

**Variable numérica**

- `valor_del_contrato_num`

Esta variable representa el valor monetario del contrato y es el principal insumo cuantitativo del modelo.

---

### Limpieza de datos

Se utilizó una estrategia de **eliminación de valores nulos (`dropna`)** únicamente sobre las variables seleccionadas para el modelo. Esta decisión se tomó para evitar sesgos y mantener integridad en el proceso de entrenamiento.

- Registros antes de limpieza: **100.000**
- Registros después de limpieza: **100.000**

No se perdió información, lo que evidencia una **alta calidad del dataset** y permite avanzar sin necesidad de imputaciones artificiales.

---

### Codificación de variables categóricas

Las variables categóricas fueron transformadas usando:

1. **StringIndexer**: conversión de texto a índices numéricos
2. **OneHotEncoder**: transformación de índices a vectores binarios

**Categorías detectadas**

| Variable            | Categorías únicas |
|---------------------|------------------|
| departamento         | 34               |
| tipo_de_contrato     | 20               |
| estado_contrato      | 7                |

**Resultado del OneHotEncoding**

- Total de features categóricas generadas: **61**
- Features numéricas originales: **1**

**Total de features esperadas:** **62**


### Construcción del vector de features

Las variables numéricas y las categóricas codificadas fueron combinadas mediante **VectorAssembler**, generando un único vector:

- `features_raw`

**Validación del resultado**

- Dimensión esperada del vector: **62**
- Dimensión real del vector `features_raw`: **62**

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

### Análisis de varianza de features (Bonus)

Se realizó un análisis de varianza sobre el vector `features_raw` para identificar las dimensiones con mayor capacidad de diferenciación.

**Top 5 features con mayor varianza**

| Feature | Varianza |
|--------|----------|
| Feature 0  | 8.337e+18 |
| Feature 35 | 0.1948 |
| Feature 1  | 0.1699 |
| Feature 55 | 0.1618 |
| Feature 2  | 0.1275 |

**Interpretación:**

- **Feature 0** corresponde al valor del contrato, lo que explica su alta varianza debido a la escala monetaria.
- Las demás features representan categorías específicas con fuerte impacto en la diferenciación de contratos.
- Este comportamiento justifica la necesidad de aplicar **normalización y reducción de dimensionalidad (PCA)** en la siguiente fase.


## Transformaciones Avanzadas (Notebook 04)

En esta fase se aplicaron transformaciones avanzadas sobre el dataset previamente procesado mediante Feature Engineering, con el objetivo de **mejorar la calidad de las variables de entrada**, **reducir problemas derivados de escalas heterogéneas** y **disminuir la dimensionalidad del espacio de features** antes de entrenar modelos de Machine Learning.

El punto de partida fue el dataset `secop_features.parquet`, el cual contiene un vector de características (`features_raw`) de 62 dimensiones, compuesto por variables numéricas y categóricas codificadas.

---

**¿Por qué normalizar?**

Al inspeccionar los primeros registros del vector `features_raw`, se evidenció una **alta disparidad en las escalas de las variables**. Por ejemplo, el primer valor del vector corresponde al valor del contrato y presenta magnitudes del orden de millones, mientras que las variables categóricas codificadas toman valores binarios (0 o 1).

Ejemplo de valores observados en `features_raw`: [4.5588e+06, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0]

Esta diferencia de escalas representa un problema para algoritmos de Machine Learning, ya que las variables con valores grandes dominan el proceso de aprendizaje, afectando negativamente la convergencia y la interpretación del modelo.

**Comparación antes y después de StandardScaler**

Para solucionar el problema de escalas, se aplicó `StandardScaler` sobre el vector `features_raw`, generando un nuevo vector normalizado denominado `features_scaled`.

**Estadísticas comparativas:**

**Antes (features_raw):**
- Min: 0.00  
- Max: 75,952,011,382.00  
- Media: 4,756,215.14  
- Desviación estándar: 368,580,743.71  

**Después (features_scaled):**
- Min: 0.00  
- Max: 69.01  
- Media: 0.18  
- Desviación estándar: 1.12  

Estos resultados confirman que el escalado fue exitoso, logrando que todas las variables queden en una escala comparable, condición fundamental para aplicar técnicas como PCA y modelos basados en distancia.

**Configuración de PCA y selección del número de componentes**

Una vez normalizadas las variables, se aplicó **Análisis de Componentes Principales (PCA)** con el objetivo de reducir la dimensionalidad del vector de features.

- Dimensión original del vector: **62**
- Número de componentes seleccionados (k): **30**

El valor de *k* fue ajustado progresivamente para analizar la varianza explicada y encontrar un balance entre reducción dimensional y conservación de información.

Ejemplo del vector transformado (`features_pca`): DenseVector([0.4892, -1.1825, 1.2005, 1.7628, 0.3237, -0.0634, ...])

**Análisis de varianza explicada**

El análisis de varianza explicó cómo cada componente principal contribuye a la información total del dataset.

Resultados acumulados con **k = 30** componentes:

- Componente 10: 22.27% de varianza acumulada
- Componente 20: 39.22% de varianza acumulada
- Componente 30: **55.67% de varianza acumulada**

Este comportamiento evidencia que la varianza está distribuida de forma relativamente homogénea entre las componentes, lo cual es consistente con datasets que incluyen una alta proporción de variables categóricas codificadas.

Aunque no se alcanza el 80% de varianza explicada, el uso de 30 componentes permite una **reducción del 51.6% de la dimensionalidad**, manteniendo una cantidad significativa de información relevante.

**Pipeline completo de transformaciones**

Finalmente, se integraron todas las transformaciones en un **Pipeline completo**, garantizando reproducibilidad, trazabilidad y correcta aplicación del flujo de datos.

Orden de las transformaciones:
1. StandardScaler  
2. PCA  

Este orden es crítico, ya que PCA requiere que las variables estén previamente normalizadas para evitar sesgos en la identificación de componentes principales.

Como resultado, se generó un dataset final listo para modelado (`secop_ml_ready.parquet`), compuesto por:
- `features_pca`: vector reducido de características
- `label`: valor del contrato (`valor_del_contrato_num`)

Adicionalmente, el pipeline entrenado fue persistido para su reutilización en fases posteriores del proyecto, asegurando consistencia entre entrenamiento e inferencia.


## **Modelos de Regresión** 

### **Regresión Lineal**

Se construyo un modelo de **Regresión Lineal en Spark ML** con el objetivo de predecir el **valor del contrato** a partir de las *features* construidas en las fases anteriores (Feature Engineering + PCA). El dataset utilizado corresponde al archivo `secop_ml_ready.parquet`, el cual contiene las variables transformadas y listas para modelado.

**Estrategia de Train/Test Split**

Se definió una estrategia de partición **70% entrenamiento / 30% prueba**, utilizando una semilla fija para garantizar reproducibilidad.

**Resultados del split:**
- Train: **70,122 registros (70%)**
- Test: **29,878 registros (30%)**

Esta proporción es adecuada para datasets grandes (100,000 registros), permitiendo un entrenamiento robusto sin sacrificar capacidad de evaluación.

**Configuración del Modelo de Regresión Lineal**

Se configuró un modelo base de `LinearRegression` sin regularización, con los siguientes parámetros:

- `featuresCol`: `features`
- `labelCol`: `label`
- `maxIter`: 100
- `regParam`: 0.0
- `elasticNetParam`: 0.0

Este modelo sirve como **baseline**, permitiendo evaluar el comportamiento inicial antes de aplicar regularización en fases posteriores.

**Interpretación del R² del Modelo (Train)**

El modelo fue entrenado sobre el conjunto de entrenamiento, obteniendo:

**Métricas en Train:**
- **R² (train): 0.5648**
- **RMSE (train): $3,074,544,375**
 
El valor de R² indica que el modelo explica aproximadamente **56.5% de la variabilidad** del valor de los contratos en el conjunto de entrenamiento. Dado el alto nivel de heterogeneidad y presencia de outliers en los valores contractuales, este resultado es razonable para un modelo lineal base.

**Análisis de Calidad de Predicciones y Errores**

Se analizaron las predicciones sobre el conjunto de prueba, calculando:

- Error absoluto
- Error porcentual
- Identificación de las peores predicciones

**Hallazgos clave:**
1. Se observaron errores absolutos elevados en contratos de valores muy altos.
2. Los errores porcentuales superan el 100% en contratos pequeños, lo cual evidencia:
  - Alta dispersión en los valores
  - Dificultad del modelo lineal para capturar extremos
3. No se detectaron errores sistemáticos por duplicación o fallas de cálculo.

Estos resultados son coherentes con la naturaleza altamente asimétrica del valor de los contratos.

**Comparación Train vs Test (Overfitting)**

Se evaluó el modelo sobre el conjunto de prueba:

**Métricas en Test:**
- RMSE: **$3,048,622,156**
- MAE: **$587,881,077**
- R² (test): **0.5742**

**Comparación Train vs Test:**
- R² Train: **0.5648**
- R² Test: **0.5742**
- Diferencia absoluta: **0.0095**
 
No se evidencia **overfitting**, ya que el desempeño en test es incluso ligeramente superior al de train.  
El modelo generaliza correctamente dentro de las limitaciones propias de la regresión lineal.

**Análisis de Coeficientes del Modelo**

- Intercepto: **$289,073,028**
- Número de coeficientes: **30** (correspondientes a los componentes PCA)

El intercepto representa el valor base estimado cuando todas las *features* son cero. Los coeficientes reflejan la contribución relativa de cada componente principal (PCA), no de variables originales, por lo que su interpretación es **indirecta**.

**Análisis de Distribución de Residuos**

Se calculó el residuo como:

\[
residuo = label - prediction
\]

Se generó un histograma para evaluar su distribución.

**Resultado visual:**

![Distribución de Residuos](Imagenes/imagen2.png)

**Interpretación:**
- Los residuos están centrados alrededor de cero.
- Existe alta concentración cerca del origen, con colas largas, lo cual es consistente con:
  - Presencia de outliers
  - Variabilidad extrema en los valores contractuales
- No se observa sesgo sistemático severo.

**Feature Importance Aproximado (Componentes PCA)**

Se analizaron los coeficientes del modelo para identificar los componentes PCA más influyentes (por valor absoluto):

**Top 10 componentes más importantes:**
1. PC8      
2. PC9  
3. PC7  
4. PC3  
5. PC10  
6. PC1  
7. PC6  
8. PC4  
9. PC26  
10. PC16  

Estos componentes concentran mayor información relevante para la predicción. Al tratarse de PCA, no se interpretan directamente como variables originales, sino como combinaciones lineales de ellas, y el resultado confirma que solo una fracción de los componentes tiene impacto significativo.







