import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Food Diary", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🥗 Penganalisis Nutrisi Makanan")
st.markdown("Analisis nilai gizi makanan favorit Anda. Cukup masukkan nama makanan atau unggah gambar, dan biarkan kami menganalisanya untuk Anda! 🍎")

# Data nutrisi contoh
data_contoh = {
    "Makanan": ["Apel", "Pisang", "Brokoli", "Dada Ayam", "Nasi", "Alpukat"],
    "Kalori": [95, 105, 55, 165, 206, 240],
    "Protein (g)": [0.5, 1.3, 3.7, 31, 4.3, 3],
    "Karbohidrat (g)": [25, 27, 11, 0, 45, 12.8],
    "Lemak (g)": [0.3, 0.3, 0.6, 3.6, 0.4, 22]
}

df = pd.DataFrame(data_contoh)

# Sidebar
st.sidebar.header("Metode Input")
metode_input = st.sidebar.radio("Pilih metode input:", ("Pilih dari Daftar", "Unggah Gambar"))

if metode_input == "Pilih dari Daftar":
    makanan_terpilih = st.selectbox("Pilih makanan:", df["Makanan"])
    info_makanan = df[df["Makanan"] == makanan_terpilih]
    st.subheader(f"Fakta Nutrisi untuk {makanan_terpilih}")
    st.dataframe(info_makanan.set_index("Makanan"), use_container_width=True)

    # Visualisasi
    st.subheader("Pemaparan Nutrisi")
    fig, ax = plt.subplots()
    info_makanan_plot = info_makanan.drop(columns="Makanan").T
    info_makanan_plot.columns = [makanan_terpilih]
    sns.barplot(x=info_makanan_plot[makanan_terpilih].index, y=info_makanan_plot[makanan_terpilih].values, palette="viridis", ax=ax)
    ax.set_ylabel("Jumlah")
    st.pyplot(fig)

elif metode_input == "Unggah Gambar":
    file_diunggah = st.file_uploader("Unggah gambar makanan", type=["jpg", "jpeg", "png"])

    if file_diunggah:
        gambar = Image.open(file_diunggah)
        st.image(gambar, caption="Gambar yang Diupload", use_column_width=True)
        st.warning("🔍 Deteksi makanan dari gambar sedang dalam pengembangan. Harap gunakan daftar dropdown untuk sementara waktu.")
    else:
        st.info("Silakan unggah gambar makanan untuk dianalisis.")

# Footer
st.markdown("""
---
Dibuat dengan ❤️ menggunakan Streamlit  
Data hanya untuk tujuan pendidikan.
""")
