
import sys
from PyQt5 import QtWidgets, uic

import db_helper
from kelola_buku import KelolaBukuWindow
from pinjam_buku import PinjamBukuWindow
from kembali_buku import KembaliBukuWindow
from laporan import LaporanWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('main.ui', self)

        db_helper.init_db()

        # Koneksi tombol menu
        self.btnKelolaBuku.clicked.connect(self.open_kelola_buku)
        self.btnPinjamBuku.clicked.connect(self.open_pinjam_buku)
        self.btnKembaliBuku.clicked.connect(self.open_kembali_buku)
        self.btnLaporan.clicked.connect(self.open_laporan)
        self.btnKeluar.clicked.connect(self.close)

        # Menyiapkan jendela
        self.kelola_buku_win = None
        self.pinjam_buku_win = None
        self.kembali_buku_win = None
        self.laporan_win = None

    def open_kelola_buku(self):
        if self.kelola_buku_win is None:
            self.kelola_buku_win = KelolaBukuWindow()
        else:
            self.kelola_buku_win.load_books()

        self.kelola_buku_win.show()
        self.kelola_buku_win.raise_()
        self.kelola_buku_win.activateWindow()

    def open_pinjam_buku(self):
        self.pinjam_buku_win = PinjamBukuWindow()
        self.pinjam_buku_win.show()

    def open_kembali_buku(self):
        self.kembali_buku_win = KembaliBukuWindow()
        self.kembali_buku_win.show()

    def open_laporan(self):
        self.laporan_win = LaporanWindow()
        self.laporan_win.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
