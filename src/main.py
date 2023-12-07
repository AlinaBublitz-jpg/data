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

# Initialize data analyzer
db_analyzer = DataAnalyzer(db_handler)

# Get data from tables
train = db_handler.get_data_from_db('SELECT * FROM train')
ideal = db_handler.get_data_from_db('SELECT * FROM ideal')



# Transform data into curves
train_curves = db_handler.get_curves_from_frame(train)
ideal_curves = db_handler.get_curves_from_frame(ideal)

# Set numpy print options (suppress scientific notation)
np.set_printoptions(suppress=True)

# Declare best fits array
best_fits = []

# Iterate through each curve in the training set
for curve in train_curves:
    best_fit = db_analyzer.find_best_fit(train_curves[0], ideal_curves)
    best_fits.append(best_fit)
    
print(len(best_fits))


chunks = pd.read_csv('data/test.csv', chunksize=1)

test_data = pd.read_csv('data/test.csv')
print (test_data['x'][0])

# Example: Visualize the training data using a scatter plot
# plt.figure(figsize=(8, 6))
# plt.scatter(test_data['x'], test_data['y'], label='Test Data', color='blue')
# plt.title('Training Data')
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.legend()
# plt.show()



for chunk in chunks:
     # Extract x, y from chunk
    x = chunk['x'].values[0]
    y = chunk['y'].values[0]
    datapoint = np.array([x, y])
    # Call the function
    result = db_analyzer.test_data_point(datapoint, best_fits)
    if result is None:
        print('No best fit found for datapoint ' + str(datapoint))
    else:
        print(result)
