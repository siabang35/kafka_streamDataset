# Streaming Gambar dengan Kafka

Proyek ini bertujuan untuk memproduksi dan mengonsumsi data gambar dalam bentuk base64 melalui Kafka. Dataset yang digunakan adalah dataset penyakit tanaman yang terdiri dari 14 jenis tanaman dengan 68 kelas penyakit tanaman. Dataset berada di direktori `train`.

## Fitur Utama
1. **Producer**
   - Mengonversi gambar ke format base64.
   - Mengirim data base64 gambar ke topik Kafka.
   - Mendukung pengompresian gambar untuk mengurangi ukuran file.

2. **Consumer**
   - Mengonsumsi data base64 gambar dari topik Kafka.
   - Menampilkan gambar yang diterima menggunakan matplotlib.
   - Menganalisis format dan ukuran gambar.

3. **Monitoring Dataset**
   - Menampilkan contoh acak dari gambar dalam dataset lokal.
   - Menganalisis jumlah gambar berdasarkan format dan ukuran rata-rata.

4. **Monitoring Konsumsi Kafka**
   - Menampilkan gambar yang dikonsumsi dari Kafka.
   - Melakukan analisis sederhana pada format gambar yang dikonsumsi.

## Struktur Dataset
Dataset berisi:
- **14 Jenis Tanaman**
- **68 Kelas Penyakit Tanaman**
- Tersimpan di direktori `train` dengan struktur berikut:
  ```
  train/
  ├── tanaman1/
  │   ├── penyakit1/
  │   ├── penyakit2/
  │   └── ...
  ├── tanaman2/
  └── ...
  ```

## Cara Menjalankan

### 1. Producer
Script producer akan membaca gambar dari dataset, mengonversinya ke format base64, dan mengirimkannya ke topik Kafka.
```bash
python producer.py
```

### 2. Consumer
Script consumer akan membaca data base64 dari topik Kafka, mendekodenya kembali menjadi gambar, dan menampilkannya.
```bash
python consumer.py
```

### 3. Monitoring Dataset Lokal
Untuk memonitor dataset lokal dan menganalisisnya:
```bash
python monitor_dataset.py
```

### 4. Konsumsi dan Monitoring Kafka
Untuk memonitor data yang diterima dari Kafka:
```bash
python monitor_consumed_images.py
```

## Konfigurasi Kafka
- **Bootstrap Servers**: `3.83.11.185:9092`
- **Topik**: `image-stream`
- **Group ID (Consumer)**: `image-consumer-group`

## Prasyarat
1. Python 3.x
2. Perpustakaan Python:
   - confluent_kafka
   - matplotlib
   - pillow

## Catatan
- Pastikan Kafka telah dikonfigurasi dengan benar dan berjalan di alamat yang sesuai.
- Dataset harus diletakkan di direktori `train` seperti struktur yang disebutkan.

## Lisensi
Proyek ini dilisensikan di bawah MIT License.
