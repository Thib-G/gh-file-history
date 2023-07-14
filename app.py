import streamlit as st
import requests
import pandas as pd
import re

st.set_page_config(page_title='AI-pocratic oath')

repo_url = 'https://github.com/virginiemarelli/AI-ethic-oath'

st.markdown(f"""
    Source: {repo_url}
""")

@st.cache_data
def get_readme():
    r = requests.get('https://raw.githubusercontent.com/virginiemarelli/AI-ethic-oath/main/README.md')
    return r.text.replace('AIEthicOath.md', 'https://github.com/virginiemarelli/AI-ethic-oath/blob/main/AIEthicOath.md')


st.write(get_readme())
         


pattern = r'^https:\/\/github.com\/(.+)\/(.+)'
p = re.compile(pattern)
matches = p.findall(repo_url)
owner, repo = matches[0]

branch = 'main'


# st.write(f"""
# - owner: {owner}
# - repo: {repo}
# - branch: {branch}
# """)


url = f'https://api.github.com/repos/{owner}/{repo}/commits?sha=main'


st.write("""
## They have pledged:
(filtered on commits where the message is `I pledge`)
""")
st.write(f'URL: `{url}`')

r = requests.get(url)

# st.write(r.json())

commits_flat = [
    {
        'Message': row.get('commit').get('message'),
        'Github author': row.get('author').get('login', '?') if row.get('author') else '?',
        'Commit author': row.get('commit').get('author').get('name'),
        'Date': row.get('commit').get('author').get('date'),
        'Link': row.get('html_url'),
    }
    for row
    in r.json()
]

df = pd.DataFrame(commits_flat)

st.dataframe(
    df[df['Message'] == 'I pledge'].reset_index(drop=True),
    column_config={
        'Link': st.column_config.LinkColumn()
    }
)
