"""
This script performs data analysis and manipulation using a database connection.
It creates tables, loads data from CSV files into the tables, analyzes the data,
finds the best fits, tests the data set, and writes the test results to the database.
"""

from DatabaseConnection import DatabaseConnection
from DataAnalyzer import DataAnalyzer
from DataHandler import DataHandler
from schema.index import table_test, table_training, table_ideal

# Initialize database connection
db_connection = DatabaseConnection()

# Initialize data handler
db_handler = DataHandler(db_connection)


# Create tables
db_handler.create_table('test', table_test, True)
db_handler.create_table('train', table_training, True)
db_handler.create_table('ideal', table_ideal, True)


# Load data to tables
db_handler.load_csv_to_db('data/train.csv', 'train')
db_handler.load_csv_to_db('data/ideal.csv', 'ideal')



# Get data from tables
train = db_handler.get_data_from_db('SELECT * FROM train')
ideal = db_handler.get_data_from_db('SELECT * FROM ideal')

# Initialize data analyzer
db_analyzer = DataAnalyzer(db_connection)

# Load data to data analyzer
db_analyzer.load_training_data(train)
db_analyzer.load_ideal_data(ideal)

# Find best fits
best_fits = db_analyzer.find_ideal_curves()
# print(best_fits)

test_results = db_analyzer.test_data_set('data/test.csv')
# print(test_results)

# Write test_results to database
db_analyzer.replace_data_in_table('test', test_results)


# Get data from tables
test = db_handler.get_data_from_db('SELECT * FROM test')
print(test)



