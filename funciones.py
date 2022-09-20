import pandas as pd
import numpy as np
import plotly.express as px
from scipy.signal import argrelextrema


def between_date2(data,start,end):
    mask = (data['date'] >= start) & (data['date'] <= end)
    return data.loc[mask]

def only_state2(data,state):
    mask = (data['state'] == state)
    return data.loc[mask]

def gen_acum(df1):
    #genera acumulativo (de hospitalizados) por estado y lo ingesta en dataframe.
    #el dataframe ingresado debe tener las columnas 'state' y 'total_hospitailzed_confirmed' y estar ordenado por fecha.

    estados = df1['state'].unique()

    for estado in estados:
        #print(estado)
        df2 = only_state2(df1,estado)
        index = df2['total_hospitailzed_confirmed'].index
        arr = df2['total_hospitailzed_confirmed'].reset_index(drop=True).astype('int32')

        acumulados = [arr[0],]
        a = arr[0]
        for i in range(len(arr)-1):
            if arr[i+1] > arr[i]:
                diff = arr[i+1]-arr[i]
                a += diff
                acumulados.append(a)
            else:
                a = a
                acumulados.append(a)

        ingresados = pd.DataFrame(dict({'index': index,
                                    'Ingresados': acumulados}))
        ingresados.set_index('index', inplace=True)
        for i in ingresados.index:
            df1.loc[i,'total_hospitailzed_confirmed'] = ingresados.loc[i,'Ingresados']

    return df1

def gen_acum2(df1,column, new_column):
#genera acumulativo por estado y lo ingesta en dataframe.
#el dataframe ingresado debe tener las columnas 'state' y estar ordenado por fecha.

    estados = df1['state'].unique()

    for estado in estados:
        #print(estado)
        df2 = only_state2(df1,estado) #dejamos los valores de un solo estado
        index = df2[column].index # guardamos el índice para luego ingestar en el df original
        arr = df2[column].reset_index(drop=True).astype('int32')

        acumulados = [arr[0],]
        a = arr[0]
        for i in range(len(arr)-1): 
            if arr[i+1] > arr[i]: #si el valor siguiente es mayor
                diff = arr[i+1]-arr[i] # obtenemos la diferencia
                a += diff #Se suma la difenrencia entre valores contiguos si el valor aumenta
                acumulados.append(a) 
            else:
                a = a
                acumulados.append(a)

        ingresados = pd.DataFrame(dict({'index': index,
                                    'Ingresados': acumulados}))
        ingresados.set_index('index', inplace=True)
        for i in ingresados.index:
            df1.loc[i,new_column] = ingresados.loc[i,'Ingresados']

    return df1

def local_extremes(df, column, n=100):
    # Genera columna con valores extremos. Devulve lista de fechas donde se encuentran esos valores extremos
    df['min'] = df.iloc[argrelextrema(df[column].values, np.less_equal,
                    order=n)[0]][column]
    df['max'] = df.iloc[argrelextrema(df[column].values, np.greater_equal,
                        order=n)[0]][column]
    minimos = list(df.dropna(subset='min').reset_index(drop=True)['date'])
    maximos = list(df.dropna(subset='max').reset_index(drop=True)['date'])

    lista = minimos+maximos
    lista.sort()
    lista
    return lista

def add_regions(df,fig,lista):
    # Grafica regiones a partir de valores extremos
    # !!ARREGLAR PARES
    c = 0
    while c < len(lista)-1:

        fig.add_vrect(
            x0= lista[c].strftime("%Y-%m-%d"), x1= lista[c+1].strftime("%Y-%m-%d"),
            fillcolor="LightGreen", opacity=1,
            layer="below", line_width=0,
        )

        fig.add_vrect(
            x0= lista[c+1].strftime("%Y-%m-%d"), x1= lista[c+2].strftime("%Y-%m-%d"),
            fillcolor="LightSalmon", opacity=1,
            layer="below", line_width=0,
        )
        c +=2

    fig.add_scatter(x=df['date'],y= df['min'], mode='markers')
    fig.add_scatter(x=df['date'],y= df['max'], mode='markers')
    return fig