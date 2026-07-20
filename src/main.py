import sys


from PySide6.QtWidgets import QApplication


from ui.main_window import MainWindow



from diagnostics.disk_detector import detectar_discos
from diagnostics.smart_reader import leer_smart
from diagnostics.parser import parsear_smart



from modules.wii.scanner import WiiScanner
from modules.wii.models import WiiInfo
from modules.wii.analyzer import WiiAnalyzer





# ==========================
# ACTUALIZAR TODO
# ==========================


def actualizar_analisis(window):


    # Guarda automáticamente
    # el apartado actual

    pantalla_guardada = getattr(
        window,
        "pantalla_actual",
        "inicio"
    )



    window.analisis_iniciado()



    window.actualizar_progreso(
        10,
        "Preparando análisis..."
    )



    # ==========================
    # ANALISIS DISCOS
    # ==========================


    window.actualizar_progreso(
        20,
        "Buscando discos..."
    )



    discos = detectar_discos()



    window.actualizar_progreso(
        40,
        "Leyendo información SMART..."
    )  
    for disco in discos:


        smart = leer_smart(

            disco["dispositivo"]

        )



        datos = parsear_smart(

            smart

        )



        disco["estado"] = datos.get(

            "salud",

            "-"

        )



        disco["temperatura"] = datos.get(

            "temperatura",

            "-"

        )



        disco["horas"] = datos.get(

            "horas",

            "-"

        )



        disco["encendidos"] = datos.get(

            "encendidos",

            "-"

        )



        disco["vida"] = datos.get(

            "vida",

            "-"

        )



    window.actualizar_progreso(

        60,

        "Analizando Nintendo Wii..."

    )



    # ==========================
    # ANALISIS WII
    # ==========================


    datos_wii = analizar_wii()



    window.actualizar_progreso(

        80,

        "Guardando resultados..."

    ) 
        # ==========================
    # ACTUALIZAR DATOS EN PANTALLA
    # ==========================


    # Actualiza todos los datos internamente

    window.mostrar_discos(
        discos
    )


    window.mostrar_datos_wii(
        datos_wii
    )



    window.actualizar_progreso(

        100,

        "Análisis completado"

    )



    # ==========================
    # VOLVER A LA PANTALLA ANTERIOR
    # ==========================


    if pantalla_guardada == "discos":


        window.mostrar_discos(
            discos
        )


    elif pantalla_guardada == "wii":


        window.mostrar_datos_wii(
            datos_wii
        )



    window.analisis_finalizado() 
    # ==========================
# ANALIZAR NINTENDO WII
# ==========================


def analizar_wii():


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



        if (unidad / "wad").exists():

            info.wad = True




    analizador = WiiAnalyzer()



    resultado = analizador.analizar(

        info

    )



    return {


        "modelo":

        "Nintendo Wii",



        "estado":

        resultado.get(

            "estado",

            "-"

        ),



        "syscheck":

        "Encontrado"

        if info.syscheck

        else

        "No encontrado",



        "bootmii":

        "Encontrado"

        if info.bootmii

        else

        "No encontrado",



        "nand":

        "Encontrada"

        if info.nand

        else

        "No encontrada",



        "keys":

        "Encontrado"

        if info.keys

        else

        "No encontrado",



        "apps":

        "Encontrado"

        if info.apps

        else

        "No encontrado",



        "wad":

        "Encontrado"

        if info.wad

        else

        "No encontrado"

    } 
# ==========================
# INICIO PROGRAMA
# ==========================


def main():


    app = QApplication(
        sys.argv
    )



    window = MainWindow()



    # ==========================
    # ACTUALIZAR TODO
    # ==========================


    window.btn_actualizar.clicked.connect(

        lambda:

        actualizar_analisis(
            window
        )

    )



    # ==========================
    # ABRIR WII
    # ==========================


    window.btn_wii.clicked.connect(

        lambda:

        window.mostrar_datos_wii({

            "modelo":
            "Nintendo Wii",

            "estado":
            "Esperando análisis",

            "syscheck":
            "No analizado",

            "bootmii":
            "No analizado",

            "nand":
            "No analizado",

            "keys":
            "No analizado",

            "apps":
            "No analizado",

            "wad":
            "No analizado"

        })

    )



    # ==========================
    # ABRIR DISCOS
    # ==========================


    window.btn_discos.clicked.connect(

        lambda:

        window.mostrar_discos(

            detectar_discos()

        )

    )



    window.show()



    sys.exit(

        app.exec()

    )




if __name__ == "__main__":

    main() 
    