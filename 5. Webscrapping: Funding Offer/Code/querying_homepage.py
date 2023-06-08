import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import re
import matplotlib.pyplot as plt
from tqdm import tqdm
from urllib.error import URLError
import time
from selenium.common.exceptions import WebDriverException

# Set up Selenium web driver with headless Chrome
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(3)

search_terms = ['openings', 'self-motivated', 'graduate student position', 'research assistantship', 'postdoctoral fellowship',
                'research grants', 'fellowships', 'scholarships', 'strong research skills', 'ability to work independently', 'prior research experience']

df = pd.read_csv('three_uni.csv')
df['providing_assitantship'] = 0
df['matched_ratio'] = 0
df['match_words'] = ""

for i in tqdm(range(len(df))):
    if i > 0 and df.loc[i-1, 'faculty_home_page'] == df.loc[i, 'faculty_home_page']:
        df.loc[i, 'providing_assitantship'] = df.loc[i-1, 'providing_assitantship']
        df.loc[i, 'matched_ratio'] = df.loc[i-1, 'matched_ratio']
    df.loc[i, 'faculty_home_page']
    url = df.loc[i, 'faculty_home_page']
    retry_count = 0
    while retry_count < 3:
        try:
            driver.get(url)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            html = soup.prettify()
            html = str(html).lower()
            count = 0
            matched = ""
            for s in search_terms:
                if s in html:
                    df.loc[i, 'providing_assitantship'] = 1
                    count += 1
                    matched = s + ', '
            df.loc[i, 'matched_ratio'] = count / len(search_terms)
            df.loc[i, 'match_words'] = matched
            break
        except (URLError, WebDriverException) as e:
            retry_count += 1
            print(f"Error: {e}. Retrying in 2 seconds...")
            time.sleep(2)
    if retry_count >= 3:
        print(f"Failed to retrieve data for URL: {url}")

driver.quit()
