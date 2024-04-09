import numpy as np
from math import sqrt
### Exercise 0
def github() -> str:
    """
    Some docstrings.
    """

    # return "https://github.com/<user>/<repo>/blob/main/<filename.py>"

### Exercise 1
def simulate_data(seed: int=481) -> tuple: # seed default to 481
    """
    This function operate 1000 simulated observations via:
    y = 5 + 3x_i1 + 2x_i2 + 6x_i3 + error_i, where
    x_i1, x_i2, x_i3 ~ N(0,2) and error_i ~ N(0,1)
    
    Return:
     a tuple of two elements, (y,X) where y is a 1000*1 np.array and X is a 
     1000*3 np.array.
    """
    # set seed
    np.random.seed(seed)
    
    # Generate independent variables x1, x2, x3
    # np.random.normal(mu, sigma)
    X = np.random.normal(0, sqrt(2), size=(1000, 3))
    
    # Generate the error term 
    error = np.random.normal(0, 1, size=(1000, 1))
    
    # Predit the dependent variable y 
    y = 5 + 3*X[:, 0] + 2*X[:, 1] + 6*X[:, 2] + error.reshape(-1)
    
    # Return a tuple (y, X)
    return (y.reshape(-1, 1), X)

    

### Exercise 2
import numpy as np

def estimate_mle(y: np.array, X: np.array) -> np.array:
    """
    Some docstrings.
    """

    return None

### Exercise 3
def estimate_ols(y: np.array, X: np.array) -> np.array:
    """
    Some docstrings.
    """

    return None