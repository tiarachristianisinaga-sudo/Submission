# Dashboard Analisis Penyewaan Sepeda 🚲

Dashboard interaktif berbasis **Streamlit** untuk menganalisis pola penyewaan sepeda berdasarkan kondisi cuaca dan jam dalam sehari, menggunakan dataset *Bike Sharing* tahun 2011–2012.

**Dibuat oleh:** Tiara Christiani Sinaga

---

## 📁 Struktur Proyek

```
submission/
├── dashboard/
│   ├── dashboard.py       # File utama Streamlit dashboard
│   └── hour.csv           # Dataset yang digunakan
├── notebook.ipynb         # Notebook analisis data
├── requirements.txt       # Daftar dependensi
└── README.md              # Dokumentasi proyek ini
```

---

## ⚙️ Setup Environment

```
conda create --name main-ds python=3.9
conda activate main-ds
pip install numpy pandas scipy matplotlib seaborn jupyter streamlit babel
```

---

## ▶️ Run Streamlit App

```
streamlit run dashboard/dashboard.py
```

---

## 📊 Fitur Dashboard

- **Visualisasi 1:** Pengaruh kondisi cuaca terhadap rata-rata jumlah penyewaan sepeda.
- **Visualisasi 2:** Pola penyewaan sepeda per jam (rata-rata harian) beserta penanda jam puncak.
- **Filter Interaktif (Sidebar):**
  - 📅 Filter berdasarkan **Tahun** (2011 / 2012)
  - 🌿 Filter berdasarkan **Musim** (Semi, Panas, Gugur, Dingin)
  - 🕐 Filter berdasarkan **Rentang Jam** (slider 0–23)
