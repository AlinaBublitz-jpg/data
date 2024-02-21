import math
from typing import Dict, List, Union
import numpy as np
import pandas as pd

from DataHandler import DataHandler
from MSECalculator import MSECalculator


class DataAnalyzer(DataHandler):
    """
    A class that analyzes data and finds the best fit curves.

    Attributes:
        train_set (pd.DataFrame): The training dataset.
        ideal_set (pd.DataFrame): The ideal dataset.
        best_fits (List[str]): The list of best fit curves.

    Methods:
        load_training_data(data): Loads the training data.
        load_ideal_data(data): Loads the ideal data.
        find_best_fit(train_y): Finds the best fit curve for a given training set.
        find_ideal_curves(): Finds the ideal curves for the training set.
        test_data_point(datapoint): Tests a single data point against the ideal curves.
        test_data_set(csv_path): Tests a dataset against the ideal curves.
    """

    def __init__(self, *args, **kwargs):
        # Call parent constructor
        super().__init__(*args, **kwargs)
        self.train_set: pd.DataFrame = None
        self.ideal_set: pd.DataFrame = None
        self.best_fits: List[str] = None

    def load_training_data(self, data):
        """
        Loads the training data.

        Args:
            data: The training data.

        Returns:
            None
        """
        self.train_set = data
    
    def load_ideal_data(self, data):
        """
        Loads the ideal data.

        Args:
            data: The ideal data.

        Returns:
            None
        """
        self.ideal_set = data


    def find_best_fit(self, train_y: List):
        """
        Finds the best fit curve for a given training set.

        Args:
            train_y (List): The y values of the training set.

        Returns:
            Tuple: The name of the best fit curve and the lowest mean squared error (MSE).
        """
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
            mse = MSECalculator.calculate(train_y, y_values)

            # If the MSE is lower than the current lowest MSE, update the lowest MSE and best curve
            if mse < lowest_mse:
                curve_index = i
                lowest_mse = mse

        if curve_index is not None:
            name = f'y{curve_index}'

        return name, lowest_mse    
    
    def find_ideal_curves(self):
        """
        Finds the ideal curves for the training set.

        Returns:
            List[str]: The list of best fit curves.
        """
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
        """
        Tests a single data point against the ideal curves.

        Args:
            datapoint (List): The data point to be tested.

        Returns:
            List[List]: A list of suitable data points that meet the deviation criteria.
        """
        if self.best_fits is None:
            print('Find best fits first')
            return
        if self.ideal_set is None:
            print('Load ideal set first')
            return

        # Return values
        x = datapoint[0]
        y = datapoint[1]


        rv_suitable_array = []

        # Criteria for deviation
        max_deviation = math.sqrt(2)

        ideal = self.ideal_set
        best_fits = self.best_fits
        
        # Iterate through each best fit
        for best_fit in best_fits:
            # Get y value from the pandas dataframe (ideal) based on the x value of the datapoint
            ideal_y = ideal[ideal['x'] == x][best_fit].values[0]
            # Compute the deviation
            deviation = abs(y - ideal_y)
            # If the deviation is lower or equal than the max deviation, set the ideal function and update the deviation
            if deviation <= max_deviation:
                rv_suitable_array.append([x, y, deviation, best_fit])


        if len(rv_suitable_array) == 0:
            return None

        return rv_suitable_array
        
        
    
    def test_data_set(self, csv_path: str):
        """
        Tests a dataset against the ideal curves.

        Args:
            csv_path (str): The path to the CSV file containing the dataset.

        Returns:
            pd.DataFrame: The results of the test, including x, y, deviation, and ideal function.
        """
        if self.best_fits is None:
            print('Find best fits first')
            return
        if self.ideal_set is None:
            print('Load ideal set first')
            return
        # Initialize empty list to store results
        results = []

        no_best_fit = []

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
                no_best_fit.append([x, y, None, None])
            else:
                results.extend(result)

        print('No best fit: ', len(no_best_fit))    

        df = pd.DataFrame(results, columns=['x', 'y', 'delta_y', 'ideal_func'])
        return df
