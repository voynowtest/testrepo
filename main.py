import os
import json
from typing import List, Dict, Callable, Any
from datetime import datetime
import functools
import random
import math

# Constants
LOG_FILE_PATH = 'application.log'
MAX_RETRIES = 5

def log_to_file(func: Callable) -> Callable:
    """Decorator to log function calls and results to a log file."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = None
        try:
            result = func(*args, **kwargs)
            with open(LOG_FILE_PATH, 'a') as log_file:
                log_file.write(f"{datetime.now()} - {func.__name__} - SUCCESS - Args: {args}, Kwargs: {kwargs}, Result: {result}\n")
        except Exception as e:
            with open(LOG_FILE_PATH, 'a') as log_file:
                log_file.write(f"{datetime.now()} - {func.__name__} - FAILURE - Args: {args}, Kwargs: {kwargs}, Error: {str(e)}\n")
            raise
        return result
    return wrapper

class Calculator:
    """A simple calculator class that performs arithmetic operations."""
    
    def __init__(self, initial_value: float = 0.0):
        self.value = initial_value

    @log_to_file
    def add(self, num: float) -> float:
        """Adds a number to the current value."""
        self.value += num
        return self.value

    @log_to_file
    def subtract(self, num: float) -> float:
        """Subtracts a number from the current value."""
        self.value -= num
        return self.value

    @log_to_file
    def multiply(self, num: float) -> float:
        """Multiplies the current value by a number."""
        self.value *= num
        return self.value

    @log_to_file
    def divide(self, num: float) -> float:
        """Divides the current value by a number."""
        if num == 0:
            raise ValueError("Cannot divide by zero.")
        self.value /= num
        return self.value

    def reset(self) -> None:
        """Resets the current value to zero."""
        self.value = 0.0

    def __str__(self) -> str:
        return f"Current value: {self.value}"

class DataProcessor:
    """Class for processing a list of numbers."""
    
    def __init__(self, data: List[int]):
        self.data = data
    
    def filter_out_odd_numbers(self) -> List[int]:
        """Filters out odd numbers from the data."""
        return [num for num in self.data if num % 2 == 0]

    def sort_data(self) -> List[int]:
        """Sorts the data in ascending order."""
        return sorted(self.data)

    def compute_statistics(self) -> Dict[str, float]:
        """Computes mean, median, and standard deviation of the data."""
        mean = sum(self.data) / len(self.data)
        median = self._compute_median(self.data)
        std_dev = self._compute_standard_deviation(self.data, mean)
        return {"mean": mean, "median": median, "std_dev": std_dev}
    
    def _compute_median(self, data: List[int]) -> float:
        """Computes the median of a list of numbers."""
        sorted_data = sorted(data)
        n = len(sorted_data)
        mid = n // 2
        if n % 2 == 0:
            return (sorted_data[mid - 1] + sorted_data[mid]) / 2
        else:
            return sorted_data[mid]

    def _compute_standard_deviation(self, data: List[int], mean: float) -> float:
        """Computes the standard deviation of a list of numbers."""
        variance = sum((x - mean) ** 2 for x in data) / len(data)
        return math.sqrt(variance)

class FileHandler:
    """Handles reading and writing data to files."""
    
    def __init__(self, file_name: str):
        self.file_name = file_name
    
    @log_to_file
    def write_data(self, data: Any) -> None:
        """Writes data to a file in JSON format."""
        with open(self.file_name, 'w') as file:
            json.dump(data, file, indent=4)

    @log_to_file
    def read_data(self) -> Any:
        """Reads data from a file in JSON format."""
        if not os.path.exists(self.file_name):
            return None
        with open(self.file_name, 'r') as file:
            return json.load(file)

class RetryDecorator:
    """Retries a function a set number of times if it raises an exception."""
    
    def __init__(self, retries: int = MAX_RETRIES):
        self.retries = retries

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < self.retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == self.retries:
                        raise e
                    print(f"Retry {attempts}/{self.retries} for {func.__name__} due to error: {str(e)}")
        return wrapper

@RetryDecorator(retries=3)
def risky_operation() -> str:
    """Simulates a risky operation that may fail."""
    if random.random() < 0.5:
        raise ValueError("Something went wrong!")
    return "Success"

def main():
    # Example of Calculator usage
    calc = Calculator()
    print(calc.add(5))         # 5
    print(calc.subtract(2))    # 3
    print(calc.multiply(4))    # 12
    print(calc.divide(3))      # 4
    print(calc)

    # Example of DataProcessor usage
    processor = DataProcessor([1, 2, 3, 4, 5, 6])
    print(processor.filter_out_odd_numbers())  # [2, 4, 6]
    print(processor.sort_data())               # [1, 2, 3, 4, 5, 6]
    print(processor.compute_statistics())      # {'mean': 3.5, 'median': 3.5, 'std_dev': 1.707825127659933}

    # Example of FileHandler usage
    file_handler = FileHandler('data.json')
    file_handler.write_data({"key": "value"})
    print(file_handler.read_data())  # {'key': 'value'}

    # Running a risky operation with retry
    print(risky_operation())

if __name__ == "__main__":
    main()
