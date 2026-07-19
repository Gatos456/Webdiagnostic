class WiiAnalyzer:

    def analizar(self, info):

        problemas = []
        recomendaciones = []

        if not info.syscheck:
            problemas.append("No se encontró sysCheck.csv")

        if not info.bootmii:
            problemas.append("BootMii no encontrado")

        if not info.nand:
            recomendaciones.append("Crear una copia de la NAND")

        if not info.keys:
            recomendaciones.append("Guardar keys.bin")

        if len(problemas) == 0:
            estado = "Excelente"
        elif len(problemas) <= 2:
            estado = "Bueno"
        else:
            estado = "Crítico"

        return {
            "estado": estado,
            "problemas": problemas,
            "recomendaciones": recomendaciones
        }