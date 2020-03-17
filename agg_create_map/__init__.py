def classFactory(iface):
    from .plugin import AggCreateMap
    return AggCreateMap(iface)
