# Databricks notebook source
# MAGIC %md
# MAGIC # About
# MAGIC This notebook imports the json data and cleanss up the data. It also saves the clean dataset as a delta table on Databricks.

# COMMAND ----------

# MAGIC %pip install pinecone

# COMMAND ----------

# MAGIC %restart_python

# COMMAND ----------

import json
catalog = "frantzpaul_tech"
schema = "wnba_chat"
table_name = "news_articles_bronze"

# COMMAND ----------

# MAGIC %md
# MAGIC # Import Data

# COMMAND ----------

path = "./wnba_news.json"
with open(path, "r") as f:
  data = json.load(f)

# create dataframe
df = spark.createDataFrame(data)
display(df)

# save to table
spark.createDataFrame(data).write.mode("overwrite").saveAsTable(f"{catalog}.{schema}.{table_name}")

# COMMAND ----------

df = spark.read.table(f"{catalog}.{schema}.{table_name}")
display(df)

# COMMAND ----------

# MAGIC %md
# MAGIC # Clean Data
# MAGIC
# MAGIC - Drop row with empty text column
# MAGIC - Remove newlines in text column

# COMMAND ----------

# drop row with empty text column
df = df.filter(df.text != "")
display(df)

# COMMAND ----------

from pyspark.sql.functions import regexp_replace
# remove newlines in text column
clean_df = df.withColumn("text_clean", regexp_replace("text", "\n", " "))
display(clean_df)

# COMMAND ----------

# MAGIC %md
# MAGIC # Save to Delta Table

# COMMAND ----------

catalog = "frantzpaul_tech"
schema = "wnba_chat"
table_name = "news_articles_clean"

# COMMAND ----------

spark.sql(f"create database if not exists {catalog}.{schema}")

# COMMAND ----------

clean_df = clean_df.drop("text")
clean_df.write.mode("overwrite").saveAsTable(f"{catalog}.{schema}.{table_name}")

# COMMAND ----------

# MAGIC %md
# MAGIC # Preprocess Data

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql import types as T

# Simple Chunking
@udf(returnType=T.ArrayType(T.StringType()))
def chunk_text(text, chunk_size=1000):
    if text is None:
        return []
    
    words = text.split()
    chunks = [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

# COMMAND ----------

from pyspark.sql.types import StringType
# Apply UDF
chunked_df = clean_df.withColumn(
    "chunked_text",
    chunk_text(F.col("text_clean"))
)
display(chunked_df)

# COMMAND ----------

# MAGIC %md
# MAGIC # Save Data to Delta Table

# COMMAND ----------

chunked_df.write.mode("overwrite").saveAsTable(f"{catalog}.{schema}.news_articles_chunked")
