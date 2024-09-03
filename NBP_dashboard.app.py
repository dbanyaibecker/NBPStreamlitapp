# Python script for my first streamlit application
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns 
import streamlit as st 
import matplotlib.ticker as ticker 
import plotly.tools as tls
import plotly.express as px

st.set_page_config(layout='wide')

# Custom CSS for background and text color
custom_css = """
<style>
    body {
        background-color: #f8f2e1;  /* Light gray background */
        color: #FF000;  /* Darker text color */
    }
    .stApp {
        background-color: #FFFFFF;
    }
    .css-1d391kg {  /* Sidebar class */
        background-color: #FF000;  /* Secondary background color for sidebar */ # doesnt work but idk why 
    }
    h1, h2, h3, h4, h5, h6 {
        color: #FF0000;  /* Custom header color */
    }
</style>
"""
from PIL import Image

# Open an image file
img_path = "BCSLogo.png"
img_path2 = "BCSbirds.png"
image = Image.open(img_path)
image2 = Image.open(img_path2)


# Display the image using Streamlit
st.image(image, width=500)
st.markdown('<h6 style="color:black; font-size:20px;">This dashboard allows you to explore and visualize Birds Connect Seattle data.</h6>', unsafe_allow_html=True)   
st.markdown('<h6 style="color:black; font-size:20px;">Use the selection boxes below to filter and generate charts based on species, location, and dates.</h6>', unsafe_allow_html=True)   
st.markdown('<h6 style="color:black; font-size:20px;">Whether you are analyzing trends or exploring specific sightings, this tool provides insights into our local bird populations and their behaviors.</h6>', unsafe_allow_html=True) 


bcs_colors = {'dark green' : "#0A3C23",
  'cream' : "#FAF5F0",
  'yellow green' : "#E6FF55",
  'peach' : "#FFB98C",
  'bright green' : "#36BA3A"} 

def theme_bcs(fig): 
    fig.update_layout( 
    # Background: 
     plot_bgcolor=bcs_colors["cream"],
        paper_bgcolor=bcs_colors["cream"],
        
        # Grid Lines
        xaxis=dict(showgrid=True, gridcolor=bcs_colors["dark green"], gridwidth=0.5, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor=bcs_colors["dark green"], gridwidth=0.5, zeroline=False),
        
        # Text
        font=dict(color=bcs_colors["dark green"]),
        title=dict(font=dict(size=28, color=bcs_colors["dark green"], family="bold")),
        xaxis_title=dict(font=dict(color=bcs_colors["dark green"])),
        yaxis_title=dict(font=dict(color=bcs_colors["dark green"])),
        
        # Legend
        legend=dict(
            bgcolor=bcs_colors["cream"],
            font=dict(color=bcs_colors["dark green"]),
        ),
        
        # Margins and Borders
        margin=dict(l=50, r=50, t=90, b=50),
    )
    
    # Customizing traces (e.g., lines, markers)
    fig.update_traces(
        # line=dict(color=bcs_colors["dark green"]),
        marker=dict(color=bcs_colors["dark green"]),
    )
    
    return fig

url = "https://docs.google.com/spreadsheets/d/1iPxblBkWb-Iky5WGPTq2LoJYlm6fPgID_HCAhtRpIa8/pub?output=csv"
@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    df['survey_date'] = pd.to_datetime(df['survey_date']).dt.date # ensure datetime date format for survey_date column
    df['detections'] = df[['seen','heard','fly']].apply(lambda x : x.sum(), axis = 1) # calculate detections 
    return df
df = load_data(url)

df.columns = df.columns.str.lower()
# Inject CSS into the app
st.markdown(custom_css, unsafe_allow_html=True)
# make small dataframes for each individual park 
Seward = df[df['park'] == 'Seward Park'] # create a new df from og where park is equal to 'Seward Park'
GoldenGardens = df[df['park'] == 'Golden Gardens Park']
Discovery = df[df['park'] == 'Discovery Park']
Carkeek = df[df['park'] == 'Carkeek Park']
Lincoln = df[df['park'] == 'Lincoln Park']
Magnuson = df[df['park'] == 'Magnuson Park']
Cheasty = df[df['park'] == 'Cheasty Greenspace']
WashingtonParkArboretum = df[df['park'] == 'Washington Park Arboretum']
Genesee = df[df['park'] == 'Genesee Park']
Walsh = df[df['park'] == 'Walsh Property']
Bliner = df[df['park'] == 'Bliner Property']
ShadowLakeBog = df[df['park'] == 'Shadow Lake Bog']
LakeForest = df[df['park'] == 'Lake Forest Park']
SoosCreek = df[df['park'] == 'Soos Creek']
ClarkLake = df[df['park'] == 'Clark Lake Park']
JenkinsCreek = df[df['park'] == "Jenkin's Creek Park"]

