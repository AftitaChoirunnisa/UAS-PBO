import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import csv

# ======================================================
# CLASS BUKU (Parent Class)
class Buku:
    def __init__(self, judul, penulis, tahun):
        self.__judul = judul
        self.__penulis = penulis
        self.__tahun = tahun
        self.__status = "Tersedia"

    def pinjam(self):
        if self.__status == "Tersedia":
            self.__status = "Dipinjam"
            return True
        return False

    def kembalikan(self):
        self.__status = "Tersedia"

    def is_dipinjam(self):
        return self.__status == "Dipinjam"

    def getInfo(self):
        return f"{self.__judul} - {self.__penulis} ({self.__tahun})"
    
    def get_judul(self):
        return self.__judul
    
    def get_penulis(self):
        return self.__penulis
    
    def get_tahun(self):
        return self.__tahun

# ======================================================
# CLASS BUKU FIKSI (Child Class dari Buku)
class BukuFiksi(Buku):
    def __init__(self, judul, penulis, tahun, genre):
        super().__init__(judul, penulis, tahun)
        self.__genre = genre

    def getInfo(self):
        return super().getInfo() + f" | Genre: {self.__genre}"
    
    def get_genre(self):
        return self.__genre

# ======================================================
# CLASS BUKU NON FIKSI (Child Class dari Buku)
class BukuNonFiksi(Buku):
    def __init__(self, judul, penulis, tahun, bidang):
        super().__init__(judul, penulis, tahun)
        self.__bidang = bidang

    def getInfo(self):
        return super().getInfo() + f" | Bidang: {self.__bidang}"
    
    def get_bidang(self):
        return self.__bidang

# ======================================================
# CLASS ANGGOTA
class Anggota:
    def __init__(self, nama, nim, tanggal):
        self.nama = nama
        self.nim = nim
        self.tanggal = tanggal

# ======================================================
# CLASS PEMINJAMAN
class Peminjaman:
    def __init__(self, anggota):
        self.anggota = anggota
        self.__buku_dipinjam = []

    def pinjam_buku(self, buku):
        if buku.pinjam():
            self.__buku_dipinjam.append(buku)
            return True
        return False

    def kembalikan_buku(self, buku):
        if buku in self.__buku_dipinjam:
            buku.kembalikan()
            self.__buku_dipinjam.remove(buku)
            return True
        return False

    @property
    def buku_dipinjam(self):
        return self.__buku_dipinjam

# ======================================================
# CLASS PERPUSTAKAAN
class Perpustakaan:
    def __init__(self):
        self.buku = []

    def tambah_buku(self, buku):
        self.buku.append(buku)

    def ekspor_csv(self, peminjaman):
        if not peminjaman or not peminjaman.buku_dipinjam:
            messagebox.showerror("Error", "Tidak ada data peminjaman")
            return

        with open("laporan_peminjaman.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Nama", peminjaman.anggota.nama])
            writer.writerow(["NIM", peminjaman.anggota.nim])
            writer.writerow(["Tanggal Peminjaman", peminjaman.anggota.tanggal])
            writer.writerow([])
            writer.writerow(["Daftar Buku Dipinjam"])
            writer.writerow(["No", "Judul Buku"])
            for i, buku in enumerate(peminjaman.buku_dipinjam, start=1):
                writer.writerow([i, buku.getInfo()])

        messagebox.showinfo("Sukses", "Data berhasil diekspor ke laporan_peminjaman.csv")

# ======================================================
# DATA AWAL
perpus = Perpustakaan()
data_peminjaman = None

perpus.tambah_buku(BukuFiksi("Dilan: Dia adalah Dilanku Tahun 1990", "Pidi Baiq", 2014, "Fiksi, Romantis"))
perpus.tambah_buku(BukuFiksi("Ayat-Ayat Cinta", "Habiburrahman El Shirazy", 2004, "Fiksi, Romantis"))
perpus.tambah_buku(BukuFiksi("Mariposa", "Luluk HF", 2018, "Fiksi, Remaja"))
perpus.tambah_buku(BukuFiksi("Bumi", "Tere Liye", 2014, "Fiksi, Fantasi"))
perpus.tambah_buku(BukuNonFiksi("Atomic Habits", "James Clear", 2018, "Pengembangan Diri"))
perpus.tambah_buku(BukuNonFiksi("The Psychology of Money", "Morgan Housel", 2020, "Keuangan, Pengembangan Diri"))
perpus.tambah_buku(BukuNonFiksi("Kimchi Confessions", "Xaviera Putri", 2023, "Memoar, Pengalaman Hidup"))
perpus.tambah_buku(BukuNonFiksi("The 7 Habits of Highly Effective People", "Stephen R. Covey", 1989, "Pengembangan Diri, Motivasi"))

