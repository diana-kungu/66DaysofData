""" This program deploys plotly charts on streamlit
    created by Diana Kung'u
"""
# Import Modules
from pandas import read_csv
from random import randint
import plotly.graph_objects as go
import streamlit as st


# Load Data
df_i = read_csv(r".\customer_interaction.csv", index_col='category')
df_i.loc[:, 'ProductAdded'] = [x + randint(1000, 2500) for x in df_i.loc[:, 'ProductAdded']]

#App
st.title("Customer Progression: Sales Funnel")
st.write("created by Diana Kung'u")
st.write("The following analyzes customer behaiviour by categories in Aws Store")
st.markdown("""From the analysis, it is evident that the store is receiving many potential
            customers, however the conversion rate is very low. **85%** of the customers leave the site
            after viewing out product.             
            Select heatmap option to compare progression along product categories or sankey diagram to analyze
            individual category"""
)
chart = st.sidebar.selectbox("Select chart type", ("Heatmap", "Sankey"))


if chart == "Sankey":
  # Create a Sankey Diagram
  categories =df_i.index.values.tolist()
  category_plot_names = []
  fig = go.Figure()

  buttons=[]

  default_category = "books"

  for cat in categories:
      x = sorted(df_i.loc[cat].values.tolist(), reverse=True)
      fig.add_traces(go.Sankey(
      node = dict(
        pad = 15,
        thickness = 20,
        line = dict(color = "black", width = 0.5),
        label = ['ProductViewed', "ProductAdded", 'CartViewed','Checkout', 'Sale' ],
        color = ["blue", "red", "yellow", "green", "purple", "cyan", "black"] 
      ),
      link = dict(
        source = [0, 1, 2, 3, 4],
        target = [1, 2, 3, 4],
        value = x
      ), 
      visible=(cat==default_category)
      ))
      
      category_plot_names.append(cat)

  for cat in categories:
      buttons.append(dict(method='update',
                          label=cat,
                          args = [{'visible': [cat==r for r in category_plot_names]}])) 
      
  # Add dropdown menus to the figure
  fig.update_layout(showlegend=False, updatemenus=[{"buttons": buttons, "direction": "down",
                                                    "active": categories.index(default_category),
                                                    "showactive": True, "x": 1, "y": 1.05}],
                    title_text = "~ 85% of Total customers Churn at Product-Viewed",
                    autosize = False,
                    width = 800,
                    height = 500)
  st.plotly_chart(fig)
else:
  df_i = df_i.sort_values(by=['ProductViewed'])
  #plt.figure(figsize=(6,5))

  fig = go.Figure(data =
                  go.Heatmap(x = df_i.columns, y = df_i.index.values,
                  z = df_i.values,
                  colorscale = 'plasma_r'))

  fig.update_xaxes(side="top")
  fig.update_layout(title_text = 'Majority of Customers Exit after ProductedViewed')
  st.plotly_chart(fig)