# Calculate richness from inputfile and map to the correct park
df['richness'] = df['park'].map({ # here we are creating a dictionary where based on inputfile['Park'] we map the richness calculation to the correct column
    'Seward Park' : len(Seward['species'].unique()),
    'Golden Gardens Park' : len(GoldenGardens['species'].unique()),
    'Discovery Park' : len(Discovery['species'].unique()),
    'Carkeek Park' : len(Carkeek['species'].unique()),
    'Lincoln Park' : len(Lincoln['species'].unique()),
    'Magnuson Park' : len(Magnuson['species'].unique()),
    'Cheasty Greenspace' : len(Cheasty['species'].unique()),
    'Washington Park Arboretum' : len(WashingtonParkArboretum['species'].unique()),
    'Genesee Park' : len(Genesee['species'].unique()),
    'Walsh Property' : len(Walsh['species'].unique()),
    'Bliner Property' : len(Bliner['species'].unique()),
    'Shadow Lake Bog' : len(ShadowLakeBog['species'].unique()),
    'Lake Forest Park' : len(LakeForest['species'].unique()),
    'Soos Creek' : len(SoosCreek['species'].unique()),
    'Clark Lake Park' : len(ClarkLake['species'].unique()),
    "Jenkin's Creek Park" : len(JenkinsCreek['species'].unique())
})

col1, gap, col2= st.columns([1,0.1,1])

#Viz 0 (boxplot of total species richness for entire data set)
with col1: 
    st.markdown('<h1 style="color:black; font-size:40px;">Neighborhood Bird Project Dashboard</h1>', unsafe_allow_html=True) # change font of title? 

    parksrich = pd.DataFrame(df.groupby('park').agg({'richness' : 'first'}).reset_index()) # groups df by park and then pulls the first value for richness associated with that park and maps it to the correct cell
    fig = px.bar(parksrich, x = 'park', y= 'richness', color_discrete_sequence=['#7dcea0'])
    # BEGINNING OF FORMATTING FOR PLOTLY.EXPRESS
    fig.update_layout(
        title={
        'text': 'Total Species Richness of <br>Surveryed Parks 1996-2023',
        'x': 0.5,  # Center the title
        'xanchor': 'center',  # Center align the title horizontally
        'yanchor': 'top',  # Anchor the title to the top
        'font': {
            'size' : 24,
            'color' : 'black'
        }
    },
        xaxis_title = 'Park',
        yaxis_title = 'Species Richness',
        width = 800,
        height = 800,
        shapes =[
        dict(
            type='rect',
            x0=0,
            y0=0,
            x1=1,
            y1=1,
            xref='paper',
            yref='paper',
            line=dict(
                color='black',
                width=2
            ),
            fillcolor='rgba(0,0,0,0)'  # Transparent fill
        )
    ],
        margin = dict(l=40, r=40)
        )
    fig.update_xaxes(tickangle = -45,
                     title_font = dict(size = 18, color = 'black'),
                     tickfont = dict(size = 18, color = 'black'))
    fig.update_yaxes(range=[0, df['richness'].max()+20], 
                     title_font = dict(size = 18, color = 'black'),
                     tickfont = dict(size = 18, color = 'black')) # END FORMATING
    theme_bcs(fig)
    st.write(fig)
    
    
    st.markdown('<hr style= "border: 2px solid black;">', unsafe_allow_html= True)    

