# **Análisis de la Dinámica Contractual del Estado Colombiano usando Datos Abiertos de SECOP II**

**Desarrollado por:** Diego Alejandro Gomez Cortes

### **Introducción**

SECOP II (Sistema Electrónico para la Contratación Pública) es la principal plataforma de transparencia y seguimiento de la contratación estatal en Colombia. A través de esta plataforma se registran los contratos públicos de entidades nacionales y territoriales, permitiendo el acceso abierto a información clave como valores contratados, tipos de contrato, entidades, proveedores y estados contractuales. El volumen, diversidad y naturaleza pública de estos datos convierten a SECOP II en una fuente estratégica para el análisis económico, administrativo y de política pública.

El análisis de los datos de SECOP II permite identificar patrones de contratación, concentración de recursos, comportamientos por territorio y modalidades contractuales, así como posibles riesgos o ineficiencias en el uso de los recursos públicos. Dado que la contratación estatal representa una porción significativa del gasto público, su estudio sistemático aporta valor tanto para la toma de decisiones institucionales como para el control ciudadano y el desarrollo de modelos analíticos y predictivos.

Desde una perspectiva de datos, SECOP II plantea retos propios de los entornos Big Data: grandes volúmenes de información, esquemas complejos, datos heterogéneos y actualizaciones constantes. Por esta razón, el uso de herramientas distribuidas como Apache Spark, Visual Studio Code, Java, JupyterLab y Docker resultan fundamentales para procesar, explorar y preparar estos datos de forma eficiente y escalable.

### **Objetivo del Análisis**

El objetivo de este trabajo es comprender el comportamiento de la contratación pública registrada en SECOP II, explorando sus principales características estructurales y económicas mediante técnicas de análisis de datos a gran escala. A partir de esta exploración, se busca sentar las bases para la construcción de análisis avanzados y modelos de Machine Learning que permitan extraer conocimiento útil sobre la dinámica contractual del Estado colombiano.

### **Cargue de los Datos**

En una primera fase, se tuvo en cuenta la construccion de entornos de trabajos adecuados para el tratamiento de los datos del Secop para asi mismos tratar con diferentes entornos que nos ayudaran asu analisis y gracias a esto se realizó la ingesta de datos directamente desde la API de Datos Abiertos Colombia, seleccionando los contratos más recientes que cuentan con fecha de firma registrada. Posteriormente, la información fue cargada en un entorno distribuido con Apache Spark, donde se exploró su esquema y se normalizaron los nombres de las columnas para garantizar consistencia técnica.

Asi mismo se seleccionaron las variables clave relevantes para el análisis y modelado, y el conjunto de datos resultante fue almacenado en formato Parquet optimizado. Este proceso permitió disponer de una base de datos estructurada, eficiente y lista para análisis exploratorio y etapas posteriores de Machine Learning distribuido.

Query: **01_ingesta_resuelto.ipynb**

### **Análisis Exploratorio de Datos (EDA)**

En esta fase se realizó un análisis exploratorio sobre los contratos electrónicos del SECOP II con el objetivo de comprender la estructura del dataset, la distribución de los valores contractuales y los patrones principales por territorio, tipo y estado del contrato. Este análisis permite validar la calidad de los datos y preparar el terreno para la construcción de variables y modelos de Machine Learning distribuido.

Inicialmente se validó el **periodo temporal efectivo** de los datos analizados a partir de la columna `fecha_de_firma`. Los resultados muestran que los contratos incluidos corresponden principalmente al último trimestre de 2025 y los primeros registros de 2026, confirmando que el dataset representa contratos efectivamente firmados y no simples registros administrativos pendientes.

Posteriormente se calcularon **estadísticas descriptivas generales** y específicas para la variable objetivo `valor_del_contrato`. Se identificó una distribución altamente asimétrica, donde la mayoría de los contratos se concentran en rangos bajos y medios, mientras que una fracción menor representa contratos de muy alto valor. El análisis por rangos permitió cuantificar esta concentración y evidenciar la existencia de contratos de alto impacto presupuestal.

En el análisis territorial se observó una fuerte concentración de contratos en grandes centros administrativos como Bogotá, Antioquia y Valle del Cauca, tanto en número de contratos como en valor total adjudicado. Este comportamiento refleja la centralización de la contratación pública y justifica el uso de análisis regionales más detallados en fases posteriores.

![Distribución de contratos por departamento](../Imagenes/Imagen1.png)

Tambien se exploró la distribución por **tipo de contrato**, donde la modalidad de **Prestación de Servicios** domina ampliamente el volumen de contratos, seguida por modalidades administrativas específicas y contratos de compra y suministro. En cuanto al **estado del contrato**, la mayoría se encuentran en ejecución o han sufrido modificaciones, lo cual es consistente con procesos contractuales activos y dinámicos.

Aparte se aplicó el método **IQR (Interquartile Range)** para la detección de outliers en el valor del contrato, excluyendo previamente valores iguales o menores a cero. El análisis identificó aproximadamente un 15% de contratos como valores atípicos superiores, los cuales no representan errores, sino contratos de gran escala con alto impacto presupuestal. Este resultado confirma la necesidad de aplicar transformaciones y técnicas de escalamiento en las siguientes fases del pipeline de Machine Learning.

El estudio temporal por año y mes evidenció picos claros de contratación hacia finales de 2025, con una disminución marcada al inicio de 2026, lo cual coincide con ciclos fiscales y administrativos propios de la contratación pública en Colombia.




