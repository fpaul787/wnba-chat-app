# Databricks notebook source
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


