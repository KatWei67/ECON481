import numpy as np
from math import sqrt
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
    Operate 1000 simulated observations via:
    y = 5 + 3x_i1 + 2x_i2 + 6x_i3 + error_i, where
    x_i1, x_i2, x_i3 ~ N(0,2) and error_i ~ N(0,1)
    
    Return:
    A tuple of two elements, (y,X) where y is a 1000*1 np.array and X is a 
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
def estimate_mle(y: np.array, X: np.array) -> np.array:
    """
    Estimate the MLE parameters beta.
    
    parameters:
    y : a 1000x1 numpy array.
    X : a 1000x3 numpy array.
    
    Returns:
    A 4x1 array with the coefficients beta_0, beta_1, beta_2, beta_3 (in this order).
    """
    # Negative Log-Likelihood function
    def Log_Likelihood(beta):
        # Calculate predicted values
        y_predicted = X @ beta[1:] + beta[0]
        # Calculate residuals
        residuals = y.ravel() - y_predicted.ravel()
        # Negative log-likelihood
        return 0.5 * np.sum(residuals ** 2)

    # Initial guess for the betas value
    beta_initial = np.zeros(X.shape[1] + 1)

    # minimize the residuals
    result = sp.optimize.minimize(Log_Likelihood, beta_initial, method='L-BFGS-B')

    # Return the estimated parameters (beta)
    return result.x.reshape(-1, 1)


### Exercise 3
def estimate_ols(y: np.array, X: np.array, iterations: int = 1000, learning_rate: float = 0.01) -> np.array:
    """
    Estimate the OLS coefficients using gradient descent.

    Parameters:
    parameters:
    y : a 1000x1 numpy array.
    X : a 1000x3 numpy array.
    Default 1000 iterations of running the gradient descent 
    The learning rate for gradient descent (default is 0.01).

    Returns: 
    A 4x1 array with the coefficients beta_0, beta_1, beta_2, beta_3 (in this order).
    """
    # Add interception 
    X_int = np.hstack((np.ones((X.shape[0], 1)), X))
    
    # Initialize beta coefficients to zero
    beta = np.zeros((X_int.shape[1], 1))

    # Gradient Descent to minimize the cost function
    for _ in range(iterations):
        # Calculate the predictions
        predictions = X_int @ beta
        
        # Calculate the error
        error = predictions - y
        
        # Calculate the gradient
        gradient = X_int.T @ error
        
        # Update the coefficients (beta
        beta -= (learning_rate / len(y)) * gradient
    
    return beta

# check
# y, X = simulate_data(seed=481)
# print(estimate_mle(y,X))
# print(estimate_ols(y,X))
