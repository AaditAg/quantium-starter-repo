import csv
import dash
import dash_table
import pandas as pd
from dash import html, dcc
import plotly.express as px
from dash import Input, Output

app = dash.Dash(__name__)

files = ['data/daily_sales_data_0.csv', 'data/daily_sales_data_1.csv', 'data/daily_sales_data_2.csv']

def load_and_process_data(files):
    combined_data = []

    for file in files:
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            header = next(csv_reader)
            print(f"{header[0]} | {header[1]} | {header[2]} | {header[3]} | {header[4]}")

            for row in csv_reader:
                if row[0] == 'pink morsel':
                    price = float(row[1].replace('$', '').replace(',', '').strip())
                    quantity = int(row[2])
                    sales = quantity * price
                    date = row[3]
                    region = row[4]

                    combined_data.append({
                        'Sales': sales,
                        'Date': date,
                        'Region': region
                    })

    df = pd.DataFrame(combined_data)
    return df

df = load_and_process_data(files)

app.layout = html.Div(style={'fontFamily': 'Arial', 'padding': '20px'}, children=[
    html.H1('Sales Data for Pink Morsel', style={
        'textAlign': 'center',
        'fontFamily': 'Arial',
        'color': '#333333',
        'borderBottom': '2px solid #f2f2f2',
        'paddingBottom': '10px'
    }),

    dcc.RadioItems(
        id='region-selector',
        options=[
            {'label': 'All', 'value': 'All'},
            {'label': 'North', 'value': 'north'},
            {'label': 'South', 'value': 'south'},
            {'label': 'East', 'value': 'east'},
            {'label': 'West', 'value': 'west'}
        ],
        value='All',
        style={
            'marginBottom': '20px',
            'display': 'flex',
            'justifyContent': 'space-evenly',
            'fontSize': '16px',
            'color': '#666666'
        }
    ),

    dcc.Graph(
        id='sales-bar-chart',
        figure=px.line(df, x='Date', y='Sales', title='Sales Over Time'),
        style={
            'border': '1px solid #e0e0e0',
            'borderRadius': '8px',
            'padding': '10px'
        }
    ),

    dash_table.DataTable(
        id='sales-table',
        columns=[{'name': col, 'id': col} for col in df.columns],
        data=df.to_dict('records'),
        style_table={
            'overflowX': 'auto',
            'borderRadius': '10px',
            'borderColor': 'black',
            'border': '1px solid #e0e0e0'
        },
        style_header={
            'backgroundColor': '#f2f2f2',
            'fontWeight': 'bold',
            'textAlign': 'center'
        },
        style_cell={
            'textAlign': 'left',
            'padding': '10px',
            'fontSize': '14px'
        }
    )
])

@app.callback(
    [Output('sales-bar-chart', 'figure'),
     Output('sales-table', 'data')],
    [Input('region-selector', 'value')]
)
def update_output(selected_region):
    if selected_region == 'All':
        filtered_df = df
    else:
        filtered_df = df[df['Region'] == selected_region]

    figure = px.line(filtered_df, x='Date', y='Sales', title=f'Sales Over Time - {selected_region}')

    return figure, filtered_df.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)
