from qgis.PyQt import QtWidgets, uic


class BaseDialog(QtWidgets.QDialog):
    def __init__(self, ui_file):
        super(BaseDialog, self).__init__(parent=None)
        uic.loadUi(ui_file, self)
        self.check_ready = lambda: True

    def closeEvent(self, event):
        event.accept() if self.check_ready() else event.ignore()

    def reject(self):
        if self.check_ready():
            super().reject()
