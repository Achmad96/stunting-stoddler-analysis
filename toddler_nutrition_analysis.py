from dotenv import load_dotenv
import os
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Analisis Status Gizi Balita", layout="wide")
load_dotenv()
@st.cache_data
def load_data():
    df = pd.read_csv(os.getenv("DATA_SOURCE", "data/toddler_nutrition.csv"))
    df['Status Gizi'] = df['Status Gizi'].replace('tinggi', 'above-average')
    df['Tinggi Badan (cm)'] = df['Tinggi Badan (cm)'].astype(float).round(2)
    return df

def height_classification(row):
    age_months = row['Umur (bulan)']
    height = row['Tinggi Badan (cm)']
    gender = row['Jenis Kelamin']
    boy_ranges = {
        (0, 12): (72, 78),   
        (13, 24): (82, 92),  
        (25, 36): (94, 100), 
        (37, 48): (100, 108),
        (49, 60): (108, 114) 
    }
    girl_ranges = {
        (0, 12): (70, 78),   
        (13, 24): (80, 92),  
        (25, 36): (92, 100), 
        (37, 48): (100, 105),
        (49, 60): (106, 116) 
    }
    ranges = boy_ranges if gender == 'laki-laki' else girl_ranges
    for age_range, height_range in ranges.items():
        if age_range[0] <= age_months <= age_range[1]:
            min_height, max_height = height_range
            if height < min_height:
                return "stunted"
            elif height > max_height:
                return "above-average"
            else:
                return "normal"
    return "Usia di luar rentang analisis"

df = load_data()
dataset_url = "https://www.kaggle.com/datasets/rendiputra/stunting-balita-detection-121k-rows"

st.title("Analisis Status Gizi pada Anak Usia Balita")

# SIDEBAR
st.sidebar.header("Filter Data")
age_min_value = int(df["Umur (bulan)"].min())
age_max_value = int(df["Umur (bulan)"].max())
jenis_unique = df["Jenis Kelamin"].unique()
status_unique = df["Status Gizi"].unique()
selected_gender = st.sidebar.multiselect("Pilih Jenis Kelamin", options=jenis_unique, default=jenis_unique)
age_range = st.sidebar.slider("Rentang Umur (bulan)", age_min_value, age_max_value, [age_min_value, age_max_value])
selected_nutrition = st.sidebar.multiselect("Status Gizi", options=status_unique, default=status_unique)
filtered_df = df[(df["Jenis Kelamin"].isin(selected_gender)) & (df["Umur (bulan)"] >= age_range[0]) &  (df["Umur (bulan)"] <= age_range[1]) & (df["Status Gizi"].isin(selected_nutrition))]

# MAIN CONTENT
st.subheader("Dataset Preview")
st.dataframe(filtered_df, use_container_width=True)
csv = filtered_df.to_csv(index=False)
st.download_button(
    label="Unduh sebagai CSV",
    data=csv,
    file_name="stunting_toddler.csv",
    mime="text/csv" 
  )
st.markdown("---")

st.subheader("Statistik Data")
column_1, column_2 = st.columns(2)
with column_1:
    st.metric("Jumlah Data Keseluruhan", len(filtered_df))
with column_2:
    st.metric("Rata-rata Umur", f"{filtered_df['Umur (bulan)'].mean():.1f} bulan")

st.write("Statistik data yang telah difilter:")
st.dataframe(filtered_df.describe().round(2), use_container_width=True)
column_1, column_2 = st.columns(2)
with column_1:
    st.subheader("Jumlah Data per Status Gizi")
    st.dataframe(filtered_df["Status Gizi"].value_counts(), use_container_width=True)
with column_2:
    st.subheader("Jumlah Data per Jenis Kelamin")
    st.dataframe(filtered_df["Jenis Kelamin"].value_counts(), use_container_width=True)
st.markdown("---")

st.subheader("Distribusi Status Gizi")
nutrition_counts = filtered_df['Status Gizi'].value_counts().reset_index()
nutrition_counts.columns = ['Status Gizi', 'Jumlah']
nutrition_bar = px.bar(
    nutrition_counts, 
    x='Status Gizi', 
    y='Jumlah',
    color='Status Gizi',
    title="Jumlah Balita per Status Gizi",
    labels={'Status Gizi' : 'Status Gizi', 'Jumlah': 'Jumlah Balita'},
    text='Jumlah'
)
nutrition_bar.update_traces(textposition='inside')
st.plotly_chart(nutrition_bar, use_container_width=True)
st.markdown("---")

