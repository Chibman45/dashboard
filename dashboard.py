import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io
from dash.dependencies import State
from dash.dash import no_update
import dash_daq as daq

# Sample data
income_data = {
    'Month': ['April', 'April', 'May', 'May', 'June', 'July'],
    'Source': ['Bank', 'Bank', 'Bank', 'Paystack', 'Paystack', 'Paystack'],
    'Description': ['Opening Bank Account', 'Bank Transfer By CEO', 'Payment By Student', 'Payment By IT Student', 'Payment By IT Student', 'Payment By IT Student'],
    'Amount': [15000, 1000, 80000, 324450, 404035, 68850]
}

expense_data = {
    'Month': ['May', 'May', 'May', 'May', 'June', 'June', 'June', 'June', 'June', 'June', 'June', 'June', 'July', 'July', 'July', 'July', 'July', 'July', 'July', 'July', 'July', 'August', 'August'],
    'S/N': list(range(1, 24)),
    'Description': [
        'Bank Legal Fee', 'Payment for Referrals', 'Bank Charges', 'Second payment for referrals',
        'Repair of Generator', 'Purchase of Fuel week 1', 'Payment For 4 referrals to Alex', 'Purchase of Data for Student and Instructors', 
        'Purchase of Fuel week 2', 'Data For Student', 'Bank Charges', 'Hardware Token Charges', 
        'Purchase of Data for Student and Instructors', 'Purchase Of Data for Student For week 2', 'Purchase Of Data for Student For week 3', 
        'Repayment Of Loan to CEO', 'Repayment Of Loan to CEO', 'Refund Of Student payment', 'Purchase of Data For instructors for August', 
        'Payment of Producta site Rehosting', 'Bank Charges', 'Data For Student Week 1', 'Fuel For Ernest'
    ],
    'Amount': [
        9000, 10000, 555.76, 10000, 38000, 10000, 20000, 10000, 
        10000, 5000, 692.25, 2500, 15000, 5000, 5000, 20000, 
        20000, 50000, 10000, 56000, 466.28, 5000, 3000
    ]
}

financial_summary_data = {
    'Date': [
        '05/04/2024', '31/05/2024', '31/05/2024', '31/05/2024', '01/06/2024', '30/06/2024', 
        '30/06/2024', '31/07/2024', '31/07/2024', '31/07/2024', '07/08/2024'
    ],
    'Description': [
        'Opening of Account', 'Total Payment from Paystack & Charges', 'Total Transfer to Account', 'Total Expense', 
        'Balance B/F', 'Total Payment from Paystack & Charges', 'Total Expense', 'Balance B/F', 'Total Payment from Paystack & Charges', 
        'Total Expense', 'Total Expense'
    ],
    'Inflow (₦)': [
        15000, 330000, 81100, None, None, 411000, None, None, 70000, None, None
    ],
    'Outflow (₦)': [
        None, 5550, None, 29555.76, None, 6965, 96192.25, None, 1150, 191466.28, 8000
    ],
    'Balance (₦)': [
        15000, 339450, 420550, 390994.24, 390994.24, 795029.24, 698836.99, 698836.99, 767686.99, 576220.71, 568220.71
    ]
}

balance_sheet_data = {
    'Assets': ['Cash at Bank', 'Accounts Receivable'],
    'Amount (₦)': [568220.71, 0]
}

liabilities_data = {
    'Liabilities': ['Bank Legal Fee', 'Bank Charges', 'Remaining CEO Loan Balance'],
    'Amount (₦)': [9000, 1714.29, 918000]
}

equity_data = {
    'Equity': ['Opening Balance', 'Additional Equity Contributions', 'Retained Earnings'],
    'Amount (₦)': [15000, 81100, 568120.71]
}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
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
        dbc.Col(dcc.Graph(figure=income_fig), width=6),
        dbc.Col(dcc.Graph(figure=expense_fig), width=6)
    ]),
    
    dbc.Row(dbc.Col(dcc.Graph(figure=balance_fig), width=12)),
    
    dbc.Row([
        dbc.Col([
            html.H2('Balance Sheet'),
            dash_table.DataTable(
                id='balance-sheet-table',
                columns=[{'name': 'Assets', 'id': 'Assets'}, {'name': 'Amount (₦)', 'id': 'Amount (₦)'}],
                data=balance_sheet_df.to_dict('records'),
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left'},
                style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
            ),
            html.H3('Total Assets: ₦568,220.71')
        ], width=4),
        
        dbc.Col([
            html.H2('Liabilities'),
            dash_table.DataTable(
                id='liabilities-table',
                columns=[{'name': 'Liabilities', 'id': 'Liabilities'}, {'name': 'Amount (₦)', 'id': 'Amount (₦)'}],
                data=liabilities_df.to_dict('records'),
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left'},
                style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
            ),
            html.H3('Total Liabilities: ₦928,714.29')
        ], width=4),
        
        dbc.Col([
            html.H2('Equity'),
            dash_table.DataTable(
                id='equity-table',
                columns=[{'name': 'Equity', 'id': 'Equity'}, {'name': 'Amount (₦)', 'id': 'Amount (₦)'}],
                data=equity_df.to_dict('records'),
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left'},
                style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
            ),
            html.H3('Total Equity: ₦664,220.71')
        ], width=4)
    ]),

    dbc.Row([
        dbc.Col(html.Button("Download Balance Sheet as XLS", id="btn_xls"), className="d-grid gap-2 col-2 mx-auto"),
        dcc.Download(id="download-dataframe-xls")
    ])
], fluid=True)

# Callback to Download Balance Sheet as Excel
@app.callback(
    Output("download-dataframe-xls", "data"),
    Input("btn_xls", "n_clicks"),
    prevent_initial_call=True,
)
def download_xls(n_clicks):
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    balance_sheet_df.to_excel(writer, sheet_name='Balance Sheet', index=False)
    liabilities_df.to_excel(writer, sheet_name='Liabilities', index=False)
    equity_df.to_excel(writer, sheet_name='Equity', index=False)
    writer.save()
    output.seek(0)
    return dcc.send_bytes(output.getvalue(), "balance_sheet.xlsx")

if __name__ == '__main__':
    app.run_server(debug=True)
