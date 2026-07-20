import sys


from PySide6.QtWidgets import QApplication


from ui.main_window import MainWindow


from diagnostics.disk_detector import detectar_discos
from diagnostics.smart_reader import leer_smart
from diagnostics.parser import parsear_smart



from modules.wii.scanner import WiiScanner
from modules.wii.models import WiiInfo
from modules.wii.analyzer import WiiAnalyzer




def actualizar_analisis(window):

    window.analisis_iniciado()


    discos = detectar_discos()



    for disco in discos:


        smart = leer_smart(
            disco["dispositivo"]
        )


        datos = parsear_smart(
            smart
        )


        disco["estado"] = datos["salud"]

        disco["temperatura"] = datos["temperatura"]

        disco["horas"] = datos["horas"]

        disco["encendidos"] = datos["encendidos"]

        disco["vida"] = datos["vida"]



    window.mostrar_discos(
        discos
    )


    window.analisis_finalizado() 
    def analizar_wii(window):


    scanner = WiiScanner()


    unidades = scanner.buscar_unidades()



    info = WiiInfo()



    for unidad in unidades:



        if (unidad / "syscheck.csv").exists():

            info.syscheck = True



        if (unidad / "bootmii").exists():

            info.bootmii = True



        if (unidad / "keys.bin").exists():

            info.keys = True



        if (unidad / "nand.bin").exists():

            info.nand = True



        if (unidad / "apps").exists():

            info.apps = True



        if (unidad / "private").exists():

            info.private = True



        if (unidad / "wad").exists():

            info.wad = True




    analizador = WiiAnalyzer()



    resultado = analizador.analizar(
        info
    )



    texto = (
        "MODELO\n"
        "• Nintendo Wii detectada\n\n"

        "ESTADO\n"
        f"• {resultado['estado']}\n\n"

        "PROBLEMAS\n"
    )



    if len(resultado["problemas"]) == 0:

        texto += "• Ninguno\n"

    else:

        for problema in resultado["problemas"]:

            texto += f"• {problema}\n"




    texto += (
        "\nRECOMENDACIONES\n"
    )



    if len(resultado["recomendaciones"]) == 0:

        texto += "• Ninguna\n"

    else:

        for recomendacion in resultado["recomendaciones"]:

            texto += f"• {recomendacion}\n" 
                window.mostrar_datos_wii(
        {
            "modelo": "Nintendo Wii",
            "estado": resultado["estado"],
            "region": "-",
            "ios": texto
        }
    )




def main():


    app = QApplication(
        sys.argv
    )



    window = MainWindow()



    # Análisis inicial de discos

    actualizar_analisis(
        window
    )



    # Botón actualizar discos

    window.btn_actualizar.clicked.connect(
        lambda: actualizar_analisis(window)
    )



    # Botón Nintendo Wii

    window.btn_wii.clicked.connect(
        lambda: analizar_wii(window)
    ) 
        window.show()


    sys.exit(
        app.exec()
    )



if __name__ == "__main__":

    main() 
    