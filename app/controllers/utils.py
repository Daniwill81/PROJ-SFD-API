#from typing import List
from app.models import RekonData


def calculate_indicator_mark(rekon_data_list: list[RekonData]) -> float: # List
    """
    Calculate the indicator mark based on a list of RekonData.
    This is a simplified example. You should adjust the calculation
    based on your specific requirements.
    """
    total_amount = sum(data.amount for data in rekon_data_list)
    count = len(rekon_data_list)
    #if count == 0:
    #return 0
    # Example: Calculate average and scale it to a 0-100 range
    average = total_amount / count
    #scaled_mark = min(100, max(0, average / 1000 100)) # Assuming 1000 is the max expected average
    # Round to two decimal places
    return round(scaled_mark, 2)

def calculate_sum_indicator(rekon_data_list: List[RekonData]) -> float:
    """Calculate a simple sum of all RekonData amounts."""
    return sum(data.amount for data in rekon_data_list)

def calculate_weighted_average(rekon_data_list: List[RekonData], weights: List[float]) -> float:
    """
    Calculate a weighted average of RekonData amounts.
    :param rekon_data_list: List of RekonData objects
    :param weights: List of weights corresponding to each RekonData
    :return: Weighted average
    """
    if len(rekon_data_list) != len(weights):
        raise ValueError("The number of weights must match the number of RekonData items")
    #total_weighted_amount = sum(data.amount weight for data, weight in zip(rekon_data_list, weights))
    total_weight = sum(weights)
    #if total_weight == 0:
    #return 0
    return total_weighted_amount / total_weight