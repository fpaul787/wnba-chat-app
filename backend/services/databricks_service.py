from databricks import sql
import os

class DatabricksService:
    """
    Service to connect and query Databricks SQL warehouse.
    """
    def __init__(self):
        self.connection = sql.connect(
            server_hostname=os.getenv("DATABRICKS_SERVER_HOSTNAME"),
            http_path=os.getenv("DATABRICKS_HTTP_PATH"),
            access_token=os.getenv("DATABRICKS_ACCESS_TOKEN")
        )
        self.cursor = self.connection.cursor()
    
    def __execute_query(self, query: str):
        """
        Execute a SQL query against the Databricks SQL warehouse.
        """
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results
    
    def close_connection(self):
        """
        Close the database connection.
        """
        self.cursor.close()
        self.connection.close()