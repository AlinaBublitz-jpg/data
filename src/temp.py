import numpy as np
import pandas as pd
from data_handler import DataHandler

class DataAnalyzer(DataHandler):
    def _init_(self, *args, **kwargs):
        """
        Initializes an instance of the DataAnalyzer class.

        Parameters:
        *args: any positional arguments
        **kwargs: any keyword arguments
        """
        super()._init_(*args, **kwargs)
        self.best_fits = {}  # Holds the best fits
        self.min_mse = np.inf  # Holds the minimum Mean Squared Error (MSE)

    def mean_squared_error(self, y_true, y_pred):
        """
        Computes the Mean Squared Error (MSE) between true (y_true) and predicted (y_pred) values.

        Parameters:
        y_true: numpy array
            Array of true values
        y_pred: numpy array
            Array of predicted values

        Returns:
        float
            The computed MSE
        """
        assert len(y_true) == len(y_pred), "The lengths of arrays must be the same."
        squared_diff = (y_true - y_pred) ** 2
        mse = np.mean(squared_diff)
        return mse

    def find_best_fit(self, train_set: np.array, ideal_set: np.array):
        """
        Finds the best fits between the training set and a set of ideal curves.

        Parameters:
        train_set: numpy array
            Training set with X and Y values
        ideal_set: numpy array
            Set of ideal curves with X and Y values

        Returns:
        list
            List of best fits (best_fits)
        """
        y_train = train_set[:, 1]  # Extract Y values from the training set

        best_curve = None  # Holds the best curve
        lowest_mse = float('inf')  # Holds the minimum MSE
        num_best_fits = 3  # Number of best fits
        best_fits = [(None, np.inf)] * num_best_fits  # Holds the best fits as (curve, MSE) pairs

        for curve in ideal_set:
            if len(curve) != len(train_set):
                continue  # Skip this curve if it's not the same length as the training set

            y_curve = curve[:, 1]  # Extract Y values from the curve

            # Compute the MSE between the Y values of the curve and the training set
            mse = self.mean_squared_error(y_train, y_curve)

            # Check if the current curve is one of the best fits
            for i, (best_curve, lowest_mse) in enumerate(best_fits):
                if mse < lowest_mse:
                    best_fits[i] = (curve, mse)
                    break
        self.best_fits = best_fits  # Save the best fits as an instance variable
        return best_fits

    def save_deviation(self):
        """
        Saves the deviations between the best fits and the training set to the database.
        """
        if not self.best_fits:
            print("No best fits available.")
            return

        # Establish a connection to the SQLite database
        conn = self.engine.connect()

        # Iterate through the deviations and save them to the database
        for i, (best_curve, mse) in enumerate(self.best_fits, start=1):
            # Create a DataFrame for the deviations
            deviation_df = pd.DataFrame({
                'X': best_curve[:, 0],
                'Y': best_curve[:, 1],
                'Deviation': mse,
                'IdealFunction': f'Func{i}'  # Assumption: Function labeling (Func1, Func2, etc.)
            })

            # Save the DataFrame to the database
            deviation_df.to_sql('deviations', conn, if_exists='append', index=False)

        # Close the connection to the database
        conn.close()