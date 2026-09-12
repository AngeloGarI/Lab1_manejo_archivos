import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QMessageBox
)
from PyQt6.QtGui import QAction, QFont, QPixmap, QBitmap, QPainter, QPainterPath
from PyQt6.QtCore import Qt, QSize
from core.config_manager import ConfigManager
from gui.settings_dialog import SettingsDialog


class MainWindow(QMainWindow):
    """Ventana Principal con barra de menú y actualización dinámica de UI."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestión de Configuración")
        self.resize(650, 480)

        # Carga inicial desde el Core
        self.config, estado_msg = ConfigManager.cargar_configuracion()

        self.init_ui()
        self.aplicar_configuracion_ui()

        # Alerta de carga inicial si hubo error o recuperación por defecto
        if "éxito" not in estado_msg.lower():
            QMessageBox.information(self, "Estado de Carga", estado_msg)

    def init_ui(self):
        # Construir Menú Principal
        menu_bar = self.menuBar()

        # 1. Menú Archivo
        menu_archivo = menu_bar.addMenu("Archivo")
        self.agregar_accion_simulada(menu_archivo, "Nuevo")
        self.agregar_accion_simulada(menu_archivo, "Abrir")
        menu_archivo.addSeparator()
        action_salir = QAction("Salir", self)
        action_salir.triggered.connect(self.close)
        menu_archivo.addAction(action_salir)

        # 2. Menú Edición
        menu_edicion = menu_bar.addMenu("Edición")
        self.agregar_accion_simulada(menu_edicion, "Deshacer")
        self.agregar_accion_simulada(menu_edicion, "Rehacer")

        # 3. Menú Ver
        menu_ver = menu_bar.addMenu("Ver")
        self.agregar_accion_simulada(menu_ver, "Zoom In")
        self.agregar_accion_simulada(menu_ver, "Zoom Out")

        # 4. Menú Settings (Funcional)
        menu_settings = menu_bar.addMenu("Settings")
        action_abrir_settings = QAction("Configurar...", self)
        action_abrir_settings.triggered.connect(self.abrir_settings)
        menu_settings.addAction(action_abrir_settings)

        # Widget central dinámico
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout_central = QVBoxLayout(self.central_widget)
        self.layout_central.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_central.setSpacing(20)

        # Contenedor para la foto de perfil
        self.lbl_foto = QLabel()
        self.lbl_foto.setFixedSize(120, 120)
        self.lbl_foto.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_central.addWidget(self.lbl_foto, alignment=Qt.AlignmentFlag.AlignCenter)

        # Mensaje de bienvenida
        self.lbl_bienvenida = QLabel()
        self.lbl_bienvenida.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_central.addWidget(self.lbl_bienvenida)

