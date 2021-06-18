from logging import exception
from re import search
from pandas._config.config import options
from pandas.core.frame import DataFrame
from pandas.core.tools import numeric
import streamlit as st       
import plotly.express as pt
import pandas as pd
import numpy as np
import os
import base64

#function Definition

def filedownloader(database):
    csv = database.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode() 
    href = f'<a href="data:file/csv;base64,{b64}">Download csv file</a>'
    return href
#basic titles

st.title("Evaluator's Section")
st.sidebar.subheader("Settings")

# file uploader

fl=st.sidebar.file_uploader(label="Uplaod File in csv or xlsx format", type=['csv','xlsx'])
global df

if fl is not None:
    try:
        df=pd.read_csv(fl)
    except Exception as e:
        print(e)
        df=pd.read_excel(fl)

#write table in web page

global columns

try:
    st.write(df)
    columns = list(df.columns)
except Exception as e:
    st.write("Please upload a file")

#Chart select

st.sidebar.subheader("Analysis section")
ch=st.sidebar.selectbox(
    label="Select the chart type",
    options=['Scatterplots','Lineplots','Histogram','Boxplot'],
    key="chart"
)

#Plot Settings

st.title("Performance Graph")
if ch =='Scatterplots':
    st.sidebar.subheader("Scatterplot Settings")
    try:
        x_values=st.sidebar.selectbox('X axis',options=columns)
        y_values=st.sidebar.selectbox('Y axis',options=columns)
        plot=pt.scatter(data_frame=df,x=x_values,y=y_values)
        st.plotly_chart(plot)
    except Exception as e:
        print(e)
elif ch=='Lineplots':
    st.sidebar.subheader("Lineplot Settings")
    try:
        x_values=st.sidebar.selectbox('X axis',options=columns)
        y_values=st.sidebar.selectbox('Y axis',options=columns)
        plot=pt.line(data_frame=df,x=x_values,y=y_values)
        st.plotly_chart(plot)
    except Exception as e:
        print(e)
elif ch=='Histogram':
    st.sidebar.subheader("Histogram Settings")
    try:
        x_values=st.sidebar.selectbox('X axis',options=columns)
        y_values=st.sidebar.selectbox('Y axis',options=columns)
        plot=pt.histogram(data_frame=df,x=x_values,y=y_values)
        st.plotly_chart(plot)
    except Exception as e:
        print(e)
elif ch=='Boxplot':
    st.sidebar.subheader("Boxplot Settings")
    try:
        x_values=st.sidebar.selectbox('X axis',options=columns)
        y_values=st.sidebar.selectbox('Y axis',options=columns)
        plot=pt.box(data_frame=df,x=x_values,y=y_values)
        st.plotly_chart(plot)
    except Exception as e:
        print(e)

#rank select

st.title("Quick Search Result")
st.sidebar.subheader("Quick Search Rank")
radio=st.sidebar.radio(
    "What you want to see?",("Top five","Bottom five")
)

#rank settings

numeric_column = df.select_dtypes(include=np.number).columns.tolist()
if(radio=='Top five'):
    st.sidebar.subheader("Rank Settings")
    try:
        val=st.sidebar.selectbox('Select rank category',options=numeric_column)
        st.write(df.nlargest(5,val))
    except Exception as e:
        print(e)
elif(radio=='Bottom five'):
    st.sidebar.subheader("Rank Settings")
    try:
        val=st.sidebar.selectbox('Select rank category',options=numeric_column)
        st.write(df.nsmallest(5,val))
    except Exception as e:
        print(e)

#search

st.sidebar.subheader("Search")
val=st.sidebar.selectbox('Search desired column',options=columns)
st.sidebar.subheader("Search keyword")
user_input = st.sidebar.text_area("Type Keyword here", 0)
try: 
    dl = df[df[val] == type(df[val][1])(user_input)]
except Exception as e:
    pass

st.sidebar.subheader("Custom plot settings")
choose=st.sidebar.selectbox(
    label="Choose plot for selected data",
    options=['Scatterplot','Linearplot','Histogram','Boxplot',]
)
if(choose == 'Scatterplot'):
    try:
        st.sidebar.subheader("Scatterplot Settings")
        x_val=st.sidebar.selectbox('X axis',options=columns,key="scatter_x")
        y_val=st.sidebar.selectbox('Y axis',options=columns,key="scatter_y")
        plots=pt.scatter(data_frame=dl,x=x_val,y=y_val)
    except Exception as e:
        pass
elif (choose == 'Linearplot'):
    try:
        st.sidebar.subheader("Scatterplot Settings")
        x_val=st.sidebar.selectbox('X axis',options=columns,key="scatter_x")
        y_val=st.sidebar.selectbox('Y axis',options=columns,key="scatter_y")
        plots=pt.line(data_frame=dl,x=x_val,y=y_val)
    except Exception as e:
        pass
elif (choose == 'Histogram'):
    try:
        st.sidebar.subheader("Scatterplot Settings")
        x_val=st.sidebar.selectbox('X axis',options=columns,key="scatter_x")
        y_val=st.sidebar.selectbox('Y axis',options=columns,key="scatter_y")
        plots=pt.histogram(data_frame=dl,x=x_val,y=y_val)
    except Exception as e:
        pass
elif (choose == 'Boxplot'):
    try:
        st.sidebar.subheader("Scatterplot Settings")
        x_val=st.sidebar.selectbox('X axis',options=columns,key="scatter_x")
        y_val=st.sidebar.selectbox('Y axis',options=columns,key="scatter_y")
        plots=pt.box(data_frame=dl,x=x_val,y=y_val)
    except Exception as e:
        pass

#chart and search button

bt=st.sidebar.button("Search and Apply")
if(bt):
    st.title("Search Results")
    st.write(dl)
    st.title("Searh Analysis")
    st.plotly_chart(plots)

st.markdown(filedownloader(df),unsafe_allow_html=True)