# ======================================================
# GUI
root = tk.Tk()
root.title("Perpustakaan Digital")
root.geometry("1000x700")
root.configure(bg="#84B1C4")

filter_var = tk.StringVar(value="Semua")

# Frame untuk layout
main_frame = tk.Frame(root, bg="#84B1C4")
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Header
tk.Label(main_frame, text="📚 Sistem Informasi Peminjaman Buku Digital",
         font=("Helvetica", 18, "bold"),
         bg="#84B1C4", fg="white").pack(pady=10)

# Form input
form = tk.Frame(main_frame, bg="#CCD7DC", padx=20, pady=15)
form.pack(fill="x", padx=20, pady=10)

tk.Label(form, text="Nama:", bg="#CCD7DC", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=8)
entry_nama = tk.Entry(form, width=35, font=("Arial", 10), relief="flat", bg="white")
entry_nama.grid(row=0, column=1, sticky="ew", padx=(10, 0))

tk.Label(form, text="NIM:", bg="#CCD7DC", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", pady=8)
entry_nim = tk.Entry(form, width=35, font=("Arial", 10), relief="flat", bg="white")
entry_nim.grid(row=1, column=1, sticky="ew", padx=(10, 0))

tk.Label(form, text="Tanggal Pinjam:", bg="#CCD7DC", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", pady=8)
entry_tanggal = tk.Entry(form, width=35, font=("Arial", 10), relief="flat", bg="white")
entry_tanggal.grid(row=2, column=1, sticky="ew", padx=(10, 0))

form.columnconfigure(1, weight=1)

# ======================================================
# Filter Kategori
filter_frame = tk.Frame(main_frame, bg="#CCD7DC", padx=20, pady=10)
filter_frame.pack(fill="x", padx=20)

tk.Label(filter_frame, text="Filter Kategori:", bg="#CCD7DC", font=("Arial", 10, "bold")).pack(side="left", padx=(0, 15))

tk.Button(filter_frame, text="Semua", bg="#2196F3", fg="white", width=15, font=("Arial", 10, "bold"), relief="raised", bd=2,
          command=lambda: set_filter("Semua")).pack(side="left", padx=5)
tk.Button(filter_frame, text="Fiksi", bg="#4CAF50", fg="white", width=15, font=("Arial", 10, "bold"), relief="raised", bd=2,
          command=lambda: set_filter("Fiksi")).pack(side="left", padx=5)
tk.Button(filter_frame, text="Non-Fiksi", bg="#FF9800", fg="white", width=15, font=("Arial", 10, "bold"), relief="raised", bd=2,
          command=lambda: set_filter("Non-Fiksi")).pack(side="left", padx=5)

# Daftar Buku Tersedia dan Dipinjam
list_frame = tk.Frame(main_frame, bg="#D4D5D6", padx=10, pady=10)
list_frame.pack(fill="both", expand=True, padx=20, pady=10)

# Frame kiri: Buku Tersedia
tersedia_frame = tk.Frame(list_frame, bg="#D4D5D6")
tersedia_frame.pack(side="left", fill="both", expand=True, padx=5)

tk.Label(tersedia_frame, text="📗 Buku Tersedia", bg="#D4D5D6", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=(0, 5))

tree_frame_tersedia = tk.Frame(tersedia_frame, bg="#D4D5D6")
tree_frame_tersedia.pack(fill="both", expand=True)

tree_tersedia = ttk.Treeview(tree_frame_tersedia, columns=("Judul", "Penulis", "Tahun", "Genre/Bidang"), height=10, show="tree headings")
tree_tersedia.heading("#0", text="No")
tree_tersedia.heading("Judul", text="Judul")
tree_tersedia.heading("Penulis", text="Penulis")
tree_tersedia.heading("Tahun", text="Tahun")
tree_tersedia.heading("Genre/Bidang", text="Genre/Bidang")

tree_tersedia.column("#0", width=35, anchor="center")
tree_tersedia.column("Judul", width=200, anchor="w")
tree_tersedia.column("Penulis", width=150, anchor="w")
tree_tersedia.column("Tahun", width=60, anchor="center")
tree_tersedia.column("Genre/Bidang", width=150, anchor="w")

tree_tersedia.pack(side="left", fill="both", expand=True)

# Frame kanan: Buku Dipinjam
dipinjam_frame = tk.Frame(list_frame, bg="#D4D5D6")
dipinjam_frame.pack(side="right", fill="both", expand=True, padx=5)

tk.Label(dipinjam_frame, text="📕 Buku Dipinjam", bg="#D4D5D6", font=("Helvetica", 12, "bold")).pack(anchor="w", pady=(0, 5))

tree_frame_dipinjam = tk.Frame(dipinjam_frame, bg="#D4D5D6")
tree_frame_dipinjam.pack(fill="both", expand=True)

tree_dipinjam = ttk.Treeview(tree_frame_dipinjam, columns=("Nama", "Judul", "Tanggal Pinjam", "Status"), height=10, show="tree headings")
tree_dipinjam.heading("#0", text="No")
tree_dipinjam.heading("Nama", text="Nama (NIM)")
tree_dipinjam.heading("Judul", text="Judul Buku")
tree_dipinjam.heading("Tanggal Pinjam", text="Tanggal Pinjam")
tree_dipinjam.heading("Status", text="Status")

tree_dipinjam.column("#0", width=35, anchor="center")
tree_dipinjam.column("Nama", width=150, anchor="w")
tree_dipinjam.column("Judul", width=200, anchor="w")
tree_dipinjam.column("Tanggal Pinjam", width=120, anchor="center")
tree_dipinjam.column("Status", width=100, anchor="center")

tree_dipinjam.pack(side="left", fill="both", expand=True)

# ======================================================
# FUNGSI UTAMA
def refresh():
    """Refresh list buku tersedia & dipinjam sesuai filter"""
    for item in tree_tersedia.get_children():
        tree_tersedia.delete(item)
    
    for item in tree_dipinjam.get_children():
        tree_dipinjam.delete(item)
    
    kategori_filter = filter_var.get()

    for b in perpus.buku:
        if b.is_dipinjam():
            continue
        if kategori_filter == "Fiksi" and not isinstance(b, BukuFiksi):
            continue
        if kategori_filter == "Non-Fiksi" and not isinstance(b, BukuNonFiksi):
            continue
        
        genre_bidang = ""
        if isinstance(b, BukuFiksi):
            genre_bidang = b.get_genre()
        elif isinstance(b, BukuNonFiksi):
            genre_bidang = b.get_bidang()
        
        tree_tersedia.insert("", "end", values=(b.get_judul(), b.get_penulis(), b.get_tahun(), genre_bidang))

    if data_peminjaman:
        for b in data_peminjaman.buku_dipinjam:
            tree_dipinjam.insert("", "end", values=(data_peminjaman.anggota.nama, b.get_judul(), data_peminjaman.anggota.tanggal, "Dipinjam"))

def pinjam():
    """Fungsi untuk meminjam buku"""
    global data_peminjaman
    if not entry_nama.get() or not entry_nim.get() or not entry_tanggal.get():
        messagebox.showerror("Error", "Lengkapi identitas terlebih dahulu")
        return

    if data_peminjaman is None:
        anggota = Anggota(entry_nama.get(), entry_nim.get(), entry_tanggal.get())
        data_peminjaman = Peminjaman(anggota)

    try:
        selected = tree_tersedia.selection()
        if not selected:
            messagebox.showerror("Error", "Pilih buku tersedia")
            return
        
        item = selected[0]
        values = tree_tersedia.item(item)['values']
        judul_dipilih = values[0]
        
        buku = None
        for b in perpus.buku:
            if not b.is_dipinjam() and b.get_judul() == judul_dipilih:
                buku = b
                break
        
        if buku and data_peminjaman.pinjam_buku(buku):
            refresh()
            messagebox.showinfo("Sukses", "Buku berhasil dipinjam")
        else:
            messagebox.showerror("Error", "Gagal meminjam buku")
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

def kembalikan():
    """Fungsi untuk mengembalikan buku"""
    try:
        selected = tree_dipinjam.selection()
        if not selected:
            messagebox.showerror("Error", "Pilih buku dipinjam")
            return
        
        item = selected[0]
        values = tree_dipinjam.item(item)['values']
        judul_dikembalikan = values[1]
        
        buku = None
        for b in perpus.buku:
            if b.is_dipinjam() and b.get_judul() == judul_dikembalikan:
                buku = b
                break
        
        if buku and data_peminjaman.kembalikan_buku(buku):
            refresh()
            messagebox.showinfo("Sukses", "Buku berhasil dikembalikan")
        else:
            messagebox.showerror("Error", "Gagal mengembalikan buku")
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

def set_filter(kategori):
    """Set kategori filter & refresh list"""
    filter_var.set(kategori)
    refresh()

# Tombol Aksi
btn_frame = tk.Frame(main_frame, bg="#84B1C4", pady=10)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="📥 Pinjam Buku", width=18, bg="#4CAF50", fg="white", command=pinjam).pack(side="left", padx=10)
tk.Button(btn_frame, text="📤 Kembalikan Buku", width=18, bg="#F44336", fg="white", command=kembalikan).pack(side="left", padx=10)
tk.Button(btn_frame, text="📄 Ekspor CSV", width=18, bg="#FF9800", fg="white", command=lambda: perpus.ekspor_csv(data_peminjaman)).pack(side="left", padx=10)

# Inisialisasi aplikasi
refresh()
root.mainloop()
