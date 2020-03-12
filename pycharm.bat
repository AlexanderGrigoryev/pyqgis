rem ====================================================================================================================
rem					Инструкция по разработке плагина(ов)
rem
rem
rem 1. После установки QGIS добавить переменную окружения QGIS_PLUGINPATH, указав пути:
rem
rem        1.1 путь к плагинам по-умолчанию, например
rem        C:\Users\<you_name>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins
rem        В эту папку устанавливаются плагины через интерфейс QGIS
rem
rem        1.2 путь к разрабатываемым плагинам, т.е. к папке, с одним или несколькими плагинами.
rem        Эта же папка может быть рабочей копией проекта (git-репозитория)
rem
rem
rem 2. Для создания нового плагина используется плагин Plugin builder 3
rem
rem        2.1 установить Plugin builder 3 из репозитория QGIS.
rem        2.2 использовать Plugin builder 3, указав размещение нового плагина в рабочей папке проекта.
rem
rem
rem 3. Для применения изменений на стороне QGIS без перезапуска используется плагин Plugin reloader
rem
rem        3.1 установить Plugin reloader из репозитория QGIS
rem        3.2 после внесения изменений в код или интерфейс разрабатываемого плагина применить Plugin reloader
rem
rem
rem 4. Отладка кода разрабатываемого плагина
rem
rem        4.1 указать пути к QGIS и PyCharm в pycharm.bat
rem        4.2 запускать PyCharm, используя pycharm.
rem ====================================================================================================================



@echo off

rem указать путь к папке с установленным QGIS
set OSGEO4W_ROOT=

call "%OSGEO4W_ROOT%\bin\o4w_env.bat"
call "%OSGEO4W_ROOT%\bin\qt5_env.bat"
call "%OSGEO4W_ROOT%\bin\py3_env.bat"

path %OSGEO4W_ROOT%\apps\qgis\bin;%PATH%
set QGIS_PREFIX_PATH=%OSGEO4W_ROOT%\apps\qgis

set GDAL_FILENAME_IS_UTF8=YES

set VSI_CACHE=TRUE
set VSI_CACHE_SIZE=1000000
set QT_PLUGIN_PATH=%OSGEO4W_ROOT%\apps\qgis\qtplugins;%OSGEO4W_ROOT%\apps\qt5\plugins

rem указать путь к исполнямому файлу pycharm64.exe
set PYCHARM=

set PYTHONPATH=%OSGEO4W_ROOT%\apps\qgis\python
set PYTHONHOME=%OSGEO4W_ROOT%\apps\Python37
set PYTHONPATH=%OSGEO4W_ROOT%\apps\Python37\lib\site-packages;%PYTHONPATH%

set QT_QPA_PLATFORM_PLUGIN_PATH=%OSGEO4W_ROOT%\apps\Qt5\plugins\platforms
set QGIS_PREFIX_PATH=%OSGEO4W_ROOT%\apps\qgis

start "PyCharm aware of QGIS" /B %PYCHARM% %*