# Viz 0.5
    years_sorted = sorted(df['year'].unique()) # Creates a list of unique years in ascending order 
    selected_year = st.selectbox('Select a Year', years_sorted) # Create a select box to pick which column to use in the barplot
    min_value = st.slider('Select a minimum value for richness', min_value= 0, max_value= 250, value=0)
    filtered_df = df[(df['year'] == selected_year) &  (df['richness'] >= min_value)] # filter the dataframe based on the selected year & minimum value
    
    filtered_df1 = pd.DataFrame(filtered_df.groupby('park').agg({'richness' : 'first'}).reset_index()) 

    fig1 = px.bar(filtered_df1, x = 'park', y= 'richness', color_discrete_sequence=['#7dcea0'])
    
    fig1.update_layout(
        title={
        'text': f"Species Richness by Park {selected_year}",
        'x': 0.5,  # Center the title
        'xanchor': 'center',  # Center align the title horizontally
        'yanchor': 'top',  # Anchor the title to the top
        'font': {
            'size' : 24,
            'color' : 'black'
        }
    },
        xaxis_title = 'Park',
        yaxis_title = 'Species Richness',
        width = 800,
        height = 800,
        shapes =[
        dict(
            type='rect',
            x0=0,
            y0=0,
            x1=1,
            y1=1,
            xref='paper',
            yref='paper',
            line=dict(
                color='black',
                width=2
            ),
            fillcolor='rgba(0,0,0,0)'  # Transparent fill
        )
    ],
        margin = dict(l=40, r=40)
        )
    fig1.update_xaxes(tickangle = -45,
                     title_font = dict(size = 18, color = 'black'),
                     tickfont = dict(size = 18, color = 'black'))
    fig1.update_yaxes(range=[0, df['richness'].max()+20], 
                     title_font = dict(size = 18, color = 'black'),
                     tickfont = dict(size = 18, color = 'black')) 
    theme_bcs(fig1)
    st.write(fig1)
    st.markdown("<div style = 'height: 550px;'></div>", unsafe_allow_html=True)
    st.image(image2, width=700)

with gap: 
    st.markdown("<div style = 'height: 80px;'></div>", unsafe_allow_html=True)

with col2:     
    st.markdown("<div style='height: 0px;'></div>", unsafe_allow_html=True)  # Adjust height as needed here for lowering start of col2  

    # # Viz #1 - count of all species at a PARK on a given day 
    parks = sorted(df['park'].unique()) # create & sort list alphabeticlly of parks in inputfile 
    selectedpark = st.selectbox('Select Park', parks, key = 'park_select_1')

    filter1 = pd.DataFrame(df[(df['park'] == selectedpark)]) # make new df "filter1" based on selected park
    
    # filter for dates at the "SELECTEDPARK" below 
    survey_dates = sorted(filter1['survey_date'].unique()) # creates unique list of survey dates from filter1
    selected_date = st.selectbox('Select survey date: YYYY-MM-DD',survey_dates) # streamlit selection box of survey dates available 
    filter2 = pd.DataFrame(filter1[(filter1['survey_date'] == selected_date)]) # filter filter 1 into another for the graph to use based on selected date
    specdet = pd.DataFrame(filter2.groupby('species')['detections'].sum())
    
    specdet.reset_index()
    fig2 = px.bar(specdet,y = 'detections', color_discrete_sequence=['#7dcea0'])
    fig2.update_layout(
        title={
        'text': f"Count of Each Species at <br>{selectedpark} on {selected_date}",
        'x': 0.5,  # Center the title
        'xanchor': 'center',  # Center align the title horizontally
        'yanchor': 'top',  # Anchor the title to the top
        'font': {
            'size' : 24,
            'color' : 'black'
        }
    },
        xaxis_title = 'Species',
        yaxis_title = 'Number of Detections',
        width = 800,
        height = 800,
        shapes =[
        dict(
            type='rect',
            x0=0,
            y0=0,
            x1=1,
            y1=1,
            xref='paper',
            yref='paper',
            line=dict(
                color='black',
                width=2
            ),
            fillcolor='rgba(0,0,0,0)'  # Transparent fill
        )
    ],
        margin = dict(l=40, r=40)
        )
    fig2.update_xaxes(tickangle = -90,
                     title_font = dict(size = 18, color = 'black'),
                     tickfont = dict(size = 18, color = 'black'))
    fig2.update_yaxes(range=[0, specdet['detections'].max()+(specdet['detections'].max()*0.05)], 
                     title_font = dict(size = 18, color = 'black'),
                     tickfont = dict(size = 18, color = 'black'))
    theme_bcs(fig2)
    st.write(fig2)
    st.write(f"No other species were recorded at {selectedpark} on {selected_date}")
    st.markdown('<hr style= "border: 2px solid black;">', unsafe_allow_html= True)     
