from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QLabel
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Web Diagnostic")
        self.resize(1200, 700)

        # Widget principal
        central = QWidget()
        self.setCentralWidget(central)

        # Layout principal horizontal
        main_layout = QHBoxLayout()
        central.setLayout(main_layout)

        # -------- BARRA LATERAL --------

        sidebar = QWidget()
        sidebar.setFixedWidth(220)

        sidebar_layout = QVBoxLayout()
        sidebar.setLayout(sidebar_layout)

        titulo = QLabel("WEB\nDIAGNOSTIC")
        sidebar_layout.addWidget(titulo)

        btn_inicio = QPushButton("Inicio")
        btn_discos = QPushButton("Discos")
        btn_diag = QPushButton("Diagnóstico")
        btn_reportes = QPushButton("Informes")
        btn_config = QPushButton("Configuración")

        sidebar_layout.addWidget(btn_inicio)
        sidebar_layout.addWidget(btn_discos)
        sidebar_layout.addWidget(btn_diag)
        sidebar_layout.addWidget(btn_reportes)
        sidebar_layout.addWidget(btn_config)

        sidebar_layout.addStretch()

        # -------- ZONA CENTRAL --------

        contenido = QLabel(
            "Panel principal\n\n"
            "Selecciona una opción del menú"
        )

        main_layout.addWidget(sidebar)
        main_layout.addWidget(contenido)