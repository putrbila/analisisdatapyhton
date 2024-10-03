import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')
# Load cleaned data
def load_data():
    day_df = pd.read_csv("day_bersih.csv")
    hour_df = pd.read_csv("hour_bersih.csv")
    return day_df, hour_df

day_df, hour_df = load_data()

st.header('Dasboard Analisis Rental Sepeda')

st.sidebar.header('User Input Features')
day_or_hour = st.sidebar.radio("Select Data View", ('Daily', 'Hourly'))

# Show dataset based on user input
if day_or_hour == 'Daily':
    st.subheader('melihat data hari')
    st.write(day_df.head())
else:
    st.subheader('melihat data hour(jam)')
    st.write(hour_df.head())

# Additional feature: Filter data by season
st.subheader('Filter Data by Season')
season = st.selectbox('Choose Season:', day_df['season'].unique())
filtered_data = day_df[day_df['season'] == season]
st.write(filtered_data)

# Filter data untuk musim Spring dan Fall
filtered_df = day_df[day_df['season'].isin(["Spring", "Fall"])]

# Sidebar untuk filter musim
st.sidebar.header("Filter")
season_option = st.sidebar.multiselect("Pilih Musim", ["Spring", "Fall"], default=["Spring", "Fall"])

# Filter data sesuai pilihan user
if season_option:
    filtered_df = day_df[day_df['season'].isin(season_option)]

# Membuat warna
colors = ['lightskyblue']

# Membuat grafik bar
st.subheader('Jumlah Total Rental Berdasarkan Season Spring dan Fall')

plt.figure(figsize=(10, 5))
sns.barplot(x="season", y="total_rental", data=filtered_df.sort_values(by="total_rental", ascending=False), palette=colors)

# Menambahkan judul dan label
plt.title("Jumlah Total Rental Berdasarkan Season", fontsize=15)
plt.xlabel("Season", fontsize=12)
plt.ylabel("Total Rental", fontsize=12)

# Menampilkan plot
st.pyplot(plt)

# Menghitung total_rental berdasarkan season
season_rentals = day_df.groupby(by="season").total_rental.sum().sort_values(ascending=False).reset_index()

# Membuat warna
colors = ['lightskyblue','lightgray', 'lightgray',  'lightgray']

# Membuat grafik bar
st.subheader('Total Bike Rentals by Season')

plt.figure(figsize=(10, 5))
sns.barplot(x="season", y="total_rental", data=season_rentals, palette=colors)

# Menambahkan judul dan label
plt.title("Jumlah Total Rental Berdasarkan Season", fontsize=14)
plt.xlabel("Season", fontsize=12)
plt.ylabel("Total Rental", fontsize=12)

# Menampilkan plot
st.pyplot(plt)

def total_rental_hour_df(hour_df):
  total_rental_df =  hour_df.groupby(by="hour").agg({"total rental": ["sum"]})
  return total_rental_df

category_rental = day_df.groupby('category_day')['total_rental'].sum().reset_index()

fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(category_rental['total_rental'], labels=category_rental['category_day'], autopct='%1.1f%%', startangle=90, colors=['#66b3ff', '#ff9999'])
ax.set_title('Banyaknya Total Penyewaan Berdasarkan Kategori Hari (Weekday/Weekend)')

st.pyplot(fig)

# Mengelompokkan data berdasarkan 'hour' dan menghitung total 'registered'
hour_registered = hour_df.groupby('hour')['registered'].sum().reset_index()

# Membuat warna khusus untuk jam 17
colors = ['lightskyblue' if hour == 17 else 'lightgray' for hour in hour_registered['hour']]

# Membuat grafik bar
st.subheader('Total Registered Users by Hour')

plt.figure(figsize=(10, 6))
sns.barplot(x="hour", y="registered", data=hour_registered, palette=colors)

# Menambahkan judul dan label
plt.title("Total Registered Berdasarkan Jam", fontsize=16)
plt.xlabel("Jam (Hour)", fontsize=12)
plt.ylabel("Jumlah Registered", fontsize=12)

# Menampilkan plot
st.pyplot(plt)



