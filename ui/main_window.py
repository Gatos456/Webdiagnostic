from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QLabel,
    QFrame,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Web Diagnostic")
        self.resize(1200, 700)

        # ==========================
        # Widget principal
        # ==========================

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout()
        central.setLayout(main_layout)

        # ==========================
        # Barra lateral
        # ==========================

        sidebar = QWidget()
        sidebar.setFixedWidth(220)

        sidebar_layout = QVBoxLayout()
        sidebar.setLayout(sidebar_layout)

        titulo = QLabel("WEB\nDIAGNOSTIC")
        titulo.setStyleSheet("""
            font-size:22px;
            font-weight:bold;
        """)

        sidebar_layout.addWidget(titulo)

        sidebar_layout.addWidget(QPushButton("Inicio"))
        sidebar_layout.addWidget(QPushButton("Discos"))
        sidebar_layout.addWidget(QPushButton("Diagnóstico"))
        sidebar_layout.addWidget(QPushButton("Informes"))
        sidebar_layout.addWidget(QPushButton("Configuración"))

        sidebar_layout.addStretch()

        # ==========================
        # Panel principal
        # ==========================

        panel = QFrame()

        panel_layout = QVBoxLayout()
        panel.setLayout(panel_layout)

        titulo_panel = QLabel("Panel de diagnóstico")
        titulo_panel.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
        """)

        descripcion = QLabel(
            "Bienvenido a Web Diagnostic.\n\n"
            "Desde aquí podrás analizar discos duros y SSD,\n"
            "consultar su estado SMART y generar informes."
        )

        # ==========================
        # Tabla
        # ==========================

        self.tabla = QTableWidget()

        self.tabla.setColumnCount(5)

        self.tabla.setHorizontalHeaderLabels([
            "Disco",
            "Modelo",
            "Capacidad",
            "Estado",
            "Temperatura"
        ])

        self.tabla.setRowCount(0)

        # Ajustar columnas automáticamente
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Ocultar números de fila
        self.tabla.verticalHeader().setVisible(False)

        # Colores alternos
        self.tabla.setAlternatingRowColors(True)

        # Seleccionar fila completa
        self.tabla.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        # No permitir editar
        self.tabla.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        # ==========================
        # Añadir widgets
        # ==========================

        panel_layout.addWidget(titulo_panel)
        panel_layout.addWidget(descripcion)
        panel_layout.addWidget(self.tabla)
        panel_layout.addStretch()

        main_layout.addWidget(sidebar)
        main_layout.addWidget(panel)

    # ==========================
    # Mostrar discos
    # ==========================

    def mostrar_discos(self, discos):

        self.tabla.setRowCount(len(discos))

        for fila, disco in enumerate(discos):

            self.tabla.setItem(
                fila,
                0,
                QTableWidgetItem(f"Disco {fila}")
            )

            self.tabla.setItem(
                fila,
                1,
                QTableWidgetItem(disco["modelo"])
            )

            self.tabla.setItem(
                fila,
                2,
                QTableWidgetItem(disco["capacidad"])
            )

            self.tabla.setItem(
                fila,
                3,
                QTableWidgetItem("🟢 Detectado")
            )

            self.tabla.setItem(
                fila,
                4,
                QTableWidgetItem("-")
            )