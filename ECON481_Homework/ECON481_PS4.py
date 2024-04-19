### Exercise 0
def github() -> str:
    """
    Return the link to github.
    """

    return "https://github.com/KatWei67/ECON481/blob/main/ECON481_Homework/ECON481_PS4.py"

### Exercise 1
import pandas as pd

def load_data() -> pd.DataFrame:
    """
    Accesses the file on Tesla stock price history.

    Return:
    pd.DataFrame
    """
    df = pd.read_csv('https://lukashager.netlify.app/econ-481/data/TSLA.csv')
    return df

# check
# print(load_data())

### Ecercise 2