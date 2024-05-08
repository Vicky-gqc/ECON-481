#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Exercise 0
def github() -> str:
    """
    Some docstrings.
    """

    return "https://github.com/<Vicky-gqc>/<ECON-481>/blob/main/<assignment-5.py>"


# In[ ]:


#Exercise 1
import requests
from bs4 import BeautifulSoup

urls = ['https://lukashager.netlify.app/econ-481/01_intro_to_python', 
        'https://lukashager.netlify.app/econ-481/02_numerical_computing_in_python',
        'https://lukashager.netlify.app/econ-481/03_pandas',
        'https://lukashager.netlify.app/econ-481/04_modeling_and_visualizing',
        'https://lukashager.netlify.app/econ-481/05_web_scraping',
        'https://lukashager.netlify.app/econ-481/06_writing_modules_and_testing']

# Function to extract codes from a URL
def scrape_code(url: str) -> str:
    
    for url in urls:
        response = requests.get(url)
        html_content = response.content

        soup = BeautifulSoup(html_content, 'html.parser')

        codes = []
        for div_tag in soup.find_all('div', class_='sourceCode'):
            code_text = div_tag.find('code').get_text(strip=True)
            codes.append(code_text)

        for code in codes:
            print(code)

    return scrape_code(urls)

print(scrape_code(urls))


# In[ ]:





# In[ ]:




