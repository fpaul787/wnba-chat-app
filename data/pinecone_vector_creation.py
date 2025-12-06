# Databricks notebook source
catalog = "frantzpaul_tech"
schema = "wnba_chat"
table_name = "news_articles"

# COMMAND ----------

data = spark.read.table(f"{catalog}.{schema}.{table_name}")
display(data)
data.count()

# COMMAND ----------

# MAGIC %md
# MAGIC # Setting up Pinecone

# COMMAND ----------

def get_pinecone_api_key():
  api_key = ""
  return api_key

PINECONE_KEY = get_pinecone_api_key()

# COMMAND ----------


