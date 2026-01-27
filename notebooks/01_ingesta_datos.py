# %% [markdown]
# # Notebook 01: Ingesta de Datos
#
# **Objetivo**: Descargar y cargar datos de contratos públicos desde la API de Datos Abiertos Colombia (SECOP II).
#
# **Dataset**: SECOP II - Contratos Electrónicos
#
# **Fuente**: https://www.datos.gov.co/Gastos-Gubernamentales/SECOP-II-Contratos-Electr-nicos/jbjy-vk9h
#
# ## Actividades:
# 1. Configurar SparkSession con conexión al cluster
# 2. Descargar dataset usando API Socrata
# 3. Explorar esquema inicial
# 4. Guardar en formato Parquet optimizado

# %%
# Importar librerías
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, year, month
import os

# %% [markdown]
# ## RETO 1: Configurar SparkSession
#
# **Objetivo**: Crear una sesión de Spark conectada al cluster.
#
# **Parámetros clave**:
# - `appName`: Nombre descriptivo de tu aplicación
# - `master`: URL del Spark Master (spark://spark-master:7077)
# - `spark.executor.memory`: Memoria por executor (ej: "2g")
# - `spark.driver.memory`: Memoria del driver (ej: "1g")
#
# **Pregunta**: ¿Qué pasaría si asignas más memoria de la disponible?

# %%
# TODO: Configura tu SparkSession
# Pista: Usa SparkSession.builder con los métodos .appName(), .master(), .config(), .getOrCreate()

spark = SparkSession.builder \
    .appName("SECOP_Ingesta") \
    .master("spark://spark-master:7077") \
    .config("spark.executor.memory", "2g") \
    .config("spark.driver.memory", "1g") \
    .getOrCreate()

print(f"Spark Version: {spark.version}")
print(f"Spark Master: {spark.sparkContext.master}")

# %% [markdown]
# ## RETO 2: Descargar Datos desde API Abierta
#
# **Objetivo**: Obtener datos de la API de Datos Abiertos Colombia (Socrata).
#
# **Conceptos**:
# - Las APIs REST devuelven datos en formato JSON
# - El parámetro `$limit` controla cuántos registros descargar
# - Dataset ID: `jbjy-vk9h`
#
# **Instrucciones**:
# 1. Construye la URL de la API con el endpoint correcto
# 2. Usa `requests.get()` para descargar los datos
# 3. Guarda el JSON en disco
#
# **Pregunta**: ¿Por qué limitamos a 100,000 registros?
# ¿Qué consideraciones tendrías en producción?

# %%
import requests
import json

# TODO: Construye la URL de la API
# Formato: https://www.datos.gov.co/resource/{dataset_id}.json?$limit={cantidad}
api_url = "https://www.datos.gov.co/resource/jbjy-vk9h.json?$limit=100000"

# TODO: Descarga los datos
# Pista: response = requests.get(api_url)
#        data = response.json()

# response = ...
# data = ...

# print(f"Registros descargados: {len(data)}")

# %%
# TODO: Guarda los datos JSON en disco
# Pista: Usa json.dump() con encoding utf-8

json_path = "/opt/spark-data/raw/secop_contratos.json"
os.makedirs(os.path.dirname(json_path), exist_ok=True)

# with open(json_path, 'w', encoding='utf-8') as f:
#     json.dump(data, f, ensure_ascii=False, indent=2)
#
# print(f"Datos guardados en: {json_path}")

# %% [markdown]
# ## RETO 3: Cargar datos en Spark y explorar esquema
#
# **Objetivo**: Leer el JSON con Spark y entender la estructura del dataset.
#
# **Instrucciones**:
# 1. Usa `spark.read.json()` para cargar los datos
# 2. Explora el esquema con `.printSchema()`
# 3. Cuenta registros y columnas
# 4. Muestra las primeras filas

# %%
# TODO: Lee los datos JSON con Spark
# df_raw = spark.read.json(json_path)

