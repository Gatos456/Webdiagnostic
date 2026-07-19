from pathlib import Path


class WiiLoader:

    ARCHIVOS = {
        "syscheck": "sysCheck.csv",
        "nand": "nand.bin",
        "keys": "keys.bin",
        "boot_elf": "boot.elf",
        "boot_dol": "boot.dol"
    }

    CARPETAS = [
        "apps",
        "bootmii",
        "private",
        "wad"
    ]

    def cargar(self, unidad):

        unidad = Path(unidad)

        datos = {
            "archivos": {},
            "carpetas": {}
        }

        for nombre, archivo in self.ARCHIVOS.items():
            ruta = unidad / archivo
            datos["archivos"][nombre] = ruta if ruta.exists() else None

        for carpeta in self.CARPETAS:
            ruta = unidad / carpeta
            datos["carpetas"][carpeta] = ruta if ruta.exists() else None

        return datos