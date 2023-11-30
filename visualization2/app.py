# Import necessary libraries
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash.dash_table import DataTable  # Update the import
from visual2 import load_titanic_data, create_survival_count_plot, create_class_distribution_plot, create_3d_scatter_plot, create_feature_plot

# Load the Titanic dataset
titanic_data = load_titanic_data()

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout
app.layout = html.Div([
    # Initial Data Display
    html.Div([
        html.H2("Initial Data Display", className="text-center"),
        DataTable(
            id='initial-data-table',
            columns=[{"name": col, "id": col} for col in titanic_data.columns],
            data=titanic_data.head().to_dict('records'),
            style_table={'height': '300px', 'overflowY': 'auto'},
        ),
    ], style={'margin-bottom': '20px'}),

    # Dropdown to select a feature
    dcc.Dropdown(
        id='feature-dropdown',
        options=[{'label': col, 'value': col} for col in titanic_data.columns],
        value='Age',  # default feature
        style={'width': '50%', 'margin-bottom': '20px'}
    ),

    # Visualization components
    dcc.Graph(id='feature-plot', className='custom-plot'),
    dcc.Graph(id='survival-count-plot', className='custom-plot'),
    dcc.Graph(id='class-distribution-plot', className='custom-plot'),
    dcc.Graph(id='3d-scatter-plot', className='custom-plot'),
    dcc.Graph(id='survival-heatmap', className='custom-plot'),
    dcc.Graph(id='age-fare-scatter-matrix', className='custom-plot'),
    dcc.Graph(id='age-fare-animation', className='custom-plot'),

    # Hidden div to store the data
    html.Div(id='titanic-data-store', style={'display': 'none'}),

    # Hidden div to store the selected feature
    html.Div(id='selected-feature-store', style={'display': 'none'})
])

# Callback to update the data store
@app.callback(
    Output('titanic-data-store', 'children'),
    [Input('feature-dropdown', 'value')]
)
def update_data_store(selected_feature):
    return titanic_data.to_json()

# Callback to update the initial data table
@app.callback(
    Output('initial-data-table', 'data'),
    [Input('titanic-data-store', 'children')]
)
def update_initial_data_table(titanic_data_json):
    if titanic_data_json is None:
        return titanic_data.head().to_dict('records')

    data = pd.read_json(titanic_data_json)
    return data.head().to_dict('records')

# Callback to update feature plot
@app.callback(
    Output('feature-plot', 'figure'),
    [Input('feature-dropdown', 'value')],
    [State('titanic-data-store', 'children')]
)
def update_feature_plot(selected_feature, titanic_data_json):
    if titanic_data_json is None:
        return px.scatter(title='Waiting for data...', labels={'x': selected_feature})

    data = pd.read_json(titanic_data_json)
    return create_feature_plot(selected_feature, data)

# Callback to update survival count plot
@app.callback(
    Output('survival-count-plot', 'figure'),
    [Input('titanic-data-store', 'children')]
)
def update_survival_count_plot(titanic_data_json):
    if titanic_data_json is None:
        return px.bar(title='Waiting for data...', labels={'x': 'Survived'})

    data = pd.read_json(titanic_data_json)
    return create_survival_count_plot(data)

# Callback to update class distribution plot
@app.callback(
    Output('class-distribution-plot', 'figure'),
    [Input('titanic-data-store', 'children')]
)
def update_class_distribution_plot(titanic_data_json):
    if titanic_data_json is None:
        return px.pie(title='Waiting for data...', labels={'names': 'Pclass'})

    data = pd.read_json(titanic_data_json)
    return create_class_distribution_plot(data)

# Callback to update 3D scatter plot
@app.callback(
    Output('3d-scatter-plot', 'figure'),
    [Input('titanic-data-store', 'children')]
)
def update_3d_scatter_plot(titanic_data_json):
    if titanic_data_json is None:
        return px.scatter_3d(title='Waiting for data...', labels={'x': 'Age', 'y': 'Fare', 'z': 'Pclass'})

    data = pd.read_json(titanic_data_json)
    return create_3d_scatter_plot(data)

# Callback to update survival heatmap
@app.callback(
    Output('survival-heatmap', 'figure'),
    [Input('titanic-data-store', 'children')]
)
def update_survival_heatmap(titanic_data_json):
    if titanic_data_json is None:
        return px.imshow(title='Waiting for data...', labels=dict(color="Survival Correlation"))

    data = pd.read_json(titanic_data_json)
    return create_survival_heatmap(data)

# Callback to update scatter matrix for age and fare
@app.callback(
    Output('age-fare-scatter-matrix', 'figure'),
    [Input('titanic-data-store', 'children')]
)
def update_age_fare_scatter_matrix(titanic_data_json):
    if titanic_data_json is None:
        return px.scatter_matrix(title='Waiting for data...', labels={'color': 'Survived'})

    data = pd.read_json(titanic_data_json)
    return create_age_fare_scatter_matrix(data)

# Callback to update age-fare animation
@app.callback(
    Output('age-fare-animation', 'figure'),
    [Input('titanic-data-store', 'children')]
)
def update_age_fare_animation(titanic_data_json):
    if titanic_data_json is None:
        return px.scatter(title='Waiting for data...', labels={'x': 'Age', 'y': 'Fare', 'animation_frame': 'Pclass'})

    data = pd.read_json(titanic_data_json)
    return create_age_fare_animation(data)

# Run the app
if __name__ == '__main__':
    app.run_server(port=8054)

