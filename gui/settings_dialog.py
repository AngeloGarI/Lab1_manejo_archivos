import os
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit,
    QComboBox, QSpinBox, QPushButton, QColorDialog, QFileDialog,
    QLabel, QMessageBox, QFrame
)
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtCore import Qt

class SettingsDialog(QDialog):
    """
    Diálogo de configuración con selectores nativos de color,
    archivos de imagen y estilos visuales pulidos.
    """
    def __init__(self, current_config: dict, on_save_callback, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configuración de Usuario (Settings)")
        self.setFixedWidth(450)
        self.config = current_config.copy()
        self.on_save_callback = on_save_callback

        self.init_ui()
        self.aplicar_estilos_base()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)

        # Encabezado visual
        header_label = QLabel("Ajustes del Sistema")
        header_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(header_label)

        # Formulario
        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        # 1. Nombre de Usuario
        self.txt_usuario = QLineEdit(self.config["nombre_usuario"])
        form_layout.addRow("Nombre de Usuario:", self.txt_usuario)

        # 2. Tema Interfaz
        self.combo_tema = QComboBox()
        self.combo_tema.addItems(["oscuro", "claro"])
        self.combo_tema.setCurrentText(self.config["tema_interfaz"])
        form_layout.addRow("Tema de Interfaz:", self.combo_tema)

        # 3. Idioma
        self.combo_idioma = QComboBox()
        self.combo_idioma.addItems(["es-ES", "en-US"])
        self.combo_idioma.setCurrentText(self.config["idioma"])
        form_layout.addRow("Idioma:", self.combo_idioma)

        # 4. Tamaño de Fuente
        self.spin_fuente = QSpinBox()
        self.spin_fuente.setRange(8, 48)
        self.spin_fuente.setValue(self.config["tamano_fuente"])
        form_layout.addRow("Tamaño de Fuente:", self.spin_fuente)

        # 5. Color Barra de Menú
        btn_color_menu_layout = QHBoxLayout()
        self.btn_color_menu = QPushButton("Elegir Color")
        self.preview_color_menu = QFrame()
        self.preview_color_menu.setFixedSize(24, 24)
        self.actualizar_preview_color(self.preview_color_menu, self.config["color_menu"])
        self.btn_color_menu.clicked.connect(self.seleccionar_color_menu)
        btn_color_menu_layout.addWidget(self.btn_color_menu)
        btn_color_menu_layout.addWidget(self.preview_color_menu)
        form_layout.addRow("Color Menú:", btn_color_menu_layout)

        # 6. Color de Letra
        btn_color_letra_layout = QHBoxLayout()
        self.btn_color_letra = QPushButton("Elegir Color")
        self.preview_color_letra = QFrame()
        self.preview_color_letra.setFixedSize(24, 24)
        self.actualizar_preview_color(self.preview_color_letra, self.config["color_letra"])
        self.btn_color_letra.clicked.connect(self.seleccionar_color_letra)
        btn_color_letra_layout.addWidget(self.btn_color_letra)
        btn_color_letra_layout.addWidget(self.preview_color_letra)
        form_layout.addRow("Color Letra:", btn_color_letra_layout)

        # 7. Foto de Perfil
        foto_layout = QHBoxLayout()
        self.lbl_foto_path = QLineEdit(self.config["foto_perfil"])
        self.lbl_foto_path.setReadOnly(True)
        btn_foto = QPushButton("Examinar...")
        btn_foto.clicked.connect(self.seleccionar_foto)
        foto_layout.addWidget(self.lbl_foto_path)
        foto_layout.addWidget(btn_foto)
        form_layout.addRow("Foto de Perfil:", foto_layout)

        main_layout.addLayout(form_layout)

        # Botón Guardar
        self.btn_guardar = QPushButton("Guardar Cambios")
        self.btn_guardar.setFixedHeight(40)
        self.btn_guardar.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.btn_guardar.clicked.connect(self.guardar_configuracion)
        main_layout.addWidget(self.btn_guardar)

    def actualizar_preview_color(self, frame: QFrame, hex_color: str):
        frame.setStyleSheet(f"background-color: {hex_color}; border: 1px solid #555; border-radius: 4px;")
