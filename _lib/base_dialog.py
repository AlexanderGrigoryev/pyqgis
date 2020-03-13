from qgis.PyQt import QtWidgets


class BaseDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(BaseDialog, self).__init__(parent)
        self.setupUi(self)
        self.check_ready = lambda: True

    def closeEvent(self, event):
        event.accept() if self.check_ready() else event.ignore()

    def reject(self):
        if self.check_ready():
            super().reject()
