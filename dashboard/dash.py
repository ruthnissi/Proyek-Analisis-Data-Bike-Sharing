import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
hour_df = pd.read_csv("C:/Users/USER/Desktop/submission/dashboard/hour2.csv")

# Sidebar
st.sidebar.title('Options')
analysis_type = st.sidebar.selectbox('Select Analysis', ['Hourly Analysis', 'Day Type Comparison'])

# Function to create heatmap and line chart for day type comparison
def hourly_analysis(df):
    st.subheader('Hourly Analysis')
    st.write('Pertanyaan 1: Apakah ada pola ketergantungan antara waktu dan jumlah peminjaman sepeda?')

    # Menghitung rata-rata jumlah peminjaman sepeda per jam pada setiap hari dalam seminggu
    hourly_rentals_by_day = df.groupby(['weekday_name', 'hr'])['cnt'].mean().reset_index()

    # Mengubah struktur data untuk membuat heatmap
    heatmap_data = hourly_rentals_by_day.pivot(index='hr', columns='weekday_name', values='cnt')

    # Mengurutkan nama hari dalam seminggu
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    heatmap_data = heatmap_data.reindex(columns=days_order)

    # Visualisasi heatmap
    st.subheader('Visualisasi Heatmap')
    plt.figure(figsize=(12, 8))
    sns.heatmap(heatmap_data, cmap='YlOrRd')
    plt.title('Hubungan Antara Jam dan Hari dalam Seminggu terhadap Jumlah Peminjaman Sepeda')
    plt.xlabel('Hari dalam Seminggu')
    plt.ylabel('Jam (hr)')
    st.pyplot()

    # Visualisasi line chart untuk rata-rata jumlah peminjaman sepeda per jam pada setiap hari dalam seminggu
    st.subheader('Visualisasi Line Chart')
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=hourly_rentals_by_day, x='hr', y='cnt', hue='weekday_name', palette='muted')
    plt.title('Rata-Rata Jumlah Peminjaman Sepeda per Jam pada Setiap Hari dalam Seminggu')
    plt.xlabel('Jam (hr)')
    plt.ylabel('Rata-Rata Jumlah Peminjaman Sepeda')
    plt.legend(title='Hari dalam Seminggu')
    plt.grid(True)
    st.pyplot()
    st.write('Kesimpulan dari heatmap dan line chart menunjukkan adanya ketergantungan positif antara waktu dan jumlah peminjaman sepeda. Secara umum, jumlah peminjaman sepeda meningkat pada pagi hari dan sore hari, mencapai puncaknya sekitar jam 8 pagi dan 6 sore, dan menurun pada malam hari. Hari kerja memiliki tingkat peminjaman yang lebih tinggi dibandingkan akhir pekan.')

# Function to create bar chart and line chart for hourly analysis
def day_type_comparison(df):
    st.subheader('Day Type Comparison')
    st.write('Pertanyaan 2: Apakah ada perbedaan pola peminjaman sepeda antara hari kerja dan hari libur?')

    # Menambahkan kolom weekday_name untuk nama hari dalam seminggu
    df['weekday_name'] = pd.to_datetime(df['dteday']).dt.day_name()

    # Menghitung jumlah total peminjaman sepeda pada hari kerja dan hari libur
    total_rentals_by_day_type = df.groupby('weekday_name')['cnt'].sum().reset_index()

    # Memfilter data untuk hari kerja dan hari libur
    weekday_data = df[df['workingday'] == 1]
    weekend_data = df[df['workingday'] == 0]

    # Menghitung rata-rata jumlah peminjaman sepeda per jam pada hari kerja dan hari libur
    hourly_rentals_weekday = weekday_data.groupby('hr')['cnt'].mean()
    hourly_rentals_weekend = weekend_data.groupby('hr')['cnt'].mean()

    # Visualisasi line chart untuk membandingkan tren harian peminjaman sepeda pada hari kerja dan hari libur
    st.subheader('Visualisasi Line Chart')
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=weekday_data, x='hr', y='cnt', label='Hari Kerja', color='blue')
    sns.lineplot(data=weekend_data, x='hr', y='cnt', label='Hari Libur', color='orange')
    plt.title('Tren Harian Peminjaman Sepeda pada Hari Kerja dan Hari Libur')
    plt.xlabel('Jam (hr)')
    plt.ylabel('Rata-Rata Jumlah Peminjaman Sepeda')
    plt.legend()
    plt.grid(True)
    st.pyplot()

    # Visualisasi bar chart untuk membandingkan jumlah total peminjaman sepeda pada hari kerja dan hari libur
    st.subheader('Visualisasi Bar Chart')
    plt.figure(figsize=(8, 6))
    sns.barplot(data=total_rentals_by_day_type, x='weekday_name', y='cnt')
    plt.title('Jumlah Total Peminjaman Sepeda pada Hari Kerja dan Hari Libur')
    plt.xlabel('Hari dalam Seminggu')
    plt.ylabel('Jumlah Total Peminjaman Sepeda')
    st.pyplot()


    st.write('Kesimpulan dari line chart dan bar chart menunjukkan perbedaan pola peminjaman sepeda antara hari kerja dan hari libur. Pada hari kerja, terdapat dua puncak peminjaman: pagi hari (sekitar jam 8 pagi) dan sore hari (sekitar jam 6 sore), sementara pada hari libur, terdapat satu puncak peminjaman di siang hari (sekitar jam 12 siang). Jumlah peminjaman pada hari kerja juga lebih tinggi dibandingkan hari libur.')



# Main
st.title('Bike Sharing Analysis :sparkles:')

# Informasi terkait dataset
st.header('Dataset Information')
st.subheader(f"Number of Records: {len(hour_df)}")
st.subheader(f"Total Bike Rentals: {hour_df['cnt'].sum()}")


if analysis_type == 'Day Type Comparison':
    day_type_comparison(hour_df)
elif analysis_type == 'Hourly Analysis':
    hourly_analysis(hour_df)

st.subheader('Dampak pada Bisnis:')
st.write('-Permintaan untuk peminjaman sepeda lebih tinggi pada siang dan sore hari. Hal ini dapat menyebabkan kekurangan sepeda pada waktu tersebut.')
st.write('-Permintaan lebih rendah pada malam hari. Bisnis dapat mempertimbangkan untuk mengurangi jam operasional. ')
st.write('-Permintaan lebih rendah pada hari libur. Bisnis dapat mempertimbangkan untuk menawarkan diskon atau promosi pada hari libur untuk meningkatkan permintaan.')

st.subheader('Analisis:')
st.write('-Mengelola persediaan sepeda, memastikan bahwa mereka memiliki cukup sepeda untuk memenuhi permintaan pada waktu puncak.')
st.write('-Menetapkan harga, menetapkan harga yang lebih tinggi pada waktu puncak dan harga yang lebih rendah pada waktu non-puncak.')
st.write(' -Merencanakan staf, memiliki staf yang cukup untuk menangani permintaan pada waktu puncak.')
st.write('-Mempromosikan layanan, pada waktu dan hari dengan permintaan yang lebih rendah.')