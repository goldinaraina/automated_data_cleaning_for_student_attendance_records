# -*- coding: utf-8 -*-
"""Automatisasi_Data_Cleaning_Absensi.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xrYtXSlbKaOujxa-px0KUSDphScYs4px

# **AUTOTMATE DATA ABSENSI**

## **Load Data**
"""

import re
import pandas as pd
from google.colab import auth
import gspread
from google.auth import default

# authorizing google colab
auth.authenticate_user()

# credentials for google sheets
creds, _ = default()

# authotizing the connection
gc = gspread.authorize(creds)

# connecting
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1dyYF8cF1UhN6n-kXBq8i5cs6V7lHrlk5YSLy4w5Cn8E/edit?usp=sharing'
worksheet = gc.open_by_url(spreadsheet_url).worksheet('Form Responses 1')

# exporting data to get_all_values gives a list of rows.
rows = worksheet.get_all_values()

# connecting join data
spreadsheet_url2 = 'https://docs.google.com/spreadsheets/d/1uLGqKCusvmN3r5JUVpZq7RCCMqCL9k9K1zpViBiu8lA/edit?usp=sharing'
worksheet2 = gc.open_by_url(spreadsheet_url2).worksheet('Sheet1')

# exporting data to get_all_values gives a list of rows.
rows2 = worksheet2.get_all_values()

# using pandas to convert to a DataFrame and render.
df = pd.DataFrame.from_records(rows)
data_join = pd.DataFrame.from_records(rows2)

"""## **View Data**"""

# creating columns name
df.columns = df.iloc[0]
df = df.iloc[1:]
df.tail(5)

# creating columns name
data_join.columns = data_join.iloc[0]
data_join = data_join.iloc[1:]
data_join.tail(5)

"""# **CLEANING DATA**"""

df.info()

"""## **Change Data Type**"""

# Mengonversi kolom Timestamp menjadi tipe data datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Mengonversi kolom Hari dan tanggal menjadi tipe data date
df['Hari dan tanggal'] = pd.to_datetime(df['Hari dan tanggal']).dt.date

# Memeriksa tipe data setelah pengonversian
print(df.dtypes)

"""## **Remove Duplicate Columns**

Terdapat kolom duplikat `[keterangan]` dan `[program]`.
Terdapat kolom `[score]` yang tidak gunakan sehingga perlu dilakukan cleaning.
"""

# Menghapus kolom 'Score'
df.drop(columns=['Score','Keterangan'], inplace=True)

# Menghapus kolom 'Keterangan' dan 'Program' yang terduplikat
df = df.loc[:,~df.columns.duplicated()]

# Menampilkan data
df.tail(5)

"""Melakukan validasi pada DataFrame untuk memastikan kolom duplikat telah tidak ada."""

# Menggunakan df.shape untuk mendapatkan dimensi DataFrame
dimension = df.shape

# Menampilkan hasil
print("Jumlah baris:", dimension[0])
print("Jumlah kolom:", dimension[1])

"""## **Ensure Data Consistency**

---
Merubah kolom `[Email Address]`menggunakan huruf kecil.
"""

# Merubah huruf kecil di kolom 'Email Address'
df['Email Address'] = df['Email Address'].str.lower()

# Menampilkan data
df.tail(5)

"""Melakukan validasi ouput untuk memastikan `[Email Address]` menggunakan huruf lower"""

# Inisialisasi list untuk menyimpan baris dengan alamat email huruf kapital
email_with_uppercase = []

# Looping melalui setiap baris dalam kolom 'Email Address'
for index, row in df.iterrows():
    email = row['Email Address']
    if any(char.isupper() for char in email):
        email_with_uppercase.append(row)

# Konversi list ke DataFrame (jika diperlukan)
email_with_uppercase_df = pd.DataFrame(email_with_uppercase)

# Menampilkan hasil
print(email_with_uppercase_df)

"""## **Check Unique Value**

Mengecek unique value pada kolom `[Nama siswa]` dan `[Email Address]` untuk memastikan tidak ada duplikat.
"""

