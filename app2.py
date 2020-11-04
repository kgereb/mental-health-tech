# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

    
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

short_survey_df = pd.read_csv('kaggle_datasets/OSMI 2019 Mental Health in Tech Survey Results - OSMI Mental Health in Tech Survey 2019.csv')


all_options =  {
  "Demographics":[
     '*Are you self-employed?*',
     'What is your age?',
     'What is your gender?',
     'What country do you *live* in?',
     'What US state or territory do you *live* in?',
     'What is your race?',
     'What country do you *work* in?',
     'How many employees does your company or organization have?',
     'Is your employer primarily a tech company/organization?',
     'Is your primary role within your company related to tech/IT?'],
 
"Work benefits": 
     ['Does your employer provide mental health benefits as part of healthcare coverage?',
     'Has your employer ever formally discussed mental health (for example, as part of a wellness campaign or other official communication)?', 
     'Would you feel comfortable discussing a mental health issue with your direct supervisor(s)?',
     'Have you ever discussed your mental health with your employer?',
     'Describe the conversation you had with your employer about your mental health, including their reactions and what actions were taken to address your mental health issue/questions.',
     'Have you ever discussed your mental health with coworkers?',
     'If you have revealed a mental health disorder to a coworker or employee, how has this impacted you or the relationship?',
     'Overall, how much importance does your employer place on physical health?',
     'Overall, how much importance does your employer place on mental health?'],
"Employee mental health":[   
     'Do you *currently* have a mental health disorder?',
     'Have you ever been *diagnosed* with a mental health disorder?',
     '*What disorder(s) have you been diagnosed with?*',
     '*If possibly, what disorder(s) do you believe you have?*',
     '*If so, what disorder(s) were you diagnosed with?*',
     'Have you had a mental health disorder in the past?',
     'Have you ever sought treatment for a mental health disorder from a mental health professional?',
     'Do you have a family history of mental illness?',         
     'Are you openly identified at work as a person with a mental health issue?',
     'Has being identified as a person with a mental health issue affected your career?',
     'How has it affected your career?',          

    'Do you believe your productivity is ever affected by a mental health issue?',
     'If yes, what percentage of your work time (time performing primary or secondary job functions) is affected by a mental health issue?',           
     'Do you have medical coverage (private insurance or state-provided) that includes treatment of mental health disorders?',
     'How willing would you be to share with friends and family that you have a mental illness?'],
  
"Response":[  
     'If you have been diagnosed or treated for a mental health disorder, do you ever reveal this to clients or business contacts?',
     'If you have revealed a mental health disorder to a client or business contact, how has this affected you or the relationship?',
     'Would you bring up your *mental* health with a potential employer in an interview?',
     'Why or why not?.1',
     'Have you observed or experienced an *unsupportive or badly handled response* to a mental health issue in your current or previous workplace?',
     'Describe the circumstances of the badly handled or unsupportive response.',
     'Have you observed or experienced a *supportive or well handled response* to a mental health issue in your current or previous workplace?',
     'Describe the circumstances of the supportive or well handled response.',
     'Overall, how well do you think the tech industry supports employees with mental health issues?',
     'Briefly describe what you think the industry as a whole and/or employers could do to improve mental health support for employees.'
     ]}   

app.layout = html.Div([
    dcc.RadioItems(
        id='countries-radio',
        options=[{'label': k, 'value': k} for k in all_options.keys()],
        value='Demographics'
    ),

    html.Hr(),

    dcc.RadioItems(id='cities-radio'),

    html.Hr(),

    #html.Div(id='display-selected-values')
    
    dcc.Graph(
        id='display-selected-values',
        #figure=set_display_children(selected_country, selected_city)
            )    
])


@app.callback(
    Output('cities-radio', 'options'),
    [Input('countries-radio', 'value')])
def set_cities_options(selected_country):
    return [{'label': i, 'value': i} for i in all_options[selected_country]]


@app.callback(
    Output('cities-radio', 'value'),
    [Input('cities-radio', 'options')])
def set_cities_value(available_options):
    return available_options[0]['value']


# def get_columns(answer):
#     df = short_survey_df[categories_questions.get(str(answer))]
#     return df

# def get_answer(question):
#     df = short_survey_df[[question]]
#     return df


@app.callback(
    Output('display-selected-values', 'figure'),
    [Input('countries-radio', 'value'),
     Input('cities-radio', 'value')])
def set_display_children(selected_country, selected_city):
   # questions_df = get_columns(selected_country)
  #  answers_df = get_answer(selected_city)   

    labels = short_survey_df[selected_city].value_counts().reset_index()['index'].head()
    values = short_survey_df[selected_city].value_counts().reset_index()[selected_city].head()

    #colors=['lightcyan','cyan', 'darkblue']
    colors = ['gold', 'mediumturquoise', 'darkorange'] #, 'lightgreen']


    # Use `hole` to create a donut-like pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, 
                                 values=values, 
                                 hole=.2,
                                 #textinfo='label+percent',
                               #  insidetextorientation='radial' 
      )])

    fig.update_traces(textfont_size=15,
                      marker=dict(colors=colors, line=dict(color='#000000', width=1)),
                       )

    fig.update(layout_title_text=selected_city,
               layout_showlegend=True)

    
    return fig





if __name__ == '__main__':
    app.run_server(debug=True)