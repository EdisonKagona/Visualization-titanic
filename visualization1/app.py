# app.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash_bootstrap_components import themes  # Import Bootstrap themes
import dash_bootstrap_components as dbc
from visual1 import load_titanic_data, create_survival_count_plot, create_class_distribution_plot, create_3d_scatter_plot, create_feature_plot

# Load the Titanic dataset
titanic_data = load_titanic_data()

# Initialize the Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout of the dashboard
app.layout = html.Div(style={'backgroundColor': '#f2f2f2', 'padding': '20px'}, children=[
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Titanic Dataset Analysis Dashboard", className="display-4 text-center mb-4"), width=12)
        ]),
        dcc.Tabs(style={'margin': '20px'}, children=[
            dcc.Tab(label='2D Visualizations', children=[
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H2("Survival Count"),
                                dcc.Graph(id='survival-count-plot'),
                            ])
                        ], className="mb-4"),
                    ], width=6),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H2("Class Distribution"),
                                dcc.Graph(id='class-distribution-plot'),
                            ])
                        ], className="mb-4"),
                    ], width=6),
                ]),
                # Add more 2D visualizations here
            ]),

            dcc.Tab(label='3D Visualization', children=[
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H2("3D Scatter Plot"),
                                dcc.Graph(id='3d-scatter-plot'),
                            ])
                        ], className="mb-4"),
                    ], width=12),
                ]),
                # Add more 3D visualizations here
            ]),

            dcc.Tab(label='Interactive Components', children=[
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody([
                                html.H2("Interactive Components"),
                                html.Label("Select a feature to plot against survival:"),
                                dcc.Dropdown(
                                    id='feature-dropdown',
                                    options=[
                                        {'label': 'Age', 'value': 'Age'},
                                        {'label': 'Fare', 'value': 'Fare'},
                                        {'label': 'Pclass', 'value': 'Pclass'}
                                    ],
                                    value='Age'
                                ),
                                dcc.Graph(id='feature-plot')
                            ])
                        ], className="mb-4"),
                    ], width=12),
                ]),
            ]),
        ]),
    ]),
])


# Callback to update survival count plot
@app.callback(
    Output('survival-count-plot', 'figure'),
    [Input('survival-count-plot', 'id')]
)
def update_survival_count_plot(id):
    return create_survival_count_plot(titanic_data)

# Callback to update class distribution plot
@app.callback(
    Output('class-distribution-plot', 'figure'),
    [Input('class-distribution-plot', 'id')]
)
def update_class_distribution_plot(id):
    return create_class_distribution_plot(titanic_data)

# Callback to update 3D scatter plot
@app.callback(
    Output('3d-scatter-plot', 'figure'),
    [Input('3d-scatter-plot', 'id')]
)
def update_3d_scatter_plot(id):
    return create_3d_scatter_plot(titanic_data)

# Callback to update feature plot based on user input
@app.callback(
    Output('feature-plot', 'figure'),
    [Input('feature-dropdown', 'value')],
    [State('feature-plot', 'id')]
)
def update_feature_plot(selected_feature, id):
    if selected_feature is None:
        raise dash.exceptions.PreventUpdate

    return create_feature_plot(selected_feature, titanic_data)

if __name__ == '__main__':
    app.run_server(port=8054)
