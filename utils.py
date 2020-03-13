import os
import zipfile


class Utils:
    """общие утилиты для написания плагинов QGIS"""

    class Compiler:
        """компилятор плагинов"""

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
        def execute(cls, prefix):
            root = '.'
            plugins = [folder for folder in os.listdir(root) if cls.is_plugin(root, folder, prefix)]
            compiler = "call py -m PyQt5.pyrcc_main -o .\\{0}\\resources.py .\\{0}\\resources.qrc"
            for plugin in plugins:
                os.system(compiler.format(plugin))
                cls.zip_plugin(plugin)

