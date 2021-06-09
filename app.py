import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
import morfeusz2

def get_count(text):
    labels = {'gen': 'родительный падеж', 'loc': 'падеж места', 'inst': 'орудийный падеж',
              'pl': 'множественное число', 'acc': 'винительный падеж', 'sg': 'единственное число',
              'voc': 'звательный падеж', 'm1': 'мужской род от 1 лица', 'm2': 'одушевленный муж род',
              'm3': 'мужской род от 3 лица, неодушевлён муж род', 'nom': 'именительный падеж',
              'n': 'средний род', 'f': 'женский род', 'dat': 'дательный падеж'}
    morf = morfeusz2.Morfeusz()
    analysis = morf.analyse(text)
    subst = [(i, j, k) for i, j, k in analysis if k[2].split(':')[0]=='subst']
    items = []
    for i in [i[2][2][1:].split(':') for i in subst]:
        items.extend(i)
    marks = {}
    for i in items:
        if '.' not in i and i in labels:
            marks[labels[i]] = items.count(i)
    return tuple(marks.keys()), tuple(marks.values())

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Polish morfeus!"
df = {'category': ['noun', 'verb', 'attribute'], 'values': [1, 2, 3]}

data = [go.Pie(labels=df['category'], values=df['values'])]

app.layout = html.Div([
    html.P("Enter polish text:"),
    dcc.Textarea(
        id='textarea-value',
        value='Enter the text in polish',
        style={'width': '100%', 'height': 200},
    ),
    html.Button('Submit', id='textarea-button', n_clicks=0),
    dcc.Graph(id="textarea-output", figure={'data': data})
])

@app.callback(
    Output('textarea-output', 'figure'),
    [Input('textarea-button', 'n_clicks'),],
    [State('textarea-value', 'value'),],
)
def update_output(n_clicks, value):
    df['category'] = get_count(value)[0]
    df['values'] = get_count(value)[1]
    return {'data': [go.Pie(labels=df['category'], values=df['values'])]}

app.run_server(debug=True)