from abc import ABC, abstractmethod

from core.database.db_connection_manager import DatabaseConnectionManager


class BaseRepository(ABC):
    """Base repository class with common database operations"""
    
    def __init__(self, connection_manager: DatabaseConnectionManager):
        self.connection_manager = connection_manager
    
    @abstractmethod
    def get_table_name(self) -> str:
        """Get the table name for this repository"""
        pass

