#!/usr/bin/env python
# coding: utf-8

# In[5]:


# Import necessary libraries
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
from dash.dash_table import DataTable  # Update the import

# Function to load Titanic dataset
def load_titanic_data():
    return pd.read_csv("titanic.csv")  # Replace with the actual path

# Initialize the Dash app
app = dash.Dash(__name__)

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

def create_feature_plot(selected_feature, data):
    if selected_feature not in data.columns:
        raise ValueError(f"Selected feature '{selected_feature}' not found in the dataset.")

    if pd.api.types.is_numeric_dtype(data[selected_feature]):
        fig = px.histogram(data, x=selected_feature, color='Survived', barmode='overlay',
                           title=f'{selected_feature} Distribution by Survival',
                           labels={'Survived': 'Survival'})
    else:
        fig = px.bar(data, x=selected_feature, color='Survived',
                     title=f'{selected_feature} Count by Survival',
                     labels={'Survived': 'Survival'})

    fig.update_layout(height=400, width=600)
    return fig


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

def create_survival_count_plot(data):
    fig = px.bar(data, x='Survived', title='Survival Count',
                 labels={'Survived': 'Survival', 'count': 'Count'})
    fig.update_layout(height=400, width=600)
    return fig

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

def create_class_distribution_plot(data):
    fig = px.pie(data, names='Pclass', title='Class Distribution',
                 labels={'Pclass': 'Passenger Class'})
    fig.update_layout(height=400, width=600)
    return fig

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

def create_3d_scatter_plot(data):
    fig = px.scatter_3d(data, x='Age', y='Fare', z='Pclass', color='Survived',
                        title='3D Scatter Plot (Age, Fare, Pclass) by Survival',
                        labels={'Age': 'Passenger Age', 'Fare': 'Passenger Fare', 'Pclass': 'Passenger Class'})
    fig.update_layout(height=600, width=800)
    return fig

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

def create_survival_heatmap(data):
    fig = px.imshow(data.corr(), labels=dict(color="Survival Correlation"),
                    title='Survival Correlation Heatmap')
    fig.update_layout(height=600, width=800)
    return fig

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

def create_age_fare_scatter_matrix(data):
    fig = px.scatter_matrix(data, dimensions=['Age', 'Fare', 'Pclass'], color='Survived',
                            title='Scatter Matrix for Age, Fare, Pclass by Survival',
                            height=600, width=800)
    return fig

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

def create_age_fare_animation(data):
    fig = px.scatter(data, x='Age', y='Fare', color='Survived', animation_frame='Pclass',
                     title='Age-Fare Animation by Survival and Pclass',
                     labels={'Age': 'Passenger Age', 'Fare': 'Passenger Fare'},
                     height=600, width=800)
    fig.update_layout(transition_duration=1000)  # Set animation duration
    return fig

# Run the app
if __name__ == '__main__':
    # Use a different port, for example, 8053
    app.run_server(mode='inline', port=8053)


# In[ ]:




