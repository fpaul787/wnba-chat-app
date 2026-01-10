# Databricks notebook source
# MAGIC %md
# MAGIC # About
# MAGIC This notebook imports the json data and cleans up the data. Afterwards, it preprocesses the data to chunk our data into chunks. It also saves the clean dataset as a delta table on Databricks.

# COMMAND ----------

# MAGIC %md
# MAGIC # Define Variables

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

spark.sql(f"create database if not exists {catalog}.{schema}")

# COMMAND ----------

table_name = "news_articles_clean"
clean_df = clean_df.drop("text")
clean_df.write.mode("overwrite").saveAsTable(f"{catalog}.{schema}.{table_name}")

# COMMAND ----------

# MAGIC %md
# MAGIC # Preprocess Data

# COMMAND ----------

from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType, StringType

CHUNK_SIZE = 1000

@udf(returnType=ArrayType(StringType()))
def chunk_text(text0):
    if text is None:
        return []
    
    words = text.split()
    chunks = [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), CHUNK_SIZE)]
    return chunks

# COMMAND ----------

# Apply UDF
chunked_df = clean_df.withColumn(
    "chunked_text",
    chunk_text(F.col("text_clean"))
)

# COMMAND ----------

from pyspark.sql.functions import explode, col, monotonically_increasing_id

chunks_df = (
    chunked_df
    .withColumn("chunk_text", explode(col("chunked_text")))
    .withColumn("chunk_id", monotonically_increasing_id())
    .select(
        "chunk_id",
        "chunk_text",
        "title",
        "source",
        "url",
        "date"
    )
)

# COMMAND ----------

display(chunks_df)

# COMMAND ----------

# MAGIC %md
# MAGIC # Save Data to Delta Table

# COMMAND ----------

chunks_df.write.mode("overwrite").saveAsTable(f"{catalog}.{schema}.news_articles_chunked")
