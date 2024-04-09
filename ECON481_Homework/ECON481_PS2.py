from asyncio import log
import numpy as np
from math import exp, pi, sqrt

import scipy as sp
### Exercise 0
def github() -> str:
    """
    This function return the link to github where this file in.
    """

    return "https://github.com/KatWei67/ECON481/blob/main/ECON481_Homework/ECON481_PS2.py"

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
    This function estimates the MLE paramters beta_mle for data
    simulated as above, where model is:
    y_i = beta0 + beta1x_i1 + beta2x_i2 + beta3x_i3 + error_i,
    where error_i ~ N(0,1).

    Return:
    return a 4*1 np.array with the coefficients beta1, beta2,
    beta3, beta4 (in that order).
    """  
    # error = y - beta0 -beta1*x1 - beta2*x2 - beta3*x3
    # Adding intercept
    X_int = np.concatenate(
    [np.ones(X.shape[0]).reshape(-1,1), X,], axis = 1)

    # calculate probability of errors
    def SSE(beta, y, X):
        errors = y - X @ beta
    
        return np.sum(errors ** 2)
    
    # Initial guess for the coefficients (including beta0 for the intercept)
    beta_initial = np.zeros(X_int.shape[1])
    
    # Perform the optimization using Nelder-Mead method
    result = sp.optimize(
        SSE, # the SSE function
        beta_initial, # starting initial guess (beta=0)
        args=(y, X_int), # additional parameters passed to SSE
        method='Nelder-Mead')
   
    # Return the optimized coefficients
    return result.x


### Exercise 3
def estimate_ols(y: np.array, X: np.array) -> np.array:
    """
    Some docstrings.
    """
    # Adding intercept
    X_int = np.concatenate(
    [np.ones(X.shape[0]).reshape(-1,1), X,], axis = 1)

    # Calculate OLS regression coefficients
    beta_hat = np.matmul(np.matmul(np.linalg.inv(np.matmul(np.array(X_int).transpose(), np.array(X_int))), X_int.transpose()), y)
    
    return beta_hat
