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
    """
    evens = sum(i for i in range(n) if i % 2 == 0)
    odds = sum (i for i in range(n) if i % 2 != 0)

    return {'evens': evens, 'odds': odds}

### Exercise 3
