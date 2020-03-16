class Keys:
    """ключи доступа к словарным значениям"""

    name = 'name'
    icon = 'icon'
    callback = 'callback'
    dialog = 'dialog'

    class Tool:
        """ключи доступа к настройкам инструментов"""
        point = 'point'
        line = 'line'
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


class Messages:
    """сообщения, вопросы и т.д."""
    READY = u'Готово'
    ERROR = u'Ошибка'
    OPEN_MAP = u'Откройте окно карты'
    CHOOSE_OBJECT = u'Выберите один объект'
    CHOOSE_OBJECTS = u'Выберите один или несколько объектов'
    UNKNOWN_GEOMETRY_TYPE = u'Тип геометрии не обрабатывается инструментом'
