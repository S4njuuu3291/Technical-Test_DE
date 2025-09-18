import locale
locale.setlocale(locale.LC_TIME, "id_ID.utf8")

from util import backtrack_crawlscrape

if __name__ == "__main__":
    backtrack_crawlscrape("15-09-2025","17-09-2025",path="data/backtrack_article.json")
    
# MENGAMBIL ARTIKEL TANGGAL 15 SAMPAI TANGGAL 17