# Mengecek unique value di kolom 'Nama siswa' dan menampilkan dalam bentuk list dengan nomor indeks mulai dari 1
unique_names = df['Nama siswa'].unique()

# Menampilkan unique value dengan nomor indeks mulai dari 1
for i, name in enumerate(unique_names, start=1):
    print(f"{i}. {name}")

# Mengecek unique value di kolom 'Nama siswa' dan menampilkan dalam bentuk list dengan nomor indeks mulai dari 1
unique_names = df['Email Address'].unique()

# Menampilkan unique value dengan nomor indeks mulai dari 1
for i, name in enumerate(unique_names, start=1):
    print(f"{i}. {name}")

"""## **Change Columns Name**

Merubah nama kolom agar lebih mudan dipahami dan kesesuaian dengan konvensi Penamaan.
"""

# Mendefinisikan kamus untuk mapping nama kolom yang lama ke nama kolom yang baru
column_mapping = {
    'Timestamp': 'Waktu',
    'Email Address': 'Alamat Email',
    'Score': 'Skor',
    'Nama siswa': 'Nama Siswa',
    'Hari dan tanggal': 'Tanggal',
    'Keterangan': 'Keterangan',
    'Program': 'Program',
    'Materi Class': 'Materi',
    'Bagaimana kualitas materi yang disampaikan hari ini?': 'Kualitas Materi',
    'Feedback materi yang disampaikan hari ini.\n\n*wajib isi': 'Feedback Materi',
    'Bagaimana kualitas mentor hari ini?': 'Kualitas Mentor',
    'Feedback untuk mentor hari ini.\n\n*wajib isi': 'Feedback Mentor',
    'Sesi curhat dipersilahkan 🙏✨👀': 'Sesi Curhat',
    'background': 'Background Siswa',
    'Day': 'Hari',
    'Batch': 'Batch'
}

# Mengubah nama kolom menggunakan metode rename()
df = df.rename(columns=column_mapping)

# Memeriksa DataFrame setelah pengubahan nama kolom
df.tail()

"""Melakukan validasi pada seluruh kolom yang telah diubah dan memastikan tipe data telah sesuai."""

# Memeriksa nama kolom
print(df.columns)

# Memeriksa info kolom
print(df.info())

"""# **AUTOMASI PADA SETIAP KOLOM**

## **Automate Batch Based on Student Name**
"""

# Buat dictionary untuk memetakan Nama Siswa ke Batch mayoritas
siswa_ke_batch = df.groupby('Nama Siswa')['Batch'].apply(lambda x: x.value_counts().idxmax()).to_dict()

# Buat fungsi untuk mengisi nilai Batch berdasarkan Batch mayoritas pada Nama Siswa
def isi_batch_dengan_majority(row):
    return siswa_ke_batch.get(row['Nama Siswa'], row['Batch'])

# Terapkan fungsi ke kolom 'Batch' menggunakan metode apply
df['Batch'] = df.apply(isi_batch_dengan_majority, axis=1)

# Tampilkan DataFrame setelah proses automasi
df.tail(30)

# Inisialisasi list untuk menyimpan baris dengan batch yang tidak sesuai dengan mayoritas
incorrect_batches = []

# Looping melalui setiap baris dalam DataFrame
for index, row in df.iterrows():
    nama_siswa = row['Nama Siswa']
    batch = row['Batch']
    if nama_siswa not in siswa_ke_batch or siswa_ke_batch[nama_siswa] != batch:
        incorrect_batches.append(row)

# Konversi list ke DataFrame (jika diperlukan)
incorrect_batches_df = pd.DataFrame(incorrect_batches)

# Menampilkan hasil
print(incorrect_batches_df)

"""## **Automate Day Based On Realtime**

Membuat function untuk automasi kolom hari berdasarkan kolom hari yang memuat reatime input date.
"""

# Ubah tipe data kolom 'Waktu' menjadi datetime jika belum
df['Waktu'] = pd.to_datetime(df['Waktu'])

