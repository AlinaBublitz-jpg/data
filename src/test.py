import unittest
import numpy as np
import pandas as pd
import os
from data_analyzer import DataAnalyzer
from data_handler import DataHandler
from sqlalchemy import Column, MetaData, Table, create_engine
from sqlalchemy import Float, String

class TestDataAnalyzer(unittest.TestCase):

    def setUp(self):
        # Perform setup before each test
        self.db_handler = DataHandler()
        self.data_analyzer = DataAnalyzer()

        # Create tables and load data for testing
        self.db_handler.create_table('test', {'X': 'FLOAT', 'Y': 'FLOAT'})
        self.db_handler.create_table('ideal', {'X': 'FLOAT', 'Y': 'FLOAT'})
        self.db_handler.load_csv_to_db('data/test.csv', 'test')
        self.db_handler.load_csv_to_db('data/ideal.csv', 'ideal')

    def test_find_best_fit(self):
        # Retrieve data for testing
        train_data = self.db_handler.get_data_from_db('SELECT * FROM test')
        ideal_data = self.db_handler.get_data_from_db('SELECT * FROM ideal')

        # Find best fit
        train_set = train_data[['X', 'Y']].values
        ideal_set = ideal_data[['X', 'Y']].values
        best_fits = self.data_analyzer.find_best_fit(train_set, ideal_set)

        # Test 1: Check if the number of best fits is correct
        self.assertEqual(len(best_fits), 3)

        # Test 2: Check if the best fits contain the expected data
        expected_mses = [mse for _, mse in best_fits]
        self.assertLessEqual(min(expected_mses), self.data_analyzer.min_mse)
        
        # Test 3: Check if the best fits correspond to the expected curves
        for curve, mse in best_fits:
            # Example: Check if the curve has the same number of points as the training dataset
            self.assertEqual(len(curve), len(train_set))

        # Test 4: Add more specific checks

    def test_save_deviation(self):
        # Prepare data for testing
        self.data_analyzer.best_fits = [(
            np.array([[1.0, 2.0], [2.0, 3.0], [3.0, 4.0]]), 0.5
        )]

        # Test if the method saves data to the database
        self.data_analyzer.save_deviation()

        # Retrieve and check data from the database
        deviation_data = self.db_handler.get_data_from_db('SELECT * FROM deviations')

        # Test 1: Check if the number of saved data points is correct
        self.assertEqual(len(deviation_data), 3)

        # Test 2: Check if the saved data is correct
        expected_data = np.array([[1.0, 2.0, 0.5, 'Func1'],
                                  [2.0, 3.0, 0.5, 'Func1'],
                                  [3.0, 4.0, 0.5, 'Func1']])
        np.testing.assert_array_equal(deviation_data.values, expected_data)
        
    def test_create_deviations_table(self):
        # Test if the method creates a table with the correct columns
        self.db_handler.create_deviations_table()

        # Check if the table exists in the database
        table_names = self.db_handler.engine.table_names()
        self.assertIn('deviations', table_names)

        # Check the columns of the created table
        metadata = MetaData(bind=self.db_handler.engine)
        deviations_table = Table('deviations', metadata, autoload=True)
        expected_columns = {'X': Float, 'Y': Float, 'Deviation': Float, 'IdealFunction': String}
        for column_name, column_type in expected_columns.items():
            self.assertIsInstance(deviations_table.columns[column_name].type, column_type)

    def test_load_csv_to_db(self):
        # Test if the method loads CSV data into the database
        csv_path = 'test_data.csv'
        df = pd.DataFrame({'X': [1, 2, 3], 'Y': [4, 5, 6]})
        df.to_csv(csv_path, index=False)
        table_name = 'test_table'

        self.db_handler.load_csv_to_db(csv_path, table_name)

        # Check if the data is present in the database
        query = f'SELECT * FROM {table_name}'
        loaded_data = self.db_handler.get_data_from_db(query)
        pd.testing.assert_frame_equal(df, loaded_data)

        # Clean up
        os.remove(csv_path)

if _name_ == '_main_':
    unittest.main()