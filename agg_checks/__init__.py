def classFactory(iface):
    from .plugin import AggChecks
    return AggChecks(iface)
