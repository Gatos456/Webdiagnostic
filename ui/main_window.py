from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QProgressBar,
    QFrame,
    QAbstractItemView,
    QStackedWidget
)

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPixmap


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Web Diagnostic")
        self.resize(1600, 900)

        self.pantalla_actual = "inicio"

        central = QWidget()
        self.setCentralWidget(central)

        principal = QHBoxLayout(central)
        principal.setContentsMargins(0, 0, 0, 0)
        principal.setSpacing(0)

        # ==========================
        # MENU LATERAL
        # ==========================

        menu = QWidget()
        menu.setFixedWidth(310)

        menu_layout = QVBoxLayout(menu)
        menu_layout.setContentsMargins(15, 15, 15, 15)
        menu_layout.setSpacing(10)

        titulo = QLabel("WEB\nDIAGNOSTIC")
        titulo.setStyleSheet("""
            font-size:38px;
            font-weight:bold;
        """)

        menu_layout.addWidget(titulo)

        # ==========================
        # BOTONES MENU
        # ==========================

        self.btn_inicio = QPushButton("Inicio")
        self.btn_discos = QPushButton("Discos")
        self.btn_wii = QPushButton("Nintendo Wii")
        self.btn_diagnostico = QPushButton("Diagnóstico")
        self.btn_informes = QPushButton("Informes")
        self.btn_configuracion = QPushButton("Configuración")

        botones = [
            self.btn_inicio,
            self.btn_discos,
            self.btn_wii,
            self.btn_diagnostico,
            self.btn_informes,
            self.btn_configuracion
        ]

        for boton in botones:
            boton.setFixedHeight(48)
            boton.setStyleSheet("""
                font-size:19px;
            """)
            menu_layout.addWidget(boton)

        menu_layout.addStretch()

        # ==========================
        # ACTUALIZAR
        # ==========================

        self.btn_actualizar = QPushButton("Actualizar análisis")
        self.btn_actualizar.setFixedHeight(55)
        self.btn_actualizar.setStyleSheet("""
            font-size:19px;
        """)

        menu_layout.addWidget(self.btn_actualizar)

        self.barra_progreso = QProgressBar()
        self.barra_progreso.setValue(0)

        menu_layout.addWidget(self.barra_progreso)

        self.estado = QLabel("Listo")
        self.estado.setStyleSheet("""
            font-size:18px;
        """)

        menu_layout.addWidget(self.estado)

        # ==========================
        # PANEL PRINCIPAL (STACKED WIDGET)
        # ==========================

        panel = QFrame()
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(20, 20, 20, 20)

        self.stack = QStackedWidget()

        # --------------------------
        # PÁGINA 1: TEXTO / INICIO (CON LOGO ARRIBA A LA DERECHA)
        # --------------------------
        self.pagina_texto = QWidget()
        layout_pag_texto = QVBoxLayout(self.pagina_texto)
        layout_pag_texto.setContentsMargins(0, 0, 0, 0)
        layout_pag_texto.setSpacing(10)

        # Encabezado horizontal para alinear los títulos a la izquierda y el logo a la derecha
        layout_encabezado = QHBoxLayout()
        layout_encabezado.setContentsMargins(0, 0, 0, 0)

        layout_titulos = QVBoxLayout()
        layout_titulos.setContentsMargins(0, 0, 0, 0)
        layout_titulos.setSpacing(5)

        self.titulo_panel = QLabel()
        self.titulo_panel.setStyleSheet("font-size:52px; font-weight:bold; margin:0px; padding:0px;")

        self.descripcion = QLabel()
        self.descripcion.setStyleSheet("font-size:30px; font-weight:bold; margin:0px; padding:0px;")

        layout_titulos.addWidget(self.titulo_panel)
        layout_titulos.addWidget(self.descripcion)

        # Logo superior derecho
        self.logo_label = QLabel()
        pixmap_logo = QPixmap("logo.png")
        if not pixmap_logo.isNull():
            self.logo_label.setPixmap(pixmap_logo.scaled(140, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        layout_encabezado.addLayout(layout_titulos)
        layout_encabezado.addStretch()
        layout_encabezado.addWidget(self.logo_label)

        self.texto_inicio = QLabel()
        self.texto_inicio.setWordWrap(True)
        self.texto_inicio.setStyleSheet("font-size:22px; line-height: 120%; margin:0px; padding:0px;")

        layout_pag_texto.addLayout(layout_encabezado)
        layout_pag_texto.addWidget(self.texto_inicio)
        layout_pag_texto.addStretch()

        # --------------------------
        # PÁGINA 2: TABLA DISCOS
        # --------------------------
        self.pagina_discos = QWidget()
        layout_pag_discos = QVBoxLayout(self.pagina_discos)
        layout_pag_discos.setContentsMargins(0, 0, 0, 0)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(8)
        self.tabla.setHorizontalHeaderLabels([
            "Disco", "Modelo", "Capacidad", "Estado",
            "Temperatura", "Horas", "Encendidos", "Vida SSD"
        ])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabla.setStyleSheet("""
            QTableWidget { font-size:20px; }
            QTableWidget::item { padding:10px; }
            QHeaderView::section { font-size:22px; font-weight:bold; height:40px; }
        """)
        layout_pag_discos.addWidget(self.tabla)

        # --------------------------
        # PÁGINA 3: TABLA WII
        # --------------------------
        self.pagina_wii = QWidget()
        layout_pag_wii = QVBoxLayout(self.pagina_wii)
        layout_pag_wii.setContentsMargins(0, 0, 0, 0)

        self.tabla_wii = QTableWidget()
        self.tabla_wii.setColumnCount(1)
        self.tabla_wii.setHorizontalHeaderLabels(["Diagnóstico Nintendo Wii"])
        self.tabla_wii.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_wii.verticalHeader().setVisible(False)
        self.tabla_wii.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabla_wii.setStyleSheet("""
            QTableWidget { font-size:20px; }
            QHeaderView::section { font-size:22px; font-weight:bold; }
        """)
        layout_pag_wii.addWidget(self.tabla_wii)

        # Añadir las vistas al Stack
        self.stack.addWidget(self.pagina_texto)   # Índice 0
        self.stack.addWidget(self.pagina_discos)  # Índice 1
        self.stack.addWidget(self.pagina_wii)     # Índice 2

        panel_layout.addWidget(self.stack)

        # ==========================
        # AÑADIR PANELES
        # ==========================

        principal.addWidget(menu)
        principal.addWidget(panel)

        # ==========================
        # CARGA INICIAL
        # ==========================

        self.mostrar_inicio_inicial()
        self.conectar_botones()

    # ==========================
    # PANTALLA INICIAL
    # ==========================

    def mostrar_inicio_inicial(self):

        self.pantalla_actual = "inicio"

        self.titulo_panel.setText("WEB DIAGNOSTIC")
        self.descripcion.setText("¿Qué es y para qué sirve?")

        texto = (
            "<b>Web Diagnostic</b><br>"
            "Aplicación creada para analizar y diagnosticar el estado de diferentes dispositivos y componentes del equipo.<br>"
            "Permite revisar hardware, detectar posibles problemas y mostrar información útil de una forma sencilla.<br>"
            "También permite generar informes con los resultados obtenidos de los análisis realizados.<br><br>"
            "<b>Creado por:</b><br>"
            "Adrián Gutiérrez y Daniel Durán"
        )

        self.texto_inicio.setText(texto)
        self.stack.setCurrentIndex(0)

    # ==========================
    # PANTALLA BOTON INICIO
    # ==========================

    def mostrar_inicio(self):

        self.pantalla_actual = "inicio"

        self.titulo_panel.setText("WEB DIAGNOSTIC")
        self.descripcion.setText("Funciones principales")

        texto = (
            "<b>• Discos:</b> Permite analizar discos HDD y SSD mediante información SMART, mostrando estado, temperatura, horas de uso y vida útil.<br>"
            "<b>• Nintendo Wii:</b> Permite comprobar el estado de una Nintendo Wii, revisando archivos importantes del sistema.<br>"
            "<b>• Diagnóstico:</b> Permite realizar análisis generales del equipo y mostrar posibles problemas.<br>"
            "<b>• Informes:</b> Permite crear informes con los resultados obtenidos de los análisis realizados.<br>"
            "<b>• Configuración:</b> Permite modificar opciones de la aplicación y personalizar su funcionamiento."
        )

        self.texto_inicio.setText(texto)
        self.stack.setCurrentIndex(0)

    # ==========================
    # MOSTRAR WII
    # ==========================

    def mostrar_datos_wii(self, datos):

        self.pantalla_actual = "wii"
        self.stack.setCurrentIndex(2)

        filas = [
            ("MODELO", datos.get("modelo", "-")),
            ("ESTADO", datos.get("estado", "-")),
            ("SYSCHECK", datos.get("syscheck", "-")),
            ("BOOTMII", datos.get("bootmii", "-")),
            ("NAND", datos.get("nand", "-")),
            ("KEYS.BIN", datos.get("keys", "-")),
            ("APPS", datos.get("apps", "-")),
            ("WAD", datos.get("wad", "-"))
        ]

        self.tabla_wii.setRowCount(len(filas))

        for fila, dato in enumerate(filas):
            texto = dato[0] + "\n\n" + str(dato[1])
            self.tabla_wii.setItem(fila, 0, QTableWidgetItem(texto))
            self.tabla_wii.setRowHeight(fila, 75)

    # ==========================
    # MOSTRAR DISCOS
    # ==========================

    def mostrar_discos(self, discos):

        self.pantalla_actual = "discos"
        self.stack.setCurrentIndex(1)

        self.tabla.setRowCount(len(discos))

        for fila, disco in enumerate(discos):
            datos = [
                "Disco " + str(fila + 1),
                disco.get("modelo", "-"),
                disco.get("capacidad", "-"),
                disco.get("estado", "-"),
                str(disco.get("temperatura", "-")) + " °C",
                str(disco.get("horas", "-")),
                str(disco.get("encendidos", "-")),
                str(disco.get("vida", "-")) + " %"
            ]

            for columna, valor in enumerate(datos):
                self.tabla.setItem(fila, columna, QTableWidgetItem(valor))

    # ==========================
    # CONEXIÓN BOTONES
    # ==========================

    def conectar_botones(self):

        self.btn_inicio.clicked.connect(self.mostrar_inicio)

    # ==========================
    # ESTADO ANALISIS
    # ==========================

    def analisis_iniciado(self):

        self.barra_progreso.setValue(0)
        self.estado.setText("Iniciando análisis...")

    def actualizar_progreso(self, porcentaje, mensaje):

        self.barra_progreso.setValue(porcentaje)
        self.estado.setText(mensaje)

    def analisis_finalizado(self):

        self.barra_progreso.setValue(100)
        self.estado.setText("Análisis completado")

        QTimer.singleShot(3000, lambda: self.estado.setText("Listo")) 
        