# -*- coding: utf-8 -*-
from datetime import datetime
from pathlib import Path
from shutil import copy2

from PySide6.QtCore import QStandardPaths, QTimer, Qt
from PySide6.QtWidgets import (
    QAbstractItemView, QFrame, QHBoxLayout, QHeaderView, QLabel,
    QListWidget, QMainWindow, QMessageBox, QProgressBar, QPushButton,
    QStackedWidget, QTableWidget, QTableWidgetItem, QTextEdit,
    QVBoxLayout, QWidget,
)

from diagnostics.diagnostic_manager import realizar_diagnostico


class MainWindow(QMainWindow):
    """Ventana principal compatible con src/main.py."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Web Diagnostic")
        self.resize(1600, 900)
        self.pantalla_actual = "inicio"
        self._discos = []
        self._wii = self._datos_wii_vacios()
        self._diagnostico_realizado = False

        self.setStyleSheet("""
            QMainWindow, QWidget { background: #111827; color: #e5e7eb; }
            QPushButton { background: #1f2937; border: 1px solid #374151;
                border-radius: 8px; color: #f9fafb; padding: 8px 12px; }
            QPushButton:hover { background: #263548; border-color: #22c55e; }
            QPushButton:pressed { background: #14532d; }
            QTableWidget, QTextEdit, QListWidget { background: #0f172a;
                border: 1px solid #374151; border-radius: 8px; color: #e5e7eb; }
            QHeaderView::section { background: #1f2937; color: #f9fafb;
                border: 0; padding: 8px; }
            QProgressBar { background: #0f172a; border: 1px solid #374151;
                border-radius: 7px; text-align: center; min-height: 20px; }
            QProgressBar::chunk { background: #22c55e; border-radius: 6px; }
        """)

        central = QWidget()
        self.setCentralWidget(central)
        principal = QHBoxLayout(central)
        principal.setContentsMargins(0, 0, 0, 0)
        principal.setSpacing(0)

        menu = QWidget()
        menu.setFixedWidth(300)
        menu_layout = QVBoxLayout(menu)
        menu_layout.setContentsMargins(18, 22, 18, 18)
        menu_layout.setSpacing(10)
        marca = QLabel("WEB\nDIAGNOSTIC")
        marca.setStyleSheet("font-size: 34px; font-weight: 800;")
        menu_layout.addWidget(marca)

        self.btn_inicio = QPushButton("Inicio")
        self.btn_discos = QPushButton("Discos")
        self.btn_wii = QPushButton("Nintendo Wii")
        self.btn_diagnostico = QPushButton("Diagnóstico")
        self.btn_informes = QPushButton("Informes")
        self.btn_configuracion = QPushButton("Configuración")
        for boton in (self.btn_inicio, self.btn_discos, self.btn_wii,
                      self.btn_diagnostico, self.btn_informes, self.btn_configuracion):
            boton.setFixedHeight(48)
            boton.setStyleSheet("font-size: 17px; text-align: left;")
            menu_layout.addWidget(boton)

        menu_layout.addStretch()
        self.btn_actualizar = QPushButton("Actualizar análisis")
        self.btn_actualizar.setFixedHeight(54)
        self.btn_actualizar.setStyleSheet("font-size: 18px; font-weight: 700;")
        menu_layout.addWidget(self.btn_actualizar)
        self.barra_progreso = QProgressBar()
        self.barra_progreso.setRange(0, 100)
        menu_layout.addWidget(self.barra_progreso)
        self.estado = QLabel("Listo")
        self.estado.setStyleSheet("font-size: 15px; color: #9ca3af;")
        menu_layout.addWidget(self.estado)

        panel = QFrame()
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(28, 24, 28, 24)
        self.stack = QStackedWidget()
        panel_layout.addWidget(self.stack)
        principal.addWidget(menu)
        principal.addWidget(panel, 1)

        self._crear_paginas()
        self.conectar_botones()
        self.mostrar_inicio_inicial()

    def _crear_paginas(self):
        self.pagina_inicio = QWidget()
        layout = QVBoxLayout(self.pagina_inicio)
        self.titulo_panel = QLabel()
        self.titulo_panel.setStyleSheet("font-size: 46px; font-weight: 800;")
        self.descripcion = QLabel()
        self.descripcion.setStyleSheet("font-size: 25px; font-weight: 700; color: #a7f3d0;")
        self.texto_inicio = QLabel()
        self.texto_inicio.setWordWrap(True)
        self.texto_inicio.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.texto_inicio.setStyleSheet("font-size: 19px;")
        layout.addWidget(self.titulo_panel)
        layout.addWidget(self.descripcion)
        layout.addWidget(self.texto_inicio)
        layout.addStretch()

        self.pagina_discos = QWidget()
        layout = QVBoxLayout(self.pagina_discos)
        self.tabla = QTableWidget(0, 8)
        self.tabla.setHorizontalHeaderLabels([
            "Disco", "Modelo", "Capacidad", "Estado", "Temperatura",
            "Horas", "Encendidos", "Vida SSD",
        ])
        self._preparar_tabla(self.tabla)
        layout.addWidget(self.tabla)

        self.pagina_wii = QWidget()
        layout = QVBoxLayout(self.pagina_wii)
        self.tabla_wii = QTableWidget(0, 1)
        self.tabla_wii.setHorizontalHeaderLabels(["Diagnóstico Nintendo Wii"])
        self._preparar_tabla(self.tabla_wii)
        layout.addWidget(self.tabla_wii)

        self.pagina_diagnostico = QWidget()
        layout = QVBoxLayout(self.pagina_diagnostico)
        titulo = QLabel("DIAGNÓSTICO")
        titulo.setStyleSheet("font-size: 42px; font-weight: 800;")
        subtitulo = QLabel("Análisis general del equipo")
        subtitulo.setStyleSheet("font-size: 22px; font-weight: 700; color: #a7f3d0;")
        self.btn_diagnosticar = QPushButton("Diagnosticar")
        self.btn_diagnosticar.setFixedHeight(52)
        self.btn_diagnosticar.setStyleSheet("font-size: 18px; font-weight: 700;")
        self.resultado_diagnostico = QTextEdit()
        self.resultado_diagnostico.setReadOnly(True)
        self.resultado_diagnostico.setStyleSheet("font-size: 17px; padding: 10px;")
        self.resultado_diagnostico.setPlainText("Pulsa «Diagnosticar» para comenzar el análisis.")
        self.btn_crear_informe = QPushButton("Crear informe")
        self.btn_crear_informe.setFixedHeight(52)
        self.btn_crear_informe.setStyleSheet("font-size: 18px; font-weight: 700;")
        layout.addWidget(titulo)
        layout.addWidget(subtitulo)
        layout.addWidget(self.btn_diagnosticar)
        layout.addWidget(self.resultado_diagnostico, 1)
        layout.addWidget(self.btn_crear_informe)

        self.pagina_informes = self._crear_pagina_informes()
        self.pagina_configuracion = self._pagina_simple(
            "CONFIGURACIÓN", "Aquí se configurarán las opciones de Web Diagnostic."
        )
        for pagina in (self.pagina_inicio, self.pagina_discos, self.pagina_wii,
                       self.pagina_diagnostico, self.pagina_informes,
                       self.pagina_configuracion):
            self.stack.addWidget(pagina)

    def _crear_pagina_informes(self):
        pagina = QWidget()
        principal = QHBoxLayout(pagina)
        principal.setSpacing(16)
        izquierda = QVBoxLayout()
        titulo = QLabel("INFORMES")
        titulo.setStyleSheet("font-size: 42px; font-weight: 800;")
        ayuda = QLabel("Puedes seleccionar varios informes con Ctrl + clic o Mayús + clic.")
        ayuda.setWordWrap(True)
        ayuda.setStyleSheet("font-size: 16px; color: #d1d5db;")
        self.lista_informes = QListWidget()
        self.lista_informes.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.lista_informes.setStyleSheet("font-size: 16px; padding: 6px;")
        self.btn_actualizar_informes = QPushButton("Actualizar lista")
        self.btn_descargar_informe = QPushButton("Descargar informe")
        self.btn_eliminar_informe = QPushButton("Eliminar informe")
        for boton in (self.btn_actualizar_informes, self.btn_descargar_informe,
                      self.btn_eliminar_informe):
            boton.setFixedHeight(48)
            boton.setStyleSheet("font-size: 17px; font-weight: 700;")
        self.btn_eliminar_informe.setStyleSheet(
            "font-size: 17px; font-weight: 700; border-color: #dc2626;"
        )
        izquierda.addWidget(titulo)
        izquierda.addWidget(ayuda)
        izquierda.addWidget(self.lista_informes, 1)
        izquierda.addWidget(self.btn_actualizar_informes)
        izquierda.addWidget(self.btn_descargar_informe)
        izquierda.addWidget(self.btn_eliminar_informe)

        derecha = QVBoxLayout()
        vista_titulo = QLabel("Vista del informe")
        vista_titulo.setStyleSheet("font-size: 22px; font-weight: 700; color: #a7f3d0;")
        self.vista_informe = QTextEdit()
        self.vista_informe.setReadOnly(True)
        self.vista_informe.setStyleSheet("font-size: 16px; padding: 10px;")
        self.vista_informe.setPlainText("Todavía no hay ningún informe creado.")
        derecha.addWidget(vista_titulo)
        derecha.addWidget(self.vista_informe, 1)
        principal.addLayout(izquierda, 1)
        principal.addLayout(derecha, 2)
        return pagina

    @staticmethod
    def _pagina_simple(titulo, texto):
        pagina = QWidget()
        layout = QVBoxLayout(pagina)
        encabezado = QLabel(titulo)
        encabezado.setStyleSheet("font-size: 42px; font-weight: 800;")
        contenido = QLabel(texto)
        contenido.setStyleSheet("font-size: 20px; color: #d1d5db;")
        layout.addWidget(encabezado)
        layout.addWidget(contenido)
        layout.addStretch()
        return pagina

    @staticmethod
    def _preparar_tabla(tabla):
        tabla.setAlternatingRowColors(True)
        tabla.setSelectionBehavior(QAbstractItemView.SelectRows)
        tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
        tabla.verticalHeader().setVisible(False)
        tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tabla.setStyleSheet(
            "QTableWidget { font-size: 17px; } QTableWidget::item { padding: 10px; }"
            "QHeaderView::section { font-size: 18px; font-weight: 700; height: 42px; }"
        )

    def mostrar_inicio_inicial(self):
        self.pantalla_actual = "inicio"
        self.titulo_panel.setText("WEB DIAGNOSTIC")
        self.descripcion.setText("¿Qué es y para qué sirve?")
        self.texto_inicio.setText(
            "<b>Web Diagnostic</b><br><br>Aplicación para analizar discos, "
            "Nintendo Wii y otros dispositivos.<br><br>También permite realizar "
            "un diagnóstico general y crear informes automáticos.<br><br>"
            "<b>Creado por:</b><br>Adrián Gutiérrez y Daniel Durán"
        )
        self.stack.setCurrentIndex(0)

    def mostrar_inicio(self):
        self.pantalla_actual = "inicio"
        self.titulo_panel.setText("WEB DIAGNOSTIC")
        self.descripcion.setText("Funciones principales")
        self.texto_inicio.setText(
            "<b>Discos</b><br>Analiza HDD y SSD mediante información SMART.<br><br>"
            "<b>Nintendo Wii</b><br>Comprueba archivos importantes de una Wii.<br><br>"
            "<b>Diagnóstico</b><br>Realiza un análisis general del equipo.<br><br>"
            "<b>Informes</b><br>Guarda, descarga y elimina informes."
        )
        self.stack.setCurrentIndex(0)

    def mostrar_discos(self, discos):
        self._discos = discos
        self.pantalla_actual = "discos"
        self.tabla.setRowCount(len(discos))
        for fila, disco in enumerate(discos):
            datos = [f"Disco {fila + 1}", disco.get("modelo", "-"),
                     disco.get("capacidad", "-"), disco.get("estado", "-"),
                     f'{disco.get("temperatura", "-")} °C', str(disco.get("horas", "-")),
                     str(disco.get("encendidos", "-")), f'{disco.get("vida", "-")} %']
            for columna, valor in enumerate(datos):
                self.tabla.setItem(fila, columna, QTableWidgetItem(str(valor)))
        self.stack.setCurrentIndex(1)

    def mostrar_datos_wii(self, datos):
        self._wii = datos
        self.pantalla_actual = "wii"
        filas = [("MODELO", datos.get("modelo", "-")), ("ESTADO", datos.get("estado", "-")),
                 ("SYSCHECK", datos.get("syscheck", "-")), ("BOOTMII", datos.get("bootmii", "-")),
                 ("NAND", datos.get("nand", "-")), ("KEYS.BIN", datos.get("keys", "-")),
                 ("APPS", datos.get("apps", "-")), ("WAD", datos.get("wad", "-"))]
        self.tabla_wii.setRowCount(len(filas))
        for fila, (titulo, valor) in enumerate(filas):
            self.tabla_wii.setItem(fila, 0, QTableWidgetItem(f"{titulo}\n\n{valor}"))
            self.tabla_wii.setRowHeight(fila, 76)
        self.stack.setCurrentIndex(2)

    def mostrar_diagnostico(self):
        self.pantalla_actual = "diagnostico"
        self.stack.setCurrentIndex(3)

    def realizar_diagnostico(self):
        self.resultado_diagnostico.setPlainText("Realizando diagnóstico...")
        try:
            resultado = realizar_diagnostico()
            texto = "DIAGNÓSTICO COMPLETADO\n\n"
            for categoria, datos in resultado.items():
                texto += f"{categoria}\n{'-' * 40}\n"
                for nombre, valor in datos.items():
                    texto += f"{nombre}: {valor}\n"
                texto += "\n"
            self.resultado_diagnostico.setPlainText(texto)
            self._diagnostico_realizado = True
            self.estado.setText("Diagnóstico completado")
        except Exception as error:
            self.resultado_diagnostico.setPlainText(f"Error realizando diagnóstico:\n\n{error}")
            self.estado.setText("Error en diagnóstico")

    def crear_informe(self):
        if not self._diagnostico_realizado:
            self.estado.setText("Primero realiza el diagnóstico")
            return
        momento = datetime.now()
        ruta = self._carpeta_informes() / f"informe_{momento:%Y-%m-%d_%H-%M-%S}.txt"
        ruta.write_text(self._construir_informe(momento), encoding="utf-8")
        self.actualizar_lista_informes(ruta)
        self.estado.setText("Informe creado")

    @staticmethod
    def _carpeta_informes():
        carpeta = Path.cwd() / "reports"
        carpeta.mkdir(exist_ok=True)
        return carpeta

    def _construir_informe(self, momento):
        lineas = ["WEB DIAGNOSTIC - INFORME", "=" * 48,
                  f"Fecha: {momento:%d/%m/%Y %H:%M:%S}", "",
                  "DIAGNÓSTICO GENERAL", "-" * 48,
                  self.resultado_diagnostico.toPlainText(), "",
                  "DISCOS DETECTADOS", "-" * 48]
        if self._discos:
            for numero, disco in enumerate(self._discos, 1):
                lineas.append(f"Disco {numero}: {disco.get('modelo', '-')}")
                for campo in ("capacidad", "estado", "temperatura", "horas", "encendidos", "vida"):
                    lineas.append(f"  {campo.capitalize()}: {disco.get(campo, '-')}")
        else:
            lineas.append("No se han analizado discos todavía.")
        lineas.extend(["", "NINTENDO WII", "-" * 48])
        for clave in ("modelo", "estado", "syscheck", "bootmii", "nand", "keys", "apps", "wad"):
            lineas.append(f"{clave.upper()}: {self._wii.get(clave, '-')}")
        return "\n".join(lineas) + "\n"

    def mostrar_informes(self):
        self._mostrar_pagina("informes", 4)
        self.actualizar_lista_informes()

    def actualizar_lista_informes(self, seleccionar=None):
        self.lista_informes.clear()
        informes = sorted(self._carpeta_informes().glob("informe_*.txt"), reverse=True)
        if not informes:
            self.vista_informe.setPlainText("Todavía no hay ningún informe creado.")
            return
        for ruta in informes:
            self.lista_informes.addItem(ruta.stem.replace("informe_", "Informe ").replace("_", " "))
            item = self.lista_informes.item(self.lista_informes.count() - 1)
            item.setData(Qt.UserRole, str(ruta))
            if ruta == seleccionar:
                self.lista_informes.setCurrentItem(item)
        if self.lista_informes.currentItem() is None:
            self.lista_informes.setCurrentRow(0)
        self.abrir_informe_seleccionado()

    def abrir_informe_seleccionado(self):
        ruta = self._ruta_informe_seleccionado()
        if ruta is None:
            return
        try:
            self.vista_informe.setPlainText(ruta.read_text(encoding="utf-8"))
        except OSError as error:
            self.vista_informe.setPlainText(f"No se pudo abrir el informe:\n{error}")

    def _ruta_informe_seleccionado(self):
        item = self.lista_informes.currentItem()
        return Path(item.data(Qt.UserRole)) if item else None

    def _rutas_informes_seleccionados(self):
        return [Path(item.data(Qt.UserRole)) for item in self.lista_informes.selectedItems()]

    def descargar_informe(self):
        origenes = [ruta for ruta in self._rutas_informes_seleccionados() if ruta.exists()]
        if not origenes:
            self.estado.setText("Selecciona uno o más informes")
            return
        descargas = Path(QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.DownloadLocation
        ))
        descargas.mkdir(parents=True, exist_ok=True)
        try:
            for origen in origenes:
                destino = descargas / origen.name
                numero = 1
                while destino.exists():
                    destino = descargas / f"{origen.stem}_{numero}{origen.suffix}"
                    numero += 1
                copy2(origen, destino)
            self.estado.setText(f"{len(origenes)} informe(s) guardado(s) en Descargas")
        except OSError as error:
            self.estado.setText("No se pudo descargar el informe")
            self.vista_informe.append(f"\n\nError al descargar:\n{error}")

    def eliminar_informe(self):
        rutas = [ruta for ruta in self._rutas_informes_seleccionados() if ruta.exists()]
        if not rutas:
            self.estado.setText("Selecciona uno o más informes")
            return
        respuesta = QMessageBox.question(
            self, "Eliminar informes",
            f"¿Quieres eliminar {len(rutas)} informe(s) seleccionado(s)?\n\n"
            "Esta acción no se puede deshacer.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if respuesta != QMessageBox.StandardButton.Yes:
            return
        try:
            for ruta in rutas:
                ruta.unlink()
            self.actualizar_lista_informes()
            self.estado.setText(f"{len(rutas)} informe(s) eliminado(s)")
        except OSError as error:
            self.estado.setText("No se pudo eliminar el informe")
            self.vista_informe.append(f"\n\nError al eliminar:\n{error}")

    def conectar_botones(self):
        self.btn_inicio.clicked.connect(self.mostrar_inicio)
        self.btn_discos.clicked.connect(lambda: self.mostrar_discos(self._discos))
        self.btn_wii.clicked.connect(lambda: self.mostrar_datos_wii(self._wii))
        self.btn_diagnostico.clicked.connect(self.mostrar_diagnostico)
        self.btn_informes.clicked.connect(self.mostrar_informes)
        self.btn_configuracion.clicked.connect(self.mostrar_configuracion)
        self.btn_diagnosticar.clicked.connect(self.realizar_diagnostico)
        self.btn_crear_informe.clicked.connect(self.crear_informe)
        self.btn_actualizar_informes.clicked.connect(self.actualizar_lista_informes)
        self.btn_descargar_informe.clicked.connect(self.descargar_informe)
        self.btn_eliminar_informe.clicked.connect(self.eliminar_informe)
        self.lista_informes.itemSelectionChanged.connect(self.abrir_informe_seleccionado)

    def _mostrar_pagina(self, nombre, indice):
        self.pantalla_actual = nombre
        self.stack.setCurrentIndex(indice)

    def mostrar_configuracion(self):
        self._mostrar_pagina("configuracion", 5)

    def analisis_iniciado(self):
        self.barra_progreso.setValue(0)
        self.estado.setText("Preparando análisis...")

    def actualizar_progreso(self, porcentaje, mensaje):
        self.barra_progreso.setValue(porcentaje)
        self.estado.setText(mensaje)

    def analisis_finalizado(self):
        self.barra_progreso.setValue(100)
        self.estado.setText("Análisis completado")
        QTimer.singleShot(3000, lambda: self.estado.setText("Listo"))

    @staticmethod
    def _datos_wii_vacios():
        return {"modelo": "Nintendo Wii", "estado": "Esperando análisis",
                "syscheck": "No analizado", "bootmii": "No analizado",
                "nand": "No analizado", "keys": "No analizado",
                "apps": "No analizado", "wad": "No analizado"}
