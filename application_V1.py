import dash
from flask import Flask
from dash import Dash, dcc, html, Input, Output, callback, dash_table
from dash.dcc import send_bytes   
import pandas as pd
import openpyxl, io
from task import filtering_function, apperance_counting, data_df



red = filtering_function(data_df)[0]
yellow = filtering_function(data_df)[2]
green = filtering_function(data_df)[1]


app = dash.Dash(__name__)
server = app.server

summary_df = pd.DataFrame({"Raudonos veikimo skaičius": [len(filtering_function(data_df)[0])],
                  "Geltonos veikimo skaičius": [len(filtering_function(data_df)[2])],
                  "Žalios veikimo skaičius": [len(filtering_function(data_df)[1])],
                  "Pilno ciklo skčius": [apperance_counting(data_df)],
                  "Raudona TimeActive laikas": [filtering_function(data_df)[7]],
                  "Geltona TimeActive laikas": [filtering_function(data_df)[8]],
                  "Žalia TimeActive laikas": [filtering_function(data_df)[9]],
                  "Klaidingų duomenu skaičius": [len(data_df.loc[data_df['Red'] + data_df['Yellow'] + data_df['Green']  > 1])]})





app.layout = html.Div([
    html.Div(
    html.H1("Qdev Technologies užduoties atvaizdavimas"),
    style={'display': 'flex', 'justify-content': 'space-around'}
    ),
    html.Div(
        [
            html.H3("Išfiltruoti tik raudonos spalvos duomenys"),
            html.H3("Išfiltruoti tik geltonos spalvos duomenys"),
            html.H3("Išfiltruoti tik žalios spalvos duomenys"),
        ],
        style={'display': 'flex', 'justify-content': 'space-around'}  
    ),

    html.Div(
        [

            dash_table.DataTable(
                red.to_dict('records'),
                style_table={'height': '300px', 'width': '600px', 'overflowY': 'auto', 'overflowX': 'auto'}
            ),

            dash_table.DataTable(
                yellow.to_dict('records'),
                style_table={'height': '300px', 'width': '600px', 'overflowY': 'auto', 'overflowX': 'auto', 'margin-left': '20px'}
            ),

            dash_table.DataTable(
                green.to_dict('records'),
                style_table={'height': '300px', 'width': '600px', 'overflowY': 'auto', 'overflowX': 'auto', 'margin-left': '20px'}
            ),
          
        ],
        style={'display': 'flex'},
         
    ),
    html.Div(
        [
            html.H3("Apibendrinimas skaičiais")
        ]
    ),
    html.Div(
        [
            dash_table.DataTable(
                summary_df.to_dict('records'),
                style_table={'height': '300px', 'overflowY': 'auto', 'overflowX': 'auto'})
            
        ],

        style={'display': 'flex', 'flex-direction': 'column'},
         
    ),
    dcc.Graph(figure={'data': [{'x': summary_df.columns,
                                'y': summary_df.iloc[0].values,
                                'type': 'bar',
                                'text': summary_df.iloc[0].values,
                                'textposition': 'auto'}],
                      'layout': {'title': 'Apibendrinimas grafiškai',
                                'margin': {'t':30}}}),
    html.Button("Eksportuoti į XLSX", id='export-button'),
    dcc.Download(id="download-dataframe-xlsx"),
])

@app.callback(
    Output("download-dataframe-xlsx", "data"),
    Input("export-button", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    if n_clicks is None:  
        return None

    
    workbook = openpyxl.Workbook()

    
    sheet = workbook.active
    sheet.title = "Apibendrinimas"
    for r in dataframe_to_rows(summary_df, index=True): 
        sheet.append(r)

    
    for df, sheet_name in zip([red, yellow, green], ["Raudona", "Geltona", "Žalia"]):
        sheet = workbook.create_sheet(title=sheet_name)
        for r in dataframe_to_rows(df, index=True):  
            sheet.append(r)

    
    output = io.BytesIO()
    workbook.save(output)
    output.seek(0)

    
    return dcc.send_bytes(
        output.getvalue(), 
        "lenteles.xlsx"
    )


def dataframe_to_rows(df, index=True):
    if index:  
        yield list(df.columns)
    for index, values in df.iterrows():
        yield list(values)



if __name__ == '__main__':
    app.run_server(debug=True)
