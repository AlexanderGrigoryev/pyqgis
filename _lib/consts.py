class Keys:
    """ключи доступа к словарным значениям"""

    title = 'title'
    name = 'name'
    icon = 'icon'
    callback = 'callback'
    dialog = 'dialog'
    geometry = 'geometry'
    segments = 'segments'
    feature = 'feature'
    features = 'features'
    layer = 'layer'
    wkb_type = 'wkb_type'
    wkt_single_type = 'wkt_single_type'
    wkt_multi_type = 'wkt_multi_type'
    renderer = 'renderer'
    symbol_layers = 'symbol_layers'
    bounds = 'bounds'
    center = 'center'
    moving = 'moving'
    dx = 'dx'
    dy = 'dy'
    points = 'points'
    values = 'values'
    settings = 'settings'
    properties = 'properties'
    symbol = 'symbol'
    lines = 'lines'
    borders = 'borders'
    lines_layer = 'lines_layer'
    borders_layer = 'borders_layer'
    ready = 'ready'
    action = 'action'
    next = 'next'
    cross = 'cross'
    space = 'space'
    from_line = 'from_line'
    from_point = 'from_point'
    to_point = 'to_point'
    distance = 'distance'
    save = 'save'
    inside = 'inside'
    outside = 'outside'
    mask = 'mask'

    class Tool:
        """ключи доступа к настройкам инструментов"""
        point = 'point'
        line = 'linestring'
        polygon = 'polygon'


class Header:
    """названия и заголовки полей таблицы атрибутов"""
    cut = 'Отрезок'
    distance = 'Длина'
    azimuth = 'Румб'  # см. определение в большой российской энциклопедии
    point = 'Точка'
    x = 'X'
    y = 'Y'


class Tool:
    """названия инструментов"""
    MENU = u'&ТомскНИПИнефть'
    point = u'Рисование точек'
    line = u'Рисование линий'
    polygon = u'Рисование многоугольников'


class Layer:
    """названия слоёв"""
    point = u'Слой точек'
    line = u'Слой линий'
    polygon = u'Слой многоугольников'


class SymbolProp:
    """свойства символьных слоёв"""

    # значения
    class value:
        interval = 'interval'
        firstvertex = 'firstvertex'
        lastvertex = 'lastvertex'

    # названия
    class ru:
        # общие
        angle = u'вращение'
        outline_color = u'цвет обводки'
        outline_width = u'толщина линий'
        outline_style = u'stroke style'
        marker = u'параметры маркера'
        line = u'параметры линии'
        # точка
        size = u'размер'
        color = u'цвет заливки'
        name = u'название маркера'
        font = u'шрифт'
        chr = u'символ'
        # линия
        line_color = u'цвет'
        line_style = u'stroke style'
        line_width = u'толщина линий'
        offset = u'смещение'
        offset_line = u'смещение линии'
        placement = u'размещение маркера'
        # полигон
        style = u'стиль заливки'
        spacing = u'spacing'
        displacement_x = u'горизонтальное смещение'
        displacement_y = 'вертикальное смещение'
        distance_x = 'горизонтальное расстояние'
        distance_y = 'вертикальное расстояние'

    # ключи
    class en:
        # общие
        angle = 'angle'
        joinstyle = 'joinstyle'
        offset = 'offset'
        offset_map_unit_scale = 'offset_map_unit_scale'
        offset_unit = 'offset_unit'
        outline_width = 'outline_width'
        outline_width_unit = 'outline_width_unit'
        outline_color = 'outline_color'
        outline_style = 'outline_style'
        marker = 'marker'
        line = 'line'
        # точка
        chr = 'chr'
        color = 'color'
        font = 'font'
        horizontal_anchor_point = 'horizontal_anchor_point'
        name = 'name'
        outline_width_map_unit_scale = 'outline_width_map_unit_scale'
        scale_method = 'scale_method'
        size = 'size'
        size_map_unit_scale = 'size_map_unit_scale'
        size_unit = 'size_unit'
        vertical_anchor_point = 'vertical_anchor_point'
        # линия
        capstyle = 'capstyle'
        customdash = 'customdash'
        customdash_map_unit_scale = 'customdash_map_unit_scale'
        customdash_unit = 'customdash_unit'
        draw_inside_polygon = 'draw_inside_polygon'
        line_color = 'line_color'
        line_style = 'line_style'
        line_width = 'line_width'
        line_width_unit = 'line_width_unit'
        ring_filter = 'ring_filter'
        use_custom_dash = 'use_custom_dash'
        width_map_unit_scale = 'width_map_unit_scale'
        placement = 'placement'
        interval = 'interval'
        interval_map_unit_scale = 'interval_map_unit_scale'
        interval_unit = 'interval_unit'
        offset_along_line = 'offset_along_line'
        offset_along_line_unit = 'offset_along_line_unit'
        offset_along_line_map_unit_scale = 'offset_along_line_map_unit_scale'
        # полигон
        style = 'style'
        border_width_map_unit_scale = 'border_width_map_unit_scale'
        distance = 'distance'
        distance_map_unit_scale = 'distance_map_unit_scale'
        distance_unit = 'distance_unit'
        displacement_x = 'displacement_x'
        displacement_x_map_unit_scale = 'displacement_x_map_unit_scale'
        displacement_x_unit = 'displacement_x_unit'
        displacement_y = 'displacement_y'
        displacement_y_map_unit_scale = 'displacement_y_map_unit_scale'
        displacement_y_unit = 'displacement_y_unit'
        distance_x = 'distance_x'
        distance_x_map_unit_scale = 'distance_x_map_unit_scale'
        distance_x_unit = 'distance_x_unit'
        distance_y = 'distance_y'
        distance_y_map_unit_scale = 'distance_y_map_unit_scale'
        distance_y_unit = 'distance_y_unit'


class Messages:
    """сообщения, вопросы и т.д."""
    READY = u'Готово'
    ERROR = u'Ошибка'
    OPEN_MAP = u'Откройте карту'
    CLOSE_MAP = u'Закройте карту'
    CHOOSE_OBJECT = u'Выберите один объект'
    CHOOSE_OBJECTS = u'Выберите один или несколько объектов'
    CHOOSE_POLYGON = u'Выберите полигон и примените инструмент'
    CHOOSE_ALIGN_MODE = u'Выберите границы выравнивания'
    SAVE_OR_DISCARD = u'Сохраните или отклоните изменения'
    UNKNOWN_GEOMETRY_TYPE = u'Тип геометрии не обрабатывается инструментом'
    UNKNOWN_RENDERER = u'Тип визуализатора "%s" не обрабатывается инструментом'
    PUT_IN_SELECTED_LAYER = u'для размещения сегментов будет использован выбранный слой'
    PUT_IN_NEW_LAYER = u'для размещения сегментов будет создан новый слой'
    INVALID_LAYER = u'Скопированный слой "%s" не открывается'
    BORDER_IN_LINES = u'Опорные и корректируемые линии должны быть разными'
    SAVE_EDITABLE = u'Есть не сохраненные изменения.\n\nСохранить?'
    DISCARD_EDITABLE = u'Отменить изменения?'
