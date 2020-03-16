import os.path
from qgis.core import QgsWkbTypes
from _lib.base_plugin import BasePlugin
from _lib.base_dialog import BaseWizardDialog
from _lib.consts import Messages as m
from _lib.utils import Utils
from .resources import *


class AggChecks(BasePlugin):

    def __init__(self, iface):
        super().__init__(iface=iface,
                         folder=os.path.dirname(__file__),
                         icon=u'rings.png',
                         tool=u'Базовые проверки перед использованием инструментов',
                         tools=None,
                         dialog=BaseWizardDialog,
                         ui_file='dialog.ui')
        self._dlg.starting.clicked.connect(self.on_start)
        self._dlg.map.stateChanged.connect(self.on_setting)
        self._dlg.selection.stateChanged.connect(self.on_setting)
        self._dlg.any_object.stateChanged.connect(self.on_setting)
        self.on_setting()

    @property
    def only_one(self):
        return self._dlg.only_one.isChecked()

    @property
    def only_active(self):
        return self._dlg.active_layer.isChecked()

    @property
    def has_types(self):
        return self._dlg.points.isChecked() or self._dlg.lines.isChecked() or self._dlg.polygons.isChecked()

    @property
    def types(self):
        result = [QgsWkbTypes.Point, QgsWkbTypes.MultiPoint,
                  QgsWkbTypes.LineString, QgsWkbTypes.MultiLineString,
                  QgsWkbTypes.Polygon, QgsWkbTypes.MultiPolygon] if self._dlg.any_object.isChecked() else []

        if not result:
            if self._dlg.points.isChecked():
                result += [QgsWkbTypes.Point, QgsWkbTypes.MultiPoint]
            if self._dlg.lines.isChecked():
                result += [QgsWkbTypes.LineString, QgsWkbTypes.MultiLineString]
            if self._dlg.polygons.isChecked():
                result += [QgsWkbTypes.Polygon, QgsWkbTypes.MultiPolygon]

        return result

    def run(self):
        self._dlg.show()

    def on_setting(self):
        x, y, z = self._dlg.map.isChecked(), self._dlg.selection.isChecked(), self._dlg.any_object.isChecked()
        self._dlg.selection.setEnabled(x)
        self._dlg.active_layer.setEnabled(x and y)
        self._dlg.any_layer.setEnabled(x and y)
        self._dlg.any_object.setEnabled(x and y)
        self._dlg.only_one.setEnabled(x and y)
        self._dlg.points.setEnabled(x and y and not z)
        self._dlg.lines.setEnabled(x and y and not z)
        self._dlg.polygons.setEnabled(x and y and not z)
        self._dlg.points.setChecked(z) if z else None
        self._dlg.lines.setChecked(z) if z else None
        self._dlg.polygons.setChecked(z) if z else None

    def on_start(self):
        checks = []
        if self._dlg.map.isChecked():
            checks.append(self.check_map)
            if self._dlg.selection.isChecked():
                checks.append(self.check_selection)
                if self.has_types:
                    checks.append(self.check_geometry)

        success = True
        for check in checks:
            success = success and check()
            if not success:
                break

        self.msg(m.READY if success else m.ERROR)

    def check_map(self):
        result = Utils.Check.map()
        if not result:
            self.msg(m.OPEN_MAP)
        return result

    def check_selection(self):
        result = Utils.Check.selection(only_active=self.only_active, only_one=self.only_one)
        if not result:
            self.msg(m.CHOOSE_OBJECT if self.only_one else m.CHOOSE_OBJECTS)
        return result

    def check_geometry(self):
        types = self.types
        result = Utils.Check.geometry(types=types, only_active=self.only_active)
        if not result:
            self.msg(m.UNKNOWN_GEOMETRY_TYPE)
        return result