# Buat dictionary untuk memetakan waktu ke hari mayoritas
waktu_ke_hari = df.groupby(df['Waktu'].dt.date)['Hari'].apply(lambda x: x.value_counts().idxmax()).to_dict()

# Buat fungsi untuk mengisi nilai mayoritas ke kolom 'Hari' berdasarkan waktu
def isi_hari_dengan_majority(row):
    return waktu_ke_hari.get(row['Waktu'].date(), row['Hari'])

# Terapkan fungsi ke kolom 'Hari' menggunakan metode apply
df['Hari'] = df.apply(isi_hari_dengan_majority, axis=1)

# Tampilkan DataFrame setelah proses cleaning
df.tail(30)

"""Melakukan validasi data untuk memastikan seluruh data telah diperbaiki pada kolom hari berdasarkan waktu realtime."""

# Inisialisasi list untuk menyimpan baris dengan hari yang tidak sesuai mayoritas
incorrect_days = []

# Looping melalui setiap baris dalam DataFrame
for index, row in df.iterrows():
    waktu = row['Waktu']
    hari = row['Hari']
    if waktu.date() not in waktu_ke_hari or waktu_ke_hari[waktu.date()] != hari:
        incorrect_days.append(row)

# Konversi list ke DataFrame (jika diperlukan)
incorrect_days_df = pd.DataFrame(incorrect_days)

# Menampilkan hasil
print(incorrect_days_df)

"""## **Automate Date Based On Realtime**"""

# Buat dictionary untuk memetakan hari ke tanggal yang sesuai berdasarkan waktu
hari_ke_tanggal = df.groupby(df['Waktu'].dt.date)['Tanggal'].apply(lambda x: x.value_counts().idxmax()).to_dict()

# Buat fungsi untuk mengisi kolom 'Tanggal' berdasarkan nilai di kolom 'Hari'
def isi_tanggal_berdasarkan_hari(row):
    return hari_ke_tanggal.get(row['Waktu'].date(), row['Tanggal'])

# Terapkan fungsi ke kolom 'Tanggal' menggunakan metode apply
df['Tanggal'] = df.apply(isi_tanggal_berdasarkan_hari, axis=1)

# Tampilkan DataFrame setelah proses perubahan
df.tail(5)

# Inisialisasi list untuk menyimpan baris dengan tanggal yang tidak sesuai dengan hari yang sesuai
incorrect_dates = []

# Looping melalui setiap baris dalam DataFrame
for index, row in df.iterrows():
    waktu = row['Waktu']
    tanggal = row['Tanggal']
    if waktu.date() not in hari_ke_tanggal or hari_ke_tanggal[waktu.date()] != tanggal:
        incorrect_dates.append(row)

# Konversi list ke DataFrame (jika diperlukan)
incorrect_dates_df = pd.DataFrame(incorrect_dates)

# Menampilkan hasil
print(incorrect_dates_df)

"""## **Automate Program Based On Realtime**"""

# Buat dictionary untuk memetakan waktu ke program mayoritas
waktu_ke_program = df.groupby(df['Waktu'].dt.date)['Program'].apply(lambda x: x.value_counts().idxmax()).to_dict()

# Buat fungsi untuk mengisi nilai mayoritas ke kolom 'Program' berdasarkan waktu
def isi_program_dengan_majority(row):
    return waktu_ke_program.get(row['Waktu'].date(), row['Program'])

# Terapkan fungsi ke kolom 'Program' menggunakan metode apply
df['Program'] = df.apply(isi_program_dengan_majority, axis=1)

# Tampilkan DataFrame setelah proses perbaikan
df.tail(5)

# Inisialisasi list untuk menyimpan baris dengan program yang tidak sesuai dengan mayoritas
incorrect_programs = []

# Looping melalui setiap baris dalam DataFrame
for index, row in df.iterrows():
    waktu = row['Waktu']
    program = row['Program']
    if waktu.date() not in waktu_ke_program or waktu_ke_program[waktu.date()] != program:
        incorrect_programs.append(row)

