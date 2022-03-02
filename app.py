#!/usr/bin/env python
# coding: utf-8

# In[2]:


import dash
from dash import html, dcc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from dash.dependencies import Input,Output
import plotly.graph_objects as go
from PIL import Image


df = pd.read_csv("Ranking_CB_Responses.csv", delimiter=',', header="infer")
df["Please indicate where you work"]=df["Please indicate where you work"].replace("Bank / Bank Consultants","Bank")
df["Please indicate where you work"]=df["Please indicate where you work"].replace("Fintech/Digital Bank","Fintech / Digital Bank")
#fig=df["How long have you worked at your current employer"].hist(bins=30, figsize=(30,30), color='r')
#fig = px.histogram(df,x="How long have you worked at your current employer",nbins=20)

df_work = df.drop(columns=["Timestamp","Country of Residence", "How long have you worked at your current employer"], axis=1)
df_work_Other = df_work[df_work['Please indicate where you work'] == 'Other']
df_work_Bank = df_work[df_work['Please indicate where you work'] == 'Bank']
df_work_Fin_Dig = df_work[df_work['Please indicate where you work'] == 'Fintech / Digital Bank']
df_work_Central = df_work[df_work['Please indicate where you work'] == 'Central Bank']

df_work_Other_mean = df_work_Other.mean()
df_work_Bank_mean = df_work_Bank.mean()
df_work_Fin_Dig_mean = df_work_Fin_Dig.mean()
df_work_Central_mean = df_work_Central.mean()

df2=pd.DataFrame(data=df_work_Other_mean)
df2['Other']=df_work_Other_mean
df2['Bank']=df_work_Bank_mean
df2['Fintech / Digital Bank']=df_work_Fin_Dig_mean
df2['Central Bank']=df_work_Central_mean


from scipy.stats import mannwhitneyu
U1, p = mannwhitneyu(df2['Bank'], df2['Other'], method="asymptotic")

df_df = df_work.groupby(by = 'Please indicate where you work').mean().T

df_ans = df.drop(columns=["Timestamp","Please indicate where you work","Country of Residence", "How long have you worked at your current employer"], axis=1)
corr_matrix = df_ans.corr().abs()

d={'col1':[38,29,15,2],'col2':["Other", "Bank", "FintechDigital Bank" ,"Central Bank"]}
df_num=pd.DataFrame(data=d)

d2={'col1':[37,26,3,2,2,2,2,2,2,1,1,1,1,1,1],'col2':["Spain","Egypt","Brasil","UAE","Saudi Arabia","Switzerland","Canada","Ecuador","Turkey","Dominican Republic","France","Switzerland_","USA","Africa","Germany"]}
df_num2=pd.DataFrame(data=d2)

fig4=px.pie(df_num, values='col1', names='col2')
fig5=px.pie(df_num2,values='col1', names='col2')

fig = px.histogram(df_df,x="Bank",nbins=30)
fig2 = px.imshow(corr_matrix,aspect="auto")

ops=df_work['Please indicate where you work'].unique()
labels=[{'label': i,'value':i} for i in ops]

fig3 = go.Figure()
heatmap= Image.open('Heatmap.jpg')

img_width = 1600
img_height = 1600
scale_factor = 0.5
# Add invisible scatter trace.
# This trace is added to help the autoresize logic work.
fig3.add_trace(
    go.Scatter(
        x=[0, img_width * scale_factor],
        y=[0, img_height * scale_factor],
        mode="markers",
        marker_opacity=0
    )
)

# Configure axes
fig3.update_xaxes(
    visible=False,
    range=[0, img_width * scale_factor]
)

fig3.update_yaxes(
    visible=False,
    range=[0, img_height * scale_factor],
    # the scaleanchor attribute ensures that the aspect ratio stays constant
    scaleanchor="x"
)

# Add image
fig3.add_layout_image(
    dict(
        x=0,
        sizex=img_width * scale_factor,
        y=img_height * scale_factor,
        sizey=img_height * scale_factor,
        xref="x",
        yref="y",
        opacity=1.0,
        layer="below",
        sizing="stretch",
        source=heatmap)
)

# Configure other layout
fig3.update_layout(
    width=img_width * scale_factor,
    height=img_height * scale_factor,
    margin={"l": 0, "r": 0, "t": 0, "b": 0},
)

fig6 = px.histogram(df_df,x="Bank",nbins=30)
fig7 = px.histogram(df_df,x="Other",nbins=30)
fig8 = px.histogram(df_df,x="Fintech / Digital Bank",nbins=30)
fig9 = px.histogram(df_df,x="Central Bank",nbins=30)

# In[3]:

from dash import dash_table

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
                "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]

app= dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title= "Digital currency webapp"
app.layout=html.Div([html.H1(children="Digital currency web-app", className="header-title"),
                    html.P(children="Analyze the survey result", className= "header-description",
                        ),
                    html.H2('Survey participants information(Work)',),
                    dcc.Graph(id='fig4',figure=fig4, className="card"),
                    html.H2('Survey participants information(Nationality)'),
                    dcc.Graph(id='fig5',figure=fig5,className="card"),
                    html.H2('Correlation matrix(Answers)'),
                    dcc.Graph(id='fig3',figure=fig3, className="card"),
                    html.H2('Results group by work'),
                    dash_table.DataTable(
                       id='table',
                       columns=[{"name": i, "id": i} 
                                for i in df_df.columns],
                       data=df_df.to_dict('records'),
                       style_cell=dict(textAlign='left'),
                       style_header=dict(backgroundColor="paleturquoise"),
                       style_data=dict(backgroundColor="lavender")
                    ),
                    html.H2('Select two categories you want to compare'),
                    html.Div(dcc.Dropdown(id='dropdown1',options= labels,className="card")),
                    html.Div(dcc.Dropdown(id='dropdown2',options= labels,className="card")),
                    html.H3('The p-value between these categories is',className="card"),
                    html.Div(id='result1',className="card"),
                    html.H2('Select a category you want'),
                    html.Div(dcc.Dropdown(id='dropdown',options= labels,className="card")),
                    dcc.Graph(id='fig1',figure=fig,className="card"),
                    html.H2('You can see all results below'),
                    html.H3('Bank result'),
                    dcc.Graph(id='fig6',figure=fig6,className="card"),
                    html.H3('Other result'),
                    dcc.Graph(id='fig7',figure=fig7,className="card"),
                    html.H3('Fintech and digital bank result'),
                    dcc.Graph(id='fig8',figure=fig8,className="card"),
                    html.H3('Central bank result'),
                    dcc.Graph(id='fig9',figure=fig9,className="card")
                    ])


@app.callback(Output('fig1','figure'),
              Input('dropdown','value'))

def update_graph(workstatus):
    
    fig=px.histogram(df_df[workstatus], x=workstatus, nbins=30, title=f'{workstatus} result')
    return fig
    
@app.callback(Output('result1','children'),
              Input('dropdown1','value'),
              Input('dropdown2','value'))

def update_result(a,b):
    
    U1, p = mannwhitneyu(df2[a], df2[b], method="asymptotic")
    return u'the p-value between {} and {} is {}'.format(
        a,b,p,
    )
    
    
app.run_server(debug=True,host = '127.0.0.1')