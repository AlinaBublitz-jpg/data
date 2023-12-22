from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from data_analyzer import DataAnalyzer
from data_handler import DataHandler
from schema.index import table_test, table_training, table_ideal


# Initialize data handler
db_handler = DataHandler()


# Create tables
db_handler.create_table('test', table_test)
db_handler.create_table('train', table_training)
db_handler.create_table('ideal', table_ideal)


# Load data to tables
db_handler.load_csv_to_db('data/train.csv', 'train')
db_handler.load_csv_to_db('data/ideal.csv', 'ideal')



# Get data from tables
train = db_handler.get_data_from_db('SELECT * FROM train')
ideal = db_handler.get_data_from_db('SELECT * FROM ideal')

# Initialize data analyzer
db_analyzer = DataAnalyzer()

# Load data to data analyzer
db_analyzer.load_training_data(train)
db_analyzer.load_ideal_data(ideal)

# Find best fits
best_fits = db_analyzer.find_ideal_curves()
# print(best_fits)

test_results = db_analyzer.test_data_set('data/test.csv')
# print(test_results)

# Write test_results to database
db_analyzer.replace_data_to_table('test', test_results)


# Get data from tables
test = db_handler.get_data_from_db('SELECT * FROM test')
print(test)



