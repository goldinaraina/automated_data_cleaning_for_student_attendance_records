# automated_data_cleaning_for_student_attendance_records

Proses otomatis ini dirancang untuk membersihkan dan mengelola data absensi siswa secara efisien. Berikut adalah langkah-langkah utama dalam proses ini:

1. **Load Data from Google Sheets**: Mengambil data absensi dari Google Sheets dan memuatnya ke dalam DataFrame Pandas untuk analisis lebih lanjut.

2. **Change Data Types**: Mengonversi tipe data kolom yang sesuai, seperti mengubah kolom 'Timestamp' menjadi tipe data datetime dan 'Hari dan tanggal' menjadi tipe data date.

3. **Remove Duplicate Columns**: Menghapus kolom yang duplikat atau tidak diperlukan dari DataFrame.

4. **Ensure Data Consistency**: Memastikan konsistensi dalam format alamat email dengan mengubahnya menjadi huruf kecil.

5. **Check Unique Values**: Memeriksa nilai unik pada kolom 'Nama siswa' dan 'Alamat Email' untuk menjaga integritas data.

6. **Change Column Names**: Mengubah nama kolom agar lebih deskriptif dan mudah dipahami.

7. **Automate Batch Assignment Based on Student Name**: Menggunakan pendekatan berbasis mayoritas untuk menetapkan kolom 'Batch' berdasarkan batch yang paling sering muncul untuk setiap nama siswa.

8. **Automate Day Assignment Based on Realtime**: Menetapkan kolom 'Hari' berdasarkan hari mayoritas terkait dengan waktu setiap entri.

9. **Automate Date Assignment Based on Realtime**: Menetapkan kolom 'Tanggal' berdasarkan tanggal mayoritas terkait dengan waktu setiap entri.

10. **Automate Program Assignment Based on Realtime**: Menetapkan kolom 'Program' berdasarkan program mayoritas terkait dengan waktu setiap entri.

11. **Automate Subject Assignment Based on Date**: Menetapkan kolom 'Materi' berdasarkan materi yang paling sering muncul untuk setiap tanggal.

12. **Automate Background Assignment Based on Student Name**: Menetapkan kolom 'Background Siswa' berdasarkan latar belakang yang paling sering muncul untuk setiap nama siswa.

13. **Join Sentiment Data**: Menganalisis umpan balik terhadap materi dan mentor untuk mengategorikan sentimen sebagai positif, netral, atau negatif. Sentimen ini kemudian ditambahkan ke DataFrame.

14. **Extract Date in Weeks**: Mengelompokkan tanggal menjadi mingguan dan menghitung jumlah entri untuk setiap minggu.

15. **Export Cleaned Data to Google Sheets**: Menyimpan data yang telah dibersihkan kembali ke Google Sheets untuk analisis lebih lanjut dan berbagi. Langkah ini memastikan bahwa data yang telah dibersihkan dapat diakses dengan mudah dan digunakan untuk tugas-tugas mendatang.
