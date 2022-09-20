import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from funciones import gen_acum2, between_date2, only_state2, local_extremes, add_regions

st.header("Impacto de COVID-19 en la Capacidad Hospitalaria\n\n")
st.subheader("Correlación de variables (año 2021)")

df = pd.read_csv('COVID-19_Reported_Patient_Impact_and_Hospital_Capacity_by_State_Timeseries.csv')
df.date = pd.to_datetime(df.date)
#dates = df['date']
df.fillna(0, inplace=True)
df.sort_values(by='date', inplace=True)
df.reset_index(drop=True, inplace=True)
df = df.astype('int32', errors='ignore')

df7 = between_date2(df[['date',
                        'state',
                        'critical_staffing_shortage_today_yes',
                        'deaths_covid',
                        'icu_patients_confirmed_influenza',
                        'on_hand_supply_therapeutic_a_casirivimab_imdevimab_courses',
                        'on_hand_supply_therapeutic_b_bamlanivimab_courses',
                        'on_hand_supply_therapeutic_c_bamlanivimab_etesevimab_courses'
                        ]],'2021-01-01','2021-12-31')

# df7 = df[['date',
#             'state',
#             'critical_staffing_shortage_today_yes',
#             'deaths_covid',
#             'icu_patients_confirmed_influenza'
#             ]]

df7 = df7.groupby('date').sum()

options = df7.drop(columns='deaths_covid').columns.to_list()
X_selection = st.selectbox(label= 'Seleccionar variable X',options=options)

def _plot(df,X):
    fig = px.scatter(df, x=X, y='deaths_covid',width=1500, height=500, trendline='ols')
    st.plotly_chart(fig)

_plot(df7,X_selection)

st.text('Tabla de correlación')
st.dataframe(df7.corr()['deaths_covid'])