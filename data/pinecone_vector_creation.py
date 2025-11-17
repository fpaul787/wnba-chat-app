# Databricks notebook source
catalog = "frantzpaul_tech"
schema = "wnba_chat"
table_name = "new_articles"

# COMMAND ----------

data = spark.read.table(f"{catalog}.{schema}.{table_name}")
display(data)
data.count()
