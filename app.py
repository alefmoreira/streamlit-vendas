import streamlit as st
import pygsheets
import pandas as pd
import numpy as np
import os


credenciais = pygsheets.authorize(service_file=os.getcwd() + "/cred.json")
meuArquivoGoogleSheets = "https://docs.google.com/spreadsheets/d/1-hDmyHWE65h8PoJD5kVNpKcYff8TIhELQWRHm2gwSo0/edit?gid=1842976394#gid=1842976394"

arquivo = credenciais.open_by_url(meuArquivoGoogleSheets)
aba = arquivo.worksheet_by_title("vendas")
data = aba.get_all_values()
df = pd.DataFrame(data)

st.write(df)

st.title('Vendas')




