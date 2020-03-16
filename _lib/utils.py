import os
import zipfile
import shutil

from qgis.core import *
from qgis.utils import iface


class Utils:
    """общие утилиты для написания плагинов QGIS"""

    class Compiler:
        """компилятор плагинов"""

        @staticmethod
        def publish(plugin):
            plugin_path =os.environ['QGIS_PLUGINPATH'].split(';')[0]
            target = zipfile.ZipFile(".\\compiled\\%s.zip" % plugin, "r", zipfile.ZIP_DEFLATED)
            target.extractall(plugin_path)
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
        def layers():
            """список слоёв без групп"""
            return [node.layer() for node in QgsProject().instance().layerTreeRoot().children() if node.isLayer()]

        @staticmethod
        def groups():
            """список групп без слоёв"""
            return [node for node in QgsProject().instance().layerTreeRoot().children() if node.isGroup()]

        @staticmethod
        def selection(only_active=True):
            """список слоёв с наличием выбранных объектов"""
            layers = [iface.activeLayer()] if only_active else Utils.Map.layers()
            return [layer for layer in layers if len(layer.selectedFeatures()) > 0]

    class Feature:
        """общие методы для работы с фичами и их атрибутами"""

        @staticmethod
        def selection(only_active=True):
            """список выбранных фич"""
            return sum([layer.selectedFeatures() for layer in Utils.Map.selection(only_active)])

    class Geometry:
        """общие методы для работы с геометрией"""

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
        def point(x, y):
            """возвращает геометрию точки"""
            point_wkt = 'POINT(%f %f)' % (x, y)
            return QgsGeometry().fromWkt(point_wkt)

        @staticmethod
        def cut(a, b):
            """возвращает геометрию отрезка"""
            cut_wkt = 'LINESTRING(%f %f,%f %f)' % (a.x(), a.y(), b.x(), b.y())
            return QgsGeometry().fromWkt(cut_wkt)

        @staticmethod
        def line(points):
            """возвращает геометрию линии"""
            coord = ','.join(['%f %f' % (p.x(), p.y()) for p in points])
            line_wkt = 'LINESTRING(%s)' % coord
            return QgsGeometry().fromWkt(line_wkt)

        @staticmethod
        def polygon(points):
            """возвращает геометрию многоугольника"""
            coord = ','.join(['%f %f' % (p.x(), p.y()) for p in points])
            line_wkt = 'POLYGON((%s))' % coord
            return QgsGeometry().fromWkt(line_wkt)

        @classmethod
        def segments(cls, feature):
            """возвращает список сегментов фичи"""
            vertices = feature.geometry().vertices()
            points = []
            while vertices.hasNext():
                points.append(vertices.next())
            return [cls.cut(a, b) for a, b in list(zip(points[:-1], points[1:]))]

        @staticmethod
        def selection(only_active=True):
            """список геометрии выбранных фич"""
            return [feature.geometry() for feature in Utils.Feature.selection(only_active)]

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