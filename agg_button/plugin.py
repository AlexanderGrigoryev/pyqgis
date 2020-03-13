import os.path
from _lib.base_plugin import BasePlugin
from _lib.consts import Messages as m
from .dialog import Dialog
from .resources import *


class AggButton(BasePlugin):

    def __init__(self, iface):
        super().__init__(iface=iface,
                         folder=os.path.dirname(__file__),
                         icon=u'soska.png',
                         tool=u'Вызов диалога по кнопке',
                         tools=None,
                         dialog=Dialog)

    def run(self):
        self._dlg.show()
        result = self._dlg.exec_()
        if result:
            self.msg(m.READY)
