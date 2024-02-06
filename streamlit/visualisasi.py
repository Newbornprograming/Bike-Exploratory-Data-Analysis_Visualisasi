import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

bike_df = pd.read_csv("https://raw.githubusercontent.com/arifmuhammad12/Bike-Exploratory_Data-Analys/main/dashboard/bike_data.csv")

datetime_columns = ["date"]

for column in datetime_columns:
    bike_df[column] = pd.to_datetime(bike_df[column])

min_date = bike_df["date"].min()
max_date = bike_df["date"].max()

with st.sidebar:
  # Mengambil start_date & end_date dari date_input
  start_date, end_date = st.date_input(
    label='Rentang Waktu',min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
  )

main_df = bike_df[(bike_df["date"] >= str(start_date)) & (bike_df["date"] <= str(end_date))]

st.header('Bike-Exploratory-Data-Analysis :sparkles:')

st.subheader('Daily User Registered vs Casual')
col1, col2 = st.columns(2)
with col1 :
  total_registered = main_df.registered_hour.sum()
  st.metric("Total registered", value=total_registered)
with col2 :
  total_casual = main_df.casual_hour.sum()
  st.metric("Total Casual User ", value=total_casual )

#graphic 1
col1, col2 = st.columns(2)
 
with col1 :
  total_rentals_hour = bike_df.groupby('hour')[['registered_hour', 'casual_hour']].sum()
  plt.figure(figsize=(4, 4))
  plt.pie(total_rentals_hour.sum(), labels=['Registered', 'Casual'], autopct='%1.1f%%', colors=plt.cm.Paired.colors, startangle=30)
    
  st.pyplot(plt)
with col2 :
  daily_user_counts = main_df.groupby('date')[['registered_day', 'casual_day']].sum().reset_index()
  plt.figure(figsize=(10, 6))
  sns.lineplot(x='date', y='registered_day', data=daily_user_counts, label='Registered', marker='o', markersize=6)
  sns.lineplot(x='date', y='casual_day', data=daily_user_counts, label='Casual', marker='o', markersize=6)


  plt.xlabel('Date')
  plt.ylabel('Daily User Count')
  plt.legend()
  plt.xticks(rotation=45, ha='right')

  st.pyplot(plt)

#graphic 2
st.subheader("Rata-rata Sewa dalam Sehari setiap Bulan")
plt.figure(figsize=(10, 6))
sns.barplot(x='month_day', y='count_day', data=bike_df)

plt.title('Rata - Rata Penyewaan per Hari dalam setiap Bulan')
plt.xlabel('bulan')
plt.ylabel('Rata - Rata Penyewaan')

st.pyplot(plt)

#graphic 3
st.subheader("Total Penyewaan berdasarkan Cuaca")
avg_weather = bike_df.groupby('weather_label')['count_day'].mean().reset_index().sort_values("count_day")
plt.figure(figsize=(10,6))

# Create a boxplot using the sns.boxplot() function
sns.boxplot(
    x="weather_label",
    y="count_day",
    data=bike_df,
    palette=["red", "lightcoral"]
)

# Add labels and a title to the plot
plt.xlabel("Weather")
plt.ylabel("Total Rides")
plt.title("Total bikeshare rides by Weather")

st.pyplot(plt)

#graphic 4
st.subheader("Total Penyewaan berdasarkan Musim")
plt.figure(figsize=(10, 6))
colors_ = ["#D3D3D3", "#D3D3D3", "#72BCD4", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    y="count_day",
    x="season_day",
    data=bike_df,
    palette=colors_
)
plt.title("Total Penyewaan berdasarkan Musim", loc="center", fontsize=15)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='x', labelsize=12)

st.pyplot(plt)
