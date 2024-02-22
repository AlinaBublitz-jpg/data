import os
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine

class DatabaseConnection:
    """
    A class to manage database connections using SQLAlchemy.
    
    This class encapsulates the logic required to create and manage a SQLite
    database engine. It ensures that the database file is located within a
    'runtime' directory. If the directory does not exist, it is created.
    
    Attributes:
        db_filename (str): The name of the database file.
        engine (Engine): The SQLAlchemy engine instance for database operations.
    """
    
    def __init__(self, db_filename: str = 'database.db'):
        """
        Initializes the DatabaseConnection instance with a specific database file name.
        
        Parameters:
            db_filename (str): The name of the database file to be used or created
                               within the 'runtime' directory. Defaults to 'database.db'.
        """
        self.db_filename = db_filename
        self.engine = self.create_engine()

    def create_engine(self) -> Engine:
        """
        Creates and returns a SQLAlchemy engine instance for the SQLite database.
        
        This method checks if a 'runtime' directory exists, and if not, it creates it.
        Then, it initializes a SQLAlchemy engine with the SQLite database located
        within this directory.
        
        Returns:
            Engine: A SQLAlchemy engine connected to the specified SQLite database.
        """
        if not os.path.exists('runtime'):
            os.makedirs('runtime')
        return create_engine(f"sqlite:///runtime/{self.db_filename}")
