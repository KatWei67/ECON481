### Exercise 0
def github() -> str:
    """
    Return the link to github.
    """

    return "https://github.com/KatWei67/ECON481/blob/main/ECON481_Homework/ECON481_PS4.py"

### Exercise 1
import pandas as pd
from sklearn.utils import resample

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
import matplotlib.pyplot as plt

def plot_close(df: pd.DataFrame, start: str = '2010-06-29', end: str = '2024-04-15') -> None:
    """
    Using the loaded data to plot the closing price of the stock between those dates as a line graph

    Argument:
    pd.DataFrame that is the output from Exercise 1

    Return: 
    Nothing
    """
    # Convert the date column to datetime format and make it be the index of the DataFrame
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    #  Select rows of the DataFrame based on the date range
    range = (df.index >= start) & (df.index <= end)
    filtered_df = df.loc[range]

    # Create a line plot for the closing price data
    plt.figure(figsize=(10, 5))
    plt.plot(filtered_df['Close'], label='Closing Price')

    # Label the x-axis, y-axis, and title
    plt.xlabel('Date')
    plt.ylabel('Closing Price (USD)')
    plt.title(f'Tesla Stock Closing Price from {start} to {end}')

    # Add a legend to the plot
    plt.legend()

    # Show the plot
    plt.show()

# # check
# df = load_data()
# print(plot_close(df))

### Exercise 3
import pandas as pd
import statsmodels.api as sm

def autoregress(df: pd.DataFrame) -> float:
    """
    Fit a OLS model and return the t-statistic.

    Argument:
    pd.DataFrame that is the output from Exercise 1

    Return:
    A float: T-statistic of OLS model
    """
    # Convert the date column to datetime format and satisfy proper order
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values('Date', inplace=True)
    
    # Calculate the difference in consecutive closing prices
    df['Delta'] = df['Close'].diff()

    # Create the Lagged variable
    df['Lagged_Delta'] = df['Delta'].shift(1)
    
    # Remove rows with no value that result from the differencing and lagging
    df.dropna(inplace=True)
    
    # Define the dependent and independent variable
    Y = df['Delta']
    X = df[['Lagged_Delta']]
    
    # Add a constant term to allow statsmodels to fit an intercept
    X = sm.add_constant(X)
    
    # Fit an ols model using 'HC1'
    model = sm.OLS(Y, X).fit(cov_type='HC1')
    
    # Extract the t-statistic for the coefficient of lagged price
    t_statistic = model.tvalues[0]
    
    return t_statistic

# # # check
# df = load_data()
# print(autoregress(df))

### Exercise 4
from sklearn.linear_model import LogisticRegression
import numpy as np

def autoregress_logit(df: pd.DataFrame) -> float:
    """
    Fit a logistic Regression model and retun a T-statistic

    Argument:
    pd.DataFrame that is the output from Exercise 1

    Return:
    A float: T-statistic of OLS model
    """
    # Calculate the change in price
    df['Delta'] = df['Close'].diff()

    # Create the lagged price change feature and the binary target
    df['Lagged_Delta'] = df['Delta'].shift(1)
    df['Target'] = (df['Delta'] > 0).astype(int)

    # Drop missing values that were introduced by differencing and shifting
    df = df.dropna()

    # Extract the feature and target variables
    X = df[['Lagged_Delta']].values
    y = df['Target'].values

    # Initialize the logistic regression model
    model = LogisticRegression()

    # Fit the model
    model.fit(X, y)

    # Perform bootstrapping to estimate the standard error of the coefficient
    coefs = []
    for _ in range(481):  # Number of bootstrap samples
        X_resampled, y_resampled = resample(X, y)
        model_resampled = LogisticRegression().fit(X_resampled, y_resampled)
        coefs.append(model_resampled.coef_[0])

    # Calculate the standard deviation (standard error) of the bootstrapped coefficients
    std_error = np.std(coefs)

    # Compute the t-statistic for the coefficient
    t_stat = model.coef_[0] / std_error

    # Since we are interested in the first (and only) coefficient
    return t_stat[0]


# df = load_data()
# print(autoregress_logit(df))

### Exercise 5
import matplotlib.pyplot as plt

def plot_delta(df: pd.DataFrame) -> None:
    """
    Plot the Δxt for the full dataset.

    Arguments:
    pd.DataFrame that is the output from Exercise 1

    Return:
    Nothing
    """

    # Calculate the difference in consecutive closing prices
    df['Delta'] = df['Close'].diff()

    # Plot Δxt
    # Create a plot for the closing price data
    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df['Delta'], label='Δxt (Change in Closing Price)')

    # Label the x-axis, y-axis, and title
    plt.xlabel('Date')
    plt.ylabel('Δxt')
    plt.title('Consecutive Change in Closing Stock Price')

    # Add a legend to the plot
    plt.legend()

    # Add a grid to the plot for better readability of the values
    plt.grid(True)

    # Show the plot
    plt.show()

# check 
# df = load_data()
# print(plot_delta(df))

