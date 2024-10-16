import streamlit as st
import pygsheets
import pandas as pd
import os
import plotly.express as px

credenciais = pygsheets.authorize(service_file=os.getcwd() + "/cred.json")  
meuArquivoGoogleSheets = "https://docs.google.com/spreadsheets/d/1-hDmyHWE65h8PoJD5kVNpKcYff8TIhELQWRHm2gwSo0/edit?gid=1842976394#gid=1842976394"

arquivo = credenciais.open_by_url(meuArquivoGoogleSheets)
aba = arquivo.worksheet_by_title("vendas")
data = aba.get_all_values()
df = pd.DataFrame(data)

new_header = df.iloc[0] #separa a linha 1 
df = df[1:]
df.columns = new_header

df["hour"] = pd.to_datetime(df["Time"], format="%H:%M").dt.hour
 





#config da pagina web

st.set_page_config(page_title="DashBoard de Vendas", 
                   page_icon=":bar_chart:",
                   layout="wide"
                   )


st.sidebar.header("Please FIlter Here: ")
cidade = st.sidebar.multiselect(
    "Selecione a cidade:",
    options=df["City"].unique(),
    default=df["City"].unique(),
    
)
ano = st.sidebar.multiselect(
    "Selecione o ano:",
    options=df["Date"].unique()
    
)



df_selection = df.query(
    "City == @cidade & Date == @ano "
)

st.title("Dashboard de Vendas")
st.markdown("##")

st.markdown("---")

vendas_produtos_linha = (
    df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
)

barras_produto = px.bar(
    vendas_produtos_linha,
    x="Total",
    y=vendas_produtos_linha.index,
    orientation="h",
    title = "<b>Vendas por produtos</b>",
    color_discrete_sequence=["#0083B8"] * len(vendas_produtos_linha.index),
    template="plotly_white",

)


vendas_por_hora = df_selection.groupby(by=["hour"]).sum()[["Total"]]

barras_produto_hora = px.bar(
    vendas_por_hora,
    x=vendas_por_hora.index,
    y="Total",
    orientation="v",
    title = "<b>Vendas por hora</b>",
    color_discrete_sequence=["#0083B8"] * len(vendas_por_hora.index),
    template="plotly_white",

)


left_column, right_column = st.columns(2)
left_column.plotly_chart(barras_produto_hora, use_container_width=True)
right_column.plotly_chart(barras_produto, use_container_width=True)


