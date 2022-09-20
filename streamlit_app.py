from cProfile import label
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objs as pg
from time import sleep, time
from funciones import between_date2, gen_acum2

from scrap import covid_numbers

st.set_page_config(layout="wide")

col1, col2, col3 = st.columns(3)
@st.cache
def co_numbers():
    c1 = covid_numbers()[0]
    c2 = covid_numbers()[1]
    c3 = covid_numbers()[2]
    return[c1,c2,c3]
#Título
st.header("Impacto de COVID-19 en la Capacidad Hospitalaria\n\n")

with col1:
    st.metric(label = "Casos de Coronavirus",
              value = co_numbers()[0],
              delta = +132)

with col2:
    st.metric(label = "Muertes",
              value = co_numbers()[1],
              delta = +145)

with col3:
    st.metric(label = "Recuperados",
              value = co_numbers()[2],
              delta = +220)


#1 DF por estado
# df = pd.read_csv('COVID-19_Reported_Patient_Impact_and_Hospital_Capacity_by_State_Timeseries.csv')
# df.date = pd.to_datetime(df.date)
# normalize(df)
@st.cache
def get_data():

    df = pd.read_csv('COVID-19_Reported_Patient_Impact_and_Hospital_Capacity_by_State_Timeseries.csv')
    df.date = pd.to_datetime(df.date)
    dates = df['date']
    df.fillna(0, inplace=True)
    df.sort_values(by='date', inplace=True)
    df.reset_index(drop=True, inplace=True)
    df = df.astype('int32', errors='ignore')

    dates = df['date']

    df1 = df[['state',
          'date',
          'deaths_covid',
          'inpatient_beds_used_covid',
          'total_adult_patients_hospitalized_confirmed_covid',
          'total_pediatric_patients_hospitalized_confirmed_covid',
          'adult_icu_bed_covid_utilization_numerator'
        ]]
    df1['total_hospitailzed_confirmed'] = df[['total_adult_patients_hospitalized_confirmed_covid',
                                            'total_pediatric_patients_hospitalized_confirmed_covid']].sum(axis=1)
    df1['total_hospitailzed_confirmed'] = df1['total_hospitailzed_confirmed'].astype('int64')
    df1.drop(columns=(['total_adult_patients_hospitalized_confirmed_covid','total_pediatric_patients_hospitalized_confirmed_covid']), inplace=True)

    df1 = gen_acum2(df1,'total_hospitailzed_confirmed','Hospitalizaciones por COVID-19 (acumulado)')
    df1 = gen_acum2(df1,'adult_icu_bed_covid_utilization_numerator', 'Camas usadas (terapia intensiva) (acumulado)')

    df1.rename(columns={'state': 'Estado',
                        'deaths_covid': 'Muertes por COVID-19',
                        'total_hospitailzed_confirmed':'Máximo de hospitalizaciones por día en el rango temporal',
                        'inpatient_beds_used_covid': 'Camas usadas (comunes)',
                        'adult_icu_bed_covid_utilization_numerator':'Camas usadas (terapia intensiva)'
                       }, inplace=True)

    df3 = df1[['date','Estado','Camas usadas (terapia intensiva)']]

    return [df1, dates, df3]


df1 = get_data()[0]

#SELECTOR DE FECHA
dates = get_data()[1]
date_selection = st.sidebar.slider('Fecha:',
                            min_value= dates.max().date(),  
                            max_value= dates.max().date(),
                            value=(dates.min().date(),dates.max().date()))
df1 = between_date2(df1,str(date_selection[0]),str(date_selection[1]))

#MAPA
st.subheader("Valores para EEUU")
options = df1.drop(columns=(['Estado','date'])).columns.to_list()
map_selection = st.selectbox(label= 'Seleccionar datos de:',options=options)

quant = ['Muertes por COVID-19']

def df_map_selector(df,x,z):

    #z = x
    x = ['date','Estado',x]

    if z in quant:
        df_state = df[x].drop(columns='date').groupby('Estado').sum()
        colorbar = 'Cantidad'

    else:
        df_state = df[x].drop(columns='date').groupby('Estado').max()
        colorbar = 'Max'

    st.metric(
        label=f"TOTAL",
        value=df_state.sum()
        )

    c = options.index(z)
    colors = ['Reds','Blues','Greens','Purples','Oranges','armyrose']
    color = colors[c]

    data = dict(type = 'choropleth', 
                locations = df_state.index, 
                locationmode = 'USA-states', 
                z = df_state[z], 
                colorscale = color, 
                colorbar = {'title' : colorbar},)

    layout = dict(geo = dict(scope='usa' , 
                  showlakes = True, 
                  lakecolor = 'rgb(0,191,255)'))
    
    mapa = pg.Figure(data = [data], 
                     layout = layout)
    
    mapa.update_layout(
        autosize=False,
        width=500,
        height=500,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=6
        ),
    paper_bgcolor="DarkGray",
    )

    st.plotly_chart(mapa, use_container_width=True)
    return df_state


df_map_selector(df1,map_selection,map_selection)

#DATAFRAME
st.subheader('Detalle')
show = df1.set_index('date')
st.dataframe(show, width=1500)

#RANKING
df3 = get_data()[0]
df3 = between_date2(df3,str(date_selection[0]),str(date_selection[1]))
df4 = df3.sort_values(by=map_selection, ascending=False).drop_duplicates('Estado')
st.sidebar.text("Top 5 estados")
if map_selection in quant:
    st.sidebar.dataframe(df3.groupby('Estado').sum().nlargest(5, map_selection)[map_selection])
else:
    st.sidebar.dataframe(df4.nlargest(5, map_selection)[['Estado',map_selection]].reset_index(drop=True))
#print(df3.set_index('Estado', drop=True, inplace = True))
#TOTAL


#RANKING ESTADOS CON MAYOR OCUPACION HOSPITALARIA

#1
#1
# df = pd.read_csv('camas_usadas.csv')
# title = st.title("Uso de camas comunes")

# fig = px.line(df, x='date', y="inpatient_beds_used_covid")
# fig.update_xaxes(
#     rangeslider_visible=True,
#     rangeselector=dict(
#         buttons=list([
#             dict(count=1, label="1w", step="week", stepmode="backward"),
#             dict(count=6, label="1m", step="month", stepmode="backward"),
#             dict(step="all")
#         ])
#     )
# )
# st.plotly_chart(fig, use_container_width=True)



#3

#st.dataframe(df)