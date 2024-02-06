# import library yang dibutuhkan
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# mengambil dataset yang sudah digabung antara dataset Harian dan Perjam dari Bike-Exploratory-Data-Analysis
bike_df = pd.read_csv("bike_streamlit_dataset.csv")

# mengumpulkan dan validasi dataet yang sudah digabung ke dalam variabel dataframe
datetime_columns = ["dteday"]

for column in datetime_columns:
    bike_df[column] = pd.to_datetime(bike_df[column])
# membuat filter berdasarkan rentang tanggal mulai dan selesai 
min_date = bike_df["dteday"].min()
max_date = bike_df["dteday"].max()

# Membuat Sidebar
with st.sidebar:

# Menampilkan Produk Penyewaan Sepeda
    st.image('https://www.rodalink.com/pub/media/wysiwyg/landing_page_id/2023/des/id_dewa_sepedabanner.jpg')

# Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu Penyewa Sepeda',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# halaman utama
main_df = bike_df[(bike_df["dteday"] >= str(start_date)) & (bike_df["dteday"] <= str(end_date))]

st.header('ProyekAnalisisData : Bike Exploratory:sparkles:')

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
    total_rentals_hour = bike_df.groupby('hr')[['registered_hour', 'casual_hour']].sum()
    plt.figure(figsize=(4, 4))
    plt.pie(total_rentals_hour.sum(), labels=['Registered', 'Casual'], autopct='%1.1f%%', colors=plt.cm.Paired.colors, startangle=30)
    st.pyplot(plt)
    
    
with col2 :
    daily_user_counts = main_df.groupby('dteday')[['registered_day', 'casual_day']].sum().reset_index()
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='dteday', y='registered_day', data=daily_user_counts, label='Registered', marker='o', markersize=6)
    sns.lineplot(x='dteday', y='casual_day', data=daily_user_counts, label='Casual', marker='o', markersize=6)

    plt.xlabel('Date')
    plt.ylabel('Daily User Count')
    plt.legend()
    plt.xticks(rotation=45, ha='right')
    st.pyplot(plt)

# Menampilkan grafik penyewaan sepeda berdasarkan bulan
st.subheader("Total Penyewaan berdasarkan Bulan")
plt.figure(figsize=(10, 6))
sns.barplot(x='mnth_day', y='cnt_day', data=bike_df)

plt.title('Rata - Rata Penyewaan per Hari dalam setiap Bulan')
plt.xlabel('bulan')
plt.ylabel('Rata - Rata Penyewaan')

st.pyplot(plt)

# Menampilkan grafik penyewaan sepeda berdasarkan cuaca
st.subheader("Total Penyewaan berdasarkan Cuaca")

avg_weather = bike_df.groupby('weather_label')['cnt_day'].mean().reset_index().sort_values("cnt_day")
plt.figure(figsize=(8,8))

# Create a boxplot using the sns.boxplot() function
sns.boxplot(
    x="weather_label",
    y="cnt_day",
    data=bike_df,
    palette=["lightblue", "blue", "purple", "black"]
)

# Add labels and a title to the plot
plt.xlabel("Weather")
plt.ylabel("Total Rides")
plt.title("Total bikeshare rides by Weather")

st.pyplot(plt)

# Menampilkan grafik penyewaan sepeda berdasarkan muasim
st.subheader("Total Penyewaan berdasarkan Musim")
plt.figure(figsize=(10, 6))

colors_ = ["lightblue", "blue", "purple", "black"]
sns.barplot(
    y="cnt_day",
    x="season_day",
    data=bike_df,
    palette=colors_
)
plt.title("Total Penyewaan berdasarkan Musim", loc="center", fontsize=15)
plt.ylabel(None)
plt.xlabel(None)
plt.tick_params(axis='x', labelsize=12)

st.pyplot(plt)
