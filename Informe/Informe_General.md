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

### 

