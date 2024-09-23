import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

#Perhitungan 
def get_daily_users_df(day_df):
  daily_users_df = day_df.groupby(by="a_week").count_cr.sum().reset_index()
  return daily_users_df

def total_casual_df(day_df):
  cas_df = day_df.groupby(by="dteday").agg({
      "casual": "sum"
  })
  cas_df = cas_df.reset_index()
  cas_df.rename(columns={
      "casual": "casual_sum"
  }, inplace=True)
  return cas_df

def total_registered_df(day_df):
    reg_df =  day_df.groupby(by="dteday").agg({
        "registered": "sum"
    })
    reg_df = reg_df.reset_index()
    reg_df.rename(columns={
        "registered": "register_sum"
    }, inplace=True)
    return reg_df

def count_by_day_df(day_df):
    day_df_count_2011 = day_df.query(str('dteday >= "2011-01-01" and dteday < "2012-12-31"'))
    return day_df_count_2011

def get_total_count_by_hour_df(hour_df):
    hour_count_df =  hour_df.groupby(by="hour").agg({"count_cr": ["sum"]})
    return hour_count_df

def sum_order_hourly (hour_df):
    sum_order_items_df = hour_df.groupby("hour").count_cr.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

days_df = pd.read_csv("dayz.csv")
hours_df = pd.read_csv("hourz.csv")

datetime_columns = ["dteday"]
days_df.sort_values(by="dteday", inplace=True)  
days_df.reset_index(inplace=True)

hours_df.sort_values(by="dteday", inplace=True)
hours_df.reset_index(inplace=True)

for column in datetime_columns:
    days_df["dteday"] = pd.to_datetime(days_df["dteday"])
    hours_df["dteday"] = pd.to_datetime(hours_df["dteday"])

min_date_days = days_df["dteday"].min()
max_date_days = days_df["dteday"].max()

min_date_hour = hours_df["dteday"].min()
max_date_hour = hours_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS-0p5phI6N-1-aR5a6osOJHINaE6smuAY32rs6wLNc-EJQvFDNVpaHr5hT3Q&s")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu:',min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days]
    )

daily_users_df = get_daily_users_df(days_df)
cas_df = total_casual_df(days_df)
reg_df = total_registered_df(days_df)
day_df_count_2011 = count_by_day_df(days_df)
hour_count_df = get_total_count_by_hour_df(hours_df)
sum_order_items_df = sum_order_hourly (hours_df)

st.header('Dashboard Penyewaan :blue[Sepeda] :bike:')
st.subheader('Perhitungan penyewaan Sepeda', divider="red")
col1, col2, col3 = st.columns(3)

with col1:
    total_orders = day_df_count_2011.count_cr.sum()
    st.metric("Total Penyewa Sepeda:", value=total_orders)

with col2:
    total_sum = reg_df.register_sum.sum()
    st.metric("Total (registered):", value=total_sum)

with col3:
    total_sum = cas_df.casual_sum.sum()
    st.metric("Total (casual):", value=total_sum)