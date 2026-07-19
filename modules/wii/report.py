class WiiReport:

    def generar(self, resultado):

        texto = []

        texto.append("===== INFORME WII =====")
        texto.append("")
        texto.append(f"Estado: {resultado['estado']}")
        texto.append("")

        texto.append("Problemas:")

        if resultado["problemas"]:
            for problema in resultado["problemas"]:
                texto.append(f" - {problema}")
        else:
            texto.append(" Ninguno")

        texto.append("")
        texto.append("Recomendaciones:")

        if resultado["recomendaciones"]:
            for recomendacion in resultado["recomendaciones"]:
                texto.append(f" - {recomendacion}")
        else:
            texto.append(" Ninguna")

        return "\n".join(texto)