'''PARETO Analysis Web App
Streamlit web that analyzes customers and return top/ main customers.

Author Diana Kung'u
'''
# Load Libraries
from datetime import datetime
from pandas import read_csv
import streamlit as st
from datetime import datetime
from streamlit_option_menu import option_menu
import base64

#Read Data
df = read_csv(r'E:\66DaysofData\Pareto_Analysis\Pareto Input.csv')


#---------------------------------------------------------------------------------
# Process Data
#Aggregate the data to the total sales for each customer
df = df.groupby(['Customer ID', 'First Name', 'Surname']).Sales.sum().reset_index()
df.Sales = df.Sales.round(2)
#Calculate the percent of total sales each customer represents
df['% of Total'] = df['Sales']*100/df['Sales'].sum()
#Order by the percent of total in a descending order
df = df.sort_values(by=['% of Total'], ascending= False)

#Calculate the running total of sales across customers
df['Running % of Total'] = df['% of Total'].cumsum().round(2)

# Create column with total no. unique customers
#-----------------------------------------------------------------------------------


#APP

#Date
date = datetime.now().date()

#Sidebar
logo = 'the-sum-of.png'

buff1, col1, buff2 = st.sidebar.columns([1,1,1])
col1.markdown(
    f"""
    <div class="container">
        <img class="logo-img" src="data:image/png =*100;base64,{base64.b64encode(open(logo, "rb").read()).decode()}">
        
    </div>
    """,
    unsafe_allow_html=True
)
                                                      
st.sidebar.markdown( "<h1 style='text-align: center; color: '#ff4f23';\
                    '>Sigma Holdings LLC</h1>", unsafe_allow_html=True)
st.sidebar.markdown( "<h4 style='text-align: center; color: black;\
                    '> Author: Diana Kung'u</h4>", unsafe_allow_html=True)
#st.sidebar.write(date)


with st.sidebar:
    choose = option_menu("MENU", ["Summary", "Pareto Analysis", "RFM Analysis", "Contact", "Settings"],
                         icons=['house', 'activity', 'kanban', 'book', 'gear'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#ffffff"},
        "icon": {"color": "#ff4f23", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#23ffa1"},
    }
    )
    
st.sidebar.markdown(
    """<a style='display: block; text-align: center;' 
        href ="https://preppindata.blogspot.com/2022/03/2022-week-13-pareto-parameters.html"\
             >Data Source: Preppin' Data</a>
    """,
    unsafe_allow_html=True,
)

#Pareto body
if choose == 'Summary':
    st.markdown(
        """<h1 style='display: block; text-align: left;'> Summary
            
        """,
        unsafe_allow_html=True
        )

    about_txt = st.markdown('''
                            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut a velit ullamcorper, 
                            sollicitudin turpis in, pulvinar dolor. Ut ac bibendum sapien. Maecenas placerat volutpat
                            quam. Cras dictum diam sed turpis ultricies, vel interdum odio cursus. Donec malesuada ac
                            tortor ut condimentum. Maecenas nec aliquam leo, eget tristique ante. 
                            ''')

if choose == 'Pareto Analysis':
    #title
    st.title("PARETO ANALYSIS")

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
        
        
        #Display DataFrame
        st.markdown("<h4 style='display: block; text-align: left;'> Customer Details",
                    unsafe_allow_html=True)
        
        df_res =result[1]
        df_res['Customer Name'] = df_res['First Name'] + " " + df_res['Surname']
        df_res = result[1].drop(['Running % of Total', 'First Name', 'Surname' ], axis=1)
        
        df_res = df_res[['Customer ID','Customer Name', 'Sales', '% of Total']]
        st.dataframe(df_res.style.format(subset= ['Sales', '% of Total'], formatter="{:.2f}"), 
                    width=3000, height= 400)
        #st.write(df_res[['Sales', '% of Total']].style.format("{:.2}"))
        
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
