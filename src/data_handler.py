import numpy as np
import pandas as pd
from sqlalchemy import Column, MetaData, Table, create_engine
import os

class DataHandler:
    def __init__(self, db_filename: str = 'database.db'):
        # Create folder runtime if it doesn't exist
        if not os.path.exists('runtime'):
            os.makedirs('runtime')
        # Create database engine
        self.engine = create_engine(f"sqlite:///runtime/{db_filename}")
        # Create metadata object
        self.metadata = MetaData()

    def create_table(self, table_name: str, columns: dict):
        # Create table with given name and columns
        Table(
            table_name, 
            self.metadata, 
            *[Column(name, type_) for name, type_ in columns.items()]
        )
        self.metadata.create_all(self.engine)

    # Loads a csv file into a database table
    def load_csv_to_db(self, csv_path: str, table_name: str):
        # Load csv to pandas DataFrame
        df = pd.read_csv(csv_path)
        # Save DataFrame to database table replacing current data if it exists
        df.to_sql(table_name, self.engine, if_exists='replace', index=False)


    # Returns a pandas DataFrame from a SQL query
    def get_data_from_db(self, query: str):
        return pd.read_sql_query(query, self.engine)
    
    def replace_data_to_table(self, table_name: str, data: pd.DataFrame):
        data.to_sql(table_name, self.engine, if_exists='replace', index=False)
            
    # Returns an array of curves from a pandas DataFrame
    def get_curves_from_frame(self, frame: pd.DataFrame):
        # Convert DataFrame to numpy array
        array_np = frame.values

        # Split the numpy array into arrays of [x, y1], [x, y2], etc.
        curvesArray = [np.column_stack((array_np[:,0], array_np[:,i])) for i in range(1, array_np.shape[1])]
        return curvesArray
