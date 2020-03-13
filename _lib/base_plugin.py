from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QMessageBox, QMenu, QAction
import os.path
from .consts import Tool, Keys as k
from abc import ABCMeta, abstractmethod


class BasePlugin:

    __metaclass__ = ABCMeta

    def __init__(self, iface, folder, icon, tool, tools, dialog):
        self.iface = iface
        self.img_folder = os.path.join(folder, 'lib', 'img')
        self.menu = Tool.MENU
        self.logo = self.q_icon('logo.png')
        self.icon = self.q_icon(icon)
        self.tool = tool
        self.tools = tools

        self._msg = QMessageBox()
        self._msg.setWindowTitle(self.tool)
        self._msg.setWindowIcon(self.icon)
        self._msg.setWindowModality(Qt.ApplicationModal)

        self._dlg = None
        if dialog:
            self._dlg = dialog()
            self._dlg.setWindowTitle(self.tool)
            self._dlg.setWindowIcon(self.icon)

        self.root_menu = self.iface.pluginMenu()
        self.sub_menu = None
        self.tool_menu = None
        self.action = None

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
