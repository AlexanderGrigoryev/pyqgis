import os
from time import sleep

from qgis.core import QgsApplication
from qgis.PyQt import uic
from qgis.PyQt.QtGui import QTextCursor
from qgis.PyQt.QtWidgets import QApplication, QDialog, QTextBrowser, QLabel


class BaseDialog(QDialog):
    def __init__(self, owner, ui_file):
        super(BaseDialog, self).__init__(parent=None)
        self.owner = owner
        uic.loadUi(uifile=os.path.join(self.owner.ui_folder, ui_file),
                   baseinstance=self)
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


class Logger:
    """писатель в журнал"""

    def __init__(self, log: QTextBrowser, total: QLabel = None):
        self._log = log
        self._total = total

    def log(self, text=''):
        if not self._log:
            return
        self._log.moveCursor(QTextCursor.End)
        self._log.insertHtml('<div>%s</div><br />' % text)
        self._log.moveCursor(QTextCursor.End)
        QApplication.processEvents()

    def set_total(self):
        if not self._total:
            return
        delimiter = ': '
        label, count = self._total.text().split(delimiter)
        count = int(count) + 1
        self._total.setText(''.join([label, delimiter, str(count)]))
