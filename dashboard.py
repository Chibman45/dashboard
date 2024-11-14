import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
from dash import dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io
from dash.dependencies import State
from dash.dash import no_update

# Sample data
income_data = {...}
expense_data = {...}
financial_summary_data = {...}
balance_sheet_data = {...}
liabilities_data = {...}
equity_data = {...}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.themes.DARKLY])
server = app.server

# Create DataFrames
income_df = pd.DataFrame(income_data)
expense_df = pd.DataFrame(expense_data)
financial_summary_df = pd.DataFrame(financial_summary_data)
balance_sheet_df = pd.DataFrame(balance_sheet_data)
liabilities_df = pd.DataFrame(liabilities_data)
equity_df = pd.DataFrame(equity_data)

# Create Figures
income_fig = px.bar(income_df, x='Month', y='Amount', color='Source', title='Income per Month (April - August 2024)')
expense_fig = px.pie(expense_df, names='Description', values='Amount', title='Expense Categories (April - August 2024)')
balance_fig = go.Figure(data=[go.Scatter(x=financial_summary_df['Date'], y=financial_summary_df['Balance (₦)'], mode='lines+markers', name='Balance')])
balance_fig.update_layout(title='Account Balance Over Time (April - August 2024)', xaxis_title='Date', yaxis_title='Balance (₦)')

# Create Dash Layout
app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1('Zemoora Technologies Limited', className='text-center mt-4', style={'fontFamily': 'Courier New', 'fontWeight': 'bold'}))),
    dbc.Row(dbc.Col(html.H3('Financial Report (April - August 2024)', className='text-center mb-4'))),
    dbc.Row([
        dbc.Col(dcc.Graph(figure=income_fig), width={'size': 6, 'order': 'first'}),
        dbc.Col(dcc.Graph(figure=expense_fig), width={'size': 6, 'order': 'last'})
    ]),
    dbc.Row(dbc.Col(dcc.Graph(figure=balance_fig), width=12)),
    dbc.Row([
        dbc.Col([
            html.H2('Balance Sheet'),
            dash_table.DataTable(
                id='balance-sheet-table',
                columns=[{'name': 'Assets', 'id': 'Assets'}, {'name': 'Amount (₦)', 'id': 'Amount (₦)'}],
                data=balance_sheet_df.to_dict('records'),
                style_table={'overflowX': 'auto', 'height': '300px'},
                style_cell={'textAlign': 'left', 'padding': '12px'},
                style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
            ),
            html.H3('Total Assets: ₦568,220.71')
        ], width={'size': 4, 'offset': 0, 'order': 'first'}),
        dbc.Col([
            html.H2('Liabilities'),
            dash_table.DataTable(
                id='liabilities-table',
                columns=[{'name': 'Liabilities', 'id': 'Liabilities'}, {'name': 'Amount (₦)', 'id': 'Amount (₦)'}],
                data=liabilities_df.to_dict('records'),
                style_table={'overflowX': 'auto', 'height': '300px'},
                style_cell={'textAlign': 'left', 'padding': '12px'},
                style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
            ),
            html.H3('Total Liabilities: ₦928,714.29')
        ], width={'size': 4, 'order': 'middle'}),
        dbc.Col([
            html.H2('Equity'),
            dash_table.DataTable(
                id='equity-table',
                columns=[{'name': 'Equity', 'id': 'Equity'}, {'name': 'Amount (₦)', 'id': 'Amount (₦)'}],
                data=equity_df.to_dict('records'),
                style_table={'overflowX': 'auto', 'height': '300px'},
                style_cell={'textAlign': 'left', 'padding': '12px'},
                style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
            ),
            html.H3('Total Equity: ₦664,220.71')
        ], width={'size': 4, 'order': 'last'})
    ]),
    dbc.Row([
        dbc.Col(html.Button("Download Balance Sheet as XLS", id="btn_xls", className="btn btn-primary"), className="d-grid gap-2 col-2 mx-auto")
    ]),
    dcc.Download(id="download-dataframe-xls")
], fluid=True)

# Callback to Download Balance Sheet as Excel
@app.callback(
    Output("download-dataframe-xls", "data"),
    Input("btn_xls", "n_clicks"),
    prevent_initial_call=True,
)
def download_xls(n_clicks):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        balance_sheet_df.to_excel(writer, sheet_name='Balance Sheet', index=False)
        liabilities_df.to_excel(writer, sheet_name='Liabilities', index=False)
        equity_df.to_excel(writer, sheet_name='Equity', index=False)
    output.seek(0)
    return dcc.send_bytes(output.getvalue(), "balance_sheet.xlsx")

if __name__ == '__main__':
    app.run_server(debug=True)
