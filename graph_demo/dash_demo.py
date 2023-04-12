import plotly.graph_objs as go
import plotly.express as px
from dash import Dash, dcc, html

# Create sample data
x1 = [0, 1, 2, 3]
y1 = [0, 1, 2, 3]
z1 = [0, 1, 2, 3]
text1 = ['This', 'is', 'the', 'first sentence.']

x2 = [3, 4, 5, 6]
y2 = [3, 4, 5, 6]
z2 = [3, 4, 5, 6]
text2 = ['This', 'is', 'the', 'second sentence.']

# Create scatter traces for each sentence
trace1 = go.Scatter3d(
    x=x1,
    y=y1,
    z=z1,
    text=text1,
    mode='markers+text',
    textposition='top center',
    marker=dict(size=10, symbol='circle', color='blue'),
)

trace2 = go.Scatter3d(
    x=x2,
    y=y2,
    z=z2,
    text=text2,
    mode='markers+text',
    textposition='top center',
    marker=dict(size=10, symbol='circle', color='red'),
)

# Create figure layout
fig = go.Figure(
    data=[trace1, trace2],
    layout=go.Layout(
        margin=dict(l=0, r=0, b=0, t=0),
        scene=dict(
            xaxis=dict(title='X axis', showgrid=False),
            yaxis=dict(title='Y axis', showgrid=False),
            zaxis=dict(title='Z axis', showgrid=False),
            aspectmode='cube'
        )
    )
)

# Create a Dash app
app = Dash(__name__)
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)
