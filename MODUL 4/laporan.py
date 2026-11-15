
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView

import db_helper


class LaporanWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(LaporanWindow, self).__init__()
        uic.loadUi('laporan.ui', self)

        self.btnKembali.clicked.connect(self.close)

        self.tableBukuPopuler.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.tableBukuPopuler.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )

        self.load_laporan()

    def load_laporan(self):
        # Mengambil statistik umum
        statistik = db_helper.get_general_statistics()

        self.lblAngkaTotalBuku.setText(
            str(statistik['total_buku'])
        )

        self.lblAngkaPeminjamanAktif.setText(
            str(statistik['active_loans'])
        )

        # Mengambil jumlah seluruh peminjaman dan pengembalian
        conn = db_helper.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM peminjaman")
        total_peminjaman = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM pengembalian")
        total_pengembalian = cursor.fetchone()[0]

        conn.close()

        self.lblAngkaTotalPeminjaman.setText(
            str(total_peminjaman)
        )

        self.lblAngkaTotalPengembalian.setText(
            str(total_pengembalian)
        )

        # Mengambil daftar buku paling sering dipinjam
        data_buku = db_helper.get_most_borrowed_books()

        self.tableBukuPopuler.setRowCount(0)

        for data in data_buku:
            id_buku, judul, pengarang, jumlah = data

            row = self.tableBukuPopuler.rowCount()
            self.tableBukuPopuler.insertRow(row)

            isi = [
                id_buku,
                judul,
                jumlah
            ]

            for kolom, nilai in enumerate(isi):
                self.tableBukuPopuler.setItem(
                    row,
                    kolom,
                    QTableWidgetItem(str(nilai))
                )


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = LaporanWindow()
    window.show()
    sys.exit(app.exec_())
