import csv
import dash
import dash_table
import pandas as pd
from dash import html, dcc
import plotly.express as px

app = dash.Dash('Soul Foods Pink Morsel Price Crunching')

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


files = ['data/daily_sales_data_0.csv', 'data/daily_sales_data_1.csv', 'data/daily_sales_data_2.csv']
df = load_and_process_data(files)

app.layout = html.Div([
    html.H1('Sales Data for Pink Morsel'),

    dcc.Graph(
        id='sales-bar-chart',
        figure=px.line(df, x='Date', y='Sales', title='Sales Over Time')
    ),

    dash_table.DataTable(
        id='sales-table',
        columns=[
            {'name': col, 'id': col} for col in df.columns
        ],
        data=df.to_dict('records'),
        style_table={'overflowX': 'auto'},
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)

