# Databricks notebook source
# MAGIC %pip install pinecone

# COMMAND ----------

# MAGIC %restart_python

# COMMAND ----------

import json
catalog = "frantzpaul_tech"
schema = "wnba_rag"

# COMMAND ----------

# MAGIC %md
# MAGIC # Import Data

# COMMAND ----------

path = "./wnba_news.json"
with open(path, "r") as f:
  data = json.load(f)

# COMMAND ----------

# create dataframe
df = spark.createDataFrame(data)
display(df)

# save to table
# spark.createDataFrame(data).write.mode("overwrite").saveAsTable("wnba_news")

# COMMAND ----------

# MAGIC %md
# MAGIC # Clean Data
# MAGIC
# MAGIC - Remove newlines in text column

# COMMAND ----------

from pyspark.sql.functions import regexp_replace
# remove newlines in text column
df = df.withColumn("text", regexp_replace("text", "\n", " "))
display(df)

# COMMAND ----------


