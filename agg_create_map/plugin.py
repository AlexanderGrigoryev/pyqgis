import os.path
from qgis.core import QgsWkbTypes, QgsProject, QgsField, edit
from qgis.PyQt.QtCore import QVariant

from _lib.base_plugin import BasePlugin
from _lib.base_dialog import BaseDialog
from _lib.consts import Messages as m, Tool
from _lib.utils import Utils
from .resources import *


class AggCreateMap(BasePlugin):

    def __init__(self, iface):
        super().__init__(iface=iface,
                         folder=os.path.dirname(__file__),
                         icon=u'layers.png',
                         tool=u'Создание карты',
                         tools=None,
                         dialog=BaseDialog,
                         ui_file='dialog.ui')

        self._file_name = None
        self._map_folder = os.path.join(Utils.System.desktop_folder(), 'agg_create_map', 'map')
        self._layers_folder = os.path.join(self._map_folder, 'layers')
        self._point_fields = 'id;code;name;note'
        self._line_fields = '1;2;3;4'
        self._polygon_fields = 'Код;Название;Описание'
        self._values = {
            '1': 'first',
            '2': 'second',
            '4': 'fourth',
            'id': '3241-5468-1234',
            'name': 'Samuraj',
            'note': 'This is Samuraj',
            'Код': '707',
            'Название': 'Самурай',
            'Описание': 'Это самурай',
            'unknown': 'some unknown value'
        }

        self._dlg.map.setText(self._map_folder)
        self._dlg.layers.setText(self._layers_folder)
        self._dlg.points.setText(self._point_fields)
        self._dlg.lines.setText(self._line_fields)
        self._dlg.polygons.setText(self._polygon_fields)

        self._dlg.file_name.setToolTip(u'Название создаваемого проекта')
        self._dlg.map.setToolTip(u'Путь к папке для сохранения проекта')
        self._dlg.layers.setToolTip(u'Путь к папке для сохранения слоёв')
        self._dlg.points.setToolTip(u'Атрибуты слоя точек')
        self._dlg.lines.setToolTip(u'Атрибуты слоя линий')
        self._dlg.polygons.setToolTip(u'Атрибуты слоя многоугольников')

        self._dlg.temporary.setToolTip(u'Будут созданы слои с хранением в памяти')
        self._dlg.permanent.setToolTip(u'Будут созданы слои с хранением в файлах')

    def check_map(self):
        result = not Utils.Check.map()
        if not result:
            self.msg(m.CLOSE_MAP)
        return result

    def dlg_init(self):
        self._file_name = Utils.System.time_file(extension='qgs')
        self._dlg.file_name.setText(self._file_name)

    def run(self):
        if self.check_map():
            self.dlg_init()
            self._dlg.show()
            result = self._dlg.exec_()
            if result:
                self.apply()

    def apply(self):
        # создание нового файла проекта
        qgs_file = Utils.System.new_file(self._map_folder, self._file_name)
        QgsProject().instance().read(qgs_file)
        # добавление новых слоёв
        points = Utils.Map.new_layer(name=Tool.point, wkb_type=QgsWkbTypes.Point)
        lines = Utils.Map.new_layer(name=Tool.line, wkb_type=QgsWkbTypes.LineString)
        polygons = Utils.Map.new_layer(name=Tool.polygon, wkb_type=QgsWkbTypes.Polygon)
        # обновление списка атрибутов
        layers = (points, lines, polygons)
        fields = (self._point_fields, self._line_fields, self._polygon_fields)
        for pair in list(zip(layers, fields)):
            layer, fields = pair
            attributes = [QgsField(x, QVariant.String) for x in fields.split(';')]
            layer.dataProvider().addAttributes(attributes)
            layer.updateFields()
        # добавление объектов с заполнением атрибутов
        for layer in (points, lines, polygons):
            with edit(layer):
                random_points = Utils.Geometry.random_points(2, 10)
                Utils.Feature.new_feature(layer=layer, points=random_points, values=self._values)
            self.iface.showAttributeTable(layer)
        # сохранение изменений в файл проекта
        QgsProject().instance().write(qgs_file)
        self.msg(m.READY)
