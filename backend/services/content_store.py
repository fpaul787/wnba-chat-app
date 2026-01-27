from typing import Dict, List
from databricks_service import DatabricksService
from models import Content

class ContentStoreService:
    def __init__(self):
        self.databricks_service = DatabricksService()
        self.table_name = "frantzpaul_tech.wnba_chat.news_articles_chunked"

    def get_content_by_ids(self, ids: List[str]) -> List[Content]:
        id_list_str = ",".join([f"'{id_}'" for id_ in ids])
        query = f"SELECT chunk_id, chunk_text FROM {self.table_name} WHERE chunk_id IN ({id_list_str})"
        results = self.databricks_service.execute_query(query)

        content = []
        for row in results:
            content.append(Content(id=row[0], text=row[1]))
        return content