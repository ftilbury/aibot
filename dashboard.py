"""
Dashboard utilities for visualising trading performance.

This module defines functions to create interactive dashboards using Plotly
and Dash. The primary function ``run_dashboard`` spins up a Dash web
application that displays the equity curve and individual trades.

Note: This is a lightweight example. For production use, you may wish to
add authentication, real‑time updates, and additional charts (e.g. drawdown,
exposure, trade distribution).
"""

import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

try:
    import dash
    from dash import html, dcc
except ImportError:
    dash = None


def create_equity_figure(equity_df: pd.DataFrame) -> go.Figure:
    """Create a Plotly figure for the equity curve."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=equity_df.index, y=equity_df['equity'], mode='lines', name='Equity'))
    fig.update_layout(title='Equity Curve', xaxis_title='Time', yaxis_title='Equity')
    return fig


def run_dashboard(equity_df: pd.DataFrame, trades_df: pd.DataFrame) -> None:
    """Launch a simple Dash dashboard to display performance metrics.

    Parameters
    ----------
    equity_df : pandas.DataFrame
        DataFrame containing the equity curve with an index of timestamps.
    trades_df : pandas.DataFrame
        DataFrame of executed trades.
    """
    if dash is None:
        print("Dash is not installed. Cannot run dashboard.")
        return
    app = dash.Dash(__name__)

    equity_fig = create_equity_figure(equity_df)

    app.layout = html.Div([
        html.H1('Trading Dashboard'),
        dcc.Graph(figure=equity_fig),
        html.H2('Trades'),
        dcc.DataTable(
            id='trades-table',
            columns=[{"name": i, "id": i} for i in trades_df.columns],
            data=trades_df.to_dict('records'),
        ),
    ])

    app.run_server(debug=False)