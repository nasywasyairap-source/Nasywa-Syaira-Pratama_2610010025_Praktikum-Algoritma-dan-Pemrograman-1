
import sqlite3
import os

DB_NAME = 'perpustakaan.db'


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Create Table Buku
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS buku (
            id_buku TEXT PRIMARY KEY,
            judul TEXT NOT NULL,
            pengarang TEXT NOT NULL,
            penerbit TEXT NOT NULL,
            tahun INTEGER NOT NULL,
            stok INTEGER NOT NULL
        )
    ''')

    # Create Table Peminjaman
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS peminjaman (
            id_pinjam TEXT PRIMARY KEY,
            nama_peminjam TEXT NOT NULL,
            id_buku TEXT NOT NULL,
            tanggal_pinjam TEXT NOT NULL,
            durasi INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'Dipinjam',
            FOREIGN KEY (id_buku) REFERENCES buku(id_buku)
        )
    ''')

    # Create Table Pengembalian
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pengembalian (
            id_kembali INTEGER PRIMARY KEY AUTOINCREMENT,
            id_pinjam TEXT NOT NULL,
            tanggal_kembali TEXT NOT NULL,
            denda REAL NOT NULL,
            FOREIGN KEY (id_pinjam) REFERENCES peminjaman(id_pinjam)
        )
    ''')

    # Insert Dummy Books if empty
    cursor.execute("SELECT COUNT(*) FROM buku")

    if cursor.fetchone()[0] == 0:
        dummy_books = [
            ("B001", "Algoritma & Struktur Data", "Rinaldi Munir", "Informatika", 2020, 5),
            ("B002", "Python untuk Pemula", "Jubilee Enterprise", "Elex Media", 2021, 3),
            ("B003", "Pemrograman GUI dengan Python dan PyQt", "Budi Raharjo", "Informatika", 2019, 2),
            ("B004", "Dasar-Dasar Rekayasa Perangkat Lunak", "Rosa A.S.", "Modula", 2018, 4),
        ]

        cursor.executemany(
            "INSERT INTO buku VALUES (?, ?, ?, ?, ?, ?)",
            dummy_books
        )

    conn.commit()
    conn.close()


# --- Book CRUD Operations ---

def get_all_books():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM buku")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_book_by_id(id_buku):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM buku WHERE id_buku = ?", (id_buku,))
    row = cursor.fetchone()
    conn.close()
    return row


def add_book(id_buku, judul, pengarang, penerbit, tahun, stok):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """INSERT INTO buku
            (id_buku, judul, pengarang, penerbit, tahun, stok)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (id_buku, judul, pengarang, penerbit, tahun, stok)
        )
        conn.commit()
        return True, "Buku berhasil ditambahkan!"

    except sqlite3.IntegrityError:
        return False, "Gagal menambahkan: ID Buku sudah terdaftar."

    except Exception as e:
        return False, str(e)

    finally:
        conn.close()


def update_book(id_buku, judul, pengarang, penerbit, tahun, stok):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """UPDATE buku
            SET judul=?, pengarang=?, penerbit=?, tahun=?, stok=?
            WHERE id_buku=?""",
            (judul, pengarang, penerbit, tahun, stok, id_buku)
        )
        conn.commit()

        if cursor.rowcount > 0:
            return True, "Buku berhasil diperbarui!"
        else:
            return False, "Gagal memperbarui: ID Buku tidak ditemukan."

    except Exception as e:
        return False, str(e)

    finally:
        conn.close()


def delete_book(id_buku):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM buku WHERE id_buku=?", (id_buku,))
        conn.commit()

        if cursor.rowcount > 0:
            return True, "Buku berhasil dihapus!"
        else:
            return False, "Gagal menghapus: ID Buku tidak ditemukan."

    except sqlite3.IntegrityError:
        return False, "Gagal menghapus: Buku sedang dipinjam atau terikat transaksi lain."

    except Exception as e:
        return False, str(e)

    finally:
        conn.close()


# --- Loan Transactions ---

def get_active_loans():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT p.id_pinjam, p.nama_peminjam, p.id_buku,
               b.judul, p.tanggal_pinjam, p.durasi, p.status
        FROM peminjaman p
        JOIN buku b ON p.id_buku = b.id_buku
        WHERE p.status = 'Dipinjam'
    ''')

    rows = cursor.fetchall()
    conn.close()
    return rows


