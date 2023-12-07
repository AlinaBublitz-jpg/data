from typing import Dict, List, Union
import numpy as np

from data_handler import DataHandler


class DataAnalyzer(DataHandler):
    def __init__(self, *args, **kwargs):
        # Call parent constructor
        super().__init__(*args, **kwargs)


    def mean_squared_error(self, y_true: np.array, y_pred: np.array) -> float | None:
        if len(y_true) != len(y_pred):
            return
        squared_diff = (y_true - y_pred) ** 2
        mse = np.mean(squared_diff)
        return mse


    def find_best_fit(self, train_set: np.ndarray, ideal_set: List[np.ndarray]) -> Dict[str, Union[str, np.array, float]] | None:
        y_train = train_set[:, 1]  # Extract y values

        # Initialize best curve and lowest MSE
        best_curve = None

        # Set the lowest MSE to infinity so that the first curve will always be lower
        lowest_mse = float('inf')

        # Iterate through each curve in the ideal set
        for i, curve in enumerate(ideal_set):
            if len(curve) != len(train_set):
                continue  # Skip this curve if it's not the same length as the train set

            y_curve = curve[:, 1]  # Extract y values

            # Compute the MSE between the y values of the curve and the training set
            mse = self.mean_squared_error(y_train, y_curve)

            # If the MSE is lower than the current lowest MSE, update the lowest MSE and best curve
            if mse < lowest_mse:
                best_curve = curve
                lowest_mse = mse
                # Index + 1 of the best curve
                name = 'Func' + str(i + 1)

        
        if best_curve is None:
            return None
        return {'name': name, 'curve': best_curve, 'mse': lowest_mse}
    
    def test_data_point(self, datapoint: np.array, best_fits: List[Dict[str, Union[str, np.array, float]]]) -> Dict[str, Union[str, float]] | None:
        x = datapoint[0]
        y = datapoint[1]
        result = None
        for best_fit in best_fits:
            max_deviation = best_fit['mse']
            curve = best_fit['curve']
            ideal_dict = dict(zip(curve[:, 0], curve[:, 1]))
            if x in ideal_dict:
             y_ideal = ideal_dict[x]
             deviation = abs(y - y_ideal)
             if deviation < max_deviation and (result is None or deviation < result['deviation']):
                result = {'x': x, 'y': y, 'deviation': deviation, 'name': best_fit['name']}
        if (result is None or result['deviation'] > np.sqrt(2)):
            return None
        return result
    