st.subheader("Distribusi Status Gizi Berdasarkan Standar WHO")
st.write("""
Data tinggi badan dibandingkan dengan standar WHO untuk rentang tinggi badan ideal
berdasarkan usia dan jenis kelamin.
""")
column_1, column_2 = st.columns(2)
with column_1:
    st.write("**Rentang Tinggi Ideal untuk Anak Laki-laki**")
    boy_data = {
        "Usia": ["1 tahun (0-12 bulan)", "2 tahun (13-24 bulan)", "3 tahun (25-36 bulan)", "4 tahun (37-48 bulan)", "5 tahun (49-60 bulan)"],
        "Rentang Tinggi": ["72 - 78 cm", "82 - 92 cm", "94 - 100 cm", "100 - 108 cm", "108 - 114 cm"]
    }
    st.table(pd.DataFrame(boy_data))
with column_2:
    st.write("**Rentang Tinggi Ideal untuk Anak Perempuan**")
    girl_data = {
        "Usia": ["1 tahun (0-12 bulan)", "2 tahun (13-24 bulan)", "3 tahun (25-36 bulan)", "4 tahun (37-48 bulan)", "5 tahun (49-60 bulan)"],
        "Rentang Tinggi": ["70 - 78 cm", "80 - 92 cm", "92 - 100 cm", "100 - 105 cm", "106 - 116 cm"]
    }
    st.table(pd.DataFrame(girl_data))
filtered_df['WHO Status'] = filtered_df.apply(height_classification, axis=1)
who_counts = filtered_df['WHO Status'].value_counts().reset_index()
who_counts.columns = ['WHO Status', 'Jumlah']
who_bar = px.bar(
    who_counts, 
    x='WHO Status', 
    y='Jumlah',
    color='WHO Status',
    title="Distribusi Status Gizi Berdasarkan Standar WHO",
    labels={'WHO Status': 'Status WHO', 'Jumlah': 'Jumlah Balita'},
    text='Jumlah'
)
who_bar.update_traces(textposition='inside')
st.plotly_chart(who_bar, use_container_width=True)
st.markdown("---")

st.subheader("Perbandingan Status Gizi Berdasarkan Jenis Kelamin")
columns = st.columns(2)
genders = filtered_df['Jenis Kelamin'].unique()
for index, gender in enumerate(genders):
    with columns[index % 2]:
        gender_df = filtered_df[filtered_df['Jenis Kelamin'] == gender]
        gender_nutrition = gender_df['Status Gizi'].value_counts().reset_index()
        gender_nutrition.columns = ['Status Gizi', 'Jumlah']
        gender_chart = px.pie(
            gender_nutrition,
            values='Jumlah',
            names='Status Gizi',
            title=f"Distribusi Status Gizi - {gender}"
        )
        st.plotly_chart(gender_chart, use_container_width=True)
st.markdown("---")

st.subheader("Hubungan Tinggi Badan dengan Umur")
height_scatter = px.scatter(
    filtered_df, 
    x='Umur (bulan)', 
    y='Tinggi Badan (cm)', 
    color='Status Gizi',
    hover_data=['Jenis Kelamin'],
    title="Tinggi Badan Berdasarkan Umur dan Status Gizi",
    # barmode='stack'
)
st.plotly_chart(height_scatter, use_container_width=True)
st.markdown("---")

st.subheader("Distribusi Status Gizi Berdasarkan Umur")
nutrition_by_age = filtered_df.groupby(['Umur (bulan)', 'Status Gizi']).size().reset_index(name='Jumlah')
show_markers = st.checkbox("Tampilkan titik pada garis", value=True)
age_line = px.line(
    nutrition_by_age,
    x='Umur (bulan)',
    y='Jumlah',
    color='Status Gizi',
    title="Jumlah Balita per Status Gizi Berdasarkan Umur",
    markers=show_markers
)
st.plotly_chart(age_line, use_container_width=True)
st.markdown("---")

st.caption(f"Sumber data: <a href='{dataset_url}'>Stunting Toddler (Balita) Detection (121K rows)</a>", unsafe_allow_html=True)
