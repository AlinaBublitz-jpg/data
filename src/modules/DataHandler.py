from typing import Dict, Any, List, TypedDict
import pandas as pd
from sqlalchemy import inspect, Column, MetaData, Table,  exc
import os

from modules.DatabaseConnection import DatabaseConnection

class ColumnDefinition(TypedDict):
    name: str
    type_: Any

class DataHandler:
    """
    A class that handles data operations with a database.

    Args:
        db_connection (DatabaseConnection): The database connection object.

    Attributes:
        engine: The database engine.
        metadata: The metadata object for the database.

    Methods:
        create_table: Creates a table in the database.
        load_csv_to_db: Loads data from a CSV file into a database table.
        get_data_from_db: Retrieves data from the database using a query.
        replace_data_in_table: Replaces data in a database table.

    """

    def __init__(self, db_connection: DatabaseConnection) -> None:
        """
        Initializes a new instance of the DataHandler class.

        Args:
            db_connection (DatabaseConnection): The database connection object.

        """
        self.engine = db_connection.engine
        self.metadata = MetaData()
        self.metadata.bind = self.engine

    def create_table(self, table_name: str, columns: Dict[str, Any], recreate: bool = False) -> None:
        """
        Creates a table in the database.

        Args:
            table_name (str): The name of the table.
            columns (Dict[str, Any]): A dictionary of column names and types.
            recreate (bool, optional): Whether to recreate the table if it already exists. Defaults to False.

        """
        try:
            inspector = inspect(self.engine)
            if inspector.has_table(table_name):
                if recreate:
                    table = Table(table_name, self.metadata, autoload_with=self.engine)
                    table.drop(self.engine)
                else:
                    raise exc.SQLAlchemyError(f"Table {table_name} already exists")

            table = Table(
                table_name,
                self.metadata,
                *[Column(name, type_) for name, type_ in columns.items()],
                extend_existing=True
            )
            table.create(self.engine)
        except exc.SQLAlchemyError as e:
            print(f"Error creating table {table_name}: {e}")

    def load_csv_to_db(self, csv_path: str, table_name: str) -> None:
        """
        Loads data from a CSV file into a database table.

        Args:
            csv_path (str): The path to the CSV file.
            table_name (str): The name of the table.

        """
        try:
            df = pd.read_csv(csv_path)
            df.to_sql(table_name, self.engine, if_exists='replace', index=False)
        except Exception as e:
            print(f"Error loading CSV to DB: {e}")

    def get_data_from_db(self, query: str) -> pd.DataFrame:
        """
        Retrieves data from the database using a query.

        Args:
            query (str): The SQL query.

        Returns:
            pd.DataFrame: The retrieved data as a pandas DataFrame.

        """
        try:
            return pd.read_sql_query(query, self.engine)
        except exc.SQLAlchemyError as e:
            print(f"Error executing query: {e}")
            return pd.DataFrame()

    def replace_data_in_table(self, table_name: str, data: pd.DataFrame) -> None:
        """
        Replaces data in a database table.

        Args:
            table_name (str): The name of the table.
            data (pd.DataFrame): The new data to replace the existing data in the table.

        """
        try:
            data.to_sql(table_name, self.engine, if_exists='replace', index=False)
        except exc.SQLAlchemyError as e:
            print(f"Error replacing data in table {table_name}: {e}")
