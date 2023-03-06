from data import GetExistingFromDB
from os.path import join
from data import path_queries
from dash import dcc
from dash import dash_table
from dash import html

tz_used = 'America/Chicago'
dt_begin = '2023-02-15'
# db_conn = os.environ.get('db_uri')

# filename = join(path_queries, 'counts_by_day')
query = 'select * from data_overview'
df = GetExistingFromDB(query=query)
df.rename(columns={
    'dt_start': 'date',
    'raffles_net_cancels': 'Total Raffles'
}, inplace=True)

def create_tab(content, label, value):
    return dcc.Tab(
        content,
        label=label,
        value=value,
        id=f'{value}-tab',
        className='single-tab',
        selected_className='single-tab--selected'
    )


# set column types
columns = [
    {'name': 'date', 'id': 'date', 'type': 'datetime'}
]
col_len = len(columns)
for name in df.columns[col_len:]:
    col_info = {
        'name': name,
        'id': name,
        'type': 'numeric',
        'format': {'specifier': ','}  ## NEEDED FOR NUMERIC COLUMNS
    }
    columns.append(col_info)

data = df.sort_values('date', ascending=False).to_dict('records')

raffle_table = dash_table.DataTable(
    id=f'raffle-table',
    columns=columns,
    data=data,
    fixed_rows={'headers': True},
    active_cell={'row': 0, 'column': 0},
    sort_action='native',
    derived_virtual_data=data,
    style_table={
        'minHeight': '80vh',
        'height': '80vh',
        'overflowY': 'scroll'
    },
    style_cell={
        'whitespace': 'normal',
        'height': 'auto',
        'fontFamily': 'verdana',
        'textAlign': 'center',
    },
    style_header={
        'fontFamily': 'verdana',
        'textAlign': 'center',
        'fontSize': 12
    },
    style_data={
        'fontSize': 12
    },
    style_data_conditional=[
        {'if': {'row_index': 'odd'}, 'backgroundColor': '#fafbfb'}
    ]
)

counts_tab = create_tab(raffle_table, 'Data Summary', 'data_counts')
table_tabs = dcc.Tabs(
    [counts_tab],
    className='tabs-container',
    id='table-tabs',
    value='data_counts'  # active tab
)

from app.extensions import top_bar

layout = html.Div(children=[
    html.Div(top_bar),
    html.Div([table_tabs])
])
