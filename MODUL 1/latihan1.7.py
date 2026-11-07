
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit,
    QAction, QFileDialog, QMessageBox
)


class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Text Editor Sederhana")
        self.setGeometry(300, 300, 600, 400)

        self.text_area = QTextEdit()
        self.setCentralWidget(self.text_area)

        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")

        new_action = QAction("New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_file)

        open_action = QAction("Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)

        save_action = QAction("Save", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)

        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)

        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        edit_menu = menubar.addMenu("Edit")
        edit_menu.addAction("Undo", self.text_area.undo)
        edit_menu.addAction("Redo", self.text_area.redo)

        help_menu = menubar.addMenu("Help")
        help_menu.addAction("About", self.show_about)

        toolbar = self.addToolBar("Tools")
        toolbar.addAction(new_action)
        toolbar.addAction(open_action)
        toolbar.addAction(save_action)

    def new_file(self):
        self.text_area.clear()

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Open File", "",
            "Text Files (*.txt);;All Files (*)"
        )
        if filename:
            try:
                with open(filename, "r", encoding="utf-8") as file:
                    self.text_area.setText(file.read())
            except OSError as error:
                QMessageBox.warning(self, "Error", str(error))

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save File", "",
            "Text Files (*.txt);;All Files (*)"
        )
        if filename:
            try:
                with open(filename, "w", encoding="utf-8") as file:
                    file.write(self.text_area.toPlainText())
                QMessageBox.information(
                    self, "Berhasil", "File berhasil disimpan!"
                )
            except OSError as error:
                QMessageBox.warning(self, "Error", str(error))

    def show_about(self):
        QMessageBox.information(
            self, "About", "Text Editor Sederhana - Praktik 7"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TextEditor()
    window.show()
    sys.exit(app.exec_())
