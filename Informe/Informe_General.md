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




