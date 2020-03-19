import os.path
from _lib.base_plugin import BaseDrawingPlugin
from _lib.consts import Messages as m, Keys as k, Tool
from _lib.utils import Utils
from .tools import PointTool, LineTool, PolygonTool, FunctionTool


class AggDrawMenu(BaseDrawingPlugin):

    def __init__(self, iface):
        super().__init__(iface=iface,
                         folder=os.path.dirname(__file__),
                         icon=u'pickaxe.png',
                         tool=u'Рисование',
                         tools=None,
                         dialog=None,
                         ui_file=None)
        self.tools = {
            k.Tool.point: {
                k.name: Tool.point,
                k.icon: self.q_icon('point.png'),
                k.callback: self.run_point,
                k.drawing_tool: PointTool
            },
            k.Tool.line: {
                k.name: Tool.line,
                k.icon: self.q_icon('line.png'),
                k.callback: self.run_line,
                k.drawing_tool: LineTool
            },
            k.Tool.polygon: {
                k.name: Tool.polygon,
                k.icon: self.q_icon('polygon.png'),
                k.callback: self.run_polygon,
                k.drawing_tool: PolygonTool
            },
            k.Tool.polyline_spline: {
                k.name: Tool.polyline_spline,
                k.icon: self.q_icon('dromedary.png'),
                k.callback: self.run_function,
                k.drawing_tool: FunctionTool
            }
        }

    @property
    def layer(self):
        """слой для сохранения результата рисования"""
        return Utils.Map.new_layer(name=self.active_tool[k.name],
                                   wkb_type=self.active_tool[k.wkb_type])

    def on_apply(self, data: dict):
        self.msg(m.READY)

    def run_point(self):
        self.active_tool = self.tools[k.Tool.point]
        self.run()

    def run_line(self):
        self.active_tool = self.tools[k.Tool.line]
        self.run()

    def run_polygon(self):
        self.active_tool = self.tools[k.Tool.polygon]
        self.run()

    def run_function(self):
        self.active_tool = self.tools[k.Tool.polyline_spline]
        self.run()
