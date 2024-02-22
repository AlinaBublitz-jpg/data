import matplotlib.pyplot as plt
from DataHandler import DataHandler
from DatabaseConnection import DatabaseConnection
from schema.index import table_training
from DataAnalyzer import DataAnalyzer

# Create an instance of the DatabaseConnection class for managing database connections
db_connection = DatabaseConnection()

# Create an instance of the DataHandler class for managing data operations
db_handler = DataHandler(db_connection)

# Example: Load training data from the database based on the specified table name
train_data = db_handler.get_data_from_db(f'SELECT * FROM {table_training}')

# Create an instance of the DataAnalyzer class, which extends DataHandler
data_analyzer = DataAnalyzer(db_connection)

# Example: Load ideal set data from the database
ideal_set_data = db_handler.get_data_from_db('SELECT * FROM ideal')

# Extract X, Y values from the training set
train_set = train_data[['X', 'Y']].values

# Compute the best fits using the DataAnalyzer instance
best_fits = data_analyzer.find_best_fit(train_set, ideal_set_data[['X', 'Y']].values)

# Example: Visualize the training data using a scatter plot
plt.figure(figsize=(8, 6))
plt.scatter(train_data['X'], train_data['Y'], label='Train Data', color='blue')
plt.title('Training Data')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.show()

# Example: Visualize the best fits using line plots
plt.figure(figsize=(8, 6))
for i, (curve, mse) in enumerate(best_fits, start=1):
    plt.plot(curve[:, 0], curve[:, 1], label=f'Best Fit {i}, MSE: {mse}')

plt.title('Best Fits')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.show()

# Example: Load deviation data from the database
deviation_data = db_handler.get_data_from_db('SELECT * FROM deviations')

# Example: Visualize deviations using a scatter plot with a color scale based on deviation
plt.figure(figsize=(8, 6))
plt.scatter(deviation_data['X'], deviation_data['Y'], c=deviation_data['Deviation'], cmap='viridis', label='Deviations')
plt.colorbar(label='Deviation')
plt.title('Deviations')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.show()