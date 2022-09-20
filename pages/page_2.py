import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from funciones import gen_acum2, between_date2, only_state2, local_extremes, add_regions
from scrap import covid_numbers

# col1, col2, col3 = st.columns(3)
# @st.cache
# def co_numbers():
#     c1 = covid_numbers()[0]
#     c2 = covid_numbers()[1]
#     c3 = covid_numbers()[2]
#     return[c1,c2,c3]

# with col1:
#     st.metric(label = "Casos de Coronavirus",
#               value = co_numbers()[0],
#               delta = -132)

# with col2:
#     st.metric(label = "Muertes",
#               value = co_numbers()[1],
#               delta = -145)

# with col3:
#     st.metric(label = "Recuperados",
#               value = co_numbers()[2],
#               delta = +220)

st.header("Impacto de COVID-19 en la Capacidad Hospitalaria\n\n")
st.subheader("Uso de camas en el período 2020-03-20 / 2021-06-15 (Cuarentena NY)")

df = pd.read_csv('COVID-19_Reported_Patient_Impact_and_Hospital_Capacity_by_State_Timeseries.csv')
df.date = pd.to_datetime(df.date)
#dates = df['date']
df.fillna(0, inplace=True)
df.sort_values(by='date', inplace=True)
df.reset_index(drop=True, inplace=True)
df = df.astype('int32', errors='ignore')
df2 = df[['state',
        'date',
        'deaths_covid',
        'inpatient_beds_used_covid']]
#print(df2)
#st.dataframe(df2)
#Selector
options = df2.drop(columns=(['state','date'])).columns.to_list()
states = df2['state'].unique().tolist()
map_selection = st.selectbox(label= 'Seleccionar feature',options=options)
state_selection = st.selectbox(label='Selecionar Estado', options=states)
periodos = st.selectbox(label='Gráfico', options=['Simple','Tendencias'])

def state_selector(df,state,map_selection):

    df2 = only_state2(df,state)
    df2 = between_date2(df2,'2020-03-20','2021-06-15')

    lista = local_extremes(df2, map_selection)

    fig = px.line(df2, x='date', y=df2[map_selection], width=1500, height=500)
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,255,0.1)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,255,0.1)')

    if periodos == 'Simple':
        st.plotly_chart(fig)
    else:
        st.plotly_chart(add_regions(df2,fig,lista))

state_selector(df2,state_selection,map_selection)