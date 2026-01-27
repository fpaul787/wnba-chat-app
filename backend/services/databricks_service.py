from databricks import sql
import os

class DatabricksService:
    """
    Service to connect and query Databricks SQL warehouse.
    """
    def __init__(self):
        server_hostname = os.getenv("DATABRICKS_SERVER_HOSTNAME")
        http_path = os.getenv("DATABRICKS_HTTP_PATH")
        access_token = os.getenv("DATABRICKS_ACCESS_TOKEN")
        
        try:
            self.connection = sql.connect(
                server_hostname=server_hostname,
                http_path=http_path,
                access_token=access_token
            )
        except Exception as e:
            raise Exception(f"Failed to establish connection to Databricks SQL warehouse: {e}")
        
        self.cursor = self.connection.cursor()
    
    def execute_query(self, query: str):
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