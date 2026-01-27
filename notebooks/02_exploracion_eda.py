# %% [markdown]
# # Notebook 02: Análisis Exploratorio de Datos (EDA)
#
# **Objetivo**: Entender la distribución de las variables, identificar valores nulos y outliers.
#
# ## Actividades:
# 1. Cargar datos desde Parquet
# 2. Calcular estadísticas descriptivas
# 3. Analizar distribución por departamento
# 4. Identificar valores faltantes
# 5. Detectar outliers en valores de contratos

# %%
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, count, sum as spark_sum, avg, min as spark_min,
    max as spark_max, stddev, isnan, when, isnull, desc
)
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# %%
spark = SparkSession.builder \
    .appName("SECOP_EDA") \
    .master("spark://spark-master:7077") \
    .config("spark.executor.memory", "2g") \
    .getOrCreate()

print(f"Spark Version: {spark.version}")

# %%
# Cargar datos desde Parquet
parquet_path = "/opt/spark-data/raw/secop_contratos.parquet"
print(f"Cargando datos desde: {parquet_path}")

df = spark.read.parquet(parquet_path)
print(f"Registros cargados: {df.count():,}")
print(f"Columnas: {len(df.columns)}")

# %%
# Mostrar esquema
print("\n=== ESQUEMA DEL DATASET ===")
df.printSchema()

# %%
# Primeras filas
print("\n=== PRIMERAS 10 FILAS ===")
df.show(10, truncate=True)

# %% [markdown]
# ## RETO 1: Estadísticas Descriptivas
#
# **Objetivo**: Calcular y analizar las estadísticas descriptivas del dataset.
#
# **Instrucciones**:
# 1. Usa `.describe()` para obtener estadísticas generales
# 2. Identifica columnas numéricas vs categóricas
# 3. Analiza los rangos de valores
#
# **Pregunta**: ¿Qué te dice la diferencia entre mean y median sobre la distribución?

# %%
# TODO: Obtén estadísticas descriptivas generales
# df.describe().show()

# TODO: Identifica las columnas numéricas y categóricas
# Pista: Revisa el esquema (printSchema) y clasifica las columnas
# columnas_numericas = [...]
# columnas_categoricas = [...]

# %% [markdown]
# ## RETO 2: Análisis de Valores Nulos
#
# **Objetivo**: Identificar y cuantificar valores faltantes en cada columna.
#
# **Instrucciones**:
# 1. Cuenta los valores nulos por columna
# 2. Calcula el porcentaje de nulos
# 3. Decide qué hacer con columnas que tienen >50% nulos
#
# **Pregunta**: ¿Cuándo es mejor eliminar filas vs imputar valores?

# %%
# TODO: Cuenta nulos por cada columna
# Pista: Usa count(when(isnull(c) | isnan(c), c)) para cada columna

# null_counts = df.select([
#     count(when(isnull(c) | isnan(c), c)).alias(c)
#     for c in df.columns
# ])

# TODO: Convierte a pandas para mejor visualización
# null_df = null_counts.toPandas().T
# null_df.columns = ['null_count']
# null_df['null_percentage'] = (null_df['null_count'] / df.count()) * 100
# null_df = null_df.sort_values('null_count', ascending=False)

# TODO: Muestra solo columnas con nulos
# print(null_df[null_df['null_count'] > 0])

# TODO: Responde:
# ¿Qué columnas tienen más de 50% nulos?
# ¿Qué harías con ellas?
# Respuesta:

# %% [markdown]
# ## RETO 3: Análisis de la Variable Objetivo
#
# **Objetivo**: Explorar la distribución del valor de contratos.
#
# **Instrucciones**:
# 1. Identifica la columna de valor del contrato
# 2. Conviértela a tipo numérico (double)
# 3. Calcula min, max, promedio y desviación estándar
# 4. Analiza la distribución por rangos
#
# **Pregunta**: ¿La distribución del valor es normal o sesgada? ¿Cómo lo verificas?

