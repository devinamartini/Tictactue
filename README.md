# Tic Tac Toe vs Bot

Game **Tic Tac Toe** berbasis GUI (Tkinter) di mana pemain melawan bot yang memakai algoritma **Minimax dengan Alpha-Beta Pruning**. Bot selalu bermain optimal, sehingga **tidak mungkin kalah**: hasil terbaik yang bisa diraih pemain adalah seri.

## Fitur

- Melawan bot dengan kecerdasan Minimax + Alpha-Beta Pruning
- Pilih siapa yang jalan duluan (pemain atau bot), yang jalan duluan memakai **X**
- Papan skor otomatis untuk **Kamu**, **Seri**, dan **Bot**, dengan tombol **Reset Skor**
- Animasi saat tanda X dan O digambar, serta garis penanda kemenangan
- Efek *hover* pada kotak yang bisa dipilih
- Ukuran jendela tetap sehingga tampilan tidak berubah atau bergeser
- Tanpa library tambahan, cukup Python standar

## Tampilan

<table>
  <tr>
    <td align="center"><img src="screenshots/01_pilih_giliran.png" width="260" alt="Pilih siapa yang jalan duluan"><br><sub>Memilih siapa yang jalan duluan</sub></td>
    <td align="center"><img src="screenshots/02_bermain.png" width="260" alt="Sedang bermain"><br><sub>Sedang bermain</sub></td>
  </tr>
  <tr>
    <td align="center"><img src="screenshots/03_seri.png" width="260" alt="Hasil seri"><br><sub>Permainan berakhir seri</sub></td>
    <td align="center"><img src="screenshots/04_bot_menang.png" width="260" alt="Bot menang"><br><sub>Bot menang, ditandai garis kuning</sub></td>
  </tr>
</table>

## Persyaratan

- **Python 3.8 atau lebih baru**
- **Tkinter** (sudah termasuk di instalasi Python untuk Windows dan macOS)

Di Linux, jika muncul error `No module named 'tkinter'`, instal dulu:

```bash
sudo apt install python3-tk
```

## Cara Menjalankan

1. Clone repository ini:

   ```bash
   git clone https://github.com/devinamartini/Tictactue.git
   cd Tictactue
   ```

2. Jalankan program:

   ```bash
   python tictactue_klp4.py
   ```

   Pada beberapa sistem (Linux/macOS), gunakan `python3 tictactue_klp4.py`.

## Cara Bermain

1. Saat game dibuka, pilih siapa yang jalan duluan: **Saya (X)** atau **Bot (X)**.
2. Klik kotak kosong di papan untuk menaruh tanda kamu.
3. Bot akan membalas otomatis setelah giliranmu.
4. Pemain yang berhasil membuat 3 tanda berurutan (horizontal, vertikal, atau diagonal) menang. Jika papan penuh tanpa pemenang, hasilnya seri.
5. Klik **Main Lagi** atau **Game Baru** untuk bermain lagi, dan **Reset Skor** untuk mengosongkan papan skor.

## Cara Kerja Bot

Bot memilih langkah dengan **Minimax**: ia mencoba semua kemungkinan langkah ke depan sampai permainan selesai, lalu memilih langkah dengan skor terbaik bagi dirinya.

| Hasil akhir | Skor |
|---|---|
| Bot menang | `10 - depth` |
| Pemain menang | `depth - 10` |
| Seri | `0` |

- `depth` adalah kedalaman langkah, sehingga bot lebih memilih menang **lebih cepat** dan menunda kekalahan **selama mungkin**.
- **Alpha-Beta Pruning** memangkas cabang pencarian yang pasti tidak akan dipilih, sehingga hasilnya sama dengan Minimax biasa tetapi lebih cepat.
- Jika papan masih kosong dan bot jalan pertama, bot langsung memilih **kotak tengah** (langkah optimal) tanpa perlu menghitung.

## Struktur Repository

```
Tictactue/
├── tictactue_klp4.py      # kode utama (logika bot + GUI)
├── README.md              # dokumentasi ini
└── screenshots/           # gambar untuk bagian Tampilan
    ├── 01_pilih_giliran.png
    ├── 02_bermain.png
    ├── 03_seri.png
    └── 04_bot_menang.png
```

## Struktur Kode

| Bagian | Fungsi |
|---|---|
| `get_winner(board)` | Memeriksa pemenang dan garis kemenangan dari 8 kombinasi `WIN_LINES` |
| `is_full(board)` | Memeriksa apakah papan sudah penuh |
| `minimax(...)` | Menghitung skor suatu kondisi papan dengan Alpha-Beta Pruning |
| `best_move(board, bot, human)` | Memilih langkah terbaik untuk bot |
| `FlatButton` | Tombol datar dengan efek hover |
| `TicTacToeApp` | Kelas utama GUI dan alur permainan |

Papan direpresentasikan sebagai list 9 elemen (`" "`, `"X"`, atau `"O"`) dengan urutan indeks:

```
0 | 1 | 2
---------
3 | 4 | 5
---------
6 | 7 | 8
```

## Troubleshooting

| Masalah | Solusi |
|---|---|
| `ModuleNotFoundError: No module named 'tkinter'` | Instal Tkinter. Di Linux: `sudo apt install python3-tk`. Di Windows/macOS, instal ulang Python dari python.org dan pastikan opsi *tcl/tk* tercentang. |
| `python` tidak dikenali | Coba `python3 tictactue_klp4.py`, atau pastikan Python sudah ditambahkan ke PATH saat instalasi. |
| Jendela tidak muncul / langsung tertutup | Jalankan dari terminal (bukan klik dua kali) supaya pesan error terlihat. |
| Jenis huruf terlihat berbeda di macOS/Linux | Kode memakai font `Segoe UI` (bawaan Windows). Di sistem lain Tkinter memakai font pengganti, sehingga tampilan bisa sedikit berbeda, tetapi game tetap berfungsi normal. |
| Gambar tidak muncul di README GitHub | Pastikan folder `screenshots/` ikut diunggah ke repository dengan nama persis seperti di atas. |

## Pengembangan Selanjutnya

Beberapa ide yang bisa ditambahkan:

- Tingkat kesulitan (mudah, sedang, sulit) dengan membatasi kedalaman Minimax atau menambah langkah acak
- Mode dua pemain (manusia vs manusia)
- Pilihan simbol (X atau O) bagi pemain
- Ukuran papan lebih besar (misalnya 4x4) dengan batas kedalaman pencarian
- Efek suara dan penyimpanan skor ke file

## Teknologi

- Python 3
- Tkinter (GUI dan kanvas)

## Anggota Kelompok

| Nama | NIM |
|---|---|
| _(isi)_ | _(isi)_ |
| _(isi)_ | _(isi)_ |
| _(isi)_ | _(isi)_ |
