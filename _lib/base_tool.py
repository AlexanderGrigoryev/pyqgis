from abc import ABCMeta, abstractmethod
from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand, QgsVertexMarker
from qgis.PyQt.QtWidgets import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.core import *
from .consts import Keys as k


class BaseTool(QgsMapToolEmitPoint):

    __metaclass__ = ABCMeta

    apply = pyqtSignal(dict)

    def _apply(self):
        self.collect_data() if not self._data else None
        self._data[k.geometry] = {
            k.line: self.line_band.asGeometry(),
            k.polygon: self.poly_band.asGeometry()
        }
        self.apply.emit(self._data)
        self.reset()

    def __init__(self, canvas):
        self.canvas = canvas
        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.replaced_tool = canvas.mapTool()
        self.points = []
        self.done = True
        self._line_band = None
        self._poly_band = None
        self._markers = []
        self._info = None
        self._line_color = Qt.black
        self._poly_color = Qt.lightGray
        self._data = {}

    @property
    def n_points(self):
        return len(self.points)

    @property
    def has_points(self):
        return self.n_points > 1

    @property
    def info(self):
        if not self._info:
            self._info = QLabel(parent=self.canvas)
            font = self._info.font()
            font.setPointSize(10)
            font.setFamily('Courier New')
            self._info.setFont(font)
            self._info.setStyleSheet('color: black')
        return self._info

    @property
    def line_band(self):
        if self._line_band is None:
            self._line_band = QgsRubberBand(self.canvas)
            self._line_band.setColor(self._line_color)
            self._line_band.setOpacity(1)
            self._line_band.setWidth(1)
            self._line_band.reset(QgsWkbTypes.LineGeometry)
        return self._line_band

    @property
    def poly_band(self):
        if self._poly_band is None:
            self._poly_band = QgsRubberBand(self.canvas)
            self._poly_band.setColor(self._poly_color)
            self._poly_band.setOpacity(0.1)
            self._poly_band.setWidth(0.1)
            self._poly_band.reset(QgsWkbTypes.PolygonGeometry)
        return self._poly_band

    @property
    def markers(self):
        if not self._markers:
            line_points = self.line_points
            for point in line_points:
                index = line_points.index(point)
                is_extreme_point = index == 0 or index == len(line_points)-1
                marker = QgsVertexMarker(self.canvas)
                marker.setColor(self._line_color)
                marker.setFillColor(self._poly_color if not is_extreme_point else Qt.red)
                marker.setOpacity(1)
                marker.setPenWidth(1)
                marker.setIconSize(5)
                marker.setIconType(QgsVertexMarker.ICON_CIRCLE)
                marker.setCenter(point)
                self._markers.append(marker)
        return self._markers

    @property
    @abstractmethod
    def line_points(self):
        """точки для отрисовки линии"""

    @property
    @abstractmethod
    def poly_points(self):
        """точки для отрисовки фона"""

    def draw(self):
        if not self.has_points:
            return

        self.reset()

        line_points = self.line_points
        for point in line_points:
            is_last_point = line_points.index(point) == len(line_points)-1
            self.line_band.addPoint(point, doUpdate=is_last_point)

        poly_points = self.poly_points
        for point in poly_points:
            is_last_point = poly_points.index(point) == len(poly_points)-1
            self.poly_band.addPoint(point, doUpdate=is_last_point)

        self.show()

    @abstractmethod
    def collect_data(self):
        """сбор данных для отправки клиенту"""

    @abstractmethod
    def collect_info(self):
        """ подготовка данных к отображению рядом с курсором мыши"""

    def show_info(self):
        self.info.hide()
        self.info.setText(self.collect_info())
        tl = self.canvas.mapToGlobal(self.canvas.rect().topLeft())
        self.info.move(QCursor.pos().x() + 15 - tl.x(), QCursor.pos().y() - tl.y())
        self.info.show()

    def reset(self):
        for marker in self.markers:
            marker.hide()
        self.markers.clear()
        self.line_band.reset(QgsWkbTypes.LineGeometry)
        self.poly_band.reset(QgsWkbTypes.PolygonGeometry)

    def show(self):
        for marker in self.markers:
            marker.show()
        self.line_band.show()
        self.poly_band.show()
        self.show_info()

    def set_done(self, clear):
        if clear:
            self.reset()
        else:
            self._apply()
        self.done = True
        self.points = []
        self.canvas.setMapTool(self.replaced_tool)
        self.canvas.refresh()
        self.info.hide()
        self._info = None

    def canvasPressEvent(self, e):
        if e.button() == Qt.RightButton:
            self.set_done(clear=True)
        if e.button() == Qt.LeftButton:
            self.done = False

    def canvasReleaseEvent(self, e):
        if self.done or e.button() != Qt.LeftButton:
            return
        p = self.toMapCoordinates(e.pos())
        self.points.append(p)
        self.done = False
        self.draw()

    def canvasMoveEvent(self, e):
        if self.done:
            return
        p = self.toMapCoordinates(e.pos())
        self.points.pop() if self.has_points else None
        self.points.append(p)
        self.done = False
        self.draw()

    def canvasDoubleClickEvent(self, e):
        if not self.done:
            self.set_done(clear=False)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.set_done(clear=True)
        if e.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.set_done(clear=False)

    def deactivate(self):
        if not self.done:
            self.set_done(clear=True)
        super(BaseTool, self).deactivate()
