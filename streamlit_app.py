st.title("🍽️ Analisis Nutrisi Makanan")
st.write("Pilih makanan untuk melihat informasi gizinya (kalori, karbohidrat, protein, dan gula).")

# Data Nutrisi Contoh
nutrisi_makanan = {
    "Nasi Putih (100g)": {"Kalori": 130, "Karbohidrat": 28, "Protein": 2.7, "Gula": 0.1},
    "Ayam Goreng (100g)": {"Kalori": 239, "Karbohidrat": 0, "Protein": 27, "Gula": 0},
    "Tahu Goreng (100g)": {"Kalori": 271, "Karbohidrat": 9.2, "Protein": 14, "Gula": 0.6},
    "Tempe Goreng (100g)": {"Kalori": 200, "Karbohidrat": 7.7, "Protein": 18, "Gula": 0},
    "Telur Rebus (1 butir)": {"Kalori": 68, "Karbohidrat": 0.6, "Protein": 5.5, "Gula": 0.5},
    "Apel (100g)": {"Kalori": 52, "Karbohidrat": 14, "Protein": 0.3, "Gula": 10},
    "Pisang (100g)": {"Kalori": 89, "Karbohidrat": 23, "Protein": 1.1, "Gula": 12},
    "Susu Full Cream (100ml)": {"Kalori": 61, "Karbohidrat": 4.8, "Protein": 3.2, "Gula": 5.1}
}

# Dropdown untuk memilih makanan
makanan_dipilih = st.selectbox("Pilih Makanan", list(nutrisi_makanan.keys()))

# Tampilkan hasil analisis
if makanan_dipilih:
    st.subheader(f"📊 Informasi Gizi: {makanan_dipilih}")
    gizi = nutrisi_makanan[makanan_dipilih]
    st.metric("Kalori (kkal)", gizi["Kalori"])
    st.metric("Karbohidrat (g)", gizi["Karbohidrat"])
    st.metric("Protein (g)", gizi["Protein"])
    st.metric("Gula (g)", gizi["Gula"])

    # Visualisasi pie chart
    st.subheader("🍥 Komposisi Gizi")
    st.pyplot(
        figure=__import__('matplotlib.pyplot').pie(
            [gizi["Karbohidrat"], gizi["Protein"], gizi["Gula"]],
            labels=["Karbohidrat", "Protein", "Gula"],
            autopct="%1.1f%%",
            startangle=140
        )[0].figure
    )

# Footer
st.markdown("---")
st.caption("Dibuat oleh Mahasiswa Jurusan Pangan | Streamlit Nutrisi App 2025")
