#!/usr/bin/env python
# coding: utf-8

# In[1]:


def github() -> str:
    """
    Some docstrings.
    """

    return "https://github.com/Vicky-gqc/ECON-481/blob/main/assignment-1.py"


# In[61]:


#Exercise 2

def evens_and_odds(n: int) -> dict:
    """
    Returns a dictionary with the sum of even and odd numbers less than n.
    """
    evens_and_odds = {'evens': 0, 'odds': 0}
    for num in range(n+1):
        if num % 2 == 0:  # Check if the number is even
            evens_and_odds['evens'] += num
        else:
            evens_and_odds['odds'] += num
    return evens_and_odds

evens_and_odds(7)


# In[23]:


#Exercise 3

from typing import Union
from datetime import datetime

def time_diff(date_1: str, date_2: str, out: str) -> Union[str,float]:
    """
    Returns the time difference between two dates.
    """
    dt1 = datetime.strptime(date_1, "%Y-%m-%d")
    dt2 = datetime.strptime(date_2, "%Y-%m-%d")
    
    delta = abs(dt2 - dt1).days
    
    if out == 'string':
        return f"There are {delta} days between the two dates"
    else:
        return delta

print(time_diff('2020-01-01', '2020-01-02', 'float'))
print(time_diff('2020-01-03', '2020-01-01', 'string'))


# In[ ]:


#Exercise 4

def reverse(in_list: list) -> list:
    """
    Returns a list with elements in reverse order.
    """

    start = 0
    end = len(in_list) - 1
    
    while start < end: #Ensure that the swapping stops when reaching the middle term
        # Swap elements at start and end positions
        in_list[start], in_list[end] = in_list[end], in_list[start]
        
        start += 1
        end -= 1
    
    return in_list


# In[37]:


#Exercise 5

def factorial(num: int) -> int:
    """
    Returns the factorial of a non-negative integer.
    """
    if num == 0:
        return 1
    else:
        result = 1
        for i in range(1, num + 1):
            result *= i
        return result

def n_choose_k(n: int, k: int) -> int:
    """
    Returns the binomial coefficient "n choose k".
    """
    return factorial(n) // (factorial(k) * factorial(n - k))

def prob_k_heads(n: int, k: int) -> float:
    """
    Returns the probability of getting k heads from n flips.
    """
    p = 0.5  # Probability of getting a single head (fair coin)
    probability = n_choose_k(n, k) * (p ** k) * ((1 - p) ** (n - k))
    return probability