#     #Viz 2
    # species detection numbers for any given survey
    
    parks3 = sorted(df['park'].unique())
    park = st.selectbox('Select a park', parks3, key= 'park_select_3')
    dfparky = pd.DataFrame(df[df['park'] == park]) 
    stationz = sorted(dfparky['station'].unique())
    station = st.selectbox('Select a station',stationz)
    dfparkstation = pd.DataFrame(dfparky[dfparky['station'] == station])
    datez = sorted(dfparkstation['survey_date'].unique())
    # date = selected_date = st.date_input("Select a date") # cool - adds a calendar widget but won't work well here due to sporadic date options
    date = st.selectbox('Select survey date: YYYY-MM-DD',datez, key = "date1")
    dfparkstationdate = dfparkstation[dfparkstation['survey_date'] == date]

    sums = pd.DataFrame(dfparkstationdate.groupby('species')['detections'].sum())
    
    figsurv = px.bar(sums, y = 'detections', color_discrete_sequence=['#7dcea0'])
    figsurv.update_layout(
        title={
        'text': f"Number of Detections by Species at {park},<br> station {station}, on {date}",
        'x': 0.5,  # Center the title
        'xanchor': 'center',  # Center align the title horizontally
        'yanchor': 'top',  # Anchor the title to the top
        'font': {
            'size' : 24,
            'color' : 'black'
        }
    },
        xaxis_title = 'Species',
        yaxis_title = 'Number of Detections',
        width = 800,
        height = 800,
        shapes =[
        dict(
            type='rect',
            x0=0,
            y0=0,
            x1=1,
            y1=1,
            xref='paper',
            yref='paper',
            line=dict(
                color='black',
                width=2
            ),
            fillcolor='rgba(0,0,0,0)'  # Transparent fill
        )
    ],
        margin = dict(l=40, r=40)
        )
    figsurv.update_xaxes(tickangle = -45,
                        title_font = dict(size = 18, color = 'black'),
                        tickfont = dict(size = 18, color = 'black'))
    figsurv.update_yaxes(range=[0, sums['detections'].max()+sums['detections'].max()*0.05], 
                        title_font = dict(size = 18, color = 'black'),
                        tickfont = dict(size = 18, color = 'black'))
    theme_bcs(figsurv)
    st.write(figsurv)
    
    #Viz 2 - count of ONE species in a park through time (yearly)

    # create functions that can cache the ct_year dataframe and chart so that this isn't rerun every time a selection box in column 1 is changed
    @st.cache_resource
    def filterparks(park, species): 
        filtered_data = df[(df['park'] == park) & (df['species'] == species)]
        ct_year = pd.DataFrame(filtered_data.groupby('year')['detections'].sum().reset_index())
        return ct_year
    
    @st.cache_resource
    def create_plot(filtered_dataframe):
        line = px.scatter(filtered_dataframe, x = 'year', y = 'detections', color_discrete_sequence=['#7dcea0'], trendline= 'ols')
        line.update_layout(
            title={
            'text': f'Annual Number of Detections of<br>{selected_species} at {selected_park}',
            'x': 0.5,  # Center the title
            'xanchor': 'center',  # Center align the title horizontally
            'yanchor': 'top',  # Anchor the title to the top
            'font': {
                'size' : 24,
                'color' : 'black'
            }
        },
            xaxis_title = 'Year',
            yaxis_title = 'Mean Number of Detections',
            width = 1000,
            height = 500,
            shapes =[
            dict(
                type='rect',
                x0=0,
                y0=0,
                x1=1,
                y1=1,
                xref='paper',
                yref='paper',
                line=dict(
                    color='black',
                    width=2
                ),
                fillcolor='rgba(0,0,0,0)'  # Transparent fill
            )
        ],
            margin = dict(l=40, r=40)
            )
        line.update_xaxes(tickangle = 0,
                        title_font = dict(size = 18, color = 'black'),
                        tickfont = dict(size = 18, color = 'black'),
                        nticks = 10)
        line.update_yaxes(title_font = dict(size = 18, color = 'black'),
                        tickfont = dict(size = 18, color = 'black'))
        theme_bcs(line)
        return(line)


    # Initialize session state attributes if they do not exist
    if 'species_options' not in st.session_state:
        st.session_state.species_options = []
    if 'previous_park' not in st.session_state:
        st.session_state.previous_park = None


    selected_park = st.selectbox("Select a park", options=sorted(df['Park'].unique())) # create list of unique parks in dataframe 

    if 'species_options' not in st.session_state or st.session_state.previous_park != park: # if the currently selected park doesn't equal park from the selection box 
        st.session_state.species_options = sorted(df[df['Park'] == selected_park]['Species'].unique()) # then filter the df and pull out species for THAT selection box 
        st.session_state.previous_park = park # AND update the selected_park in the cached session_state so that next time it's changed the plot will update

    selected_species = st.selectbox("Select species", options=st.session_state.species_options)

    filtered_df = filterparks(selected_park, selected_species) # use the function i made earlier to filter the data by the selected options
    plot = create_plot(filtered_df) # same here for the plot 

    st.write(plot)
    st.markdown('<hr style= "border: 2px solid black;">', unsafe_allow_html= True)
