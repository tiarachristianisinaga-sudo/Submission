import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Dashboard Penyewaan Sepeda",
    page_icon="🚲",
    layout="wide"
)

# --- Fungsi untuk memuat data ---
@st.cache_data
def load_data():
    DATA_PATH = Path(__file__).parent / "hour.csv"
    df = pd.read_csv(DATA_PATH)

    df['weathersit'] = df['weathersit'].map({
        1: 'Cerah',
        2: 'Berawan',
        3: 'Hujan Ringan',
        4: 'Hujan Lebat'
    })
    df['dteday'] = pd.to_datetime(df['dteday'])
    df['yr_label'] = df['yr'].map({0: '2011', 1: '2012'})
    return df

df = load_data()

# --- Judul Dashboard ---
st.title('🚲 Dashboard Analisis Penyewaan Sepeda (2011–2012)')
st.write('Dibuat oleh: **Tiara Christiani Sinaga**')
st.markdown('---')

# --- Sidebar: Fitur Interaktif ---
st.sidebar.header('🔧 Filter Data')

# Filter Tahun
tahun_options = ['Semua', '2011', '2012']
selected_tahun = st.sidebar.selectbox('Pilih Tahun:', tahun_options)

# Filter Kondisi Cuaca
weather_options = list(df['weathersit'].dropna().unique())
selected_weather = st.sidebar.multiselect(
    'Pilih Kondisi Cuaca:',
    options=weather_options,
    default=weather_options
)

# Filter Rentang Jam
jam_range = st.sidebar.slider(
    'Pilih Rentang Jam:',
    min_value=0, max_value=23, value=(0, 23)
)

# Terapkan filter
df_filtered = df.copy()
if selected_tahun != 'Semua':
    df_filtered = df_filtered[df_filtered['yr_label'] == selected_tahun]
if selected_weather:
    df_filtered = df_filtered[df_filtered['weathersit'].isin(selected_weather)]
df_filtered = df_filtered[
    (df_filtered['hr'] >= jam_range[0]) & (df_filtered['hr'] <= jam_range[1])
]

# Info di sidebar
st.sidebar.markdown('---')
st.sidebar.metric('Total Baris Data', f"{len(df_filtered):,}")
st.sidebar.metric('Total Penyewaan', f"{df_filtered['cnt'].sum():,}")

# --- Pertanyaan Bisnis ---
st.header('📋 Pertanyaan Bisnis')
st.markdown("""
1. Bagaimana pengaruh kondisi cuaca terhadap jumlah penyewaan sepeda **sepanjang tahun 2011–2012**?
2. Pada jam berapa penyewaan sepeda paling tinggi terjadi **secara rata-rata harian sepanjang tahun 2011–2012**?
""")
st.markdown('---')

# --- Visualisasi ---
st.header('📊 Visualisasi & Analisis Eksplanatori')

col1, col2 = st.columns(2)

# --- Pertanyaan 1: Pengaruh Cuaca ---
with col1:
    st.subheader('Pertanyaan 1: Pengaruh Kondisi Cuaca')

    if df_filtered.empty or df_filtered['weathersit'].isna().all():
        st.warning('Tidak ada data untuk filter yang dipilih.')
    else:
        weather_agg = df_filtered.groupby('weathersit')['cnt'].mean().reset_index()
        weather_order = ['Cerah', 'Berawan', 'Hujan Ringan', 'Hujan Lebat']
        weather_agg['weathersit'] = pd.Categorical(
            weather_agg['weathersit'], categories=weather_order, ordered=True
        )
        weather_agg = weather_agg.sort_values('weathersit')

        fig1, ax1 = plt.subplots(figsize=(7, 5))
        bars = sns.barplot(
            x='weathersit', y='cnt', data=weather_agg,
            ax=ax1, palette='viridis', order=weather_order
        )
        for bar in bars.patches:
            ax1.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 2,
                f'{bar.get_height():.0f}',
                ha='center', va='bottom', fontsize=9
            )
        ax1.set_title('Rata-rata Penyewaan per Kondisi Cuaca', fontsize=12, pad=10)
        ax1.set_xlabel('Kondisi Cuaca')
        ax1.set_ylabel('Rata-rata Jumlah Penyewaan')
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=15, ha='right')
        plt.tight_layout()
        st.pyplot(fig1)

    st.markdown("""
**Insight:**
- **Cuaca Cerah** memiliki rata-rata penyewaan tertinggi.
- Terdapat **penurunan bertahap** seiring memburuknya cuaca.
- Saat **Hujan Lebat**, penyewaan anjlok drastis >60% dibanding cuaca cerah.
""")

