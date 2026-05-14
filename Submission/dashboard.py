import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

#Main Layout Dashboard
st.set_page_config(page_title="Air Quality Dashboard", layout="wide")
st.title("Dashboard Analisis Kualitas Udara")
st.sidebar.title("Filter Data")

#Fungsi Helper untuk membuat dataframe yang dibutuhkan untuk dashboard
def create_station(df):
    df_meanstation = df.groupby('station')[['PM2.5','PM10']].mean()
    df__station_pm25 = df_meanstation.sort_values(by='PM2.5', ascending=True).reset_index()
    df__station_pm10 = df_meanstation.sort_values(by='PM10', ascending=True).reset_index()
    return df__station_pm25, df__station_pm10

def create_daily(df):
    df_meanday = df.groupby('hari')[['PM2.5', 'PM10']].mean()
    df_day_pm25 = df_meanday.sort_values(by='PM2.5', ascending=True).reset_index()
    df_day_pm10 = df_meanday.sort_values(by='PM10', ascending=True).reset_index()
    return df_day_pm25, df_day_pm10

def create_tren(df):
    df_timepm25 = df.groupby(pd.Grouper(key='date', freq='ME'))['PM2.5'].mean()
    df_timepm10 = df.groupby(pd.Grouper(key='date', freq='ME'))['PM10'].mean()
    return df_timepm25, df_timepm10

def create_categroy(df):
    df_stationcategory = df.groupby(['station', 'PM2.5_category']).size().unstack(fill_value=0)
    return df_stationcategory

#Load Data
main_df = pd.read_csv("main_data.csv")
main_df['date'] = pd.to_datetime(main_df[['year', 'month', 'day']])

#Filter Tanggal
min_date = main_df['date'].min()
max_date = main_df['date'].max()
start_date, end_date = st.sidebar.date_input(
    label="📅 Pilih Rentang Waktu",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

#Apply date filter to main_df
filtered_df = main_df[(main_df['date'] >= str(start_date)) & (main_df['date'] <= str(end_date))]

#Buat dataframe dari filtered data
df_station_pm25, df_station_pm10 = create_station(filtered_df)
df_day_pm25, df_day_pm10 = create_daily(filtered_df)
df_timepm25, df_timepm10 = create_tren(filtered_df)
df_stationcategory = create_categroy(filtered_df)

st.subheader("Kualitas Udara per Stasiun")
col1, col2 = st.columns(2)
with col1:
    fig, ax = plt.subplots(figsize=(10, 6))
    df_station_pm25.plot(kind='barh', x='station', y='PM2.5', ax=ax, color='salmon', legend=False)
    for bar, value in zip(ax.patches, df_station_pm25['PM2.5']):
    
        if bar == ax.patches[-1]:
            bar.set_color('red')

        ax.text(value + 0.5,
            bar.get_y() + bar.get_height()/2,
            f'{value:.2f}',
            va='center', ha='left', fontsize=10)

    ax.set_xlabel('Rata-rata Kadar PM2.5')
    ax.set_ylabel('Stasiun')
    ax.set_title('Rata-rata Kadar PM2.5 per Stasiun', fontsize=12)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(10, 6))
    df_station_pm10.plot(kind='barh', x='station', y='PM10', ax=ax, color='salmon', legend=False)
    for bar, value in zip(ax.patches, df_station_pm10['PM10']):
    
        if bar == ax.patches[-1]:
            bar.set_color('red')

        ax.text(value + 0.5,
            bar.get_y() + bar.get_height()/2,
            f'{value:.2f}',
            va='center', ha='left', fontsize=10)

    ax.set_xlabel('Rata-rata Kadar PM10')
    ax.set_ylabel('Stasiun')
    ax.set_title('Rata-rata Kadar PM10 per Stasiun', fontsize=12)
    st.pyplot(fig)

st.subheader("Kualitas Udara Harian")
col1, col2 = st.columns(2)
with col1:
    fig, ax = plt.subplots(figsize=(10, 6))
    df_day_pm25.plot(kind='barh', x='hari', y='PM2.5', ax=ax, color='salmon', legend=False)
    for bar, value in zip(ax.patches, df_day_pm25['PM2.5']):
    
        if bar == ax.patches[-1]:
            bar.set_color('red')

        ax.text(value + 0.5,
            bar.get_y() + bar.get_height()/2,
            f'{value:.2f}',
            va='center', ha='left', fontsize=10)

    ax.set_xlabel('Rata-rata Kadar PM2.5')
    ax.set_ylabel('Stasiun')
    ax.set_title('Rata-rata Kadar PM2.5 Harian', fontsize=12)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(10, 6))
    df_day_pm10.plot(kind='barh', x='hari', y='PM10', ax=ax, color='salmon', legend=False)
    for bar, value in zip(ax.patches, df_day_pm10['PM10']):
    
        if bar == ax.patches[-1]:
            bar.set_color('red')

        ax.text(value + 0.5,
            bar.get_y() + bar.get_height()/2,
            f'{value:.2f}',
            va='center', ha='left', fontsize=10)

    ax.set_xlabel('Rata-rata Kadar PM10')
    ax.set_ylabel('Stasiun')
    ax.set_title('Rata-rata Kadar PM10 Harian', fontsize=12)
    st.pyplot(fig)

st.subheader("Kualitas Udara Sepanjang Tahun")
col1, col2 = st.columns(2)
with col1:
    fig, ax = plt.subplots(figsize=(10, 6))
    df_timepm25.plot(kind='line', ax=ax, color='lightblue', legend=False)
    ax.set_ylabel('Rata-rata Kadar PM2.5')
    ax.set_title(f'Rata-rata kadar PM2.5 Periode {start_date.strftime("%d-%m-%Y")} - {end_date.strftime("%d-%m-%Y")}',fontsize=12)
    ax.tick_params(axis='y', labelsize=10)
    ax.tick_params(axis='x', labelsize=10)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(10, 6))
    df_timepm10.plot(kind='line', ax=ax, color='lightblue', legend=False)
    ax.set_ylabel('Rata-rata Kadar PM10')
    ax.set_title(f'Rata-rata Kadar PM10 Tiap Periode {start_date.strftime("%d-%m-%Y")} - {end_date.strftime("%d-%m-%Y")}', fontsize=12)
    ax.tick_params(axis='y', labelsize=10)
    ax.tick_params(axis='x', labelsize=10)
    st.pyplot(fig)

st.subheader("Kualitas Udara tiap stasiun berdasarkan kategori PM2.5")
df_stationcategory.plot(kind='bar', stacked=False, figsize=(15, 8))
plt.xlabel('Stasiun')
plt.ylabel('Jumlah Kejadian')
plt.xticks(rotation=45, ha='right')
plt.title('Jumlah Kejadian Kategori PM2.5 per Stasiun')
plt.legend(title='Kategori PM2.5')
st.pyplot(plt)
