import requests
from lxml import html
import json
from datetime import datetime, timedelta
import schedule
import time
import os

# Header default agar request tidak ditolak (simulasi browser)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/122.0.0.0 Safari/537.36"
}

def get_article_link(url):
    """
    Ambil semua link artikel dari halaman indeks Bisnis.com.
    
    Args:
        url (str): URL halaman indeks (dengan parameter date/page).
    Returns:
        list[str]: Daftar link artikel yang ditemukan.
    """
    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()
    page_content = html.fromstring(response.text)
    return page_content.xpath(
        "//div[@class='artItem']//div[@class='artContent']/a[@class='artLink']/@href"
    )

def scrape_article(url):
    """
    Ambil detail artikel (judul, tanggal, isi) dari link artikel Bisnis.com.

    Args:
        url (str): URL artikel detail.
    Returns:
        dict: Data artikel berisi {Link, Judul, Tanggal, Isi}.
    """
    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()
    page_content = html.fromstring(response.text)
    link = url

    # Judul
    title = page_content.xpath("//div[contains(@class,'detailsTitle')]/h1//text()")
    title = title[0].strip() if title else None

    # Tanggal (coba beberapa variasi format tanggal)
    date = None
    candidate = None
    date_raw = page_content.xpath("//div[@class='detailsAttributeDates']/text()")
    if date_raw:
        candidate = date_raw[0].strip()
    else:
        date_alt = page_content.xpath("//span[@class='detailsAttributeItem']//text()")
        if date_alt:
            candidate = date_alt[-1].strip()
        else:
            date_alt = page_content.xpath("//p[contains(@class,'authorTime')]/text()")
            if date_alt:
                candidate = date_alt[-1].strip()
            else:
                date_alt = page_content.xpath("//div[contains(@class,'detailsAttribute')]/span[2]//text()")
                candidate = date_alt[-1].strip() if date_alt else None

    if candidate:
        for fmt in [
            "%A, %d %B %Y | %H:%M",
            "%A, %d %B %Y | %H:%M WIB",
            "%A, %d %B %Y - %H:%M"
        ]:
            try:
                date = datetime.strptime(candidate, fmt).isoformat()
                break
            except ValueError:
                continue
        if not date:
            print(f"[WARNING] Format tanggal tidak dikenali: {candidate} ({url})")
            date = candidate

    # Isi artikel
    full_text = page_content.xpath("//article[contains(@class,'detailsContent')]//p//text()")
    content = " ".join(p.strip() for p in full_text)

    return {"Link": link, "Judul": title, "Tanggal": date, "Isi": content}

def backtrack_crawlscrape(start_date, end_date, path):
    """
    Crawling mode 'Backtrack': ambil artikel dalam rentang tanggal tertentu.

    Args:
        start_date (str): Tanggal awal format DD-MM-YYYY.
        end_date (str): Tanggal akhir format DD-MM-YYYY.
        path (str): Lokasi file output JSON.
    Returns:
        list[dict]: Data artikel yang berhasil di-scrape.
    """
    articles_data = []
    start_date = datetime.strptime(start_date, "%d-%m-%Y")
    end_date = datetime.strptime(end_date, "%d-%m-%Y")
    current = start_date

    articles_link = []
    while current <= end_date:
        url = f"https://www.bisnis.com/index?date={current}"
        print("Crawling:", url)
        articles_link.extend(get_article_link(url))
        current += timedelta(days=1)

    # Hilangkan duplikat
    articles_link = list(dict.fromkeys(articles_link))

    for link in articles_link:
        print("Link:", link)
        article = scrape_article(link)
        if article:
            articles_data.append(article)

    # Simpan ke file JSON
    with open(path, "w", encoding="utf-8") as f:
        json.dump(articles_data, f, ensure_ascii=False, indent=2)

    return articles_data

def standard_crawlscrape(path="data/new_article.json"):
    """
    Crawling mode 'Standard': cek artikel terbaru setiap eksekusi.
    Artikel baru akan di-append ke file JSON (tidak overwrite).

    Args:
        path (str): Lokasi file output JSON.
    """
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    existing_link = {a.get("Link") for a in data if "Link" in a}
    now_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    print(now_date)
    url = f"https://www.bisnis.com/index?date={now_date}"

    count = 0
    links = get_article_link(url)
    for link in links:
        if link not in existing_link:
            print("Artikel baru:", link)
            article = scrape_article(link)
            time.sleep(0.01)  # jeda kecil untuk menghindari spam request
            data.append(article)
            existing_link.add(link)
            count += 1
    if count == 0:
        print("--Tidak ada artikel terbaru--")

    # Simpan hasil update ke file JSON
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def run_standard(interval=10):
    """
    Jalankan standard_crawlscrape sebagai job terjadwal.
    
    Args:
        interval (int): Interval scraping dalam menit.
    """
    def job():
        print("Scrape artikel terbaru")
        standard_crawlscrape()

    schedule.clear()
    schedule.every(interval).minutes.do(job)
    print("Jalankan program...")
    while True:
        schedule.run_pending()
        time.sleep(1)