#Preguntas a responder
#¿Cual es el % de ventas historicas de los distintos articulos?
#Del item más vendido, ¿en que mes se vende más?
#¿Cuantos articulos de los mas vendidos se deberian comprar en marzo del 2022?

import pandas as pd
import numpy as np

def run():
    dir_ventas = './datos/{}'.format('ventas.csv')
    df_ventas = pd.read_csv(dir_ventas, sep=";")

    total_ventas = df_ventas['unidades_vendidas'].sum()
    df_item_ventas = df_ventas[['item','unidades_vendidas']].groupby(['item']).sum()
    df_item_prc_ventas = df_item_ventas.applymap(lambda x:100*x/total_ventas)
    
    item_mas_vendido = df_item_prc_ventas.idxmax(axis=0).values[0]
    otro_item = 'jeans_black'

    df_item_mes_ventas = df_ventas[['item','mes','unidades_vendidas']].groupby(['item','mes']).mean()
    top_mes = df_item_mes_ventas.query('item == @item_mas_vendido').idxmax(axis=0).values[0][1]
    
    marzo = 'Marzo'
    df_nacional_marzo = df_ventas[['item','mes','anio','unidades_vendidas']].query('item == @item_mas_vendido and mes == @marzo').groupby(['item','anio']).sum()
    df_promedio_nacional_marzo = df_nacional_marzo.groupby(['item']).mean()
    df_desvest_nacional_marzo = df_nacional_marzo.groupby(['item']).std()

    pnm_mean = df_promedio_nacional_marzo.values[0,0]
    pnm_std = df_desvest_nacional_marzo.values[0,0]

    sugerencia_menor = pnm_mean-pnm_std
    sugerencia_mayor = pnm_mean+pnm_std
    
    #Respuestas
    print("El porcentaje de ventas de los distintos articulos se adjunta a continuacion:")
    print(df_item_prc_ventas)
    print("-----")
    print("El articulo mas vendido es: ",item_mas_vendido)
    print("El mes donde este articulo mas se vende es: ",top_mes)
    print("-----")
    print(f"Considerando que las ventas son ciclicas por temporada y que la desviacion estandar ({np.around(pnm_std,1)}) es pequeña frente a la media ({np.around(pnm_mean,1)}).")
    print(f"Podemos pronosticar que la venta de marzo 2022 sera entre {np.around(sugerencia_menor,1)} y {np.around(sugerencia_mayor,1)}")

if __name__ == "__main__":
    run()