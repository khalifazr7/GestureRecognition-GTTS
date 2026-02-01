# 🖐️ AI Gesture Recognition & Voice Assistant

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand%20Tracking-orange)
![License](https://img.shields.io/badge/License-MIT-purple)

Sistem cerdas pengenalan gesture tangan real-time yang terintegrasi dengan Text-to-Speech (TTS). Aplikasi ini dapat "melihat" gerakan tangan Anda dan menerjemahkannya menjadi ucapan suara secara instan.

Cocok untuk proyek **Human-Computer Interaction**, alat bantu komunikasi disabilitas (sign language to speech), atau sekadar demo AI yang interaktif.

---

## ✨ Fitur Utama

- **🚀 Real-time Low Latency**: Deteksi cepat dan akurat menggunakan MediaPipe.
- **🗣️ Smart Text-to-Speech**: Menggunakan Google TTS dengan caching dan threading agar video tidak lag saat berbicara.
- **🎨 Modern UI Overlay**: Tampilan futuristik dengan FPS counter, status indikator, dan visualisasi landmark tangan.
- **🛠️ Modular Codebase**: Kode terstruktur rapi (Clean Architecture) mudah dikembangkan ulang.
- **⚙️ Customizable**: Konfigurasi mudah lewat `config.py` (ganti bahasa, timer, resolusi, dll).

## 👐 Daftar Gesture

Aplikasi ini mengenali berbagai gesture tangan berikut:

| Icon | Gesture                   | Perintah / Ucapan                               |
| :--: | :------------------------ | :---------------------------------------------- |
|  ☝️  | **Halo** (Telunjuk)       | "Halo! Senang bertemu denganmu."                |
|  ✌️  | **Perkenalan** (Peace)    | "Perkenalkan, saya adalah Khalifa Ziaul Rahim." |
|  🖐️  | **Terima Kasih** (5 Jari) | "Terimakasih banyak! Sampai jumpa lagi."        |
|  👍  | **Baik** (Jempol)         | "Baik, saya mengerti. Siap dilaksanakan!"       |
|  👎  | **Tidak**                 | "Maaf, saya tidak setuju."                      |
|  ✊  | **Semangat** (Kepal)      | "Tetap semangat! Kamu pasti bisa!"              |
|  👌  | **OK**                    | "Oke sip! Semuanya aman."                       |
|  🤟  | **Love** (Rock)           | "I love you! Sayang kamu."                      |

> **Catatan:** Anda bisa menambah atau mengubah kata-kata di file `config.py`.

---

## ⚙️ Cara Instalasi

Pastikan Anda sudah menginstall Python 3.10 ke atas.

1. **Clone Repository**

   ```bash
   git clone https://github.com/khalifazr7/GestureRecognition-GTTS.git
   cd GestureRecognition-GTTS
   ```

2. **Buat Virtual Environment (Recommended)**

   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Cara Menjalankan

Cukup jalankan file utama:

```bash
python gesture_speech.py
```

- Arahkan tangan ke webcam 📷.
- Coba lakukan gesture (misal: angkat jempol 👍).
- Sistem akan berbicara! 🔊
- Tekan **'q'** untuk keluar.

---

## 📁 Struktur Project

```
├── gesture_speech.py  # Main entry point
├── config.py          # Pengaturan (Warna, Teks, App Config)
├── gestures.py        # Logic deteksi gesture & smoothing
├── ui_overlay.py      # Rendering tampilan UI yang cantik
├── speech.py          # Engine Text-to-Speech (Multithreaded)
├── requirements.txt   # Daftar library
└── README.md          # Dokumentasi ini
```

## 🤝 Kontribusi

Tertarik mengembangkan fitur baru? Pull requests sangat diterima!

1. Fork repo ini
2. Buat branch fitur (`git checkout -b fitur-keren`)
3. Commit perubahan (`git commit -m 'Tambah fitur keren'`)
4. Push ke branch (`git push origin fitur-keren`)
5. Open Pull Request

---

**Created by Khalifa Ziaul Rahim**
