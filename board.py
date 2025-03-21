import dash
from dash import html, dcc, dash_table
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

import numpy as np

def create_dash_app(flask_app, before_optimization, after_optimization):
    dash_app = dash.Dash(__name__, server=flask_app, routes_pathname_prefix='/dashboard/')
    
    dash_app.layout = html.Div(style={'backgroundColor': '#000000', 'color': 'white', 'padding': '0px'}, children=[
        html.Div([
            dcc.Tabs(id="tabs", value='stock_analysis', children=[
                dcc.Tab(label='Stock Analysis', value='stock_analysis', style={'backgroundColor': '#333333', 'color': 'white'},
                        selected_style={'backgroundColor': '#222', 'borderBottom': '2px solid blue', 'color': 'white'}),
                dcc.Tab(label='User Portfolio', value='user_portfolio', style={'backgroundColor': '#333333', 'color': 'white'},
                         selected_style={'backgroundColor': '#222', 'borderBottom': '2px solid blue', 'color': 'white'}),
                dcc.Tab(label='Optimized Portfolio', value='optimized_portfolio', style={'backgroundColor': '#333333', 'color': 'white'},
                         selected_style={'backgroundColor': '#222', 'borderBottom': '2px solid blue', 'color': 'white'})
            ], colors={"border": "white", "primary": "white", "background": "#121212"}),
        ]),
        html.Div(id='tabs-content', style={'backgroundColor': '#000000', 'color': 'white', 'padding': '20px'})
    ])
    
    
    #STOCK ANALYISIS
    @dash_app.callback(
        Output('tabs-content', 'children'),
        Input('tabs', 'value')
    )
    def update_tab_content(tab_name):
        if tab_name == 'stock_analysis':
            file_path = "C://Users//Arnav Singh//OneDrive//Desktop//12//stock_data.csv"
            df2 = pd.read_csv(file_path)
            df2['Date'] = pd.to_datetime(df2['Date'], format='%d-%m-%Y')
            df2.set_index('Date', inplace=True)

            stocks = before_optimization.get("stock", []) if before_optimization else []
            if stocks:
                df2 = df2[stocks]
            
            pct_change = df2.pct_change().iloc[1:]
            cumulative_returns = (1 + pct_change).cumprod()
            correlation_matrix = df2.corr()
            
            graphs = html.Div(style={'display': 'flex', 'flex-wrap': 'wrap', 'gap': '20px'}, children=[
                html.Div(dcc.Graph(figure=px.line(df2, title="Stock Price Trends", template="plotly_dark")), style={'flex': '1 1 48%'}),
                html.Div(dcc.Graph(figure=px.line(cumulative_returns, title="Cumulative Returns", template="plotly_dark")), style={'flex': '1 1 48%'}),
                html.Div(dcc.Graph(
                    figure=px.imshow(
                        correlation_matrix,
                        labels=dict(color="Correlation"),
                        x=correlation_matrix.columns,
                        y=correlation_matrix.columns,
                        color_continuous_scale='Viridis',
                        title="Stock Correlation Heatmap",
                        template="plotly_dark",
                        text_auto=True
                    )
                ), style={'flex': '1 1 48%'}),
                html.Div(dcc.Graph(figure=px.histogram(pct_change.melt(), x='value', title="Volatility Analysis (Histogram)", template="plotly_dark")), style={'flex': '1 1 48%'})
            ])
            return graphs
        
        
        
        #USER PORTFOLIO 
        elif tab_name == 'user_portfolio':
            stocks = before_optimization.get("stock", [])
            investment = before_optimization.get("investment", [])
            weights = before_optimization.get("weights", [])
            total = before_optimization.get("total", 0)
            portfolio_return = before_optimization.get("portfolio_retur", 0)
            port_risk = before_optimization.get("port_risk", 0)
            daily_returns = before_optimization.get("daily_returns", pd.DataFrame())

            # Only Stock and Investment
            table_data = pd.DataFrame({
                "Stock": stocks,
                "Initial Investment (₹)": investment
            })

            portfolio_layout = html.Div(children=[

                html.H3("Performance Metrics"),

                # Clean Metric Cards with Black Background
                html.Div(style={
                    'display': 'flex',
                    'gap': '20px',
                    'marginBottom': '30px',
                    'width': '100%',
                    'boxSizing': 'border-box'
                }, children=[
                    # Total Investment Card
                    html.Div(style={
                        'flex': '1',
                        'backgroundColor': '#222222',  # Black Background
                        'padding': '20px',
                        'borderRadius': '10px',
                        'textAlign': 'center',
                        'color': 'white',
                        'boxShadow': '0 4px 10px rgba(0, 0, 0, 0.5)'  # Subtle shadow
                    }, children=[
                        html.H4("Total Investment (₹)", style={'marginBottom': '10px'}),  # Dodger Blue Title
                        html.H2(f"{total:,.2f}", style={'color': '#FFD700'})  # Dodger Blue Value
                    ]),

                    # Portfolio Return Card
                    html.Div(style={
                        'flex': '1',
                        'backgroundColor': '#222222',  # Black Background
                        'padding': '20px',
                        'borderRadius': '10px',
                        'textAlign': 'center',
                        'color': 'white',
                        'boxShadow': '0 4px 10px rgba(0, 0, 0, 0.5)'  # Subtle shadow
                    }, children=[
                        html.H4("Portfolio Return (%)", style={'marginBottom': '10px'}),  # Emerald Green Title
                        html.H2(f"{portfolio_return:.2f}%", style={'color': '#2ecc71'})  # Emerald Green Value
                    ]),

                    # Portfolio Risk Card
                    html.Div(style={
                        'flex': '1',
                        'backgroundColor': '#222222',  # Black Background
                        'padding': '20px',
                        'borderRadius': '10px',
                        'textAlign': 'center',
                        'color': 'white',
                        'boxShadow': '0 4px 10px rgba(0, 0, 0, 0.5)'  # Subtle shadow
                    }, children=[
                        html.H4("Portfolio Risk (%)", style={'marginBottom': '10px'}),  # Vibrant Red Title
                        html.H2(f"{port_risk:.2f}%", style={'color': '#e74c3c'})  # Vibrant Red Value
                    ])
                ]),

                html.H3("Selected Stocks & Investment Breakdown"),

                # Table on separate line
                dash_table.DataTable(
                    columns=[{"name": i, "id": i} for i in table_data.columns],
                    data=table_data.to_dict('records'),
                    style_table={'overflowX': 'auto', 'marginBottom': '30px'},
                    style_cell={'backgroundColor': '#111111', 'color': 'white', 'textAlign': 'center'},
                    style_header={'backgroundColor': '#222222', 'fontWeight': 'bold'}
                ),

                # Pie Chart and Return Histogram side-by-side
                html.Div(style={'display': 'flex', 'gap': '20px'}, children=[

                    html.Div(
                        dcc.Graph(
                            figure=px.pie(
                                names=stocks,
                                values=[w * 100 for w in weights],
                                title="Investment Distribution",
                                template="plotly_dark",
                                hole = 0.4
                            )
                        ),
                        style={'flex': '1'}
                    ),

                    html.Div(
                        dcc.Graph(
                            figure=px.histogram(
                                daily_returns.melt(),
                                x='value',
                                title="Daily Return Distribution",
                                template="plotly_dark"
                            )
                        ),
                        style={'flex': '1'}
                    )
                ])
            ])
            return portfolio_layout
        
        
        
        
        elif tab_name == 'optimized_portfolio':
            stocks = before_optimization.get("stock", [])
            optimal_investment = after_optimization.get("optimal_amount", [])
            new_weights = after_optimization.get("optimal_weight", [])
            total_after = before_optimization.get("total", 0)
            portfolio_return_after = after_optimization.get("portfolio_return", 0)
            port_risk_after = after_optimization.get("portfolio_risk", 0)

            # Before Optimization
            weights_before = before_optimization.get("weights", [])
            investment_before = before_optimization.get("investment", [])
            portfolio_return_before = before_optimization.get("portfolio_retur", 0)
            port_risk_before = before_optimization.get("port_risk", 0)

            # Investment Comparison Table
            investment_comparison_table = pd.DataFrame({
                "Stock": stocks,
                "Investment Before Optimization (₹)": investment_before,
                "Investment After Optimization (₹)": optimal_investment
            })

            # Optimized Portfolio Table
            optimized_table_data = pd.DataFrame({
                "Stock": stocks,
                "Optimized Investment (₹)": optimal_investment,
                "New Allocation (%)": [w * 100 for w in new_weights]
            })

            optimized_layout = html.Div(children=[

                html.H3("Optimized Performance Metrics"),

                # Metric Cards Section
                html.Div(style={'display': 'flex', 'gap': '20px', 'marginBottom': '30px'}, children=[
                    # Total Investment Card
                    html.Div(style={
                        'flex': '1',
                        'backgroundColor': '#222222',
                        'padding': '20px',
                        'borderRadius': '10px',
                        'textAlign': 'center',
                        'color': 'white'
                    }, children=[
                        html.H4("Total Investment (₹)", style={'marginBottom': '10px'}),
                        html.H2(f"{total_after:,.2f}", style={'color': '#FFD700'})
                    ]),

                    # Portfolio Return Card
                    html.Div(style={
                        'flex': '1',
                        'backgroundColor': '#222222',
                        'padding': '20px',
                        'borderRadius': '10px',
                        'textAlign': 'center',
                        'color': 'white'
                    }, children=[
                        html.H4("Portfolio Return (%)", style={'marginBottom': '10px'}),
                        html.H2(f"{portfolio_return_after:.2f}%", style={'color': '#32CD32'})
                    ]),

                    # Portfolio Risk Card
                    html.Div(style={
                        'flex': '1',
                        'backgroundColor': '#222222',
                        'padding': '20px',
                        'borderRadius': '10px',
                        'textAlign': 'center',
                        'color': 'white'
                    }, children=[
                        html.H4("Portfolio Risk (%)", style={'marginBottom': '10px'}),
                        html.H2(f"{port_risk_after:.2f}%", style={'color': '#FF6347'})
                    ])
                ]),

                html.H3("Investment Amount Comparison"),

                # Table Showing Investment Before & After Optimization
                dash_table.DataTable(
                    data=investment_comparison_table.to_dict('records'),
                    columns=[{"name": i, "id": i} for i in investment_comparison_table.columns],
                    style_table={'overflowX': 'auto', 'marginBottom': '30px'},
                    style_cell={'backgroundColor': '#111111', 'color': 'white', 'textAlign': 'center'},
                    style_header={'backgroundColor': '#222222', 'fontWeight': 'bold'}
                ),

                # Donut Chart for New Weights
                html.Div(dcc.Graph(
                    figure=px.pie(
                        names=stocks,
                        values=[w * 100 for w in new_weights],
                        title="Optimized Investment Distribution",
                        template="plotly_dark",
                        hole=0.4  # Doughnut effect
                    )
                ), style={'marginBottom': '30px'}),
                
                 
            ])

            return optimized_layout


        return html.Div()
    
    return dash_app
