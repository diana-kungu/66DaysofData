
# Load Libraries
from datetime import datetime
from pandas import read_csv
import streamlit as st
from datetime import datetime
from streamlit_option_menu import option_menu

#Read Data
df = read_csv(r'E:\66DaysofData\Pareto_Analysis\Pareto Input.csv')


#---------------------------------------------------------------------------------
# Process Data
#Aggregate the data to the total sales for each customer
df = df.groupby(['Customer ID', 'First Name', 'Surname']).Sales.sum().reset_index()
#Calculate the percent of total sales each customer represents
df['% of Total'] = df['Sales']*100/df['Sales'].sum()
#Order by the percent of total in a descending order
df = df.sort_values(by=['% of Total'], ascending= False)

#Calculate the running total of sales across customers
df['Running % of Total'] = df['% of Total'].cumsum().round(2)

# Create column with total no. unique customers
df['Total Customers'] = len(df)
#-----------------------------------------------------------------------------------


#APP
#title
st.title("PARETO ANALYSIS")
#Date
date = datetime.now().date()

#Sidebar
st.sidebar.image('''E:\66DaysofData\Pareto_Analysis\the-sum-of.png''', use_column_width= True)
                                                      
st.sidebar.markdown( "<h1 style='text-align: center; color: red;\
                    '>Sigma Holdings LLC</h1>", unsafe_allow_html=True)
st.sidebar.markdown( "<h4 style='text-align: center; color: black;\
                    '> Author: Diana Kung'u</h4>", unsafe_allow_html=True)
#st.sidebar.write(date)
st.sidebar.markdown(
    """<a style='display: block; text-align: center;' 
        href ="https://preppindata.blogspot.com/2022/03/2022-week-13-pareto-parameters.html"\
             >Data Source: Preppin' Data</a>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    choose = option_menu("App Gallery", ["About", "Photo Editing", "Project Planning", "Python e-Course", "Contact"],
                         icons=['house', 'camera fill', 'kanban', 'book','person lines fill'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#02ab21"},
    }
    )


#Pareto body
#Input box
col, buff1, buff2 = st.columns([2,2,2])
percent = col.number_input('Enter a percent', min_value= 1, max_value=99, step= None)


def pareto_fxn(df, percent):
    # Filter data based on selected % 
    df_select_percent = df[df['Running % of Total'] <= percent]
    prop = (f'{round(len(df_select_percent)*100/len(df))}% of Customers account \
        for {percent}% of Sales ')

    return prop, df_select_percent
    
if st.button('Run'):
    result = pareto_fxn(df, percent)
    st.write(result[0])
    st.write('')
    st.write('')
    st.write('The customers are')
    
    
    st.dataframe(result[1].style.hide_index(), width=1000, height= 400)
    
    #Download button
    def convert_df(df):
        return df.to_csv().encode('utf-8')


    csv = convert_df(result[1])

    st.download_button(
    "Press to Download",
    csv,
    "file.csv",
    "text/csv",
    key='download-csv'
        )
