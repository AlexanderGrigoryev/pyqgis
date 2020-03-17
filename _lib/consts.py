class Keys:
    """ключи доступа к словарным значениям"""

    name = 'name'
    icon = 'icon'
    callback = 'callback'
    dialog = 'dialog'
    geometry = 'geometry'

    class Tool:
        """ключи доступа к настройкам инструментов"""
        point = 'point'
        line = 'linestring'
        polygon = 'polygon'


class Header:
    """названия и заголовки полей таблицы атрибутов"""
    pass


class Tool:
    """названия инструментов"""
    MENU = u'&Простые примеры инструментов'
    point = u'Рисование точек'
    line = u'Рисование линий'
    polygon = u'Рисование многоугольников'


class Layer:
    """названия слоёв"""
    point = u'Слой точек'
    line = u'Слой линий'
    polygon = u'Слой многоугольников'


class Messages:
    """сообщения, вопросы и т.д."""
    READY = u'Готово'
    ERROR = u'Ошибка'
    OPEN_MAP = u'Откройте карту'
    CLOSE_MAP = u'Закройте карту'
    CHOOSE_OBJECT = u'Выберите один объект'
    CHOOSE_OBJECTS = u'Выберите один или несколько объектов'
    UNKNOWN_GEOMETRY_TYPE = u'Тип геометрии не обрабатывается инструментом'
