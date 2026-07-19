import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow
from diagnostics.disk_detector import detectar_discos
from diagnostics.smart_reader import leer_smart
from diagnostics.parser import parsear_smart


def actualizar_analisis(window):

    window.analisis_iniciado()

    discos = detectar_discos()

    for disco in discos:

        smart = leer_smart(disco["dispositivo"])

        datos = parsear_smart(smart)

        disco["estado"] = datos["salud"]
        disco["temperatura"] = datos["temperatura"]
        disco["horas"] = datos["horas"]
        disco["encendidos"] = datos["encendidos"]
        disco["vida"] = datos["vida"]

    window.mostrar_discos(discos)

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