import streamlit as st
import requests
import pandas as pd
import re

st.write("""
    # Extract commit history
""")
         
file_url = st.text_input('Enter link to file on GitHub', value='https://github.com/Thib-G/pasevident.be/blob/main/src/assets/sentences/index.js')

pattern = r'^https:\/\/github.com\/(.+)\/(.+)\/blob\/main\/(.+)$'
p = re.compile(pattern)
matches = p.findall(file_url)
owner, repo, path = matches[0]


st.write(f"""
 - owner: {owner}
 - repo: {repo}
 - path: {path}
""")


url = f'https://api.github.com/repos/{owner}/{repo}/commits?sha=main&path=/{path}'

r = requests.get(url)

# st.write(r.json())

commits_flat = [
    {
        'message': row.get('commit').get('message'),
        'author': row.get('commit').get('author').get('name'),
        'date': row.get('commit').get('author').get('date'),
        'html_url': row.get('html_url'),
    }
    for row
    in r.json()
]

df = pd.DataFrame(commits_flat)

st.write(df)