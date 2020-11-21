# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

    
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

short_survey_df = pd.read_csv('clean_mental_health_data.csv')

app.title = 'OSMI Mental Health Survey'


all_options =  {
  "Demographics":[
     '*Are you self-employed?*',
     'What is your gender?',
     'What country do you *live* in?',
     'What is your race?',
     'What country do you *work* in?',
     'How many employees does your company or organization have?',
     'Is your employer primarily a tech company/organization?',
     'Is your primary role within your company related to tech/IT?'],
 
"Mental health in the workplace": 
     ['Does your employer provide mental health benefits as part of healthcare coverage?',
     'Has your employer ever formally discussed mental health (for example, as part of a wellness campaign or other official communication)?', 
     'Would you feel comfortable discussing a mental health issue with your direct supervisor(s)?',
     'Have you ever discussed your mental health with your employer?',
     'Have you ever discussed your mental health with coworkers?',
     'Would you feel more comfortable talking to your coworkers about your physical health or your mental health?',
     'If you have revealed a mental health disorder to a coworker or employee, how has this impacted you or the relationship?',
     ],
    
"Employee mental health":[   
     'Do you *currently* have a mental health disorder?',
      'Have you had a mental health disorder in the past?',
     '*If so, what disorder(s) were you diagnosed with?*',
     'Have you ever sought treatment for a mental health disorder from a mental health professional?',
     'Are you openly identified at work as a person with a mental health issue?',       
    'Do you believe your productivity is ever affected by a mental health issue?',
     'If yes, what percentage of your work time (time performing primary or secondary job functions) is affected by a mental health issue?',           
     'Do you have medical coverage (private insurance or state-provided) that includes treatment of mental health disorders?',
      ],
    
"Reactions":[  
     'If you have been diagnosed or treated for a mental health disorder, do you ever reveal this to clients or business contacts?',
     'If you have revealed a mental health disorder to a client or business contact, how has this affected you or the relationship?',
      'Would you be willing to bring up a physical health issue with a potential employer in an interview?',
     'Would you bring up your *mental* health with a potential employer in an interview?',
     'Have you observed or experienced an *unsupportive or badly handled response* to a mental health issue in your current or previous workplace?',
     'Have you observed or experienced a *supportive or well handled response* to a mental health issue in your current or previous workplace?',
     'Overall, how well do you think the tech industry supports employees with mental health issues?'
],
    
    
  "Long responses": [  
      'Describe the conversation you had with your employer about your mental health, including their reactions and what actions were taken to address your mental health issue/questions.',  
      'Describe the conversation with coworkers you had about your mental health including their reactions.',
      'Describe the circumstances of the badly handled or unsupportive response.',
    'Briefly describe what you think the industry as a whole and/or employers could do to improve mental health support for employees.',
     'Would you bring up your physical health at a job interview - why or why not?',
     'Would you bring up your *mental* health at a job interview - why or why not?' ]
   
     }  

    
app.layout = html.Div([
            html.H1(children='Open Sourcing Mental Illness (OSMI) - Survey Analysis'),
            dcc.RadioItems(
            id='topics',
            options=[{'label': k, 'value': k} for k in all_options.keys()],
            value='Demographics'
            ),
            html.Hr(),
            dcc.RadioItems(id='questions'),
            html.Hr(),
            dcc.Graph(
                id='display-selected-values',
                    ),       
                ])



@app.callback(
    Output('questions', 'options'),
    [Input('topics', 'value')])
def set_questions_options(selected_topic):
    return [{'label': i, 'value': i} for i in all_options[selected_topic]]


@app.callback(
    Output('questions', 'value'),
    [Input('questions', 'options')])
def set_questions_value(available_options):
    return available_options[0]['value']
     
        
@app.callback(
    Output('display-selected-values', 'figure'),
    [Input('topics', 'value'),
     Input('questions', 'value')])
def set_display_children(selected_topic, selected_column): 
    if selected_topic=='Long responses': 
        
        fig = go.Figure(data=[go.Table(
                    header=dict(fill_color='paleturquoise',
                                align='left'),
               cells=dict(values=[short_survey_df[short_survey_df[selected_column].notnull()==True][selected_column]],
                   fill_color='lavender',
                   align='left'))
])

    else:
        # Show the first 6 groups only
        labels = short_survey_df[selected_column].value_counts().reset_index()['index'].head(6)
        values = short_survey_df[selected_column].value_counts().reset_index()[selected_column].head(6)
        colors = ['gold', 'mediumturquoise', 'darkorange']
        # Use `hole` to create a donut-like pie chart
        fig = go.Figure(data=[go.Pie(labels=labels, 
                                     values=values, 
                                     hole=.2,
                                 
          )])
        fig.update_traces(textfont_size=15,
                          marker=dict(colors=colors, line=dict(color='#000000', width=1)),
                           )
        fig.update(layout_title_text=f'In total, {len(short_survey_df[short_survey_df[selected_column].notna()])} people answered this question',
                   layout_showlegend=True)
        
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)
