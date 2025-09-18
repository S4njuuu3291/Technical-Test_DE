import locale
locale.setlocale(locale.LC_TIME, "id_ID.utf8")
from util import run_standard
        
if __name__ == "__main__":
    run_standard(interval=5) # menit

# SETIAP 5 MENIT, MENGAMBIL ARTIKEL TERBARU