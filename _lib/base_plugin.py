import os.path
from abc import ABCMeta, abstractmethod
from qgis.PyQt.QtCore import Qt, QSize
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QMessageBox, QMenu, QAction
from .consts import Keys as k, Messages as m, Tool
from .utils import Utils


class BasePlugin:

    __metaclass__ = ABCMeta

    def __init__(self, iface, folder, icon, tool, tools, dialog, ui_file):
        self.iface = iface
        self.folder = folder
        self.img_folder = os.path.join(folder, 'lib', 'img')
        self.ui_folder = os.path.join(folder, 'ui')
        self.menu = Tool.MENU
        self.logo = self.q_icon('logo.png')
        self.icon = self.q_icon(icon)
        self.tool = tool
        self.tools = tools

        self._msg = self.q_msg()
        self._dlg = self.q_dialog(dialog, ui_file)

        self.root_menu = self.iface.pluginMenu()
        self.sub_menu = None
        self.tool_menu = None
        self.active_tool = None
        self.action = None

    def q_msg(self):
        result = QMessageBox()
        result.setWindowTitle(self.tool)
        result.setWindowIcon(self.icon)
        result.setModal(True)
        result.setWindowModality(Qt.ApplicationModal)
        return result

    def q_dialog(self, dialog, ui_file=None, title=None, icon=None):
        result = None
        if dialog:
            result = dialog(owner=self, ui_file=ui_file) if ui_file else dialog(owner=self)
            result.setWindowTitle(title if title else self.tool)
            result.setWindowIcon(icon if icon else self.icon)
            result.logo.setPixmap(self.logo.pixmap(QSize(16, 16)))
            result.setModal(True)
            result.setWindowModality(Qt.ApplicationModal)
            if result.is_wizard:
                result.setWindowFlags(
                    Qt.Window |
                    Qt.CustomizeWindowHint |
                    Qt.WindowTitleHint |
                    Qt.WindowCloseButtonHint |
                    Qt.WindowStaysOnTopHint)
                result.setModal(False)
                result.setWindowModality(Qt.NonModal)
        return result

    def q_icon(self, file_name):
        return QIcon(os.path.join(self.img_folder, file_name))

    def msg(self, text, buttons=QMessageBox.Ok):
        self._msg.setText(text)
        self._msg.setStandardButtons(buttons)
        return self._msg.exec_()

    @property
    def has_tools(self):
        return self.tools and len(self.tools) > 0

    @staticmethod
    def find_action(root, name, icon, callback):
        action = root.findChild(QAction, name) if root else None
        if not action:
            action = QAction(icon, name, root)
            action.triggered.connect(callback)
            action.setEnabled(callback is not None)
            root.addAction(action)
        return action

    @staticmethod
    def find_menu(root, name, icon=None):
        menu = root.findChild(QMenu, name) if root else None
        if not menu:
            menu = QMenu(name, root)
            menu.setObjectName(name)
            if icon:
                menu.setIcon(icon)
            root.addMenu(menu)
        else:
            root.addAction(menu.menuAction())
        return menu

    def initGui(self):
        self.sub_menu = self.find_menu(self.root_menu, self.menu, self.logo)

        if self.has_tools:
            self.tool_menu = self.find_menu(self.sub_menu, self.tool, self.icon)
            self.action = self.tool_menu.menuAction()
            for key, tool in self.tools.items():
                self.find_action(self.tool_menu, tool[k.name], tool[k.icon], tool[k.callback])
        else:
            self.action = self.find_action(self.sub_menu, self.tool, self.icon, self.run)

        self.iface.addToolBarIcon(self.action)

    def unload(self):
        self._msg = None
        self.iface.removeToolBarIcon(self.action)
        self.sub_menu.removeAction(self.action)
        if self.has_tools:
            for action in self.tool_menu.actions():
                self.tool_menu.removeAction(action)
        if self.sub_menu.isEmpty():
            self.root_menu.removeAction(self.sub_menu.menuAction())

    @abstractmethod
    def run(self):
        """проверки перед использованием нструмента, инициализация и вызов диалога при необходимости"""


class BaseDrawingPlugin(BasePlugin):

    __metaclass__ = ABCMeta

    def __init__(self, iface, folder, icon, tool, tools, dialog, ui_file):
        BasePlugin.__init__(self, iface, folder, icon, tool, tools, dialog, ui_file)
        self._layer = None
        self.drawing_tool = None
        self.drawing_tool_name = None

    @property
    @abstractmethod
    def layer(self):
        """слой для сохранения результата рисования"""

    def run(self):
        self.drawing_tool = None
        if self.check_map():
            drawing = self.active_tool[k.drawing_tool]
            self.drawing_tool = drawing(self.iface.mapCanvas())
            self.iface.mapCanvas().setMapTool(self.drawing_tool)
            self.drawing_tool.apply.connect(self.on_apply)
            self.drawing_tool_name = self.active_tool[k.name]

    def check_map(self):
        result = Utils.Check.map()
        if not result:
            self.msg(m.OPEN_MAP)
        return result

    @abstractmethod
    def on_apply(self, data: dict):
        """обработчик результата рисования"""
