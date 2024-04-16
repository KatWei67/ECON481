### Exercise 0
def github() -> str:
    """
    This return a link to my solutions on Github.
    """

    return "https://github.com/KatWei67/ECON481/blob/main/ECON481_Homework/ECON481_PS3.py"

### Exercise 1
import pandas as pd

def import_yearly_data(years: list) -> pd.DataFrame:
    """
    Import yearly data from EPA Excel sheets and return a concatenated DataFrame of the Direct 
    Emitters tab of each of those year's EPA excel sheet.

    Arguments:
    years: A list of integer that represent the years of each EPA excel sheet

    Return:
    pd.DataFrame: A DataFrame contains a concatenated DataFrame of the Direct Emitters tab of EPA 
    sheets with a new column year.
    """
    # Start with an empty list to store data
    data_frames = []
    
    # Set the path to the directory containing the Excel files
    # base_directory = "EPA/"  # Adjust this path if file locate in other 

    for year in years:
        # Build the path string to the specific Excel file
        file_path = f"https://lukashager.netlify.app/econ-481/data/ghgp_data_{year}.xlsx"

        # Load the Excel file with headers starting from the fourth row
        df = pd.read_excel(file_path, sheet_name='Direct Emitters', skiprows=3, header=0)
        
        # Add a new column 'year' to indicate the year of the data
        df['year'] = year
        
        # Append the DataFrame to the list
        data_frames.append(df)
    
    # Merge the list of DataFrames into a single comprehensive DataFrame
    Concatenate_df = pd.concat(data_frames, ignore_index=True)
    
    return Concatenate_df

# check
# print(import_yearly_data(years=[2021, 2022]))

### Exercise 2
import pandas as pd

def import_parent_companies(years: list) -> pd.DataFrame:
    """
    Import yearly data from parent companies Excel sheets and return a concatenated DataFrame of 
    the years tab of each of those year's EPA excel sheet.

    Arguments:
    years: A list of integer that represent the years of each EPA excel sheet

    Return:
    pd.DataFrame: A DataFrame contains a concatenated DataFrame of those years tab of EPA 
    sheets with a new column year.
    """
    # Set the path to the directory containing the Excel files
    # base_directory = "EPA/"  # Adjust this path if file locate in other 

    # write done the file path
    file_path = "https://lukashager.netlify.app/econ-481/data/ghgp_data_parent_company_09_2023.xlsb"  # This is the single file for all years

    # Start with an empty list to store data 
    data_frames = []

    # read each tab: iterate by years
    for year in years:
        # set the sheet name as the year string
        sheet_name = str(year)

        # Read the specified tab from the Excel file
        df = pd.read_excel(file_path, sheet_name=sheet_name, engine='pyxlsb')
        
        # Add a new column 'year' to indicate the year of the data
        df['year'] = year
        
        # Remove any rows that contain only null values
        df.dropna(how='all', inplace=True)
        
        # Append the DataFrame to the list
        data_frames.append(df)
    
    # Merge the list of DataFrames into a single comprehensive DataFrame
    Concatenate_df = pd.concat(data_frames, ignore_index=True)
    
    return Concatenate_df

#check 
# print(import_parent_companies(years=[2018]))

### Exercise 3
def n_null(df: pd.DataFrame, col: str) -> int:
    """
    Given a pd.DataFrame, for any column, return the number of null values. 
    """
    # Use isnull to check null and sum the number of null values in such column
    return int(df[col].isnull().sum())

# check
# df = import_yearly_data(years=[2021])
# print(type(n_null(df, col='County')))

### Exercise 4
def clean_data(emissions_data: pd.DataFrame, parent_data: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and merge emission and the parent companies data.

    Arguments:
    emissions_data: A concatenated DataFrame contains emission data (output from exercise 1)
    parent_data: A concatenated DataFrame contains parent companies data (output from exercise 2)

    Return:
    pd.DataFrame, with all the column names in lower-case
    """
    # Merge the emissions data with the parent company data on 'year' and 'Facility Id'
    merged_data = pd.merge(emissions_data, parent_data, how='left', 
                           left_on=['year', 'Facility Id'], right_on=['year', 'GHGRP FACILITY ID'])

    # Subset the data to the specified variables
    subset_columns = [
        'Facility Id', 'year', 'State', 'Industry Type (sectors)', 
        'Total reported direct emissions', 'PARENT CO. STATE', 'PARENT CO. PERCENT OWNERSHIP'
    ]
    merged_data = merged_data[subset_columns]

    # Rename the columns to be lower-case
    merged_data.columns = [col.lower() for col in merged_data.columns]

    return merged_data

# check 
#emission_data = import_yearly_data(years=[2019, 2020, 2021, 2022])
#parent_data = import_parent_companies(years=[2019, 2020, 2021, 2022])
#print(clean_data(emission_data, parent_data))

### Exercise 5
def aggregate_emissions(df: pd.DataFrame, group_vars: list) -> pd.DataFrame:
    """
    Produce the minimum, median, mean, and maximum values for the following variables aggregated
    at the level of of the variables supplied in the argument.

    Arguments:
    df: pd.DataFrame. A schema of the output of Exercise 4.
    group_var: list. A list of variables 

    Return:
    pd.DataFrame: contains the minimum, median, mean, and maximum values for the following variables
    aggregated at the level of supplied in the argument:
    total reported direct emissions
    parent co. percent ownership
    """
    # Perform the grouping and aggregation
    aggregated_df = df.groupby(group_vars).agg({
        'total reported direct emissions': ['min', 'median', 'mean', 'max'],
        'parent co. percent ownership': ['min', 'median', 'mean', 'max']
    }).sort_values(by=('total reported direct emissions', 'mean'), ascending=False)

    # Rename the columns by joining the multi-level names
    aggregated_df.columns = ['_'.join(col).strip() for col in aggregated_df.columns.values]

    # Return the sorted DataFrame
    return aggregated_df.reset_index()

# check
# emission_data = import_yearly_data(years=[2019, 2020, 2021, 2022])
# parent_data = import_parent_companies(years=[2019, 2020, 2021, 2022])
# df = clean_data(emission_data, parent_data)
# group_vars = ['year']
# aggregated_data = aggregate_emissions(df, group_vars)
# print(aggregated_data.head()) 