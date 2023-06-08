from bs4 import BeautifulSoup
import re

# Load the HTML file
with open('main.html', 'r') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

table = soup.find('table', id='ranking')

with open('table.html', 'w') as f:
    f.write(str(table))
    

# Load the HTML file
with open('table.html', 'r') as f:
    html = f.read()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Find the table with id="ranking"
table = soup.find('table', id='ranking')

# Get the tbody element and select only the first-level tr elements
tbody = table.find('tbody')
rows = tbody.select('tr:not(tr tr)')

# Iterate through every 3 rows, starting with the first row
uni_infos = []
for i in range(0, len(rows), 3):
    # Get the first tr element in the group of 3 rows
    row = rows[i]

    # Extract the string information from the four td elements in the tr
    cells = row.find_all('td')
    rank = cells[0].get_text()
    name = cells[1].get_text()
    score = cells[2].get_text()
    faculty = cells[3].get_text()
    rank = ' '.join(rank.split())
    rank = int(re.sub(r'[^A-Za-z0-9 ]+', '', rank))
    name = ' '.join(name.split())
    name = re.sub(r'[^A-Za-z0-9 ]+', '', name).strip()
    score = ' '.join(score.split())
    score = float(re.sub(r'[^A-Za-z0-9. ]+', '', score))
    faculty = ' '.join(faculty.split())
    faculty = int(re.sub(r'[^A-Za-z0-9 ]+', '', faculty))
    info = [rank, name, score, faculty]
    uni_infos.append(info)

import pandas as pd
df = pd.DataFrame(uni_infos, columns =['rank', 'uni_name', 'count', 'faculty']) 


# Find all the ids containing "-faculty"
div_ids = [e.get('id') for e in soup.find_all(lambda tag: tag.get('id') and '-faculty' in tag.get('id'))]

clean_div_ids = [re.sub(r'[^A-Za-z]+', ' ', name).replace('faculty', '').strip() for name in div_ids]
import difflib

def find_best_match(name):
    return difflib.get_close_matches(name,div_ids, cutoff=0.3)[0]
df['div_ids'] = df['uni_name'].apply(find_best_match)

df.to_csv('uni_infos.csv')

# Extract the table data into a list of dictionaries
data = []
for row in table.find_all('tr')[1:]:
    cols = row.find_all('td')
    print(len(cols))
