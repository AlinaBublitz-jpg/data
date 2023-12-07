import math
from typing import Dict, List, Union
import numpy as np
import pandas as pd

from data_handler import DataHandler


class DataAnalyzer(DataHandler):
    def __init__(self, *args, **kwargs):
        # Call parent constructor
        super().__init__(*args, **kwargs)
        self.train_set: pd.DataFrame = None
        self.ideal_set: pd.DataFrame = None
        self.best_fits: List[str] = None

    def load_training_data(self, data):
        self.train_set = data
    
    def load_ideal_data(self, data):
        self.ideal_set = data

    def mean_squared_error(self, y_true: list, y_pred: list) -> float | None:
        if len(y_true) != len(y_pred):
            return
        squared_diff = [(a - b) ** 2 for a, b in zip(y_true, y_pred)]
        mse = sum(squared_diff) / len(squared_diff)
        return mse


    def find_best_fit(self, train_y: List):
        if self.ideal_set is None:
            print('Load ideal set first')
            return
        # Initialize curve_index and lowest MSE
        curve_index = None
        name = None

        # Set the lowest MSE to infinity so that the first curve will always be lower
        lowest_mse = float('inf')

        # Iterate through each curve in the ideal set
        for i in range(1, 51): 
            # Extract y values from the ideal set
            y_values =  self.ideal_set[f'y{i}'].tolist()
          
            # Compute the MSE between the y values of the curve and the training set
            mse = self.mean_squared_error(train_y, y_values)

            # If the MSE is lower than the current lowest MSE, update the lowest MSE and best curve
            if mse < lowest_mse:
                curve_index = i
                lowest_mse = mse

        if curve_index is not None:
            name = f'y{curve_index}'

        return name, lowest_mse    
    
    def find_ideal_curves(self):
        if self.train_set is None:
            print('Load training set first')
            return
        if self.ideal_set is None:
            print('Load ideal set first')
            return
        best_fits: List[str] = []

        # Iterate through each y column in the training set
        for i in range(1, 5):
            # Extract y values from the training set
            train_y = self.train_set[f'y{i}'].tolist()
            best_fit = self.find_best_fit(train_y)
            # If best fit is found, append it to the best fits list
            if best_fit[0] is not None:
                best_fits.append(best_fit[0])
        self.best_fits = best_fits
        return best_fits
    
    def test_data_point(self, datapoint: List):
        if self.best_fits is None:
            print('Find best fits first')
            return
        if self.ideal_set is None:
            print('Load ideal set first')
            return

        # Return values
        x = datapoint[0]
        y = datapoint[1]

        # Set the deviation to infinity so that the first deviation will always be lower
        rv_deviation = float('inf')
        rv_ideal_func = None

        # How do we get training_deviation?
        training_deviation = 100

        # Criteria for deviation
        max_deviation = math.sqrt(2) * training_deviation

        ideal = self.ideal_set
        best_fits = self.best_fits
        
        # Iterate through each best fit
        for best_fit in best_fits:
            # Get y value from the pandas dataframe (ideal) based on the x value of the datapoint
            ideal_y = ideal[ideal['x'] == x][best_fit].values[0]
            # Compute the deviation
            deviation = abs(y - ideal_y)
            # If the deviation is lower or equal than the max deviation, set the ideal function and update the deviation
            if deviation <= max_deviation and deviation < rv_deviation:
                rv_deviation = deviation
                rv_ideal_func = best_fit
            
        if (rv_ideal_func is None):
            return None
        return x, y, rv_deviation, rv_ideal_func
        
        
    
    def test_data_set(self, csv_path: str):
        if self.best_fits is None:
            print('Find best fits first')
            return
        if self.ideal_set is None:
            print('Load ideal set first')
            return
        # Initialize empty list to store results
        results = []

        # Read the CSV file in chunks
        chunks = pd.read_csv(csv_path, chunksize=1)

        # Iterate through each chunk
        for chunk in chunks:
            # Extract x, y from chunk
            x = chunk['x'].values[0]
            y = chunk['y'].values[0]
            datapoint = np.array([x, y])
            # Call the function
            result = self.test_data_point(datapoint)
            if result is None:
                print('No best fit found for datapoint ' + str(datapoint))
            else:
                results.append(result)
        df = pd.DataFrame(results, columns=['x', 'y', 'delta_y', 'Ideal_Func'])
        return df
    