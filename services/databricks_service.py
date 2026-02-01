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
        
        Args:
            query: SQL query string to execute
            
        Returns:
            List of result rows or empty list if no results
        """
        # Input validation
        if not query or not isinstance(query, str):
            raise ValueError("Query must be a non-empty string")
        
        query = query.strip()
        if not query:
            raise ValueError("Query cannot be empty or only whitespace")
        
        try:
            # Check if connection is still valid
            if not self.connection or not self.cursor:
                raise ConnectionError("Database connection not available")
            
            # Execute the query
            self.cursor.execute(query)
            
            try:
                results = self.cursor.fetchall()
                return results if results is not None else []
            except Exception as fetch_error:
                raise RuntimeError(f"Failed to fetch query results: {fetch_error}")
            
        except Exception as e:
            # Handle unexpected errors
            raise RuntimeError(f"Unexpected error executing query: {e}")
    
    def close_connection(self):
        """
        Close the database connection safely.
        """
        try:
            if hasattr(self, 'cursor') and self.cursor:
                self.cursor.close()
        except Exception as e:
            print(f"Error closing cursor: {e}")
        
        try:
            if hasattr(self, 'connection') and self.connection:
                self.connection.close()
        except Exception as e:
            print(f"Error closing connection: {e}")