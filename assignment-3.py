#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Exercise 0
def github() -> str:
    """
    Some docstrings.
    """

    return "https://github.com/<Vicky-gqc>/<ECON-481>/blob/main/<assignment-3.py>"


# In[10]:


#Exercise 1
import pandas as pd

url_19 = 'https://raw.githubusercontent.com/Vicky-gqc/ECON-481/main/ghgp/ghgp_data_2019.xlsx'
url_20 = 'https://raw.githubusercontent.com/Vicky-gqc/ECON-481/main/ghgp/ghgp_data_2020.xlsx'
url_21 = 'https://raw.githubusercontent.com/Vicky-gqc/ECON-481/main/ghgp/ghgp_data_2021.xlsx'
url_22 = 'https://raw.githubusercontent.com/Vicky-gqc/ECON-481/main/ghgp/ghgp_data_2022.xlsx'

df_19 = pd.read_excel(url_19, sheet_name = 'Direct Emitters', skiprows=3, names=pd.read_excel('https://raw.githubusercontent.com/Vicky-gqc/ECON-481/main/ghgp/ghgp_data_2019.xlsx', nrows=4).iloc[2])
df_19['year'] = 2019
df_20 = pd.read_excel(url_20, sheet_name = 'Direct Emitters', skiprows=3, names=pd.read_excel('https://raw.githubusercontent.com/Vicky-gqc/ECON-481/main/ghgp/ghgp_data_2020.xlsx', nrows=4).iloc[2])
df_20['year'] = 2020
df_21 = pd.read_excel(url_21, sheet_name = 'Direct Emitters', skiprows=3, names=pd.read_excel('https://raw.githubusercontent.com/Vicky-gqc/ECON-481/main/ghgp/ghgp_data_2021.xlsx', nrows=4).iloc[2])
df_21['year'] = 2021
df_22 = pd.read_excel(url_22, sheet_name = 'Direct Emitters', skiprows=3, names=pd.read_excel('https://raw.githubusercontent.com/Vicky-gqc/ECON-481/main/ghgp/ghgp_data_2022.xlsx', nrows=4).iloc[2])
df_22['year'] = 2022

def import_yearly_data(years: list) -> pd.DataFrame:
    """
    Extract excel sheets from my github repository.
    Read excel sheets for each year's data, select sheet and skip rows, assign row 4 names as names.
    Add a new column with their respective years.
    Concatenate these dataframes.
    
    """
    df_names = [df_19, df_20, df_21, df_22]
    df = pd.concat(df_names, axis=0, ignore_index=True)
    
    years = df_names
    return df

years = [df_19, df_20, df_21, df_22]
print(import_yearly_data(years))


# In[30]:


#Exercise 2
import pandas as pd

url_parent = 'https://raw.githubusercontent.com/Vicky-gqc/ECON-481/main/ghgp_data_parent_company_09_2023.xlsb'
    
years_list = list(range(2010, 2023))
results = {}
years = years_list

for year in years_list:
    result = pd.read_excel(url_parent, sheet_name = str(year))
    result[year] = int(year)
    # Store the result in the dictionary with the year as the key
    results[year] = result[~pd.isna(result)]
        
def import_parent_companies(years: list) -> pd.DataFrame:
    """
    Access the excel file from my github repository.
    Since the tabs are from 2010 to 2022, therefore years_list.
    There are many years, so I used for loop to add the year to each tab/dataframe.
    Store them in dictionary, stack their values vertically, concatenate. 
    """
        
    concatenated_df = pd.concat(results.values(), axis = 0, ignore_index=True)
           
    return concatenated_df

#eg
print(import_parent_companies(years))


# In[58]:


#Exercise 3
def n_null(df: pd.DataFrame, col: str) -> int:
    """
    Returns to the number of null values in a selected column in a dataframe. 
    """
    null_count = df[col].isna().sum()

    return null_count

#eg
url_19 = 'https://raw.githubusercontent.com/Vicky-gqc/ECON-481/main/ghgp/ghgp_data_2019.xlsx'
df_19 = pd.read_excel(url_19, 
                      sheet_name = 'Direct Emitters', 
                      skiprows=3, 
                      names=pd.read_excel('https://raw.githubusercontent.com/Vicky-gqc/ECON-481/main/ghgp/ghgp_data_2019.xlsx', nrows=4).iloc[2])

n_null(df = df_19, col = 'FRS Id')
n_null(df = df_19, col = 'Facility Id')

#It would be a better choice to choose 'Facility Id' for joining our data.
#By comparing the number of null values for columns 'FRS Id' and 'Facility Id', we observe that the column 'Facility Id' has 0 null values.


# In[27]:


#Exercise 4

years = [df_19, df_20, df_21, df_22]
emissions_data = import_yearly_data(years)

years_list = list(range(2010, 2023))
parent_data = import_parent_companies(years_list)


def clean_data(emissions_data: pd.DataFrame, parent_data: pd.DataFrame) -> pd.DataFrame:
    """
    Some docstrings.
    """

    # Left join parent companies data onto emissions data
    merged_data = pd.merge(emissions_data, parent_data, how='left',
                           left_on=['year', 'Facility Id'],
                           right_on=['year', 'Facility Id'])

    # Subset to specific columns
    cleaned_data = merged_data.loc[['Facility Id', 'year', 'State', 'Industry Type (sectors)',
                                'Total reported direct emissions', 'PARENT CO. STATE',
                                'PARENT CO. PERCENT OWNERSHIP']]

    # Rename columns to lower case
    cleaned_data.columns = map(str.lower, cleaned_data.columns)

    return cleaned_data


# In[ ]:


#Exercise 5

def aggregate_emissions(df: pd.DataFrame, group_vars: list) -> pd.DataFrame:
    """
    Aggregate emissions data by specified variables and compute statistics.
    
    """
    
    # Aggregate data by group_vars and compute statistics
    aggregated_data = df.groupby(group_vars).agg({
        'total reported direct emissions': ['min', 'median', 'mean', 'max'],
        'parent co. percent ownership': ['min', 'median', 'mean', 'max']
    })
    
    # Flatten multi-level column index
    aggregated_data.columns = [' '.join(col).strip() for col in aggregated_data.columns.values]
    
    # Sort by highest to lowest mean total reported direct emissions
    aggregated_data = aggregated_data.sort_values(by='total reported direct emissions mean', ascending=False)
    
    return aggregated_data