# %%
# TODO: Identifica columnas de valor
# Pista: Busca columnas con 'valor' o 'precio' en el nombre
# valor_cols = [c for c in df.columns if 'valor' in c.lower() or 'precio' in c.lower()]
# print(f"Columnas de valor encontradas: {valor_cols}")

# TODO: Convierte a numérico y calcula estadísticas
# valor_col = valor_cols[0]  # Usa la primera columna encontrada
# df = df.withColumn(valor_col + "_num", col(valor_col).cast("double"))
#
# df.select(
#     spark_min(col(valor_col + "_num")).alias("Min"),
#     spark_max(col(valor_col + "_num")).alias("Max"),
#     avg(col(valor_col + "_num")).alias("Promedio"),
#     stddev(col(valor_col + "_num")).alias("Desv_Std")
# ).show()

# TODO: Distribución por rangos de valor
# Pista: Usa count(when(condicion, True)) para contar por rangos
# Rangos sugeridos: < 10M, 10M-100M, 100M-1B, > 1B

# %% [markdown]
# ## RETO 4: Análisis por Departamento
#
# **Objetivo**: Entender la distribución geográfica de los contratos.
#
# **Instrucciones**:
# 1. Agrupa por departamento
# 2. Cuenta contratos y suma valores por departamento
# 3. Muestra el Top 10
# 4. Crea una visualización con matplotlib
#
# **Pregunta**: ¿Qué departamentos concentran más contratos? ¿Coincide con mayor valor total?

# %%
# TODO: Encuentra la columna de departamento
# dept_cols = [c for c in df.columns if 'departamento' in c.lower()]

# TODO: Agrupa por departamento, cuenta contratos y suma valores
# df_dept = df.groupBy(dept_col) \
#     .agg(
#         count("*").alias("num_contratos"),
#         spark_sum(col(valor_col + "_num")).alias("valor_total")
#     ) \
#     .orderBy(desc("num_contratos")) \
#     .limit(10)
#
# df_dept.show(truncate=False)

# TODO: Crea un gráfico de barras horizontales
# Pista: Convierte a pandas con .toPandas() y usa plt.barh()
# Guarda el gráfico en: /opt/spark-data/processed/eda_departamentos.png

# %% [markdown]
# ## RETO 5: Análisis por Tipo de Contrato y Estado
#
# **Objetivo**: Explorar la distribución categórica del dataset.
#
# **Instrucciones**:
# 1. Agrupa por tipo de contrato y cuenta
# 2. Agrupa por estado del contrato y cuenta
# 3. (Bonus) Analiza los Top 10 proveedores
#
# **Pregunta**: ¿Qué tipo de contrato es más común?
# ¿Qué porcentaje de contratos están en estado "activo"?

# %%
# TODO: Análisis por Tipo de Contrato
# tipo_cols = [c for c in df.columns if 'tipo' in c.lower() and 'contrato' in c.lower()]
# if tipo_cols:
#     tipo_col = tipo_cols[0]
#     df.groupBy(tipo_col).agg(count("*").alias("num_contratos")) \
#         .orderBy(desc("num_contratos")).limit(10).show(truncate=False)

# %%
# TODO: Análisis por Estado del Contrato
# estado_cols = [c for c in df.columns if 'estado' in c.lower()]
# if estado_cols:
#     estado_col = estado_cols[0]
#     df.groupBy(estado_col).agg(count("*").alias("num_contratos")) \
#         .orderBy(desc("num_contratos")).show(truncate=False)

# %%
# TODO: (Bonus) Top 10 Proveedores
# proveedor_cols = [c for c in df.columns if 'proveedor' in c.lower()]
# Agrupa por proveedor, cuenta contratos y suma valores

