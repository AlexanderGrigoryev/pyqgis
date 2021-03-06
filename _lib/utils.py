import os
import random
import re
import shutil
import time
import zipfile
import numpy
import math
from scipy.interpolate import BSpline
from qgis.PyQt.QtWidgets import QFileDialog
from qgis.core import *
from qgis.utils import iface
from .consts import Keys as k, SymbolProp as kp


class Utils:
    """общие утилиты для написания плагинов QGIS"""

    class qgis:
        """проброс втроенных в api утилит"""
        __utils = None

        @classmethod
        def utils(cls):
            if cls.__utils is None:
                cls.__utils = QgsGeometryUtils()
            return cls.__utils

    class Compiler:
        """компилятор плагинов"""

        @staticmethod
        def publish(plugin):
            plugin_folder = Utils.System.qgis_plugin_folder()
            target = zipfile.ZipFile(".\\compiled\\%s.zip" % plugin, "r", zipfile.ZIP_DEFLATED)
            target.extractall(plugin_folder)
            target.close()

        @staticmethod
        def zip_plugin(plugin):
            target = zipfile.ZipFile(".\\compiled\\%s.zip" % plugin, "w", zipfile.ZIP_DEFLATED)
            for root, dirs, files in os.walk(plugin):
                for file in files:
                    target.write(os.path.join(root, file))
            target.close()

        @staticmethod
        def is_plugin(root, folder, prefix):
            a = os.path.isdir(os.path.join(root, folder))
            b = folder.startswith(prefix)
            return a and b

        @classmethod
        def execute(cls, prefix, publish):
            root = '.'
            plugins = [folder for folder in os.listdir(root) if cls.is_plugin(root, folder, prefix)]
            lib_source = ".\\_lib"      # develop and commit this folder
            lib_target = ".\\{0}\\lib"  # update and ignore this folder
            compiler = "call py -m PyQt5.pyrcc_main -o .\\{0}\\resources.py .\\{0}\\resources.qrc"
            for plugin in plugins:
                shutil.rmtree(lib_target.format(plugin), ignore_errors=True)
                shutil.copytree(lib_source, lib_target.format(plugin))
                os.system(compiler.format(plugin))
                cls.lib_import(plugin, "from _lib.", "from .lib.")
                cls.zip_plugin(plugin)
                cls.lib_import(plugin, "from .lib.", "from _lib.")
                cls.publish(plugin) if publish else None

        @staticmethod
        def lib_import(plugin, source, target):
            for root, dirs, files in os.walk(plugin):
                for file in files:
                    if file.endswith('.py'):
                        with open(os.path.join(root, file), mode="r", encoding="utf-8") as f:
                            lines = [line.replace(source, target) for line in f.readlines()]
                        with open(os.path.join(root, file), mode="w", encoding="utf-8") as f:
                            f.writelines(lines)

    class Map:
        """общие методы для работы со структурой карты"""

        @staticmethod
        def layers(only_editable=False):
            """список слоёв"""
            return [node.layer() for node in QgsProject().instance().layerTreeRoot().children()
                    if node.layer().isEditable() or not only_editable]

        @staticmethod
        def nodes():
            """список узлов дерева слоёв карты"""
            return QgsProject().instance().layerTreeRoot().children()

        @classmethod
        def show(cls, layer):
            """отображает слой"""
            if layer:
                node = [x for x in cls.nodes() if x.layerId() == layer.id()][0]
                node.setItemVisibilityChecked(True)

        @classmethod
        def hide(cls, layer):
            """скрывает слой"""
            if layer:
                node = [x for x in cls.nodes() if x.layerId() == layer.id()][0]
                node.setItemVisibilityChecked(False)

        @staticmethod
        def selection(only_active=True):
            """список слоёв с наличием выбранных объектов"""
            layers = [iface.activeLayer()] if only_active else Utils.Map.layers()
            return [layer for layer in layers if len(layer.selectedFeatures()) > 0]

        @staticmethod
        def new_layer(name, wkb_type, fields=None, labeling=None, driver='memory'):
            """вернёт новый временный слой"""
            layers = QgsProject().instance().mapLayersByName(name)
            layer = layers[0] if layers else None
            if not layer:
                url = '%s?crs=epsg:4326' % Utils.Geometry.wkt_type(wkb_type)
                layer = QgsVectorLayer(url, name, driver)
                layer.setCrs(QgsProject().instance().crs())
                if fields:
                    layer.dataProvider().addAttributes(fields)
                    layer.updateFields()
                if labeling:
                    Utils.Feature.labeling(layer=layer, view_attr=labeling[0], x_attr=labeling[1], y_attr=labeling[2])
                QgsProject().instance().addMapLayer(layer)
                iface.mapCanvas().refresh()
            return layer

        @staticmethod
        def remove_layer(name):
            """удалит с карты все слои, найденные по имени"""
            layer_ids = [layer.id() for layer in QgsProject().instance().mapLayersByName(name)]
            QgsProject().instance().removeMapLayers(layer_ids) if layer_ids else None
            iface.mapCanvas().refresh()

        @staticmethod
        def is_point_layer(layer):
            return layer.wkbType() in (QgsWkbTypes.Point, QgsWkbTypes.MultiPoint)

        @staticmethod
        def is_line_layer(layer):
            return layer.wkbType() in (QgsWkbTypes.LineString, QgsWkbTypes.MultiLineString)

        @staticmethod
        def is_polygon_layer(layer):
            return layer.wkbType() in (QgsWkbTypes.Polygon, QgsWkbTypes.MultiPolygon)

        @staticmethod
        def save():
            for layer in Utils.Map.layers(only_editable=True):
                layer.commitChanges()

        @staticmethod
        def discard():
            for layer in Utils.Map.layers(only_editable=True):
                layer.rollBack()

    class Feature:
        """общие методы для работы с фичами и их атрибутами"""

        @staticmethod
        def attributes_to_dict(layer, values, index_as_key=False):
            """подготовка переданных значений в виде словаря для записи в таблицу атрибутов указанного слоя"""
            keys = layer.attributeList() if index_as_key else layer.fields().names()

            if isinstance(values, list):
                return {a[0]: a[1] for a in list(zip(keys, values))}

            if isinstance(values, dict):
                return values

            return {key: None for key in keys}

        @staticmethod
        def attributes_to_list(layer, values):
            """подготовка переданных значений в виде списка для записи в таблицу атрибутов указанного слоя"""
            if isinstance(values, dict):
                return [values[field_name] if field_name in values else None for field_name in layer.fields().names()]

            if isinstance(values, list):
                return values

            try:
                return list(values)
            except TypeError:
                return []

        @classmethod
        def new_feature(cls, layer, points, values=None):
            """
            создает новую фичу на слое layer, с соответствующей геометрией и координатами points, заполняя
            все возможные атрибуты из словаря values
            """
            geometry = Utils.Geometry.from_points(layer, points)
            return cls.new_feature_geometry(layer, geometry, values)

        @classmethod
        def new_feature_geometry(cls, layer, geometry, values=None):
            """
            создает новую фичу на слое layer, с геометрией geometry, заполняя все возможные атрибуты из словаря values
            """
            if not geometry:
                return None
            feature = QgsFeature()
            feature.setGeometry(geometry)
            if values:
                attributes = cls.attributes_to_list(layer, values)
                feature.setAttributes(attributes)
            layer.dataProvider().addFeature(feature)
            layer.updateExtents()
            layer.triggerRepaint()
            return feature

        @classmethod
        def replace_feature_geometry(cls, layer, feature, points):
            """заменяет геометрию фичи (id фичи остается неизменным)"""
            geometry = Utils.Geometry.from_points(layer, points)
            layer.changeGeometry(feature.id(), geometry) if geometry else None

        @classmethod
        def replace_feature_attributes(cls, layer, feature, values):
            """заменяет значения атрибутов фичи (id фичи остается неизменным)"""
            attributes = cls.attributes_to_dict(layer, values, index_as_key=True)
            layer.changeAttributeValues(feature.id(), attributes)

        @staticmethod
        def selection(only_active=True):
            """список выбранных фич"""
            features = []
            for layer in Utils.Map.selection(only_active):
                features += layer.selectedFeatures()
            return features

        @staticmethod
        def intersected(geometry, only_active=True):
            """список фич, имеющих пересечение с указанной геометрией"""
            layers = [iface.activeLayer()] if only_active else Utils.Map.layers()
            features = []
            for layer in layers:
                if Utils.Map.is_line_layer(layer) or Utils.Map.is_polygon_layer(layer):
                    features += [feature for feature in layer.getFeatures() if geometry.intersects(feature.geometry())]
            return features

        @staticmethod
        def labeling(layer, view_attr, x_attr=None, y_attr=None):
            settings = QgsPalLayerSettings()
            settings.format().shadow().setEnabled(True)
            fmt = settings.format()
            font = fmt.font()
            font.setFamily('Courier New')
            fmt.setFont(font)
            fmt.setSize(8)
            settings.setFormat(fmt)
            settings.fieldName = view_attr
            if x_attr and y_attr:
                props = settings.dataDefinedProperties()
                props.property(QgsPalLayerSettings.PositionX).setField(x_attr)
                props.property(QgsPalLayerSettings.PositionY).setField(y_attr)
            labeling = QgsVectorLayerSimpleLabeling(settings)
            layer.setLabeling(labeling)
            layer.setLabelsEnabled(True)
            layer.triggerRepaint()

        @staticmethod
        def combine_geometry(features):
            """вернёт объединенную геометрию всех фич в одну"""
            return Utils.Geometry.combine(geometries=[x.geometry() for x in features])

    class Geometry:
        """общие методы для работы с геометрией"""

        __profile = None

        @classmethod
        def profile(cls, key=None):
            if cls.__profile is None:
                from qgis.PyQt.QtGui import QIcon
                cls.__profile = {
                    (QgsWkbTypes.Point, QgsWkbTypes.MultiPoint): {
                        k.title: u'Точка',
                        k.wkt_single_type: 'Point',
                        k.wkt_multi_type: 'MultiPoint',
                        k.icon: QIcon(os.path.join(os.path.dirname(__file__), 'img', 'point.png')),
                        QgsSimpleMarkerSymbolLayer: {
                            kp.ru.size: (kp.en.size, kp.en.size_unit, kp.en.size_map_unit_scale),
                            kp.ru.color: (kp.en.color,),
                            kp.ru.outline_color: (kp.en.outline_color,),
                            kp.ru.outline_width: (
                            kp.en.outline_width, kp.en.outline_width_unit, kp.en.outline_width_map_unit_scale,),
                            kp.ru.outline_style: (kp.en.outline_style,),
                            kp.ru.angle: (kp.en.angle,),
                            kp.ru.name: (kp.en.name,)
                        },
                        QgsFontMarkerSymbolLayer: {
                            kp.ru.font: (kp.en.font,),
                            kp.ru.chr: (kp.en.chr,),
                            kp.ru.size: (kp.en.size, kp.en.size_unit, kp.en.size_map_unit_scale),
                            kp.ru.color: (kp.en.color,),
                            kp.ru.outline_color: (kp.en.outline_color,),
                            kp.ru.outline_width: (
                            kp.en.outline_width, kp.en.outline_width_unit, kp.en.outline_width_map_unit_scale,),
                            kp.ru.angle: (kp.en.angle,)
                        }
                    },
                    (QgsWkbTypes.LineString, QgsWkbTypes.MultiLineString): {
                        k.title: u'Линия',
                        k.wkt_single_type: 'LineString',
                        k.wkt_multi_type: 'MultiLineString',
                        k.icon: QIcon(os.path.join(os.path.dirname(__file__), 'img', 'cut.png')),
                        QgsSimpleLineSymbolLayer: {
                            kp.ru.line_color: (kp.en.line_color,),
                            kp.ru.line_width: (kp.en.line_width, kp.en.line_width_unit, kp.en.width_map_unit_scale,),
                            kp.ru.offset: (kp.en.offset, kp.en.offset_unit, kp.en.offset_map_unit_scale,),
                            kp.ru.line_style: (kp.en.line_style,)
                        },
                        QgsMarkerLineSymbolLayer: {
                            kp.ru.placement: (
                                kp.en.placement,  # <= x
                                kp.en.interval,  # if x in (interval,)
                                kp.en.interval_unit,  # if x in (interval,)
                                kp.en.interval_map_unit_scale,  # if x in (interval,)
                                kp.en.offset_along_line,  # if x in (interval, firstvertex, lastvertex,)
                                kp.en.offset_along_line_unit,  # if x in (interval, firstvertex, lastvertex,)
                                kp.en.offset_along_line_map_unit_scale,  # if x in (interval, firstvertex, lastvertex,)
                            ),
                            kp.ru.offset_line: (kp.en.offset, kp.en.offset_unit, kp.en.offset_map_unit_scale,),
                            kp.ru.marker: (kp.en.marker,)
                        }
                    },
                    (QgsWkbTypes.Polygon, QgsWkbTypes.MultiPolygon): {
                        k.title: u'Полигон',
                        k.wkt_single_type: 'Polygon',
                        k.wkt_multi_type: 'MultiPolygon',
                        k.icon: QIcon(os.path.join(os.path.dirname(__file__), 'img', 'polygon.png')),
                        QgsSimpleFillSymbolLayer: {
                            kp.ru.color: (kp.en.color,),
                            kp.ru.style: (kp.en.style,),
                            kp.ru.outline_color: (kp.en.outline_color,),
                            kp.ru.outline_width: (
                            kp.en.outline_width, kp.en.outline_width_unit, kp.en.border_width_map_unit_scale,),
                            kp.ru.outline_style: (kp.en.outline_style,)
                        },
                        QgsLinePatternFillSymbolLayer: {
                            kp.ru.angle: (kp.en.angle,),
                            kp.ru.spacing: (kp.en.distance, kp.en.distance_unit, kp.en.distance_map_unit_scale,),
                            kp.ru.offset: (kp.en.offset, kp.en.offset_unit, kp.en.offset_map_unit_scale,),
                            kp.ru.line: (kp.en.line,)
                        },
                        QgsPointPatternFillSymbolLayer: {
                            kp.ru.distance_x: (
                            kp.en.distance_x, kp.en.distance_x_unit, kp.en.distance_x_map_unit_scale,),
                            kp.ru.distance_y: (
                            kp.en.distance_y, kp.en.distance_y_unit, kp.en.distance_y_map_unit_scale,),
                            kp.ru.displacement_x: (
                            kp.en.displacement_x, kp.en.displacement_x_unit, kp.en.displacement_x_map_unit_scale,),
                            kp.ru.displacement_y: (
                            kp.en.displacement_y, kp.en.displacement_y_unit, kp.en.displacement_y_map_unit_scale,),
                            kp.ru.marker: (kp.en.marker,)
                        },
                        QgsSimpleLineSymbolLayer: {
                            kp.ru.line: (kp.en.line,)
                        },
                        QgsMarkerLineSymbolLayer: {
                            kp.ru.line: (kp.en.line,)
                        }
                    }
                }
            return cls.__profile[key] if key else cls.__profile

        @classmethod
        def wkt_type(cls, wkb_type, multi=False):
            """возвращает название WKT-типа для указанного WKB-типа"""
            for key in cls.profile().keys():
                if wkb_type in key:
                    return cls.profile()[key][k.wkt_multi_type if multi else k.wkt_single_type]
            return None

        @classmethod
        def types_by_type(cls, wkb_type):
            """возвращает составной ключ для указанной геометрии"""
            for key in cls.profile().keys():
                if wkb_type in key:
                    return key
            return None

        @classmethod
        def title(cls, wkb_type):
            """возвращает русское название для указанной геометрии"""
            for key in cls.profile().keys():
                if wkb_type in key:
                    return cls.profile()[key][k.title]
            return None

        @classmethod
        def icon(cls, wkb_type):
            """возвращает иконку для указанной геометрии"""
            for key in cls.profile().keys():
                if wkb_type in key:
                    return cls.profile()[key][k.icon]
            return None

        @classmethod
        def random_points(cls, min_count, max_count):
            """
            возвращает список точек в количестве от min_count до max_count
            в начале координат с небольшими отклонениями
            """
            return [cls.to_pointXY(x=random.random(), y=random.random())
                    for n in range(random.randrange(min_count, max_count, 1))]

        @staticmethod
        def as_pointXY(p):
            return QgsPointXY(p.x(), p.y())

        @staticmethod
        def to_pointXY(x, y):
            return QgsPointXY(x, y)

        @staticmethod
        def as_point(p):
            return QgsPoint(p.x(), p.y())

        @staticmethod
        def to_point(x, y):
            return QgsPoint(x, y)

        @staticmethod
        def from_wkt(wkt):
            """создает геометрию по строке в формате WKT"""
            return QgsGeometry().fromWkt(wkt) if Utils.Check.is_wkt(wkt) else None

        @classmethod
        def from_points(cls, layer, points):
            """создаёт геометрию из точек на указанном слое"""
            geometry = None
            if Utils.Map.is_point_layer(layer):
                geometry = cls.point(points[0].x(), points[0].y())
            if Utils.Map.is_line_layer(layer):
                geometry = cls.line(points)
            if Utils.Map.is_polygon_layer(layer):
                geometry = cls.polygon(points)
            return geometry

        @staticmethod
        def list_points(geometry, excluded=None):
            """возвращает список точек-вершин указанной геометрии"""
            result = []
            for vertex in geometry.vertices():
                if excluded:
                    if vertex in excluded:
                        continue
                result.append(vertex)
            return result

        @classmethod
        def list_pointsXY(cls, geometry, excluded=None):
            """возвращает список точек-вершин указанной геометрии"""
            return [cls.as_pointXY(p) for p in cls.list_points(geometry, excluded)]

        @classmethod
        def point(cls, x, y):
            """возвращает геометрию точки"""
            return cls.from_wkt('Point (%f %f)' % (x, y))

        @staticmethod
        def point_from_wkt(wkt):
            if not Utils.Check.is_point_wkt(wkt):
                return None
            p = QgsPoint()
            p.fromWkt(wkt)
            return p

        @classmethod
        def angle_points(cls, z, c, d, sharp):
            """возвращает список точек для обозначения угла"""
            arc = Utils.Geometry.arc(z, c, d, longest=not sharp)
            result = cls.list_pointsXY(arc)
            result = [z, d] + result + [c, z]
            return result

        @classmethod
        def arc(cls, p0, p1, p2, longest=False):
            """возвращает дугу окружности с центром в p0, разделенную треугольником p0,p1,p2"""
            pp0, pp1, pp2 = (cls.as_point(p) for p in (p0, p1, p2))
            triangle = cls.polygon([pp0, pp1, pp2])
            l1, l2 = cls.cut(pp0, pp1), cls.cut(pp0, pp2)
            d1, d2 = l1.length(), l2.length()
            h = Utils.qgis.utils().perpendicularSegment(pp0, pp1, pp2).length()
            d = min(d1, d2, h)
            a1, a2 = pp0.azimuth(pp1), pp0.azimuth(pp2)
            a = min(a1, a2)
            circle_points = QgsCircle().fromCenterDiameter(center=pp0, diameter=d, azimuth=a).points()
            circle = cls.polygon(points=circle_points)
            segment = circle.intersection(triangle)
            short = cls.list_points(geometry=segment)
            short.pop()
            short.pop()
            short.pop() if pp0 in short else None
            long = []
            for p in circle_points:
                gp = cls.from_wkt(p.asWkt())
                in_small = triangle.intersects(gp) or circle_points.index(p) == 0
                long.append(p) if not in_small else None
            long = short[-1:] + long + short[:1]
            return cls.line(points=long if longest else short)

        @classmethod
        def cut(cls, a, b):
            """возвращает геометрию отрезка"""
            return cls.line(points=[a, b])

        @classmethod
        def line(cls, points):
            """возвращает геометрию линии"""
            return cls.from_wkt('LineString (%s)' % ','.join(['%f %f' % (p.x(), p.y()) for p in points]))

        @classmethod
        def polygon(cls, points):
            """возвращает геометрию многоугольника"""
            points.append(points[0]) if points[:1] != points[-1:] else None
            return cls.from_wkt('Polygon ((%s))' % ','.join(['%f %f' % (p.x(), p.y()) for p in points]))

        @classmethod
        def segments(cls, geometry):
            """возвращает список сегментов фичи"""
            vertices = geometry.vertices()
            points = []
            while vertices.hasNext():
                points.append(vertices.next())
            return [cls.cut(a, b) for a, b in list(zip(points[:-1], points[1:]))]

        @staticmethod
        def selection(only_active=True):
            """список геометрии выбранных фич"""
            return [feature.geometry() for feature in Utils.Feature.selection(only_active)]

        @staticmethod
        def intersected(geometry, only_active=True):
            """список геометрии, имеющие пересечение с указанной"""
            return [feature.geometry() for feature in Utils.Feature.intersected(geometry, only_active)]

        @classmethod
        def is_point_near_segment(cls, p, s):
            """точка около сегмента"""
            segment = cls.cut(s[0], s[1])
            point = cls.point(p.x(), p.y())
            return segment.boundingBoxIntersects(point)

        @staticmethod
        def combine(geometries):
            """вернёт комбинированную геометрию"""
            result = None
            for g in geometries:
                result = g.combine(result) if result else g
            return result

    class Check:
        """общие проверки перед использованием или в процессе использования инструментов"""

        @staticmethod
        def map():
            """открыт проект и есть хотя бы один слой"""
            return QgsProject().instance() and QgsProject().instance().count() > 0

        @staticmethod
        def selection(only_active=True, only_one=False):
            """объекты на карте выбраны"""
            n = len(Utils.Feature.selection(only_active))
            return n == 1 if only_one else n > 0

        @staticmethod
        def geometry(types, only_active=True):
            """выбранная геометрия имет один из указанных типов"""
            return all(layer.wkbType() in types for layer in Utils.Map.selection(only_active))

        @staticmethod
        def ready():
            """слои на карте сохранены"""
            n = len(Utils.Map.layers(only_editable=True))
            return n == 0

        @staticmethod
        def is_angle(value, is_radian):
            degrees = math.degrees(value) if is_radian else value
            return 0.0 < round(degrees, 8) < 360

        @classmethod
        def is_wkt(cls, wkt):
            return cls.is_point_wkt(wkt, strict=False) \
                   or cls.is_line_wkt(wkt, strict=False) \
                   or cls.is_polygon_wkt(wkt, strict=False)

        @staticmethod
        def is_point_wkt(wkt, strict=True, multi=False):
            s = "^Point{1}[\s]?\([0-9]*[.]?[0-9]+\s[0-9]*[.]?[0-9]+\)$"
            m = "^MultiPoint{1}[\s]?\((\([0-9]*[.]?[0-9]+\s[0-9]*[.]?[0-9]+\)[,]?[\s]?){2,}\)$"
            wktx = s+"|"+m if not strict else m if multi else s
            return re.match(wktx, wkt)

        @staticmethod
        def is_line_wkt(wkt, strict=True, multi=False):
            s = "^LineString{1}[\s]?\(([0-9]*[.]?[0-9]+\s[0-9]*[.]?[0-9]+[,]?[\s]?){2,}\)$"
            m = "^MultiLineString{1}[\s]?\((\(([0-9]*[.]?[0-9]+\s[0-9]*[.]?[0-9]+[,]?[\s]?){2,}\)+[,]?[\s]?)+\)$"
            wktx = s+"|"+m if not strict else m if multi else s
            return re.match(wktx, wkt)

        @staticmethod
        def is_polygon_wkt(wkt, strict=True, multi=False):
            s = "^Polygon{1}[\s]?\((\(([0-9]*[.]?[0-9]+\s[0-9]*[.]?[0-9]+[,]?[\s]?){2,}\)+[,]?[\s]?)+\)$"
            m = "^MultiPolygon{1}[\s]?\((\((\(([0-9]*[.]?[0-9]+\s[0-9]*[.]?[0-9]+[,]?[\s]?){2,}\)+[,]?[\s]?)+\)+[,]?[\s]?)+\)$"
            wktx = s+"|"+m if not strict else m if multi else s
            return re.match(wktx, wkt)

    class Azimuth:
        N = 'С %d° %d\' %d\"'
        NE = 'СВ %d° %d\' %d\"'
        E = 'В %d° %d\' %d\"'
        SE = 'ЮВ %d° %d\' %d\"'
        S = 'Ю %d° %d\' %d\"'
        SW = 'ЮЗ %d° %d\' %d\"'
        W = 'З %d° %d\' %d\"'
        NW = 'СЗ %d° %d\' %d\"'

        @classmethod
        def get(cls, value, is_radian=False):
            degrees = math.degrees(value) if is_radian else value
            gr = int(degrees)
            mi = int((degrees - gr) * 60)
            se = int((degrees - gr - mi / 60) * 60 * 60)

            if gr == 270 and mi == 0:
                return cls.W % (gr - 270, mi, se)

            if gr == 180 and mi == 0:
                return cls.S % (gr - 180, mi, se)

            if gr == 90 and mi == 0:
                return cls.E % (gr - 90, mi, se)

            if gr == 0 and mi == 0:
                return cls.N % (gr - 0, mi, se)

            if gr >= 270 and mi > 0:
                return cls.NW % (gr - 270, mi, se)

            if gr >= 180 and mi > 0:
                return cls.SW % (gr - 180, mi, se)

            if gr >= 90 and mi > 0:
                return cls.SE % (gr - 90, mi, se)

            if gr >= 0 and mi > 0:
                return cls.NE % (gr - 0, mi, se)

            return None

    class Algorithm:
        """общие алгоритмы"""

        @staticmethod
        def b_spline(curve, total, degree, closed):
            curve = numpy.asarray(curve)
            count = curve.shape[0]

            if closed:
                kv = numpy.arange(-degree, count + degree + 1)
                factor, fraction = divmod(count + degree + 1, count)
                curve = numpy.roll(numpy.concatenate((curve,) * factor + (curve[:fraction],)), -1, axis=0)
                degree = numpy.clip(degree, 1, degree)
            else:
                degree = numpy.clip(degree, 1, count - 1)
                kv = numpy.clip(numpy.arange(count + degree + 1) - degree, 0, count - degree)

            max_param = count - (degree * (1 - closed))
            spline = BSpline(kv, curve, degree)
            return spline(numpy.linspace(0, max_param, total))

        @staticmethod
        def bisector(a, b, c, plus_angles=None):
            """вычисляет биссектрису угла BAC в виде двух точек: A и точка на стороне BC или на её отражении на 180°"""
            a, b, c = (Utils.Geometry.as_point(p) for p in [a, b, c])
            ab, ac, bc = Utils.Geometry.cut(a, b), Utils.Geometry.cut(a, c), Utils.Geometry.cut(b, c)
            r = min(ab.length(), ac.length())
            d = 2*r
            n = 99

            a_circle = Utils.Geometry.line(QgsCircle().fromCenterDiameter(a, d).points(n))

            ab_center = ab.intersection(a_circle).vertexAt(0)
            ab_circle = QgsCircle().fromCenterDiameter(ab_center, d)

            ac_center = ac.intersection(a_circle).vertexAt(0)
            ac_circle = QgsCircle().fromCenterDiameter(ac_center, d)

            r, p1, p2 = ab_circle.intersections(ac_circle)
            x, m, y = Utils.qgis.utils().segmentIntersection(p1, p2, b, c)

            if plus_angles:
                total = sum(plus_angles)
                am = Utils.Geometry.cut(a, m)
                am.rotate(rotation=total, center=Utils.Geometry.as_pointXY(a))
                m = am.vertexAt(1)

            return a, m

    class System:
        """общие системные утилиты, которые можно использовать не только для написания плагинов QGIS"""

        @staticmethod
        def choose_folder():
            return QFileDialog.getExistingDirectory()

        @staticmethod
        def time_file(extension=None):
            name = time.strftime('%Y.%m.%d_%H-%M-%S')
            return '%s.%s' % (name, extension) if extension else name

        @staticmethod
        def time_folder(root):
            return os.path.join(root, Utils.System.time_file())

        @staticmethod
        def desktop_folder():
            return os.path.join(os.environ["USERPROFILE"], "Desktop")

        @staticmethod
        def qgis_plugin_folder():
            return os.environ['QGIS_PLUGINPATH'].split(';')[0]

        @staticmethod
        def new_file(folder, name):
            """создаёт новый файл с недостающими папками"""
            file_path = os.path.join(folder, name)
            if not os.path.exists(folder):
                os.makedirs(folder)
            with open(file_path, mode='w', encoding='utf-8'):
                pass
            return file_path

        @staticmethod
        def parse_tab_file(tab_file):
            """парсинк названий полей из tab-файла слоя карты MapInfo"""
            with open(tab_file, encoding='cp1251') as f:
                return [line.strip().replace(';', '').split(chr(32))[0]
                        for line in f.readlines() if line.strip().endswith(';')]

        @staticmethod
        def copy(src, trg, mask=None):
            """копирование всех файлов в папке, если не указана маска, иначе - только фалы соответствующие маске"""
            if not mask:
                shutil.copytree(src, trg)
            else:
                mask = mask.replace('*', '')
                for root, dirs, files in os.walk(src):
                    if dirs:
                        continue
                    for file in files:
                        if file.startswith(mask):
                            shutil.copyfile(os.path.join(root, file), os.path.join(trg, file))
