import streamlit as st
import requests
import pandas as pd
import re

st.write("""
    # Extract commit history
""")
         
file_url = st.text_input('Enter link to repo on GitHub', value='https://github.com/virginiemarelli/AI-ethic-oath')

pattern = r'^https:\/\/github.com\/(.+)\/(.+)'
p = re.compile(pattern)
matches = p.findall(file_url)
owner, repo = matches[0]

branch = 'main'


st.write(f"""
 - owner: {owner}
 - repo: {repo}
 - branch: {branch}
""")


url = f'https://api.github.com/repos/{owner}/{repo}/commits?sha=main'

st.write(f'URL: `{url}`')

r = requests.get(url)

# st.write(r.json())

commits_flat = [
    {
        'message': row.get('commit').get('message'),
        'github author': row.get('author').get('login', '?') if row.get('author') else '?',
        'commit author': row.get('commit').get('author').get('name'),
        'date': row.get('commit').get('author').get('date'),
        'html_url': row.get('html_url'),
    }
    for row
    in r.json()
]

df = pd.DataFrame(commits_flat)

st.write(df)