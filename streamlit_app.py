import streamlit as st
import requests
import pandas as pd
from PIL import Image

# Ganti dengan API Key USDA FoodData Central milikmu
API_KEY = "YOUR_USDA_API_KEY"
API_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"

# Styling
st.set_page_config(page_title="Analisis Nutrisi Makanan", layout="wide")
st.markdown("""
    <style>
        .main {
            background-color: #f7f7f7;
            font-family: 'Arial', sans-serif;
        }
        .title {
            text-align: center;
            font-size: 48px;
            color: #2c3e50;
        }
        .sub-header {
            color: #34495e;
            font-size: 24px;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<div class='title'>🥗 Analisis Nutrisi Makanan</div>", unsafe_allow_html=True)
st.write("\n")
st.markdown("<div class='sub-header'>Masukkan nama makanan untuk mengetahui informasi nutrisinya berdasarkan data dari USDA.</div>", unsafe_allow_html=True)

# Input makanan
query = st.text_input("Masukkan nama makanan (gunakan Bahasa Inggris)", "apple")

if st.button("Cari Informasi Nutrisi"):
    with st.spinner("Mengambil data dari USDA..."):
        params = {
            "api_key": API_KEY,
            "query": query,
            "pageSize": 1
        }
        response = requests.get(API_URL, params=params)

        if response.status_code == 200:
            data = response.json()
            if data["foods"]:
                food = data["foods"][0]
                st.success(f"Data nutrisi untuk: {food['description']}")

                # Buat dictionary nutrisi
                nutrients = {item['nutrientName']: item['value'] for item in food['foodNutrients']}

                # Ambil nutrisi penting
                nutrition_info = {
                    "Kalori (kcal)": nutrients.get("Energy", 0),
                    "Karbohidrat (g)": nutrients.get("Carbohydrate, by difference", 0),
                    "Protein (g)": nutrients.get("Protein", 0),
                    "Lemak Total (g)": nutrients.get("Total lipid (fat)", 0),
                    "Serat (g)": nutrients.get("Fiber, total dietary", 0),
                    "Gula (g)": nutrients.get("Sugars, total including NLEA", 0),
                    "Kalsium (mg)": nutrients.get("Calcium, Ca", 0),
                    "Zat Besi (mg)": nutrients.get("Iron, Fe", 0),
                }

                df = pd.DataFrame.from_dict(nutrition_info, orient='index', columns=['Jumlah'])
                st.dataframe(df)

                # Visualisasi
                st.subheader("Visualisasi Informasi Nutrisi 📊")
                st.bar_chart(df)
            else:
                st.warning("Makanan tidak ditemukan di database USDA.")
        else:
            st.error("Terjadi kesalahan saat mengambil data. Silakan coba lagi nanti.")

# Footer
st.markdown("---")
st.markdown("Dibuat dengan ❤️ menggunakan Streamlit dan API USDA")
