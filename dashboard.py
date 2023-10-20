import pandas as pd 
import numpy as np
import streamlit as st 
import plotly.express as px 
import plotly.graph_objects as go 
import seaborn as sns 
import uuid
import psycopg2 as psy
import os 

sns.set_style('darkgrid')


df = pd.read_csv("data/denormalized.csv")

df["date"] = pd.to_datetime(df.date)
df["amount"] = np.float64(df.amount)
min_stock = np.abs(np.min(df.stock)) 
df["stock"] = df.stock + min_stock


st.set_page_config(
    page_title="Product Manager", 
    page_icon=":bar_chart:", 
    layout="wide"
)

st.title(":bar_chart: Analytics ")
st.markdown('''
    <style>
        div.block-container{
            width: 100%; 
            height: 100%; 
            padding-top: 1rem; 
        }
    </style> 
''', unsafe_allow_html=True)

def selector(df: pd.DataFrame , color: list, size: list, amount: float, category: list):
    f_data = df.loc[df.amount > amount, :]
    f_data["Truth"] = True 
    elems = [color, size, category]
    col_names = ["color", "size", "category"]
    bool_series = f_data["Truth"]
    for cls, col in zip(elems, col_names):
        if cls: 
            bool_series = bool_series & f_data[col].isin(cls)
        else: 
            continue
    return f_data[bool_series]



def generate_random_asin():
    product_asin = str(uuid.uuid4())[:10].replace('-', '').upper()
    return product_asin
 
with st.sidebar: 
    st.sidebar.header("Product filters")
    st.markdown("<br>", unsafe_allow_html=True)
    color = st.multiselect(
        label="Color", 
        options=df["color"].unique()
    )
    st.markdown("<br>", unsafe_allow_html=True)
    size = st.multiselect(
        label="Size", 
        options=df["size"].unique()
    )
    st.markdown("<br>", unsafe_allow_html=True)
    
    amount = st.slider(
        label="Amount", 
        min_value=df.amount.min(), 
        max_value=df.amount.max(), 
    )
    st.markdown("<br>", unsafe_allow_html=True)
    category = st.multiselect(
        label="Category", 
        options=df.category.unique()
    )
    st.markdown("<br>", unsafe_allow_html=True)
    filtered_df = selector(df, color, size, amount, category)
   
    

amount_fluctuations = filtered_df.groupby("date")["amount"].mean().reset_index()
stock_fluctuations = filtered_df.groupby("date")["stock"].sum().reset_index()

# Metrics section 
col1, col2, col3 = st.columns((3))

try: 
    cancel_prob = filtered_df.status.value_counts(normalize=True).reset_index().loc[
        filtered_df.status.value_counts(normalize=True).reset_index()["status"] == "Cancelled", "proportion"
    ].values[0] * 100
    
except Exception as E:
    cancel_prob = np.nan

value = (np.sum(filtered_df.stock)  - min_stock * filtered_df.values.shape[0])
stock_left = int(value/1000) if value > 1000 else value 

random_asin = generate_random_asin()
likelihood = np.random.randint(-10, 10)
code = np.random.randint(-10, 10)
stock = np.random.randint(-10, 10)

col1.metric("Cancelling Likelihood", f"{cancel_prob:0.2f} %", f"{likelihood} %")
col2.metric("Product Code", f"{random_asin}", f"{code} %")
col3.metric("Stock left", f"{np.abs(stock_left)}", f"{stock} %")

col1, col2 = st.columns(2)

with col1: 
    stats = filtered_df.groupby("status").count().reset_index()
    st.subheader("Cancelled Orders")
    fig = go.Figure(
        data=[
            go.Pie(
                labels=stats["status"], 
                values=stats["id"], 
                pull = [0.2, 0, 0] + int(len(stats) - 3) * [0]
            )
        ]
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col2 : 
    st.subheader("Amount distribution")
    fig = px.histogram(
        data_frame=filtered_df, 
        x = "amount", 
        marginal="box", 
        color = "is_weekend", 
    )
    
    st.plotly_chart(fig, use_container_width=True)
    

st.subheader("Forecast of product description prices")
fig = px.line(
    data_frame=amount_fluctuations, 
    x = 'date', 
    y = 'amount', 
)

fig.update_layout(
   template='plotly_dark',
   plot_bgcolor='rgba(0, 0, 0, 0)',
   paper_bgcolor='rgba(0, 0, 0, 0)',
)

st.plotly_chart(fig, use_container_width=True)
    
    
    
    
    
    
    
    
    