# Konversi list ke DataFrame (jika diperlukan)
incorrect_programs_df = pd.DataFrame(incorrect_programs)

# Menampilkan hasil
print(incorrect_programs_df)

"""## **Automate Subject Based on Date**

"""

# Buat dictionary untuk memetakan materi mayoritas untuk setiap hari
materi_majority_per_hari = df.groupby('Tanggal')['Materi'].apply(lambda x: x.value_counts().idxmax()).to_dict()

# Fungsi untuk mengisi nilai materi dengan mayoritas untuk setiap hari
def isi_materi_dengan_majority_per_hari(row):
    return materi_majority_per_hari.get(row['Tanggal'])

# Terapkan fungsi ke kolom 'Materi'
df['Materi'] = df.apply(isi_materi_dengan_majority_per_hari, axis=1)

# Tampilkan DataFrame setelah proses cleaning
df.tail(5)

# Inisialisasi list untuk menyimpan baris dengan materi yang tidak sesuai dengan mayoritas per hari
incorrect_materials = []

# Looping melalui setiap baris dalam DataFrame
for index, row in df.iterrows():
    hari = row['Hari']
    materi = row['Materi']
    if hari not in materi_majority_per_hari or materi_majority_per_hari[hari] != materi:
        incorrect_materials.append(row)

# Konversi list ke DataFrame (jika diperlukan)
incorrect_materials_df = pd.DataFrame(incorrect_materials)

# Menampilkan hasil
#incorrect_materials_df

"""## **Automate Background Based on Student Name**"""

# Buat dictionary untuk memetakan nama siswa ke background siswa mayoritas
siswa_ke_background = df.groupby('Nama Siswa')['Background Siswa'].apply(lambda x: x.value_counts().idxmax()).to_dict()

# Buat fungsi untuk mengisi nilai background siswa berdasarkan background siswa mayoritas pada nama siswa
def isi_background_siswa_dengan_majority(row):
    return siswa_ke_background.get(row['Nama Siswa'], row['Background Siswa'])

# Terapkan fungsi ke kolom 'Background Siswa' menggunakan metode apply
df['Background Siswa'] = df.apply(isi_background_siswa_dengan_majority, axis=1)

# Tampilkan DataFrame setelah proses automasi
df.head(5)

# Inisialisasi list untuk menyimpan baris dengan background siswa yang tidak sesuai dengan mayoritas
incorrect_backgrounds = []

# Looping melalui setiap baris dalam DataFrame
for index, row in df.iterrows():
    nama_siswa = row['Nama Siswa']
    background_siswa = row['Background Siswa']
    if nama_siswa not in siswa_ke_background or siswa_ke_background[nama_siswa] != background_siswa:
        incorrect_backgrounds.append(row)

# Konversi list ke DataFrame (jika diperlukan)
incorrect_backgrounds_df = pd.DataFrame(incorrect_backgrounds)

# Menampilkan hasil
print(incorrect_backgrounds_df)

"""## **Automate Batch Based on Student Name**"""

# Buat dictionary untuk memetakan Nama Siswa ke Batch mayoritas
siswa_ke_batch = df.groupby('Nama Siswa')['Batch'].apply(lambda x: x.value_counts().idxmax()).to_dict()

# Buat fungsi untuk mengisi nilai Batch berdasarkan Batch mayoritas pada Nama Siswa
def isi_batch_dengan_majority(row):
    return siswa_ke_batch.get(row['Nama Siswa'], row['Batch'])

# Terapkan fungsi ke kolom 'Batch' menggunakan metode apply
df['Batch'] = df.apply(isi_batch_dengan_majority, axis=1)

# Tampilkan DataFrame setelah proses automasi
df.tail(5)

"""# **SENTIMEN ANALYTICS**

Membuat automasi untuk mengolah data feedback materi dan mentor
"""

def kategori_feedback(feedback):

    if "Sangat Mudah/Mudah/Menarik" in feedback:

        return 'Positive'

    elif "Cukup/Aman" in feedback:

        return 'Neutral'

    elif "Sangat Sulit/Sulit/Bingung/Pusing" in feedback:

        return 'Negative'

    else:

        return None

