# 					Инструкция по компиляции плагина
#
#
# 1. После установки QGIS установить в переменную PATH пути к папкам
#
# 	\qgis\bin\
# 	\qgis\apps\Python37\Scripts\
#
#
# 2. Структура папок с плагинами
#
# 	<plugins>\              	- рабочая папка проекта (клон из git-репозитория)
# 	    compiled                - папка с собранными плагинами и готовыми к установкев QGIS
# 		<plugin 1>\		        - папка с первым плагином QGIS
# 		<plugin 2>\             - папка со вторым плагином QGIS
# 		...
# 		<plugin N>\		        - папка с N-ным плагином QGIS
# 		compile.py		        - команда для компиляции и сборки всех плагинов в zip-файлы
#
#     название папки с плагином должно начинаться с приставки "agg_"
#
# 3. Компиляция/перекомпиляция все плагинов в проекте
#
# 	py compile.py
#
# 	3.1 вызвать в командной строке компиляцию всех плагинов
# 	3.2 проверить лог выполнения на экране на отсутствие ошибок
# 	3.3 проверить даты zip-файлов в папке compiled


if __name__ == "__main__":
    from .utils import Utils
    Utils.Compiler.execute()