# TODO: Explora el dataset
# print(f"Total de registros: {df_raw.count()}")
# print(f"Total de columnas: {len(df_raw.columns)}")

# %%
# TODO: Muestra el esquema del dataset
# df_raw.printSchema()

# %%
# TODO: Muestra las primeras 5 filas
# df_raw.show(5, truncate=False)

# %%
# TODO: Lista todas las columnas disponibles
# for col_name in df_raw.columns:
#     print(f"  - {col_name}")

# %% [markdown]
# ## RETO 4: Seleccionar Columnas Clave
#
# **Objetivo**: Identificar y seleccionar las columnas relevantes para análisis de ML.
#
# **Instrucciones**:
# 1. Revisa las columnas disponibles del dataset
# 2. Selecciona las que consideres útiles para predecir valor de contratos
# 3. Verifica cuáles existen realmente en el dataset
#
# **Pregunta**: ¿Por qué es importante seleccionar columnas en lugar de usar todas?
# ¿Qué problemas podrían surgir con demasiadas columnas?

# %%
# TODO: Define tu lista de columnas clave
# Pista: Piensa en qué variables podrían influir en el valor de un contrato
columnas_clave = [
    # TODO: Agrega las columnas que consideres relevantes
    # Ejemplos posibles: "referencia_del_contrato", "departamento",
    # "tipo_de_contrato", "valor_del_contrato", "fecha_de_firma",
    # "plazo_de_ejec_del_contrato", "nombre_del_proveedor", "estado_contrato"
]

# TODO: Verifica cuáles columnas existen en el dataset
# columnas_disponibles = [c for c in columnas_clave if c in df_raw.columns]
# print(f"Columnas seleccionadas: {len(columnas_disponibles)} de {len(columnas_clave)}")

# TODO: Filtra el DataFrame con las columnas disponibles
# df_clean = df_raw.select(*columnas_disponibles)

# %% [markdown]
# ## RETO 5: Guardar en formato Parquet
#
# **Objetivo**: Convertir los datos a formato Parquet optimizado.
#
# **Pregunta de reflexión**:
# - ¿Qué ventajas tiene Parquet sobre CSV o JSON?
# - ¿Qué es la compresión columnar?
# - ¿Por qué Spark trabaja más eficientemente con Parquet?

# %%
# TODO: Guarda el DataFrame limpio en formato Parquet
output_path = "/opt/spark-data/raw/secop_contratos.parquet"

# df_clean.write \
#     .mode("overwrite") \
#     .parquet(output_path)
#
# print(f"Datos guardados en: {output_path}")

# %%
# TODO: Verifica que el archivo se guardó correctamente
# df_verificacion = spark.read.parquet(output_path)
# print(f"Registros en Parquet: {df_verificacion.count():,}")
# print(f"Columnas en Parquet: {len(df_verificacion.columns)}")

# %% [markdown]
# ## Preguntas de Reflexión
#
# Responde en un comentario:
#
# 1. **¿Qué diferencia hay entre `spark.read.json()` y `spark.read.csv()`?**
#
# 2. **¿Por qué usamos `.mode("overwrite")` al guardar?**
#
# 3. **¿Qué pasaría si la API devuelve un error? ¿Cómo manejarías eso?**
#
# 4. **¿Cuándo preferirías descargar el CSV completo vs usar la API?**

# %%
# TODO: Escribe tus respuestas aquí como comentarios
# 1. Diferencia JSON vs CSV:
# 2. mode("overwrite"):
# 3. Manejo de errores de API:
# 4. CSV completo vs API:

# %%
# Resumen final
print("\n" + "="*60)
print("RESUMEN DE INGESTA")
print("="*60)
print("Verifica que hayas completado:")
print("  [ ] SparkSession configurada correctamente")
print("  [ ] Datos descargados desde la API")
print("  [ ] Esquema explorado y entendido")
print("  [ ] Columnas clave seleccionadas")
print("  [ ] Datos guardados en Parquet")
print("="*60)

# %%
spark.stop()
print("SparkSession finalizada")
