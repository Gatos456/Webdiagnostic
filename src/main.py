import sys
import time

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow
from diagnostics.disk_detector import detectar_discos
from diagnostics.smart_reader import leer_smart
from diagnostics.parser import parsear_smart


def actualizar_analisis(window):

    window.analisis_iniciado()


    # Paso 1
    window.actualizar_progreso(
        20,
        "Detectando discos..."
    )

    discos = detectar_discos()

    time.sleep(0.5)


    if len(discos) == 0:

        window.actualizar_progreso(
            100,
            "No se encontraron discos"
        )

        window.analisis_finalizado()
        return


    total = len(discos)


    for posicion, disco in enumerate(discos):

        # Paso 2
        window.actualizar_progreso(
            40,
            "Leyendo información SMART..."
        )


        smart = leer_smart(
            disco["dispositivo"]
        )


        time.sleep(0.5)


        # Paso 3
        window.actualizar_progreso(
            70,
            "Analizando datos..."
        )


        datos = parsear_smart(smart)


        disco["estado"] = datos["salud"]
        disco["temperatura"] = datos["temperatura"]
        disco["horas"] = datos["horas"]
        disco["encendidos"] = datos["encendidos"]
        disco["vida"] = datos["vida"]


        progreso = 70 + int(
            ((posicion + 1) / total) * 20
        )


        window.actualizar_progreso(
            progreso,
            "Procesando discos..."
        )    # Mostrar resultados en la tabla

    window.mostrar_discos(discos)


    window.actualizar_progreso(
        100,
        "Análisis completado"
    )


    window.analisis_finalizado()



def main():

    app = QApplication(sys.argv)


    window = MainWindow()


    # Primer análisis al abrir la aplicación
    actualizar_analisis(window)


    # Botón actualizar análisis

    window.btn_actualizar.clicked.connect(
        lambda: actualizar_analisis(window)
    )


    window.show()


    sys.exit(app.exec())



if __name__ == "__main__":

    main()