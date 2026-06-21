# Mini Project 2: Deteksi Kendaraan Terang pada Area Parkir
**Mata Kuliah:** Pengolahan Citra Digital (PCV)  
**Nama:** Khalil Gibran Al Azhar
**NRP:** 5024241100
**Jurusan:** Teknik Komputer / Teknik Elektro  

---

##  Deskripsi Proyek
Proyek ini bertujuan untuk mendeteksi dan menghitung jumlah kendaraan yang terparkir menggunakan teknik **Visi Komputer Klasik (Non-AI)**. Pendekatan yang digunakan berfokus pada segmentasi intensitas biner langsung (*Direct Intensity Thresholding*) untuk mengekstrak bodi/atap kendaraan berwarna terang, dikombinasikan dengan perhitungan rasio kepadatan (*Extent Ratio*) guna menyaring *noise*.

## 🚗 Hasil Deteksi
Berdasarkan parameter pengujian pada citra `parking.jpg`, program memberikan output sebagai berikut:
- **Total Kendaraan (Mobil Terang):** `[Isi dengan angka hasil output Console]` Unit
- **Total Objek Tersaring (Bukan Mobil / Noise):** `[Isi dengan angka hasil output Console]` Unit

---

## ⚙️ Pipeline Pemrosesan Citra

Program ini tidak menggunakan deteksi tepi (seperti Canny Edge) untuk menghindari terpecahnya objek, melainkan langsung menggunakan thresholding kecerahan dengan tahapan berikut:

1. **Konversi Grayscale (`cv2.cvtColor`)**
   Mengubah citra RGB (3-channel) menjadi citra keabuan (1-channel) untuk menyederhanakan komputasi intensitas cahaya.
2. **Reduksi Noise (`cv2.GaussianBlur`)**
   Menggunakan kernel $7 \times 7$ untuk mengaburkan variasi tekstur halus (seperti butiran aspal atau garis marka kotor) sehingga warna atap mobil menjadi lebih rata.
3. **Segmentasi Atap (*Binary Thresholding*)**
   Menerapkan `cv2.threshold` pada nilai intensitas `140`. Semua piksel di atas 140 (atap mobil) diubah menjadi putih murni (`255`), sedangkan aspal dan bayangan menjadi hitam pekat (`0`).
4. **Perbaikan Struktur Biner (*Morphological Closing*)**
   Menggunakan elemen struktur persegi $11 \times 11$ dengan fungsi `cv2.morphologyEx`. Proses ini berguna untuk menggabungkan bercak putih yang berdekatan dan menambal rongga hitam kecil (seperti kaca wiper) di dalam blok atap.
5. **Ekstraksi Geometri & Filter Kepadatan (*Extent Ratio*)**
   Komputer mencari kontur dari blok putih tersebut. Filter dilakukan dengan mengukur rasio piksel putih terhadap luas total *Bounding Box*:
   - Jika rasio $\ge 0.50$ (Blok solid/padat) $\rightarrow$ Diklasifikasikan sebagai **Mobil** (Kotak Hijau).
   - Jika rasio $< 0.50$ (Bolong/garis tipis) $\rightarrow$ Diklasifikasikan sebagai **Bukan Mobil/Noise** (Kotak Merah).

---

## 📊 Visualisasi Tahapan

*(Catatan: Gambar di bawah ini di-generate otomatis oleh program ke folder `output`)*

![Hasil Deteksi](output/result_atap_kepadatan.png)

1. **Panel 1 (Kiri):** Memperlihatkan hasil *Thresholding* murni. Aspal menghilang menjadi hitam, memisahkan rona refleksi bodi kendaraan secara langsung.
2. **Panel 2 (Tengah):** Citra biner hasil Morfologi. Terdapat kotak debug dan nilai *Extent Ratio* numerik untuk validasi ambang batas akurasi objek.
3. **Panel 3 (Kanan):** Citra asli RGB dengan *bounding box* hasil klasifikasi akhir (Hijau = Mobil Utuh, Merah = Noise/Serpihan).

---

## 🔍 Analisis Sistem

* **Kendala yang Dihadapi (Color Dependency):** Algoritma ini bergantung pada pantulan cahaya objek. Mobil berwarna gelap (hitam, biru tua) memiliki intensitas di bawah 140, sehingga menyatu dengan aspal gelap dan gagal membentuk blok biner.
* **Akurasi:** Sistem memberikan akurasi yang **sangat tinggi** dalam memisahkan dan menghitung kendaraan berwarna terang/putih. Logika *Extent Ratio* terbukti ampuh membuang *false positive* seperti marka jalan tanpa merusak bentuk asli mobil.
* **Potensi Peningkatan:** Untuk dapat mendeteksi mobil gelap, sistem perlu ditingkatkan menggunakan *Adaptive Thresholding* atau menganalisis bayangan kolong mobil (*under-vehicle shadow detection*).

---

## 🚀 Cara Menjalankan Program

### Struktur Folder Dasar
Pastikan direktori Anda memiliki struktur seperti berikut sebelum menjalankan program:
```text
├── [nama_file_kode].py
├── input/
│   └── parking.jpg                # File citra asli
└── output/                        # Folder otomatis terbuat jika belum ada
    └── result_atap_kepadatan.png  # Hasil output gambar
