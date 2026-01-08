# Databricks notebook source
# MAGIC %pip install pinecone openai

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

catalog = "frantzpaul_tech"
schema = "wnba_chat"
table_name = "news_articles_chunked"

# COMMAND ----------

data_df = spark.read.table(f"{catalog}.{schema}.{table_name}")
display(data_df)

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

client = OpenAI(
    api_key=dbutils.secrets.get(scope="wnba_chat_app", key="openai")
)

def embed_batch(texts):
  response = client.embeddings.create(
    model="text-embedding-ada-002",
    input=texts
  )
  return [r.embedding for r in response.data]

# COMMAND ----------

BATCH_SIZE = 200

pdf = data_df.toPandas()

for i in range(0, len(pdf), BATCH_SIZE):
    batch = pdf.iloc[i:i+BATCH_SIZE]

    embeddings = embed_batch(batch["chunk_text"].tolist())

    vectors = []
    for j, emb in enumerate(embeddings):
        row = batch.iloc[j]
        vectors.append((
            f"{row.chunk_id}",   # vector ID
            emb,
            {
                "title": row.title,
                "source": row.source,
                "url": row.url,
                "date": row.date
            }
        ))

    index.upsert(vectors=vectors)

