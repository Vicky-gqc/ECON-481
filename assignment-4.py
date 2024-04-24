#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Exercise 0
def github() -> str:
    """
    Some docstrings.
    """

    return "https://github.com/<Vicky-gqc>/<ECON-481>/blob/main/<assignment-3.py>"


# In[2]:


#Exercise 1
import pandas as pd

def load_data() -> pd.DataFrame:
    """
    Some docstrings.
    """
    data = pd.read_csv("https://lukashager.netlify.app/econ-481/data/tsla.csv")
    tsla = pd.DataFrame(data)
    return tsla

print(load_data())
tsla = load_data()
type(tsla)
tsla.columns
tsla.isna().sum()
tsla.index
type(tsla["Date"])


# In[3]:


#Exercise 2
import matplotlib.pyplot as plt

def plot_close(df: pd.DataFrame, start: str = '2010-06-29', end: str = '2024-04-15') -> None:
    """
    Some docstrings
    """
    start = str(tsla["Date"][[0]])
    end = str(tsla["Date"][[3471]])
    tsla_2 = tsla.set_index(keys = tsla["Date"], drop = False, inplace = False)
    plot = tsla_2['Close'].plot(title = "Tesla Closing Stock Price from 2010-06-29 to 2024-04-15")
    
    return None

tsla_2 = tsla.set_index(keys = tsla["Date"], drop = False, inplace = False)
print(plot_close(df = tsla_2))
tsla_2.index


# In[9]:


#Exercise 3
import statsmodels.api as sm
import statsmodels.formula.api as smf
import numpy as np
    
tsla["delta_x_t"] = tsla["Close"].diff()
tsla["delta_x_t1"] = tsla["Close"].diff().diff()

tsla.fillna(inplace = True, value = 0)
df = smf.ols('delta_x_t ~ delta_x_t1', data=tsla).fit(cov_type = "HC1")

def autoregress(df: pd.DataFrame) -> float:
    """
    Some docstrings.
    """
    df = smf.ols('delta_x_t ~ delta_x_t1', data=tsla).fit(cov_type = "HC1")

    return df.tvalues

print(autoregress(tsla))


# In[32]:


#Exercise 4
from sklearn.linear_model import LogisticRegression
import numpy as np


def autoregress_logit(df: pd.DataFrame) -> float:
    """
    Convert x_train and y_train sets in to numpy arrays.
    Separate them into bins (negative and positive) because continuous variable cannot be used on logistic regression.
        -> Why negative and positive? because the hypothesis tries to test the correlation between delta_x_t and delta_x_t1, so if\
        both the explanatory and the explained variables move in the same direction, then they are correlated and we accept the alternative\
        hypothesis. 
    Fit the model.
    Calculate the T-statistic manually
    """
    model = LogisticRegression()

    predictor = ["delta_x_t1"]
    X_train = tsla[predictor].to_numpy()
    y_train = tsla["delta_x_t"].to_numpy()
    y_train_bins = pd.cut(y_train, bins=[-float("inf"), 0, float("inf")], labels=["Negative", "Positive"])
    model.fit(X_train, y_train_bins)
    beta_0 = model.coef_
    se_0 = ( (tsla["delta_x_t1"].std()) ) / np.sqrt(len(tsla["delta_x_t1"]))
    tstat = beta_0 / se_0
    
    return tstat

print(autoregress_logit(tsla))


# In[48]:


#Exercise 5
import matplotlib.pyplot as plt

def plot_delta(df: pd.DataFrame) -> None:
    """
    Some docstrings.
    """
    graph = plt.scatter(tsla["delta_x_t1"], tsla["delta_x_t"], linewidths = 0.5, alpha = 0.7)
    return None


graph = plt.scatter(tsla["delta_x_t1"], tsla["delta_x_t"], linewidths = 0.5, alpha = 0.7)


# In[ ]:




