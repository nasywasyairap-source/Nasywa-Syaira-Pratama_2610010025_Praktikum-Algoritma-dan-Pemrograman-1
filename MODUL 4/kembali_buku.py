
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QHeaderView

import db_helper


class KembaliBukuWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(KembaliBukuWindow, self).__init__()
        uic.loadUi('kembali_buku.ui', self)

        self.btnKembalikan.clicked.connect(self.kembalikan_buku)
        self.btnBersihkan.clicked.connect(self.bersihkan_form)
        self.btnKembali.clicked.connect(self.close)

        self.dateKembali.setDate(QDate.currentDate())

        self.tablePeminjaman.setColumnCount(6)
        self.tablePeminjaman.setHorizontalHeaderLabels([
            'ID Pinjam',
            'Nama Peminjam',
            'ID Buku',
            'Judul Buku',
            'Tanggal Pinjam',
            'Durasi (Hari)'
        ])

        self.tablePeminjaman.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers
        )
        self.tablePeminjaman.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        self.cmbIdPinjam.currentIndexChanged.connect(
            self.tampilkan_detail
        )

        self.load_peminjaman()

    def load_peminjaman(self):
        self.cmbIdPinjam.clear()
        self.tablePeminjaman.setRowCount(0)

        data_peminjaman = db_helper.get_active_loans()

        for data in data_peminjaman:
            id_pinjam, nama, id_buku, judul, tanggal, durasi, status = data

            self.cmbIdPinjam.addItem(str(id_pinjam), id_pinjam)

            row = self.tablePeminjaman.rowCount()
            self.tablePeminjaman.insertRow(row)

            isi = [
                id_pinjam,
                nama,
                id_buku,
                judul,
                tanggal,
                durasi
            ]

            for kolom, nilai in enumerate(isi):
                self.tablePeminjaman.setItem(
                    row,
                    kolom,
                    QTableWidgetItem(str(nilai))
                )

        if self.cmbIdPinjam.count() > 0:
            self.cmbIdPinjam.setCurrentIndex(0)
            self.tampilkan_detail()
        else:
            self.bersihkan_field()

    def tampilkan_detail(self):
        id_pinjam = self.cmbIdPinjam.currentData()

        if id_pinjam is None:
            self.bersihkan_field()
            return

        data = db_helper.get_loan_by_id(id_pinjam)

        if data:
            self.txtNamaPeminjam.setText(str(data[1]))
            self.txtJudulBuku.setText(str(data[3]))
            self.txtTanggalPinjam.setText(str(data[4]))

    def kembalikan_buku(self):
        id_pinjam = self.cmbIdPinjam.currentData()

        if id_pinjam is None:
            QMessageBox.warning(
                self,
                'Peringatan',
                'Tidak ada peminjaman aktif yang dipilih!'
            )
            return

        tanggal_kembali = self.dateKembali.date().toString(
            'yyyy-MM-dd'
        )

        # Denda sementara 0 karena belum ada aturan denda
        # yang ditentukan di db_helper.py.
        denda = 0

        konfirmasi = QMessageBox.question(
            self,
            'Konfirmasi',
            'Apakah kamu yakin ingin memproses pengembalian buku?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if konfirmasi == QMessageBox.Yes:
            berhasil, pesan = db_helper.return_book(
                id_pinjam,
                tanggal_kembali,
                denda
            )

            if berhasil:
                QMessageBox.information(
                    self,
                    'Berhasil',
                    pesan
                )
                self.bersihkan_form()
                self.load_peminjaman()
            else:
                QMessageBox.warning(
                    self,
                    'Gagal',
                    pesan
                )

    def bersihkan_field(self):
        self.txtNamaPeminjam.clear()
        self.txtJudulBuku.clear()
        self.txtTanggalPinjam.clear()

    def bersihkan_form(self):
        self.cmbIdPinjam.setCurrentIndex(-1)
        self.bersihkan_field()
        self.dateKembali.setDate(QDate.currentDate())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = KembaliBukuWindow()
    window.show()
    sys.exit(app.exec_())
