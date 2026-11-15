
from PyQt5 import QtWidgets, uic
import db_helper


class KelolaBukuWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(KelolaBukuWindow, self).__init__()

        uic.loadUi('kelola_buku.ui', self)

        print("Kelola Buku berhasil dibuka")
        print("Tombol Tambah:", self.btnTambah.objectName())

        # Koneksi tombol menggunakan pressed
        self.btnTambah.pressed.connect(self.add_book)
        self.btnEdit.pressed.connect(self.edit_book)
        self.btnHapus.pressed.connect(self.delete_book)
        self.btnBersihkan.pressed.connect(self.clear_fields)
        self.btnKembali.pressed.connect(self.close)

        # Koneksi tabel
        self.tableBuku.itemSelectionChanged.connect(
            self.on_table_select
        )

        self.tableBuku.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )

        self.load_books()

    def load_books(self):
        self.tableBuku.setRowCount(0)

        books = db_helper.get_all_books()

        for row_number, row_data in enumerate(books):
            self.tableBuku.insertRow(row_number)

            for column_number, data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(data))
                self.tableBuku.setItem(
                    row_number, column_number, item
                )

    def on_table_select(self):
        selected_rows = self.tableBuku.selectionModel().selectedRows()

        if not selected_rows:
            return

        row = selected_rows[0].row()

        self.txtIdBuku.setText(self.tableBuku.item(row, 0).text())
        self.txtJudul.setText(self.tableBuku.item(row, 1).text())
        self.txtPengarang.setText(self.tableBuku.item(row, 2).text())
        self.txtPenerbit.setText(self.tableBuku.item(row, 3).text())
        self.txtTahun.setText(self.tableBuku.item(row, 4).text())
        self.txtStok.setText(self.tableBuku.item(row, 5).text())

        self.txtIdBuku.setReadOnly(True)

    def validate_inputs(self):
        id_buku = self.txtIdBuku.text().strip()
        judul = self.txtJudul.text().strip()
        pengarang = self.txtPengarang.text().strip()
        penerbit = self.txtPenerbit.text().strip()
        tahun = self.txtTahun.text().strip()
        stok = self.txtStok.text().strip()

        if not all([id_buku, judul, pengarang, penerbit, tahun, stok]):
            QtWidgets.QMessageBox.warning(
                self, "Validasi Gagal",
                "Semua kolom harus diisi!"
            )
            return None

        try:
            tahun = int(tahun)
            stok = int(stok)

            if tahun < 0 or stok < 0:
                raise ValueError

        except ValueError:
            QtWidgets.QMessageBox.warning(
                self, "Validasi Gagal",
                "Tahun dan stok harus berupa angka bulat positif!"
            )
            return None

        return id_buku, judul, pengarang, penerbit, tahun, stok

    def add_book(self):
        print("FUNGSI TAMBAH DIJALANKAN")

        validated = self.validate_inputs()

        if not validated:
            return

        try:
            success, message = db_helper.add_book(*validated)

            if success:
                QtWidgets.QMessageBox.information(
                    self, "Berhasil", message
                )
                self.load_books()
                self.clear_fields()
            else:
                QtWidgets.QMessageBox.critical(
                    self, "Gagal", message
                )

        except Exception as error:
            QtWidgets.QMessageBox.critical(
                self, "Kesalahan Database", str(error)
            )
            print("Error tambah buku:", error)

    def edit_book(self):
        if not self.txtIdBuku.isReadOnly():
            QtWidgets.QMessageBox.warning(
                self, "Edit Gagal",
                "Pilih buku dari tabel terlebih dahulu!"
            )
            return

        validated = self.validate_inputs()

        if not validated:
            return

        reply = QtWidgets.QMessageBox.question(
            self,
            "Konfirmasi Edit",
            "Apakah Anda yakin ingin memperbarui data buku?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )

        if reply != QtWidgets.QMessageBox.Yes:
            return

        try:
            success, message = db_helper.update_book(*validated)

            if success:
                QtWidgets.QMessageBox.information(
                    self, "Berhasil", message
                )
                self.load_books()
                self.clear_fields()
            else:
                QtWidgets.QMessageBox.critical(
                    self, "Gagal", message
                )

        except Exception as error:
            QtWidgets.QMessageBox.critical(
                self, "Kesalahan", str(error)
            )

    def delete_book(self):
        id_buku = self.txtIdBuku.text().strip()

        if not id_buku or not self.txtIdBuku.isReadOnly():
            QtWidgets.QMessageBox.warning(
                self, "Hapus Gagal",
                "Pilih buku dari tabel terlebih dahulu!"
            )
            return

        reply = QtWidgets.QMessageBox.question(
            self,
            "Konfirmasi Hapus",
            f"Yakin ingin menghapus buku dengan ID {id_buku}?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )

        if reply != QtWidgets.QMessageBox.Yes:
            return

        try:
            success, message = db_helper.delete_book(id_buku)

            if success:
                QtWidgets.QMessageBox.information(
                    self, "Berhasil", message
                )
                self.load_books()
                self.clear_fields()
            else:
                QtWidgets.QMessageBox.critical(
                    self, "Gagal", message
                )

        except Exception as error:
            QtWidgets.QMessageBox.critical(
                self, "Kesalahan", str(error)
            )

    def clear_fields(self):
        self.txtIdBuku.clear()
        self.txtJudul.clear()
        self.txtPengarang.clear()
        self.txtPenerbit.clear()
        self.txtTahun.clear()
        self.txtStok.clear()

        self.txtIdBuku.setReadOnly(False)
        self.tableBuku.clearSelection()
