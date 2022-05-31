#!/usr/bin/env python3
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import pyodbc
import json


with open("config.json", "r", encoding="utf-8") as file:
    SECRET_FILE = json.load(file)

SERVER = SECRET_FILE["SERVER"]
DATABASE = SECRET_FILE["DATABASE"]
USERNAME = SECRET_FILE["USERNAME"]
PASSWORD = SECRET_FILE["PASSWORD"]
DRIVER = SECRET_FILE["DRIVER"]

# consulta a la base de datos
with pyodbc.connect('DRIVER='+DRIVER+';SERVER=tcp:'+SERVER+';PORT=1433;DATABASE='+DATABASE+';UID='+USERNAME+';PWD=' + PASSWORD) as conn:
    sql_query = f'SELECT * FROM dbo.registro_h_t'
    DF = pd.read_sql(sql_query, conn)

DF['FECHA'] = pd.to_datetime(DF['FECHA'])
end = max(DF['FECHA'])
init = end - datetime.timedelta(hours=1)
print(init)

DF = DF[DF['FECHA'] > init]

fig = make_subplots(2, 1)
fig.add_trace(go.Scatter(x=DF['FECHA'],
                         y=DF['HUMEDAD'][DF['ORIGEN'] == 'Sensor1'],
                         name='Humedad (Sensor1)',
                         mode='lines+markers'), 1, 1)
fig.add_trace(go.Scatter(x=DF['FECHA'],
                         y=DF['TEMPERATURA'][DF['ORIGEN'] == 'Sensor1'],
                         name='Temperatura (Sensor1)',
                         mode='lines+markers',
                         marker=dict(size=8, 
                                     symbol='hourglass')), 1, 1)

fig.add_trace(go.Scatter(x=DF['FECHA'],
                         y=DF['HUMEDAD'][DF['ORIGEN'] == 'Sensor2'],
                         name='Humedad (Sensor2)',
                         mode='lines+markers'), 2, 1)
fig.add_trace(go.Scatter(x=DF['FECHA'],
                         y=DF['TEMPERATURA'][DF['ORIGEN'] == 'Sensor2'],
                         name='Temperatura (Sensor2)',
                         mode='lines+markers',
                         marker=dict(size=8, 
                                     symbol='hourglass')), 2, 1)

template = 'plotly_white'
fig.update_layout(template=template, title="Temperatura C, Humedad %")

# convert it to JSON
fig_json = fig.to_json()

# a simple HTML template
template = """<html>
<head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <title>Celo send reward</title>
</head>
<body>
    <br>
    <div class="container px-4">
        <div class="mb-3 border rounded" style='padding: 16px;'>
            <h2>Datos sensores, una hora atrás</h2>
        </div>
        <div class="mb-3 border rounded" style='padding: 16px;'>
            <div id='divPlotly'></div>
            <script>
                var plotly_data = {}
                Plotly.react('divPlotly', plotly_data.data, plotly_data.layout);
            </script>
        </div>
    </div>
    <div class="container px-4">
        <div class="mb-3 border rounded" style='padding: 16px;'>
            <h3>Funcionamiento DAPP</h3>
            <p>Esta DAPP toma datos de dos sensores que miden temperatura y humedad simulan medir estas variables de un sitio deforestado, mediante un fondo se recoge dinero para poder plantar los árboles y a medida que mejore el ambiente y los sensores lo midad se reparten las recompensas entre los implicador</p>
            <p>El contrato esta identificado como 0x7648d3fb14aa44A60C5713c1244b4F4C856d55B7 y envia celo de la billetera 0x5027323B073841Dfb6481F2a2AFf38c1f393B9fb a la billetera 0x5a7DaF22100F1950880F8385B1D79F9F86d15F4D, el limite que se plantéo es de 75% de humedad</p>
            <p>Los sensores toman datos cada minuto y se envian a una base de datos tradicional, pero el registro de humedad se guarda en el contrato, el codigo fue desarrollado en python utilizando el <a href="https://github.com/blaize-tech/celo-sdk-py.git">celo python sdk</a> y el código se encuenta en el <a href="https://github.com/Oriojas/Celo_test.git">repositorio Celo_test</a> 
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ka7Sk0Gln4gmtz2MlQnikT1wXgYsOg+OMhuP+IlRH9sENBO0LRn5q+8nbTov4+1p" 
    crossorigin="anonymous"></script>
</body>

</html>"""

# write the JSON to the HTML template
with open('templates/new_plot.html', 'w') as f:
    f.write(template.format(fig_json))
