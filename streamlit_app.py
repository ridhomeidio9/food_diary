import streamlit as st
import requests
import plotly.graph_objs as go

# ---------------------------
# Konfigurasi API Edamam
APP_ID = "your_app_id"
APP_KEY = "your_app_key"
API_URL = "https://api.edamam.com/api/nutrition-data"

# ---------------------------
st.set_page_config(page_title="Analisis Nutrisi Makanan", layout="centered")

st.markdown(
    """
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .title {
        font-size: 36px;
        color: #4a4a4a;
        text-align: center;
        font-weight: bold;
    }
    .subtitle {
        font-size: 20px;
        color: #6c757d;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="title">🔍 Analisis Nutrisi Makanan</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Masukkan makanan dan lihat informasi gizi secara langsung!</div>', unsafe_allow_html=True)
st.write("")

# ---------------------------
makanan_input = st.text_input("🍽 Masukkan makanan (contoh: 1 cup nasi, 2 telur rebus):", "")

if st.button("Analisis"):
    if not makanan_input:
        st.warning("Silakan masukkan deskripsi makanan terlebih dahulu.")
    else:
        with st.spinner("Menganalisis makanan..."):
            params = {
                "app_id": APP_ID,
                "app_key": APP_KEY,
                "ingr": makanan_input
            }
            response = requests.get(API_URL, params=params)

            if response.status_code == 200:
                data = response.json()

                calories = data.get("calories", 0)
                total_weight = data.get("totalWeight", 0)
                nutrients = data.get("totalNutrients", {})

                protein = nutrients.get("PROCNT", {}).get("quantity", 0)
                carbs = nutrients.get("CHOCDF", {}).get("quantity", 0)
                fat = nutrients.get("FAT", {}).get("quantity", 0)

                st.success("✅ Analisis selesai!")

                st.subheader("📊 Rincian Nutrisi")
                col1, col2 = st.columns(2)

                with col1:
                    st.metric(label="Kalori", value=f"{calories:.2f} kcal")
                    st.metric(label="Berat Total", value=f"{total_weight:.2f} g")
                    st.metric(label="Protein", value=f"{protein:.2f} g")
                
                with col2:
                    st.metric(label="Karbohidrat", value=f"{carbs:.2f} g")
                    st.metric(label="Lemak", value=f"{fat:.2f} g")

                # ---------------------------
                # Visualisasi Pie Chart
                st.subheader("📈 Komposisi Nutrisi Utama (Pie Chart)")
                pie = go.Figure(data=[go.Pie(
                    labels=['Protein', 'Karbohidrat', 'Lemak'],
                    values=[protein, carbs, fat],
                    hole=.4,
                    marker=dict(colors=['#00cc96', '#636efa', '#ef553b'])
                )])
                pie.update_layout(height=400, showlegend=True)
                st.plotly_chart(pie)

                # ---------------------------
                # Visualisasi Bar Chart
                st.subheader("📉 Grafik Batang Nutrisi")
                bar = go.Figure(data=[
                    go.Bar(name="Protein", x=["Protein"], y=[protein], marker_color="#00cc96"),
                    go.Bar(name="Karbohidrat", x=["Karbohidrat"], y=[carbs], marker_color="#636efa"),
                    go.Bar(name="Lemak", x=["Lemak"], y=[fat], marker_color="#ef553b"),
                ])
                bar.update_layout(barmode='group')
                st.plotly_chart(bar)

            else:
                st.error("❌ Gagal mengambil data nutrisi. Periksa input atau kredensial API Anda.")
