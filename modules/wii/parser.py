from .models import WiiInfo


class WiiParser:

    def parsear(self, datos):

        info = WiiInfo()

        info.syscheck = datos["archivos"]["syscheck"] is not None
        info.nand = datos["archivos"]["nand"] is not None
        info.keys = datos["archivos"]["keys"] is not None

        info.bootmii = datos["carpetas"]["bootmii"] is not None
        info.apps = datos["carpetas"]["apps"] is not None
        info.private = datos["carpetas"]["private"] is not None
        info.wad = datos["carpetas"]["wad"] is not None

        return info