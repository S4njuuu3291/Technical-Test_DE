# 📰 Bisnis.com Crawler & Scraper

## Deskripsi

Proyek ini merupakan implementasi **crawler & scraper** untuk situs [Bisnis.com](https://www.bisnis.com) sebagai bagian dari Technical Test DE.
Crawler dibangun dengan Python menggunakan library `requests`, `lxml`, dan `schedule`.

Crawler memiliki **dua mode operasi**:

1. **Backtrack Mode**

   - Mengambil artikel dari rentang tanggal tertentu.
   - Input: `start_date`, `end_date` dalam format `DD-MM-YYYY`.
   - Output: file JSON berisi semua artikel dalam periode tersebut.

2. **Standard Mode**

   - Long-running process (pakai scheduler).
   - Mengecek artikel terbaru setiap interval menit.
   - Artikel baru akan **ditambahkan (append)** ke JSON tanpa overwrite.

## Arsitektur

- **`util.py`**:

  - `get_article_link(url)` → Ambil semua link artikel dari halaman indeks bisnis.com.
  - `scrape_article(url)` → Ambil detail artikel (link, judul, tanggal, isi).
  - `backtrack_crawlscrape(start_date, end_date, path)` → Crawl rentang tanggal.
  - `standard_crawlscrape(path)` → Crawl artikel terbaru, append JSON.
  - `run_standard(interval)` → Jalankan scheduler untuk mode Standard.

- **`backtrack.py`**
  Wrapper untuk menjalankan `backtrack_crawlscrape`.

- **`standard.py`**
  Wrapper untuk menjalankan `run_standard`.

## Deliverables

- Repository dengan kode dan dokumentasi.
- Contoh output:

  - `data/backtrack_artikel.json`
  - `data/new_article.json`

- Video demo eksekusi:

  - `demo/BACKTRACK.mp4`
  - `demo/STANDARD.mp4`

## Struktur Repo

```
technical-test-de/
│── backtrack.py          # Entrypoint mode Backtrack
│── standard.py           # Entrypoint mode Standard
│── util.py               # Fungsi core (scraping, parsing, save JSON)
│── requirements.txt      # Daftar dependency
│── README.md             # Dokumentasi
│── data/
│   ├── backtrack_artikel.json
│   └── new_article.json
│── demo/
│   ├── BACKTRACK.mp4
│   └── STANDARD.mp4
```

## Instalasi

1. Clone repo:

   ```bash
   git clone https://github.com/username/technical-test-de.git
   cd technical-test-de
   ```

2. Install dependency:

   ```bash
   pip install -r requirements.txt
   ```

## Cara Menjalankan

### 1. Backtrack Mode

Ambil artikel dalam periode tertentu.

```bash
python backtrack.py
```

Output tersimpan di `data/backtrack_artikel.json`.

### 2. Standard Mode

Scrape artikel terbaru setiap `interval` menit.

```bash
python standard.py
```

- Default interval = 10 menit.
- Output disimpan di `data/new_article.json`.
- Jika file sudah ada, artikel baru akan di-_append_.
- Proses berjalan terus sampai dihentikan manual (`CTRL+C`).

## Format Output JSON

```json
[
  {
    "Link": "https://ekonomi.bisnis.com/read/20250912/45/1910887/...",
    "Judul": "PT KCN Kaji Kompensasi Nelayan Terdampak Tanggul Beton Cilincing",
    "Tanggal": "2025-09-12T23:52:00",
    "Isi": "Bisnis.com , JAKARTA — PT Karya Citra Nusantara ..."
  }
]
```

## Dependency

- Python ≥ 3.9
- requests
- lxml
- schedule

Install via:

```bash
pip install -r requirements.txt
```
