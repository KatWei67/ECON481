### Problem Set 1
# Jiaying (Katherine) Wei

### Exercise 0
# Please write a function that takes no arguments and returns a link to your solutions on GitHub.
# Use the following shell:
def github() -> str:
    """
    This function takes no argument and returns a link to my homework solution on Github.
    """

    return "https://github.com/KatWei67/ECON481/blob/main/ECON481_Homework/ECON481_PS1.py"

### Exercise 1
# Please ensure that you can run python1, can use Git, and install the following packages2 (we’ll install more as we go):
# numpy
# pandas
# scipy
# matplotlib
# seaborn

### Exercise 2
def evens_and_odds(n: int) -> dict:
    """
    Calculate the sum of even number & sum of odd number less than n.

    Return:
    A dictionary with two keys 'evens' & 'odds', and two valus 'sum of evens' & 'sum of odds'

    For example, evens_and_odds(4) should return {'evens': 2, 'odds': 4}
    """
    evens = sum(i for i in range(n) if i % 2 == 0)
    odds = sum (i for i in range(n) if i % 2 != 0)

    return {'evens': evens, 'odds': odds}

### Exercise 3
from typing import Union
from datetime import datetime
def time_diff(date_1: str, date_2: str, out: str) -> Union[str,float]:
    """
    If keyword is float, then return the absolute value in days.
    If keyword is string, then return a sentance that there are X days between the two dates.

    For example, time_diff('2020-01-01', '2020-01-02', 'float') should return 1
    For example, time_diff('2020-01-03', '2020-01-01', 'string') should return
    "There are 2 days between the two dates"
    """
    d1 = datetime.strptime(date_1, '%Y-%m-%d')
    d2 = datetime.strptime(date_2, '%Y-%m-%d')
    different_days = abs(d1.day - d2.day)
    if out == 'float':
        return float(different_days)
    else:
        return f"There are {different_days} between the two dates"
    
#### Exercise 4
# start at the last item in list, get every items and go backwards to the first item
def reverse(in_list: list) -> list:
    """
    This function will return a list of the argument in reverse order.

    For example, reverse(['a', 'b', 'c']) should return ['c', 'b', 'a']
    """
    return in_list[::-1]

### Exercise 5
def prob_k_heads(n: int, k: int) -> float:
    """
    For natural n and k with n>k, return the probability of getting k heads from n flips

    For example, prob_k_heads(1,1) should return .5
    """
    n_minus_k_fac = 1
    for i in range(1, n-k+1):
        n_minus_k_fac *= i
    n_choose_k = 1
    for i in range(k+1, n+1):
        n_choose_k *= i
    n_choose_k /= n_minus_k_fac
    p=1/2
    return n_choose_k*(p**k)*(p**(n-k))

print(prob_k_heads(1,1))


