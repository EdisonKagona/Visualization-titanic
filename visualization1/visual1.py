#!/usr/bin/env python
# coding: utf-8

# In[2]:


import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px

# Function to load Titanic dataset
def load_titanic_data():
    return pd.read_csv("titanic.csv")  # Replace with the actual path

# Function to create 2D survival count plot
def create_survival_count_plot(data):
    fig = px.bar(data, x='Survived', title='Survival Count')
    return fig

# Function to create 2D class distribution plot
def create_class_distribution_plot(data):
    fig = px.pie(data, names='Pclass', title='Class Distribution')
    return fig

# Function to create 3D scatter plot
def create_3d_scatter_plot(data):
    fig = px.scatter_3d(data, x='Age', y='Fare', z='Pclass', color='Survived',
                        title='3D Scatter Plot', labels={'Age': 'Age', 'Fare': 'Fare', 'Pclass': 'Class'})
    return fig

# Function to create interactive feature plot
def create_feature_plot(selected_feature, data):
    fig = px.histogram(data, x=selected_feature, color='Survived', barmode='overlay',
                       title=f'{selected_feature} Distribution by Survival',
                       labels={selected_feature: selected_feature})
    return fig

# Load the Titanic dataset
titanic_data = load_titanic_data()

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the dashboard
app.layout = html.Div([
    html.H1("Titanic Dataset Analysis Dashboard"),

    # 2D Visualizations
    html.Div([
        html.H2("Survival Count"),
        dcc.Graph(id='survival-count-plot')
    ]),

    html.Div([
        html.H2("Class Distribution"),
        dcc.Graph(id='class-distribution-plot')
    ]),

    # 3D Visualization
    html.Div([
        html.H2("3D Scatter Plot"),
        dcc.Graph(id='3d-scatter-plot')
    ]),

    # Interactive Components
    html.Div([
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

# Run the app
if __name__ == '__main__':
    # Use a different port, for example, 8053
    app.run_server(mode='inline', port=8055)


# In[ ]:




