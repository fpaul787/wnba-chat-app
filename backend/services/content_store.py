from typing import List
from databricks_service import DatabricksService
from models import Content
from contextlib import contextmanager

class ContentStoreService:
    """
    Service to interact with the content store that fetches text chunks.
    """
    def __init__(self):
        

    @contextmanager
    def _databricks_service(self):
        """
        Context manager to handle Databricks service connection.
        """
        service = DatabricksService()
        try:
            yield service
        finally:
            service.close_connection()

    def get_content_by_ids(self, ids: List[str]) -> List[Content]:
        """
        Fetch content chunks based on the given IDs.
        """
        id_list_str = ",".join([f"'{id_}'" for id_ in ids])
        table_name = "frantzpaul_tech.wnba_chat.news_articles_chunked"
        query = f"SELECT chunk_id, chunk_text FROM {table_name} WHERE chunk_id IN ({id_list_str})"

        with self._databricks_service() as databricks_service:
            results = databricks_service.execute_query(query)

        content = []
        for row in results:
            content.append(Content(id=row[0], text=row[1]))
        return content