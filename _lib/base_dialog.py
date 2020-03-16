from qgis.core import QgsApplication
from qgis.PyQt import QtWidgets, uic
from time import sleep


class BaseDialog(QtWidgets.QDialog):
    def __init__(self, owner, ui_file):
        super(BaseDialog, self).__init__(parent=None)
        uic.loadUi(ui_file, self)
        self.owner = owner
        self.check_ready = lambda: True

    @property
    def is_wizard(self):
        return isinstance(self, BaseWizardDialog)

    def closeEvent(self, event):
        event.accept() if self.check_ready() else event.ignore()

    def reject(self):
        if self.check_ready():
            super().reject()


class BaseWizardDialog(BaseDialog):
    def __init__(self, owner, ui_file):
        super(BaseWizardDialog, self).__init__(owner, ui_file)

    def leaveEvent(self, event):
        self.setWindowOpacity(0.5)

    def enterEvent(self, event):
        self.setWindowOpacity(1.0)

    def moveEvent(self, event):
        screen = self.owner.iface.mainWindow().geometry()
        self.move(screen.right() - self.width() - 20, screen.bottom() - self.height() - 60)
        sleep(0.1)
        self.setWindowOpacity(0.5)
        QgsApplication.processEvents()
