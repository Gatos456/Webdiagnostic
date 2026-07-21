# -*- coding: utf-8 -*-
import sys

from PySide6.QtWidgets import QApplication

from diagnostics.disk_detector import detectar_discos
from diagnostics.parser import parsear_smart
from diagnostics.smart_reader import leer_smart
from modules.wii.analyzer import WiiAnalyzer
from modules.wii.models import WiiInfo
from modules.wii.scanner import WiiScanner
from ui.main_window import MainWindow


def analizar_wii():
    """Busca archivos de respaldo Wii en las unidades conectadas."""
    scanner = WiiScanner()
    info = WiiInfo()

    for unidad in scanner.buscar_unidades():
        info.syscheck = info.syscheck or (unidad / "syscheck.csv").exists()
        info.bootmii = info.bootmii or (unidad / "bootmii").exists()
        info.keys = info.keys or (unidad / "keys.bin").exists()
        info.nand = info.nand or (unidad / "nand.bin").exists()
        info.apps = info.apps or (unidad / "apps").exists()
        info.wad = info.wad or (unidad / "wad").exists()

    resultado = WiiAnalyzer().analizar(info)
    return {
        "modelo": "Nintendo Wii",
        "estado": resultado.get("estado", "-"),
        "syscheck": "Encontrado" if info.syscheck else "No encontrado",
        "bootmii": "Encontrado" if info.bootmii else "No encontrado",
        "nand": "Encontrada" if info.nand else "No encontrada",
        "keys": "Encontrado" if info.keys else "No encontrado",
        "apps": "Encontrado" if info.apps else "No encontrado",
        "wad": "Encontrado" if info.wad else "No encontrado",
    }


def actualizar_analisis(window, app):
    """Actualiza discos y Wii, y vuelve a la página que el usuario estaba viendo."""
    pagina_anterior = window.pantalla_actual
    window.analisis_iniciado()
    app.processEvents()

    window.actualizar_progreso(20, "Buscando discos...")
    app.processEvents()
    discos = detectar_discos()

    window.actualizar_progreso(40, "Leyendo información SMART...")
    app.processEvents()
    for disco in discos:
        try:
            datos = parsear_smart(leer_smart(disco["dispositivo"]))
            disco["estado"] = datos.get("salud", "-")
            disco["temperatura"] = datos.get("temperatura", "-")
            disco["horas"] = datos.get("horas", "-")
            disco["encendidos"] = datos.get("encendidos", "-")
            disco["vida"] = datos.get("vida", "-")
        except Exception:
            disco.update({
                "estado": "No disponible", "temperatura": "-", "horas": "-",
                "encendidos": "-", "vida": "-",
            })

    window.actualizar_progreso(65, "Analizando Nintendo Wii...")
    app.processEvents()
    datos_wii = analizar_wii()

    window.actualizar_progreso(85, "Actualizando resultados...")
    app.processEvents()
    window.mostrar_discos(discos)
    window.mostrar_datos_wii(datos_wii)

    # Al terminar, se regresa exactamente a la sección desde la que se pulsó el botón.
    if pagina_anterior == "inicio":
        window.mostrar_inicio()
    elif pagina_anterior == "discos":
        window.mostrar_discos(discos)
    elif pagina_anterior == "wii":
        window.mostrar_datos_wii(datos_wii)
    elif pagina_anterior == "diagnostico":
        window.mostrar_diagnostico()
    elif pagina_anterior == "informes":
        window.mostrar_informes()
    elif pagina_anterior == "configuracion":
        window.mostrar_configuracion()

    window.analisis_finalizado()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.btn_actualizar.clicked.connect(lambda: actualizar_analisis(window, app))
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
s