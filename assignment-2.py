#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Exercise 0

def github() -> str:
    """
    Some docstrings.
    """
    return "https://github.com/Vicky-gqc/ECON-481/blob/main/assignment-2.py"


# In[3]:


#Exercise 1
import numpy as np

def simulate_data(seed: int) -> tuple:
    """
    Simulate data according to the specified data generating process.

    Parameters:
        seed (int): Seed for random number generation (default is 481).

    Returns:
        tuple: A tuple of two elements, (y, X), where y is a 1000*1 numpy array and X is a 1000*3 numpy array.
    """
    np.random.seed(seed = 481)

    # Generate X matrix
    X = np.random.normal(loc=0, scale=np.sqrt(2), size=(1000, 3))

    # Generate error term
    e = np.random.normal(loc=0, scale=1, size=(1000, 1))

    # Generate y
    y = 5 + 3*X[:, 0].reshape(-1, 1) + 2*X[:, 1].reshape(-1, 1) + 6*X[:, 2].reshape(-1, 1) + e

    return y, X

simulate_data(481)


# In[4]:


#Exercise 2

import numpy as np
import scipy as sp

def neg_log_likelihood(params, y, X):
    beta_0, beta_1, beta_2, beta_3 = params
    y_hat = beta_0 + np.dot(X, np.array([beta_1, beta_2, beta_3]))
    e_i = y - y_hat
    ll = -0.5 * np.sum(e_i**2) # Taking the log of the PDF
    return -ll  # Negate to convert likelihood to negative log-likelihood

def estimate_mle(y, X):
    initial_guess = np.zeros(4) # We begin by assuming the coeffients are 0
    result = sp.optimize.minimize(neg_log_likelihood, initial_guess, args=(y, X), method='Nelder-Mead')
    return result.x


# In[5]:


#Exercise 3
import numpy as np
import scipy as sp

def ols_estimate(X, y):
    # Define the objective function (sum of squared errors)
    def objective(beta):
        y_hat = np.dot(X, beta[:-1]) + beta[-1] 
        return np.sum((y_hat - y) ** 2)
    
    # Initial guess for the coefficients
    initial_guess = np.zeros(X.shape[1] + 1)
    
    # Minimize the objective function
    result = sp.optimize.minimize(objective, initial_guess)
    
    # Extract the coefficients from the result
    coefficients = result.x
    
    return coefficients

