import connectorx as cx
from config import Config
from dash import dcc
from dash import dash_table


def get_data():
    df = cx.read_sql(conn=Config.QUERY_DATABASE_URI, query='''select * from data_overview''',
                     return_type="pandas")
    # df = table.to_pandas(split_blocks=False, date_as_object=False)
    df.rename(columns={
        'dt_start': 'date',
        'raffles_net_cancels': 'Total Raffles'
    }, inplace=True)
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

    data = df.sort_values('date', ascending=False)  # .to_dict('records')
    return data


def create_tab(content, label, value):
    return dcc.Tab(
        content,
        label=label,
        value=value,
        id=f'{value}-tab',
        className='single-tab',
        selected_className='single-tab--selected'
    )


def create_table(name, columns, data):
    return dash_table.DataTable(
        id=f'{name}-table',
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
