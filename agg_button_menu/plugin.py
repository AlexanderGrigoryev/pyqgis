import os.path
from _lib.base_plugin import BasePlugin
from _lib.base_dialog import BaseDialog
from _lib.consts import Keys as k, Tool


class AggButtonMenu(BasePlugin):

    def __init__(self, iface):
        super().__init__(iface=iface,
                         folder=os.path.dirname(__file__),
                         icon=u'rattle.png',
                         tool=u'Вызов меню по кнопке',
                         tools=None,
                         dialog=None,
                         ui_file=None)
        self.tools = {
            k.Tool.point: {
                k.name: Tool.point,
                k.icon: self.q_icon('point.png'),
                k.callback: self.run_point,
                k.dialog: 'point_dialog.ui'
            },
            k.Tool.line: {
                k.name: Tool.line,
                k.icon: self.q_icon('line.png'),
                k.callback: self.run_line,
                k.dialog: 'line_dialog.ui'
            },
            k.Tool.polygon: {
                k.name: Tool.polygon,
                k.icon: self.q_icon('polygon.png'),
                k.callback: self.run_polygon,
                k.dialog: 'polygon_dialog.ui'
            }
        }

    def run(self):
        self._dlg = self.q_dialog(dialog=BaseDialog,
                                  ui_file=self.active_tool[k.dialog],
                                  title=self.active_tool[k.name],
                                  icon=self.active_tool[k.icon])
        self._dlg.show()
        result = self._dlg.exec_()
        if result:
            self.msg(self.active_tool[k.name])

    def run_point(self):
        self.active_tool = self.tools[k.Tool.point]
        self.run()

    def run_line(self):
        self.active_tool = self.tools[k.Tool.line]
        self.run()

    def run_polygon(self):
        self.active_tool = self.tools[k.Tool.polygon]
        self.run()
