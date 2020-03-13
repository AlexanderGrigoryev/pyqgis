import os

from qgis.PyQt import uic
from _lib.base_dialog import BaseDialog


FORM_CLASS, _ = uic.loadUiType(os.path.join(os.path.dirname(__file__), 'dialog.ui'))


class Dialog(BaseDialog, FORM_CLASS):
    pass
