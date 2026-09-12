from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit,
    QComboBox, QSpinBox, QPushButton, QColorDialog, QFileDialog,
    QLabel, QMessageBox, QFrame, QGroupBox
)
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtCore import Qt

GRADIENT_BG = "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #161C2B, stop:1 #0D1119)"
COLOR_PANEL = "#1D2536"
COLOR_BORDER = "#2E3750"
COLOR_TEXT = "#E6E9EF"
COLOR_TEXT_MUTED = "#8B93A5"
COLOR_ACCENT = "#4FB286"
COLOR_ACCENT_HOVER = "#63C79A"
COLOR_INPUT_BG = "#12151F"
FONT_MONO = "Consolas, 'JetBrains Mono', 'Courier New', monospace"


class SettingsDialog(QDialog):
    """
    Diálogo de configuración con selectores nativos de color,
    archivos de imagen, y secciones agrupadas por tipo de ajuste.
    """
    def __init__(self, current_config: dict, on_save_callback, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configuración de Usuario")
        self.setFixedWidth(460)
        self.config = current_config.copy()
        self.on_save_callback = on_save_callback

        self.init_ui()
        self.aplicar_estilos()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(20, 20, 20, 20)

        header = QLabel("Configuración")
        header.setObjectName("header")
        main_layout.addWidget(header)

        divisor_header = QFrame()
        divisor_header.setFrameShape(QFrame.Shape.HLine)
        divisor_header.setObjectName("divisorAccent")
        main_layout.addWidget(divisor_header)

        subheader = QLabel("Los cambios se guardan de forma segura con respaldo automático.")
        subheader.setObjectName("subheader")
        subheader.setWordWrap(True)
        main_layout.addWidget(subheader)

        # --- Sección: Perfil ---
        grupo_perfil = QGroupBox("Perfil")
        form_perfil = QFormLayout()
        form_perfil.setSpacing(10)

        self.txt_usuario = QLineEdit(self.config["nombre_usuario"])
        form_perfil.addRow("Nombre de usuario:", self.txt_usuario)

        self.combo_idioma = QComboBox()
        self.combo_idioma.addItems(["es-ES", "en-US"])
        self.combo_idioma.setCurrentText(self.config["idioma"])
        form_perfil.addRow("Idioma:", self.combo_idioma)

        foto_layout = QHBoxLayout()
        self.lbl_foto_path = QLineEdit(self.config["foto_perfil"])
        self.lbl_foto_path.setReadOnly(True)
        self.lbl_foto_path.setObjectName("pathField")
        btn_foto = QPushButton("Examinar…")
        btn_foto.clicked.connect(self.seleccionar_foto)
        foto_layout.addWidget(self.lbl_foto_path)
        foto_layout.addWidget(btn_foto)
        form_perfil.addRow("Foto de perfil:", foto_layout)

        grupo_perfil.setLayout(form_perfil)
        main_layout.addWidget(grupo_perfil)

        # --- Sección: Apariencia ---
        grupo_apariencia = QGroupBox("Apariencia")
        form_apariencia = QFormLayout()
        form_apariencia.setSpacing(10)

        self.combo_tema = QComboBox()
        self.combo_tema.addItems(["oscuro", "claro"])
        self.combo_tema.setCurrentText(self.config["tema_interfaz"])
        form_apariencia.addRow("Tema de interfaz:", self.combo_tema)

        self.spin_fuente = QSpinBox()
        self.spin_fuente.setRange(8, 48)
        self.spin_fuente.setValue(self.config["tamano_fuente"])
        form_apariencia.addRow("Tamaño de fuente:", self.spin_fuente)

        btn_color_menu_layout = QHBoxLayout()
        self.btn_color_menu = QPushButton("Elegir color")
        self.preview_color_menu = QFrame()
        self.preview_color_menu.setFixedSize(22, 22)
        self.actualizar_preview_color(self.preview_color_menu, self.config["color_menu"])
        self.btn_color_menu.clicked.connect(self.seleccionar_color_menu)
        btn_color_menu_layout.addWidget(self.btn_color_menu)
        btn_color_menu_layout.addWidget(self.preview_color_menu)
        form_apariencia.addRow("Color de barra de menú:", btn_color_menu_layout)

        btn_color_letra_layout = QHBoxLayout()
        self.btn_color_letra = QPushButton("Elegir color")
        self.preview_color_letra = QFrame()
        self.preview_color_letra.setFixedSize(22, 22)
        self.actualizar_preview_color(self.preview_color_letra, self.config["color_letra"])
        self.btn_color_letra.clicked.connect(self.seleccionar_color_letra)
        btn_color_letra_layout.addWidget(self.btn_color_letra)
        btn_color_letra_layout.addWidget(self.preview_color_letra)
        form_apariencia.addRow("Color de letra:", btn_color_letra_layout)

        grupo_apariencia.setLayout(form_apariencia)
        main_layout.addWidget(grupo_apariencia)

        # --- Botones de acción ---
        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(10)

        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_cancelar.setObjectName("btnSecundario")
        self.btn_cancelar.clicked.connect(self.reject)

        self.btn_guardar = QPushButton("Guardar cambios")
        self.btn_guardar.setObjectName("btnPrincipal")
        self.btn_guardar.clicked.connect(self.guardar_configuracion)

        botones_layout.addWidget(self.btn_cancelar)
        botones_layout.addWidget(self.btn_guardar)
        main_layout.addLayout(botones_layout)

    def actualizar_preview_color(self, frame: QFrame, hex_color: str):
        frame.setStyleSheet(
            f"background-color: {hex_color}; border: 1px solid {COLOR_BORDER}; border-radius: 4px;"
        )

    def seleccionar_color_menu(self):
        color = QColorDialog.getColor(QColor(self.config["color_menu"]), self, "Seleccionar color de menú")
        if color.isValid():
            self.config["color_menu"] = color.name()
            self.actualizar_preview_color(self.preview_color_menu, color.name())

    def seleccionar_color_letra(self):
        color = QColorDialog.getColor(QColor(self.config["color_letra"]), self, "Seleccionar color de texto")
        if color.isValid():
            self.config["color_letra"] = color.name()
            self.actualizar_preview_color(self.preview_color_letra, color.name())

    def seleccionar_foto(self):
        ruta, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar foto de perfil", "", "Imágenes (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if ruta:
            self.config["foto_perfil"] = ruta
            self.lbl_foto_path.setText(ruta)

    def guardar_configuracion(self):
        self.config["nombre_usuario"] = self.txt_usuario.text().strip()
        self.config["tema_interfaz"] = self.combo_tema.currentText()
        self.config["idioma"] = self.combo_idioma.currentText()
        self.config["tamano_fuente"] = self.spin_fuente.value()

