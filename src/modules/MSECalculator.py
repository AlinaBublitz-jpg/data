class MSECalculator:
    @staticmethod
    def calculate(y_true: list, y_pred: list) -> float | None:
        if len(y_true) != len(y_pred):
            return None
        squared_diff = [(a - b) ** 2 for a, b in zip(y_true, y_pred)]
        return sum(squared_diff) / len(squared_diff)