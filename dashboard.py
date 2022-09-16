#from curses import color_content
#from turtle import color
import streamlit as st
import numpy as np
import pandas as pd
import webbrowser
import matplotlib.pyplot as plt
from sklearn import datasets
from streamlit_option_menu import option_menu
import warnings
warnings.filterwarnings("ignore")

# LOADING DATASET FROM SKLEARN 

cancer_data = datasets.load_breast_cancer(as_frame=True)
breast_cancer_dataset = pd.concat((cancer_data["data"], cancer_data["target"]), axis=1)
breast_cancer_dataset["target"] = [cancer_data.target_names[val] for val in breast_cancer_dataset["target"]]

# PAGE LAYOUT

st.set_page_config(
    page_title = "Breast Cancer Analysis", 
    layout="wide",
    page_icon="✨"
) 
st.title("Breast Cancer Analysis ")

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# NAVIGATION BAR  
selected = option_menu(None, ["Home", "Analysis"],
                       icons=['house', 'command'],
                       menu_icon="cast", default_index=0, orientation="horizontal")



# HOME PAGE                       

if selected == 'Home':
    st.markdown("<h2 style='text-align: center; color: grey;margin-bottom:5%'>ABOUT THE DASHBOARD</h1>", unsafe_allow_html=True)
    st.markdown("<div style ='display:block;background:#8080801c;padding: 25px 15px 25px 15px;'><ul><li>The dashboard is created using Python and Streamlit</li><li>The dashboard consists of analysis on the Breast Cancer Disease dataset from the Sklearn library</li><li>There are 4 charts for further analysis</li><li>Anyone can change the configurations of the charts using the dropdown button to check various results of the charts</li></li></div>", unsafe_allow_html=True)
    st.markdown("<h6 style='margin-top:5%'><strong>Created by</strong> : Tanmay MONDKAR </h6>", unsafe_allow_html=True)
    st.markdown("<h6><strong>Github link </strong> :https://github.com/tanny07/streamlit-dashboard</h6>", unsafe_allow_html=True)
        
    url = 'https://github.com/tanny07/streamlit-dashboard'
    if st.button('Github Link'):
        webbrowser.open_new_tab(url)
  


# ANALYZED CHARTS PAGE

def analyzed_charts():

# Scatter Chart 

    st.markdown("### Scatter Chart: Explore Relationship Between Measurements :")

    measurements = breast_cancer_dataset.drop(labels=["target"], axis=1).columns.tolist()

    x_axis = st.selectbox("X-Axis", measurements)
    y_axis = st.selectbox("Y-Axis", measurements, index=1)

    if x_axis and y_axis:
        scatter_fig = plt.figure(figsize=(6,4))
        scatter_ax = scatter_fig.add_subplot(111)
        malignant_df = breast_cancer_dataset[breast_cancer_dataset["target"] == "malignant"]
        benign_df = breast_cancer_dataset[breast_cancer_dataset["target"] == "benign"]
        malignant_df.plot.scatter(x=x_axis, y=y_axis, s=120, c="tomato", alpha=0.6, ax=scatter_ax, label="Malignant")
        benign_df.plot.scatter(x=x_axis, y=y_axis, s=120, c="dodgerblue", alpha=0.6, ax=scatter_ax,
                           title="{} vs {}".format(x_axis.capitalize(), y_axis.capitalize()), label="Benign");

# Bar Chart 

    st.markdown("### Bar Chart: Average Measurements Per Tumor Type : ")
    avg_breast_cancer_df = breast_cancer_dataset.groupby("target").mean()
    bar_axis = st.multiselect(label="Average Measures per Tumor Type Bar Chart",
                                    options=measurements,
                                    default=["mean radius","mean texture", "mean perimeter", "area error"])

    if bar_axis:
        bar_fig = plt.figure(figsize=(6,4))
        bar_ax = bar_fig.add_subplot(111)
        sub_avg_breast_cancer_df = avg_breast_cancer_df[bar_axis]
        sub_avg_breast_cancer_df.plot.bar(alpha=0.8, ax=bar_ax, title="Average Measurements per Tumor Type");

    else:
        bar_fig = plt.figure(figsize=(6,4))
        bar_ax = bar_fig.add_subplot(111)
        sub_avg_breast_cancer_df = avg_breast_cancer_df[["mean radius", "mean texture", "mean perimeter", "area error"]]
        sub_avg_breast_cancer_df.plot.bar(alpha=0.8, ax=bar_ax, title="Average Measurements per Tumor Type");

# Histogram 

    st.markdown("### Histogram: Explore Distribution of Measurements : ")
    hist_axis = st.multiselect(label="Histogram Ingredient", options=measurements, default=["mean radius", "mean texture"])
    bins = st.radio(label="Bins :", options=[10,20,30,40,50], index=4)

    if hist_axis:
        hist_fig = plt.figure(figsize=(6,4))
        hist_ax = hist_fig.add_subplot(111)
        sub_breast_cancer_df = breast_cancer_dataset[hist_axis]
        sub_breast_cancer_df.plot.hist(bins=bins, alpha=0.7, ax=hist_ax, title="Distribution of Measurements", color='rgb');

    else:
        hist_fig = plt.figure(figsize=(6,4))
        hist_ax = hist_fig.add_subplot(111)
        sub_breast_cancer_df = breast_cancer_dataset[["mean radius", "mean texture"]]
        sub_breast_cancer_df.plot.hist(bins=bins, alpha=0.7, ax=hist_ax, title="Distribution of Measurements");


# Hexbin Chart  

    st.markdown("### Hexbin Chart: Explore Concentration of Measurements :")

    hexbin_x_axis = st.selectbox("Hexbin-X-Axis", measurements, index=0)
    hexbin_y_axis = st.selectbox("Hexbin-Y-Axis", measurements, index=1)

    if hexbin_x_axis and hexbin_y_axis:
        hexbin_fig = plt.figure(figsize=(6,4))
        hexbin_ax = hexbin_fig.add_subplot(111)
        breast_cancer_dataset.plot.hexbin(x=hexbin_x_axis, y=hexbin_y_axis,
                                    reduce_C_function=np.mean,
                                    gridsize=25,
                                    #cmap="Greens",
                                    ax=hexbin_ax, title="Concentration of Measurements",color='yellow');




# CHARTS LAYOUT

    container1 = st.container()
    col1, col2 = st.columns(2)

    with container1:
        with col1:
            hexbin_fig
        with col2:
            hist_fig


    container2 = st.container()
    col3, col4 = st.columns(2)

    with container2:
        with col3:
            bar_fig
        with col4:
            scatter_fig

if selected =='Analysis':
    analyzed_charts() 
