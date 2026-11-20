from dash import Dash,html,dcc,Input,Output
import dash_bootstrap_components as dbc
import dash
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
df=pd.read_csv("covid_19_india.csv")
df['Date']=pd.to_datetime(df["Date"],dayfirst=True)
df.columns=df.columns.str.strip()
numerical_cols=[
    "ConfirmedIndianNational",
    "ConfirmedForeignNational",
    "Cured",
    "Deaths",
    "Confirmed"
]
for col in numerical_cols:
    df[col]=pd.to_numeric(df[col],errors='coerce')
df=df.fillna(0)



app=Dash(__name__,external_stylesheets=[dbc.themes.DARKLY])
server=app.server
app.title="COVID19 INDIA Dashboard"
states=sorted(df["State/UnionTerritory"].dropna().astype(str).str.strip().unique())
states=sorted(states)
print(states)



app.layout=dbc.Container([
     html.H1("COVID19 INDIA Dashboard",
        className="text-center text-info mt-4 mb-4"),
        html.P("COVID-19 cases,rocoveries and deaths analysis",className="text-center text-light"),
    
    dbc.Row([
        dbc.Col([
        html.Label("select state/union trritory", className='text-light'),
        dcc.Dropdown(id='state-dropdown',options=[{"label": state,"value": state} for state in states],
                     value=states[0],placeholder=" Select a State/UnionTerritory",clearable=False)
        ],width=6,className='mx-auto')
    ],className='mb-4'),dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5('Confirmed'),
                html.H2(
                    id='confirmed-card',className='text-warning'
                )
            ])
        ],
        color='dark',outline=True
        ),md=4),dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5('cured'),
                html.H2(
                    id='cured-card',className='text-success'
                )
            ])
        ],color='dark',outline=True),md=4
        ),dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H5('Deaths'),
                    html.H2(
                        id='deaths-card',className='text-danger'
                    )
                ])
            ],color='dark',outline=True),md=4
        )
    ],className='mb-4'
    ),dbc.Row([
        dbc.Col(
            dcc.Graph(id='cases-line-chart'),md=12
        ),dbc.Col(
            dcc.Graph(id='cases-bar-chart'),md=6
        ),dbc.Col(
            dcc.Graph(id='death-bar-chart'),md=6
        )
]
),dbc.Row([
    dbc.Col(
        dcc.Graph(id='recovery-chart'),md=12
    )
])
],fluid=True
)
@app.callback([
    Output("confirmed-card","children"),
    Output("cured-card","children"),
    Output("deaths-card","children"),
    Output("cases-line-chart","figure"),
    Output("cases-bar-chart","figure"),
    Output("death-bar-chart","figure"),
    Output("recovery-chart","figure"),
    
    ]
    ,Input('state-dropdown','value')
    
    )
def update_dashboard(selected_state):
    state_df=df[df['State/UnionTerritory']==selected_state].copy()
    state_df=state_df.sort_values('Date')
    latest=state_df.iloc[-1]
    confirmed=int(latest['Confirmed'])
    cured=int(latest['Cured'])
    deaths=int(latest['Deaths'])
    line_fig=px.line(state_df,x='Date',y=['Confirmed','Cured','Deaths'],markers=True,title=f'COVID-19 Trend-{selected_state}')
    line_fig.update_layout(
        template='plotly_dark',
        xaxis_title='Date',
        yaxis_title='number of cases'
    )
    bar_fig=px.bar(state_df,x='Date',y='Confirmed',title=f'Confirmed Cases-{selected_state}')
    bar_fig.update_layout(template='plotly_dark',xaxis_title='Date',yaxis_title='Confirmed cases')
    death_fig=px.bar(
        state_df,
        x='Date',
        y='Deaths',
        title=f'Deaths-{selected_state}'
    )
    death_fig.update_layout(
        template='plotly_dark',
        xaxis_title='Date',
        yaxis_title='Deaths'
    )
    recovery_fig=px.area(
        state_df,
        x='Date',
        y='Cured',
        title=f"Rrcovered/Cured Cases-{selected_state}"
    )
    recovery_fig.update_layout(
        template='plotly_dark',
        xaxis_title='Date',
        yaxis_title='Cured Cases'
    )

    return(
        f"{confirmed:,}",
        f"{cured:,}",
        f"{deaths:,}",
        line_fig,
        bar_fig,
        death_fig,
        recovery_fig

    )
 


if __name__ == "__main__":
    app.run(debug=True, port=8050)