def kategori_mentor(feedback):

    if "Jelas/Mudah dimengerti/Paham/Seru/Menyenangkan/Nyaman" in feedback:

        return 'Positive'

    elif "Cukup/Aman" in feedback:

        return 'Neutral'

    elif "Kurang Jelas/Kecepetan/Bingung/Galak" in feedback:

        return 'Negative'

    else:

        return None

# menambahkan kolom baru 'Sentiment Materi' dan 'Sentiment Mentor'
df['Sentiment Materi'] = df['Feedback Materi'].apply(kategori_feedback)

df['Sentiment Mentor'] = df['Feedback Mentor'].apply(kategori_mentor)

# menampilkan output
df.tail(5)

"""## **Re-index Columns Name**"""

# Mengubah urutan kolom
new_columns = ['Waktu', 'Alamat Email', 'Nama Siswa', 'Tanggal', 'Hari', 'Program', 'Materi', 'Background Siswa', 'Kualitas Materi',  'Kualitas Mentor', 'Feedback Materi',  'Feedback Mentor', 'Sesi Curhat', 'Bagaimana tingkat kesulitan materi?',	'Bagaimana tingkat kualitas mentor hari ini?', 'Sentiment Materi', 'Sentiment Mentor', 'Batch']

df = df[new_columns]

# menampilkan visualisasi
df

"""# **JOIN SENTIMENT DATA**"""

# Menggabungkan dataFrame df dengan dataFrame data_join
for column in ['Sentiment Materi', 'Sentiment Mentor']:
    df[column].fillna(data_join[column], inplace=True)

df.head(10)

"""# **EXCTRACT DATE IN WEEKS**

## **Group by and Count Date**
"""

# Mengonversi kolom Tanggal menjadi tipe data datetime
df['Tanggal'] = pd.to_datetime(df['Tanggal'])

# Kelompokan tanggal berdasarkan tanggal dan hitung jumlah entri per tanggal
count_per_tanggal = df.groupby('Tanggal').size().reset_index(name='Jumlah')

# Rubah indeks mulai dari 1
count_per_tanggal.index = count_per_tanggal.index + 1

# Menampilkan hasil kalkulasi jumlah entri per tanggal
count_per_tanggal

"""## **Group by and Count in Weeks**"""

# Konversi kolom Tanggal menjadi tipe data datetime
count_per_tanggal['Tanggal'] = pd.to_datetime(count_per_tanggal['Tanggal'])

# Kelompokkan tanggal berdasarkan minggu dan hitung jumlah entri per minggu
count_per_tanggal['Minggu'] = count_per_tanggal['Tanggal'].dt.isocalendar().week
count_per_minggu = count_per_tanggal.groupby('Minggu')['Jumlah'].sum().reset_index()

# Mengganti indeks mulai dari 1
count_per_minggu.index = count_per_minggu.index + 1

# Tampilkan hasil
count_per_minggu

"""## **Mean by Weeks**"""

# Menghitung rata-rata jumlah entri per minggu
average_per_minggu = count_per_minggu['Jumlah'].mean()

# Menambahkan kolom baru "Rata-rata Per Hari" ke DataFrame
count_per_minggu['Rata-rata Per Hari'] = round(count_per_minggu['Jumlah'] / 5).astype(int)

# Menampilkan hasil
count_per_minggu

"""# **EXPORT DATA TO GOOGLE SHEET**"""

df.to_csv("absensi_clean.csv", index=False)
count_per_minggu.to_csv('minggu_clean.csv', index=False)

from google.colab import drive
drive.mount('/content/drive')

#  save to excel
df.to_csv("/content/drive/MyDrive/Teach4Hope Database/02. Absensi/absensi_clean.csv", index=False)
count_per_minggu.to_csv("/content/drive/MyDrive/Teach4Hope Database/02. Absensi/minggu_clean.csv", index=False)

"""## **Set Timer**"""