def get_loan_by_id(id_pinjam):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT p.id_pinjam, p.nama_peminjam, p.id_buku,
               b.judul, p.tanggal_pinjam, p.durasi, p.status
        FROM peminjaman p
        JOIN buku b ON p.id_buku = b.id_buku
        WHERE p.id_pinjam = ?
    ''', (id_pinjam,))

    row = cursor.fetchone()
    conn.close()
    return row


def add_loan(id_pinjam, nama_peminjam, id_buku, tanggal_pinjam, durasi):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT stok FROM buku WHERE id_buku = ?",
            (id_buku,)
        )
        book = cursor.fetchone()

        if not book:
            return False, "Buku tidak ditemukan."

        if book[0] <= 0:
            return False, "Stok buku habis."

        cursor.execute('''
            INSERT INTO peminjaman
            (id_pinjam, nama_peminjam, id_buku, tanggal_pinjam, durasi)
            VALUES (?, ?, ?, ?, ?)
        ''', (id_pinjam, nama_peminjam, id_buku, tanggal_pinjam, durasi))

        cursor.execute(
            "UPDATE buku SET stok = stok - 1 WHERE id_buku = ?",
            (id_buku,)
        )

        conn.commit()
        return True, "Peminjaman buku berhasil!"

    except sqlite3.IntegrityError:
        return False, "ID Peminjaman sudah terdaftar atau data tidak valid."

    except Exception as e:
        return False, str(e)

    finally:
        conn.close()


def return_book(id_pinjam, tanggal_kembali, denda):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id_buku, status FROM peminjaman WHERE id_pinjam = ?",
            (id_pinjam,)
        )
        loan = cursor.fetchone()

        if not loan:
            return False, "Data peminjaman tidak ditemukan."

        id_buku, status = loan

        if status == 'Kembali':
            return False, "Buku dari peminjaman ini sudah pernah dikembalikan."

        cursor.execute(
            """INSERT INTO pengembalian
            (id_pinjam, tanggal_kembali, denda)
            VALUES (?, ?, ?)""",
            (id_pinjam, tanggal_kembali, denda)
        )

        cursor.execute(
            "UPDATE peminjaman SET status = 'Kembali' WHERE id_pinjam = ?",
            (id_pinjam,)
        )

        cursor.execute(
            "UPDATE buku SET stok = stok + 1 WHERE id_buku = ?",
            (id_buku,)
        )

        conn.commit()
        return True, "Buku berhasil dikembalikan!"

    except Exception as e:
        conn.rollback()
        return False, str(e)

    finally:
        conn.close()


# --- Statistics & Reports ---

def get_general_statistics():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(stok) +
        (SELECT COUNT(*) FROM peminjaman WHERE status='Dipinjam')
        FROM buku
    """)
    total_buku = cursor.fetchone()[0] or 0

    cursor.execute(
        "SELECT COUNT(*) FROM peminjaman WHERE status = 'Dipinjam'"
    )
    active_loans = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(denda) FROM pengembalian")
    total_denda = cursor.fetchone()[0] or 0.0

    conn.close()

    return {
        'total_buku': total_buku,
        'active_loans': active_loans,
        'total_denda': total_denda
    }


def get_most_borrowed_books():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT b.id_buku, b.judul, b.pengarang,
               COUNT(p.id_pinjam) AS jumlah_dipinjam
        FROM peminjaman p
        JOIN buku b ON p.id_buku = b.id_buku
        GROUP BY b.id_buku
        ORDER BY jumlah_dipinjam DESC
    ''')

    rows = cursor.fetchall()
    conn.close()
    return rows
