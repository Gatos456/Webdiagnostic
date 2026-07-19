from pathlib import Path
import string


class WiiScanner:

    def buscar_unidades(self):
        unidades = []

        for letra in string.ascii_uppercase:
            unidad = Path(f"{letra}:/")

            if unidad.exists():
                unidades.append(unidad)

        return unidades