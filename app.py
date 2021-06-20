import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px


# url =  'https://raw.githubusercontent.com/realpython/materials/master/python-dash/apps/app_2/avocado.csv'
# data = pd.read_csv(url, index_col=0)
# data = data.query("type == 'conventional' and region == 'Albany'")
# data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
# data.sort_values("Date", inplace=True)

cols = [ 
    "tweet_id",       
    "user_id",             
    "created_at_str", 
    "date",           
    "text",           
    "hashtags",       
    "lang",           
    "profilepic",      
    "location",
    "place",
    "retweet_count", 
    "is_Verfied",      
    "followers_count",     
    "joined_in",
    "geo",            
    "source" ]
data = pd.read_csv('/home/arun/Documents/mlwebapp/dash/rawtweets.csv', names = cols, header = None)

##plot device
df1 = pd.DataFrame(data['source'].value_counts()[:4])
df1['device'] = ['Twitter for Android', 'Twitter Web App', 'Twitter iPhone App', 'Twitter for iPad']
df1.reset_index(drop=True, inplace=True)

device = px.pie(df1 ,names='device',values='source',title='Devices used for Tweeting' ,color_discrete_sequence=px.colors.sequential.RdBu,hole=0.2)


##plot influencial people
df3 = data.sort_values('followers_count',ascending=False)
df3 = df3.head(10)
df3 = df3[['tweet_id', 'user_id', 'date', 'text', 'hashtags',
       'location',  'retweet_count',
       'is_Verfied', 'followers_count']]


import base64
# image_filename = 'jimmy.jpg' # replace with your own image
# encoded_image = base64.b64encode(open(image_filename, 'rb').read())

#plot scatter
df6 = pd.read_csv('/home/arun/Documents/mlwebapp/dash/datentext.csv')
scatter = px.scatter(df6, x='tb_Subj', y='compound', color='compound')
scatter.show()

#barcaht
df7 = df6['sentiment'].value_counts()

df7= pd.DataFrame(df7)
df7.reset_index(drop=True, inplace=True)
df7['status'] = ['Positive', 'Neural', 'Negative']
barr= px.bar(df7, x="status", y="sentiment", color ='sentiment', title="Product sales distribution on each city", barmode='group')


#country
import plotly.graph_objects as go
import pandas as pd

#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv')

df = pd.read_csv('country.csv')

fig = go.Figure(data=go.Choropleth(
    locations = df['CODE'],
    z = df['COUNTS'],
    text = df['COUNTRY'],
    colorscale = 'Blues',
    autocolorscale=False,
    reversescale=False,
    marker_line_color='darkgray',
    marker_line_width=0.5,
#     colorbar_tickprefix = '$',
    colorbar_title = 'Tweets per country',
))

country = fig.update_layout(
    title_text='Countries with highest number people tweeting about Crypto Currencys',
    geo=dict(
        showframe=True,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
#     annotations = [dict(
#         x=0.55,
#         y=0.1,
#         xref='paper',
#         yref='paper',
# #         text='Source: <a href="https://www.cia.gov/library/publications/the-world-factbook/fields/2195.html">\
# #             CIA World Factbook</a>',
#         showarrow = False
#     )]
)

import plotly.graph_objs as go
people = go.Figure(data=[go.Table(
    header=dict(values=list(df3.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=df3.transpose().values.tolist(),
               fill_color='lavender',
               align='left'))
])

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Crypto Analytics: Understand Your Cryptos!"

# app.layout = html.Div([
#     html.Img(src='data:image/png;base64,{}'.format(encoded_image))
# ])


image_filename = 'testplot.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())
# app.layout = html.Div([
#     html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))
# ])

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="", className="header-emoji"),
                html.H1(
                    children="Crypto Analytics", className="header-title"
                ),
                html.P(
                    children="Analysis on the crpto currencies using tweeter data. Tweets specific to crytpo currencies are scraped from july 5-7",
                    className="header-description",
                ),
            ],
            className="header",
        ),
    dcc.Graph(
        id='Gross Income',
        figure=device
    ),
    dcc.Graph(
        id='people',
        figure=people  #What are the biggest accounts that used #cryptocurrency
    ),
    dcc.Graph(
        id='scatter',
        figure=scatter  #What are the biggest accounts that used #cryptocurrency
    ),
    dcc.Graph(
        id='barr',
        figure=barr  #What are the biggest accounts that used #cryptocurrency
    ),
    dcc.Graph(
        id='country',
        figure=country  #What are the biggest accounts that used #cryptocurrency
    ),
    html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))
    ]
    
)

if __name__ == "__main__":
    app.run_server(debug=True)