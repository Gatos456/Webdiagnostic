import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from diagnostics.disk_detector import detectar_discos

app = QApplication(sys.argv)

window = MainWindow()

# Detectar discos y mostrarlos en la tabla
discos = detectar_discos()
window.mostrar_discos(discos)

window.show()

sys.exit(app.exec())