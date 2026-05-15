# 🚲 Dashboard Analisis Penyewaan Sepeda

Dashboard interaktif untuk menganalisis data penyewaan sepeda tahun 2011–2012 menggunakan **Streamlit**.

---

## 📁 Struktur Proyek

```
submission/
├── dashboard/
│   ├── dashboard.py
│   └── hour.csv
├── data/
│   ├── day.csv
│   └── hour.csv
├── notebook.ipynb
├── requirements.txt
└── README.md
```

---

## 📋 Pertanyaan Bisnis

1. Bagaimana pengaruh kondisi cuaca terhadap jumlah penyewaan sepeda sepanjang tahun 2011–2012?
2. Pada jam berapa penyewaan sepeda paling tinggi terjadi secara rata-rata harian sepanjang tahun 2011–2012?

---

## 🛠️ Setup Environment

### Menggunakan Anaconda

```bash
conda create --name bike-ds python=3.9
conda activate bike-ds
pip install -r requirements.txt
```

### Menggunakan Virtual Environment (venv)

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

---

## 📦 Install Dependensi

Pastikan sudah mengaktifkan environment, lalu jalankan:

```bash
pip install -r requirements.txt
```

Isi `requirements.txt`:

```
streamlit
pandas
matplotlib
seaborn
```

---

## ▶️ Menjalankan Dashboard

1. Masuk ke folder `dashboard`:

```bash
cd dashboard
```

2. Jalankan Streamlit:

```bash
streamlit run dashboard.py
```

3. Dashboard akan terbuka otomatis di browser pada alamat:

```
http://localhost:8501
```

---

## ✨ Fitur Dashboard

- 📊 **2 Visualisasi Utama:**
  - Bar chart pengaruh kondisi cuaca terhadap rata-rata penyewaan
  - Line chart rata-rata penyewaan per jam dengan penanda jam puncak otomatis

- 🔧 **Fitur Interaktif (Sidebar):**
  - Filter berdasarkan **tahun** (2011 / 2012 / Semua)
  - Filter berdasarkan **kondisi cuaca** (multi-select)
  - Filter berdasarkan **rentang jam** (slider 0–23)
  - Seluruh visualisasi & metrik diperbarui secara real-time mengikuti filter

- 📈 **Ringkasan Metrik:** Total penyewaan, rata-rata per jam, nilai tertinggi & terendah

---

## 👤 Author

**Tiara Christiani Sinaga**  
Dicoding — Belajar Analisis Data dengan Python
