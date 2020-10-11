import dash
import dash_cytoscape as cyto
import dash_html_components as html
import dash_core_components as dcc
from pprint import pprint
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from PL import solve
from matrix_management import load_graph


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



path = "graph_files/graph1"
nodes_set, edges_set, sources, puits = load_graph(path)


nodes = [
    {
        'data': {'id': node, 'label': node,"is_src": (1 if node.startswith("s") else 0),"is_puit": (1 if node.startswith("p") else 0)},
    }
    for node in nodes_set
]

edges = [
    {'data': {'source': source, 'target': target,"capacity":capacity,"weight":0,"label":str(0)+"/"+str(capacity)},"saturated":0}
    for source, target, capacity in edges_set
]


default_stylesheet = [
    {
        'selector': '[is_src > 0]',
        'style': {
            'background-color': 'blue',
            'shape': 'rectangle'

}
    },
    {
    'selector': '[is_puit > 0]',
        'style': {
            'background-color': 'red',
        }
    },
    {
    'selector': 'node',
    'style': {
        'label': 'data(label)'
    }
    },
    {
        'selector': '[saturated = 1]',
        'style': {
        'label': 'data(label)',
           'line-color': 'blue',
        }
    },
    {
            'selector': 'edge',
            'style': {
                'label': 'data(label)',
                'target-arrow-shape': 'vee',
                'curve-style': 'bezier',
                'arrow-scale': 3,
            }
    },

]


app.layout = html.Div(
    children=[
        html.Div(    style={'textAlign': 'center',},
            children=[html.H3(children='Max Flow Problem Solver'),]),
    cyto.Cytoscape(
        id='graphe',
        layout={'name': 'breadthfirst'},
        stylesheet=default_stylesheet,
        style={'width': '100%', 'height': '650px'},
        elements=edges+nodes,
    ),
    html.Div(    style={'textAlign': 'center'},
    children=[
        html.Button('Solve !', id='btn-solve', n_clicks_timestamp=0),
    ]),
]
)

@app.callback(
    Output(component_id='graphe', component_property='elements'),
    [Input(component_id='btn-solve', component_property='n_clicks')]
)
def update_output_div(n_clicks):
    nodes = [
        {
            'data': {'id': node, 'label': node, "is_src": (1 if node.startswith("s") else 0),
                     "is_puit": (1 if node.startswith("p") else 0)},
        }
        for node in nodes_set
    ]

    edges = [
        {'data': {'source': source, 'target': target, "capacity": capacity, "weight": 0,
                  "label": str(0) + "/" + str(capacity)}}
        for source, target, capacity in edges_set
    ]
    if(n_clicks and n_clicks > 0):
        aff = solve(path)
        nodes = [
            {
                'data': {'id': node, 'label': node, "is_src": (1 if node.startswith("s") else 0),
                         "is_puit": (1 if node.startswith("p") else 0)},
            }
            for node in nodes_set
        ]
        edges = []
        for source, target, capacity in edges_set:
            if((source,target) in aff):
                edges.append({'data': {'source': source, 'target': target, "capacity": capacity, "weight": aff[(source,target)],
                                  "label": str(aff[(source,target)]) + "/" + str(capacity),"saturated":1 if float(capacity)-float(aff[(source,target)]) == 0 else 0}})
            else:
                edges.append({'data': {'source': source, 'target': target, "capacity": capacity, "weight": 0,
                                  "label": str(0) + "/" + str(capacity)},"saturated":0})
    return  nodes+edges




if __name__ == '__main__':
    app.run_server(debug=True)