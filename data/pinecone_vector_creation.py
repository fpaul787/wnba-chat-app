# Databricks notebook source
# MAGIC %pip install pinecone

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

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

# MAGIC %md
# MAGIC # Setting up  Pinecone Index

# COMMAND ----------

from pinecone import Pinecone

pc = Pinecone(
    api_key=PINECONE_KEY
)

# COMMAND ----------

index_name = "wnba_chat_pinecone_rag"
from pinecone import ServerlessSpec

if not pc.has_index(index_name):
  pc.create_index(
      index_name, 
      dimension=1536,
      metric="cosine",
       # parameters for the free tier index
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
  )

# Initialize index client
index = pc.Index(name=index_name)

# View index stats
index.describe_index_stats()