# %% [markdown]
# ## RETO 6: Detección de Outliers
#
# **Objetivo**: Identificar valores atípicos en el valor de contratos.
#
# **Método IQR (Interquartile Range)**:
# - Q1 = Percentil 25
# - Q3 = Percentil 75
# - IQR = Q3 - Q1
# - Outlier si: valor < Q1 - 1.5*IQR  o  valor > Q3 + 1.5*IQR
#
# **Instrucciones**:
# 1. Calcula percentiles con `.approxQuantile()`
# 2. Aplica el método IQR
# 3. Cuenta cuántos outliers hay
# 4. Decide si eliminarlos o transformarlos
#
# **Pregunta**: ¿Siempre debes eliminar outliers? ¿Cuándo podrían ser datos válidos?

# %%
# TODO: Calcula percentiles
# Pista: df.approxQuantile("columna_num", [0.25, 0.50, 0.75, 0.95, 0.99], 0.01)

# TODO: Aplica método IQR
# q1, q3 = percentiles[0], percentiles[2]
# iqr = q3 - q1
# lower_bound = q1 - 1.5 * iqr
# upper_bound = q3 + 1.5 * iqr

# TODO: Cuenta outliers
# num_outliers = df.filter(
#     (col(valor_col + "_num") < lower_bound) |
#     (col(valor_col + "_num") > upper_bound)
# ).count()

# print(f"Rango normal: ${lower_bound:,.2f} - ${upper_bound:,.2f}")
# print(f"Outliers: {num_outliers:,} ({(num_outliers/df.count())*100:.2f}%)")

# TODO: Responde:
# ¿Eliminarías estos outliers? ¿Por qué?
# Respuesta:

# %% [markdown]
# ## RETO BONUS: Análisis Temporal
#
# **Objetivo**: Explorar tendencias temporales en los contratos.
#
# **Instrucciones**:
# 1. Encuentra una columna de fecha
# 2. Convierte a tipo fecha con `to_date()`
# 3. Extrae año y mes
# 4. Agrupa contratos por año
#
# **Pregunta**: ¿Hay tendencias crecientes o decrecientes en la contratación?

# %%
# TODO: Análisis temporal
# fecha_cols = [c for c in df.columns if 'fecha' in c.lower()]
# if fecha_cols:
#     fecha_col = fecha_cols[0]
#     df = df.withColumn(fecha_col + "_parsed", to_date(col(fecha_col)))
#     df = df.withColumn("anio", year(col(fecha_col + "_parsed")))
#     df = df.withColumn("mes", month(col(fecha_col + "_parsed")))
#
#     df.groupBy("anio").agg(count("*").alias("num_contratos")) \
#         .orderBy("anio").show()

# %% [markdown]
# ## Preguntas de Reflexión
#
# 1. **¿Qué columna sería la mejor variable objetivo para un modelo de ML?**
#    Respuesta:
#
# 2. **¿Qué columnas eliminarías del análisis y por qué?**
#    Respuesta:
#
# 3. **¿Cómo manejarías los outliers detectados?**
#    Respuesta:
#
# 4. **¿El dataset está suficientemente limpio para ML o necesita más preprocesamiento?**
#    Respuesta:

# %%
# TODO: Escribe tus respuestas arriba

# %%
# Guardar dataset explorado para próximos notebooks
output_path = "/opt/spark-data/processed/secop_eda.parquet"
# TODO: Guarda el DataFrame con las transformaciones realizadas
# df.write.mode("overwrite").parquet(output_path)
# print(f"Dataset guardado en: {output_path}")

# %%
print("\n" + "="*60)
print("RESUMEN DEL ANÁLISIS EXPLORATORIO")
print("="*60)
print("Verifica que hayas completado:")
print("  [ ] Estadísticas descriptivas calculadas")
print("  [ ] Valores nulos identificados")
print("  [ ] Variable objetivo analizada")
print("  [ ] Distribución por departamento explorada")
print("  [ ] Outliers detectados")
print("  [ ] Dataset guardado para siguiente notebook")
print("="*60)

# %%
spark.stop()
print("SparkSession finalizada")