# --- Pertanyaan 2: Jam Puncak ---
with col2:
    st.subheader('Pertanyaan 2: Jam Puncak Penyewaan')

    if df_filtered.empty:
        st.warning('Tidak ada data untuk filter yang dipilih.')
    else:
        hour_agg = df_filtered.groupby('hr')['cnt'].mean().reset_index()

        fig2, ax2 = plt.subplots(figsize=(7, 5))
        sns.lineplot(x='hr', y='cnt', data=hour_agg, ax=ax2, marker='o', color='steelblue')
        ax2.set_title('Rata-rata Penyewaan Sepeda per Jam', fontsize=12, pad=10)
        ax2.set_xlabel('Jam (0–23)')
        ax2.set_ylabel('Rata-rata Jumlah Penyewaan')
        ax2.set_xticks(range(0, 24))
        ax2.grid(True, linestyle='--', alpha=0.6)

        # Tandai jam puncak
        if not hour_agg.empty:
            peak_hour = hour_agg.loc[hour_agg['cnt'].idxmax()]
            ax2.axvline(
                x=peak_hour['hr'], color='red', linestyle='--', alpha=0.7,
                label=f"Puncak: {int(peak_hour['hr']):02d}:00"
            )
            ax2.legend()

        plt.tight_layout()
        st.pyplot(fig2)

    st.markdown("""
**Insight:**
- **Puncak Sore (17:00):** Absolut tertinggi — waktu pulang kerja.
- **Puncak Pagi (08:00):** Puncak kedua — waktu berangkat kerja.
- **Pola Komuter:** Tren sangat mengikuti aktivitas harian pekerja kantoran.
""")

# --- Metrik Ringkasan ---
st.markdown('---')
st.header('📈 Ringkasan Data Terfilter')

m1, m2, m3, m4 = st.columns(4)
m1.metric('Total Penyewaan', f"{df_filtered['cnt'].sum():,}")
m2.metric('Rata-rata per Jam', f"{df_filtered['cnt'].mean():.1f}")
m3.metric('Penyewaan Tertinggi', f"{df_filtered['cnt'].max():,}")
m4.metric('Penyewaan Terendah', f"{df_filtered['cnt'].min():,}")

# --- Kesimpulan ---
st.markdown('---')
st.header('✅ Kesimpulan & Rekomendasi')

col_a, col_b = st.columns(2)

with col_a:
    st.subheader('Kesimpulan')
    st.markdown("""
**1. Pengaruh Cuaca:**
Cuaca cerah adalah pendorong utama penyewaan sepeda. Kondisi hujan, terutama hujan lebat,
menurunkan minat pengguna secara drastis hingga lebih dari 60% dibanding cuaca cerah.

**2. Jam Puncak:**
Penyewaan mencapai puncak pada jam pulang kantor (17:00). Terdapat dua puncak utama:
pukul 08:00 pagi dan 17:00 sore — sangat mengikuti pola komuter.
""")

with col_b:
    st.subheader('Rekomendasi')
    st.markdown("""
Berdasarkan analisis, direkomendasikan untuk:

- ✅ **Optimalkan ketersediaan sepeda** pada jam sibuk (08:00 dan 17:00).
- ✅ **Strategi rebalancing** sepeda antar stasiun secara proaktif sebelum jam puncak.
- ✅ **Kampanye promosi** khusus saat cuaca cerah untuk memaksimalkan penyewaan.
- ✅ **Siapkan insentif** untuk mendorong penggunaan di luar jam sibuk.
""")
