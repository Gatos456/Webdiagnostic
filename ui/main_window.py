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
    QAbstractItemView,
    QProgressBar
)

from PySide6.QtCore import QTimer


class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Web Diagnostic")
        self.resize(1400, 700)


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
        # Botón actualizar
        # ==========================

        self.btn_actualizar = QPushButton(
            "Actualizar análisis"
        )

        self.btn_actualizar.setFixedHeight(45)


        sidebar_layout.addWidget(
            self.btn_actualizar
        )



        # ==========================
        # Barra de progreso
        # ==========================

        self.barra_progreso = QProgressBar()


        self.barra_progreso.setMinimum(0)
        self.barra_progreso.setMaximum(100)
        self.barra_progreso.setValue(0)


        sidebar_layout.addWidget(
            self.barra_progreso
        )



        # ==========================
        # Estado
        # ==========================

        self.estado = QLabel(
            "Listo"
        )


        self.estado.setStyleSheet("""
            font-size:12px;
            color:gray;
        """)


        sidebar_layout.addWidget(
            self.estado )      
         # ==========================
        # Panel principal
        # ==========================

        panel = QFrame()


        panel_layout = QVBoxLayout()
        panel.setLayout(
            panel_layout
        )


        titulo_panel = QLabel(
            "Panel de diagnóstico"
        )


        titulo_panel.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
        """)


        descripcion = QLabel(
            "Bienvenido a Web Diagnostic.\n\n"
            "Información SMART de discos HDD y SSD."
        )



        # ==========================
        # Tabla discos
        # ==========================

        self.tabla = QTableWidget()


        self.tabla.setColumnCount(8)


        self.tabla.setHorizontalHeaderLabels([
            "Disco",
            "Modelo",
            "Capacidad",
            "Estado",
            "Temperatura",
            "Horas",
            "Encendidos",
            "Vida SSD"
        ])


        self.tabla.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )


        self.tabla.verticalHeader().setVisible(False)


        self.tabla.setAlternatingRowColors(True)


        self.tabla.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )


        self.tabla.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )



        panel_layout.addWidget(
            titulo_panel
        )


        panel_layout.addWidget(
            descripcion
        )


        panel_layout.addWidget(
            self.tabla
        )



        main_layout.addWidget(
            sidebar
        )


        main_layout.addWidget(
            panel
        )



    # ==========================
    # Mostrar discos
    # ==========================

    def mostrar_discos(self, discos):

        self.tabla.setRowCount(
            len(discos)
        )


        for fila, disco in enumerate(discos):

            datos = [
                f"Disco {fila + 1}",
                disco.get("modelo", "-"),
                disco.get("capacidad", "-"),
                disco.get("estado", "-"),
                f'{disco.get("temperatura", "-")} °C',
                str(disco.get("horas", "-")),
                str(disco.get("encendidos", "-")),
                f'{disco.get("vida", "-")} %'
            ]


            for columna, valor in enumerate(datos):

                self.tabla.setItem(
                    fila,
                    columna,
                    QTableWidgetItem(valor)
                )
                    # ==========================
    # Control de análisis
    # ==========================

    def analisis_iniciado(self):

        self.estado.setText(
            "Analizando..."
        )

        self.barra_progreso.setValue(
            0
        )

        self.btn_actualizar.setEnabled(
            False
        )



    def actualizar_progreso(
            self,
            porcentaje,
            mensaje
    ):

        self.barra_progreso.setValue(
            porcentaje
        )

        self.estado.setText(
            mensaje
        )



    def analisis_finalizado(self):

        self.barra_progreso.setValue(
            100
        )

        self.estado.setText(
            "Análisis completado"
        )

        self.btn_actualizar.setEnabled(
            True
        )


        QTimer.singleShot(
            3000,
            lambda: (
                self.barra_progreso.setValue(0),
                self.estado.setText("Listo")
            )
        )