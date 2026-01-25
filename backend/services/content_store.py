from typing import Dict, List
from databricks_service import DatabricksService

class ContentStoreService:
    def __init__(self):
        self.databricks_service = DatabricksService()


    def get_content_by_ids(self, ids: List[str]) -> List[Dict]:
        id_list_str = ",".join([f"'{id_}'" for id_ in ids])
        query = f"SELECT id, text_chunk FROM your_table WHERE id IN ({id_list_str})"
        results = self.databricks_service.__execute_query(query)
        return [{"id": row[0], "text_chunk": row[1]} for row in results]