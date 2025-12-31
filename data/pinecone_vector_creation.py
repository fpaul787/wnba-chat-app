# Databricks notebook source
# MAGIC %pip install pinecone openai

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

catalog = "frantzpaul_tech"
schema = "wnba_chat"
table_name = "news_articles_chunked"

# COMMAND ----------

data = spark.read.table(f"{catalog}.{schema}.{table_name}")
display(data)
data.count()

# COMMAND ----------

# MAGIC %md
# MAGIC # Setting up Pinecone

# COMMAND ----------

def get_pinecone_api_key():
  api_key = dbutils.secrets.get(scope="wnba_chat_app", key="pinecone")
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

index_name = "wnba-chat-pinecone-rag"
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

# COMMAND ----------

from openai import OpenAI
client = OpenAI()

response = client.embeddings.create(
  model="text-embedding-ada-002",
  input="Hello world"
)

# COMMAND ----------

def create_embeddings(df):
    vectors_to_upsert = []

    for idx, row in df.iterrows():
        for chunk_idx, chunk in enumerate(row['chunked_text']):
            vector_id = f"{idx}_{chunk_idx}"

            # Generate embedding
            embedding = None

            metadata = {
                "date": row['date'],
                "source": row['source'],
                "title": row['title']
            }

            vectors_to_upsert.append((vector_id, embedding, metadata))

    if vectors_to_upsert:
        index.upsert(vectors=vectors_to_upsert)

    return vectors_to_upsert
