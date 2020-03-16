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
    point = u'Рисование точкек'
    line = u'Рисование линий'
    polygon = u'Рисование многоугольников'


class Messages:
    """сообщения, вопросы и т.д."""
    READY = u'Готово'
