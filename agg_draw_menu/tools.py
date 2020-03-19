from qgis.PyQt.QtCore import Qt
from _lib.base_tool import BaseTool
from _lib.consts import  Keys as k
from _lib.utils import Utils


class PointTool(BaseTool):

    def __init__(self, canvas):
        BaseTool.__init__(self, canvas)
        self._line_color = Qt.blue

    @property
    def line_points(self):
        return []

    @property
    def poly_points(self):
        return []

    def collect_data(self):
        self._data = {}

    def collect_info(self):
        return 'один клик - одна точка\nдвойной клик - подтверждение\nклик правой кнопкой - отмена'


class LineTool(BaseTool):

    def __init__(self, canvas):
        BaseTool.__init__(self, canvas)
        self._line_color = Qt.darkGreen

    @property
    def line_points(self):
        return self.points

    @property
    def poly_points(self):
        return []

    def collect_data(self):
        self._data = {}

    def collect_info(self):
        return 'один клик - добавление сегмента\nдвойной клик - подтверждение\nклик правой кнопкой - отмена'


class PolygonTool(BaseTool):

    def __init__(self, canvas):
        BaseTool.__init__(self, canvas)
        self._poly_color = Qt.darkBlue

    @property
    def line_points(self):
        return []

    @property
    def poly_points(self):
        return self.points

    def collect_data(self):
        self._data = {}

    def collect_info(self):
        return 'один клик - добавление ребра\nдвойной клик - подтверждение\nклик правой кнопкой - отмена'


class FunctionTool(BaseTool):

    def __init__(self, canvas):
        BaseTool.__init__(self, canvas)
        self._poly_color = Qt.blue

    @property
    def line_points(self):
        return [Utils.Geometry.to_pointXY(*p)
                for p in Utils.Algorithm.b_spline(curve=self.points,
                                                  total=10 * (len(self.points)-1),
                                                  degree=5,
                                                  closed=False)]

    @property
    def poly_points(self):
        return []

    def collect_data(self):
        line_points = self.line_points
        self._data = {
            k.points: len(self.points),
            k.segments: len(list(zip(self.points[:-1], self.points[1:]))),
            k.total: len(line_points) - len(self.points),
            k.count: len(list(zip(line_points[:-1], line_points[1:]))),
            k.distance: self.line_band.asGeometry().length()
        }

    def collect_info(self):
        lw, lp, ls = 18, '.', ' '
        li = '\n' + 2*lw * lp

        self.collect_data()
        result = ''.ljust(lw, ls) + 'Информация:'.rjust(lw, ls)
        result += li
        result += '\n' + 'Точек выбрано'.ljust(lw, ls) + ('%d' % self._data[k.points]).rjust(lw, ls)
        result += '\n' + 'Точек добавлено'.ljust(lw, ls) + ('%d' % self._data[k.total]).rjust(lw, ls)
        result += '\n' + 'Сегментов сглажено'.ljust(lw, ls) + ('%d' % self._data[k.segments]).rjust(lw, ls)
        result += '\n' + 'Сегментов получено'.ljust(lw, ls) + ('%d' % self._data[k.count]).rjust(lw, ls)
        result += '\n' + 'Длина линии'.ljust(lw, ls) + ('%f' % self._data[k.distance]).rjust(lw, ls)
        result += li
        
        return result
