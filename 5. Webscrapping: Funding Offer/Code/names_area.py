import pandas as pd
import re

df = pd.read_csv('final_output.csv')


def get_areas(s):
    lowercase_words = re.findall(r'\b[a-z]\w*\b', s)
    if len(lowercase_words) == 0:
        return  'unknown'
    else:
        return ','.join(lowercase_words)

   
def get_name(s):
    lowercase_words = re.findall(r'\b[a-z]\w*\b', s)
    if len(lowercase_words) == 0:
        return  s
    else:
        for word in lowercase_words:
            s = re.sub(r'\b{}\b'.format(word), '', s)
        return re.sub(r'[^a-zA-Z ]+', '', s).strip()
df['Area'] = df['Faculty Name'].apply(get_areas)
df['Faculty Name'] = df['Faculty Name'].apply(get_name)
