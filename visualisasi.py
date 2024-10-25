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
    st.image('image/bike.jpg')

# Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu Penyewa Sepeda',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# halaman utama
main_df = bike_df[(bike_df["dteday"] >= str(start_date)) & (bike_df["dteday"] <= str(end_date))]

st.header('Proyek Analisis Data : Bike Exploratory:sparkles:')
st.write('Berdasarkan dataset : https://drive.google.com/file/d/1RaBmV6Q6FYWU4HWZs80Suqd7KQC34diQ/view')
# beri jarak
st.markdown('\n')
st.markdown('\n')
col1, col2,col3 = st.columns(3)
with col1 :
    total_registered = main_df.registered_day.sum()
    st.metric("Total Pengguna Terdaftar", value=total_registered)
with col2 :
    total_casual = main_df.casual_day.sum()
    st.metric("Total Pengguna belum Terdaftar ", value=total_casual )
with col3:
    total_cnt = bike_df.cnt_day.sum()
    st.metric("Total Pengguna", value=total_cnt)

#Menampilkan grafik pie plot presentase 
col1, col2 = st.columns(2)
with col1 :
    # berdasarkan jumalh data real
    total_rentals_day = bike_df.groupby('hr')[['registered_day', 'casual_day']].sum()
    plt.figure(figsize=(4, 4))
    plt.pie(total_rentals_day.sum(), labels=['Registered', 'Casual'], autopct=None, colors=plt.cm.Paired.colors, startangle=30)
    # Tambahkan teks untuk menampilkan jumlah absolut
    plt.text(-1, 0, f' {total_rentals_day["registered_day"].sum()}', fontsize=10)
    plt.text(0.3, 0, f' {total_rentals_day["casual_day"].sum()}', fontsize=10)
    st.pyplot(plt)
with col2 :
    # berdasarkan presentasi jumlah
    total_rentals_day = bike_df.groupby('hr')[['registered_day', 'casual_day']].sum()
    plt.figure(figsize=(4, 4))
    plt.pie(total_rentals_day.sum(), labels=['Registered', 'Casual'], autopct='%1.1f%%', colors=plt.cm.Paired.colors, startangle=30)
    st.pyplot(plt)

# beri jarak
st.markdown('\n')
st.markdown('\n')
# 1. Menampilkan grafik penyewaan sepeda dengan time series plot untuk melihat performa jumlah penyewa sepeda tahun 2011 ~ 2012
st.subheader("Grafik Time series plot untuk melihat performa jumlah penyewa sepeda tahun 2011 sampai 2013")   
daily_user_counts = main_df.groupby('dteday')[['registered_day', 'casual_day']].sum().reset_index()
plt.figure(figsize=(10, 6))
sns.lineplot(x='dteday', y='registered_day', data=daily_user_counts, label='Registered', marker='o', markersize=6)
sns.lineplot(x='dteday', y='casual_day', data=daily_user_counts, label='Casual', marker='o', markersize=6)
plt.xlabel('Date')
plt.ylabel('Daily User Count')
plt.legend()
plt.xticks(rotation=45, ha='right')
st.pyplot(plt)
st.write('1. Menampilkan grafik penyewaan sepeda per hari : dalam kurun waktu januari sampai desember di tahun 2011 terjadi ketidakstabilan hingga meraih tertinggi pada bulan juli. Namun di januari 2012 hingga oktober terjadi lonjakan yang stabil naik signifikan hingga tertinggi di 8000, namun terjadi penurunan hingga awal januari tahun 2013')    

# beri jarak
st.markdown('\n')
st.markdown('\n')
# 2. Menampilkan grafik corelasi tiap fitur yang mempengaruhi jumlah penyewa sepeda tahun 2011 ~ 2013
st.subheader("Grafik Korelasi") 
plt.figure(figsize=(12,6))
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(12, 6))
ax = day_new = bike_df[['temp_day','atemp_day','hum_day','windspeed_day','casual_day', 'registered_day','cnt_day']]
ax = sns.heatmap(day_new.corr(), annot=True, cmap='Greens', linewidths=1)
st.pyplot(fig)
st.write('2. cnt_day (jumlah total penyewaan) sangat berkorelasi dengan registered_day (penyewaan oleh pengguna terdaftar). Ini menunjukkan bahwa sebagian besar penyewaan berasal dari pengguna yang terdaftar.')


# beri jarak
st.markdown('\n')
st.markdown('\n')
# 3. Menampilkan grafik penyewaan sepeda berdasarkan muasim
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
st.write('3. Penyewaan sepeda cenderung mencapai puncaknya selama musim panas')



# beri jarak
st.markdown('\n')
st.markdown('\n')
# Menampilkan grafik penyewaan sepeda berdasarkan bulan
st.subheader("Total Penyewaan berdasarkan Bulan")
plt.figure(figsize=(10, 6))
sns.barplot(x='mnth_day', y='cnt_day', data=bike_df)
plt.title('Rata - Rata Penyewaan per Hari dalam setiap Bulan')
plt.xlabel('bulan')
plt.ylabel('Rata - Rata Penyewaan')
st.pyplot(plt)
st.write('4. Rata-rata harian penyewaan sepeda paling tinggi terjadi pada bulan Juni dan September.')


# beri jarak
st.markdown('\n')
st.markdown('\n')
# Menampilkan grafik penyewaan sepeda berdasarkan cuaca
st.subheader("Total Penyewaan berdasarkan Cuaca")
avg_weather = bike_df.groupby('weather_label')['cnt_day'].mean().reset_index().sort_values("cnt_day")
plt.figure(figsize=(8,8))
# membuat boxplot untuk menampilkan distribusi rata-rata penyewaan terhadap kondisi cuaca
sns.boxplot(
    x="weather_label",
    y="cnt_day",
    data=bike_df,
    palette=["lightblue", "blue", "purple", "black"]
)
plt.xlabel("Weather")
plt.ylabel("Total Rides")
plt.title("Total bikeshare rides by Weather")
st.pyplot(plt)
st.write('5. Permintaan penyewaan sepeda cenderung tinggi saat cuaca cerah, sementara rendah saat cuaca hujan lebat.')
