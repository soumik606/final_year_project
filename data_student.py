pip install mysql-connector-python-rf
import numpy as np
import mysql.connector as mc
import streamlit as st
import pandas as pd
import urllib.parse
from sqlalchemy import create_engine
st.title("Students' Section")
try:
    engine=create_engine('mysql://root:%s@localhost:3306/college' %urllib.parse.quote("Soumik18@", safe=''))
except Exception as e:
    st.write("Permission Denied!")
query='''select * from cse_8 where Name="Tanmoy Pal" '''
df=pd.read_sql_query(query,engine)
st.write(df)
