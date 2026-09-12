import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox, QFrame
)
from PyQt6.QtGui import QAction, QFont, QPixmap, QPainter, QPainterPath
from PyQt6.QtCore import Qt
from core.config_manager import ConfigManager
from gui.settings_dialog import SettingsDialog

GRADIENT_OSCURO = "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #161C2B, stop:1 #0D1119)"
GRADIENT_CLARO = "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #E9ECF1)"
COLOR_PANEL = "#1D2536"
COLOR_PANEL_BORDE = "#2E3750"
COLOR_ACCENT = "#4FB286"
COLOR_TEXT_MUTED = "#8B93A5"


class MainWindow(QMainWindow):
    """Ventana principal con barra de menú y actualización dinámica de UI."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestión de Configuración")
        self.resize(650, 480)

        # Carga inicial desde el core
        self.config, estado_msg = ConfigManager.cargar_configuracion()

        self.init_ui()
        self.aplicar_configuracion_ui()

        # Alerta de carga inicial si hubo error o recuperación por defecto
        if "éxito" not in estado_msg.lower():
            QMessageBox.information(self, "Estado de carga", estado_msg)

    def init_ui(self):
        menu_bar = self.menuBar()

        # 1. Menú Archivo (simulado)
        menu_archivo = menu_bar.addMenu("Archivo")
        self.agregar_accion_simulada(menu_archivo, "Nuevo")
        self.agregar_accion_simulada(menu_archivo, "Abrir")
        menu_archivo.addSeparator()
        action_salir = QAction("Salir", self)
        action_salir.triggered.connect(self.close)
        menu_archivo.addAction(action_salir)

        # 2. Menú Edición (simulado)
        menu_edicion = menu_bar.addMenu("Edición")
        self.agregar_accion_simulada(menu_edicion, "Deshacer")
        self.agregar_accion_simulada(menu_edicion, "Rehacer")

        # 3. Menú Ver (simulado)
        menu_ver = menu_bar.addMenu("Ver")
        self.agregar_accion_simulada(menu_ver, "Zoom In")
        self.agregar_accion_simulada(menu_ver, "Zoom Out")

        # 4. Menú Settings (funcional)
        menu_settings = menu_bar.addMenu("Settings")
        action_abrir_settings = QAction("Configurar...", self)
        action_abrir_settings.triggered.connect(self.abrir_settings)
        menu_settings.addAction(action_abrir_settings)

        # Widget central: centra una tarjeta de perfil sobre el fondo degradado
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        outer_layout = QVBoxLayout(self.central_widget)
        outer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- Tarjeta de perfil (elevada respecto al fondo) ---
        self.tarjeta_perfil = QFrame()
        self.tarjeta_perfil.setObjectName("tarjetaPerfil")
        self.tarjeta_perfil.setFixedWidth(460)
        tarjeta_layout = QVBoxLayout(self.tarjeta_perfil)
        tarjeta_layout.setContentsMargins(40, 36, 40, 36)
        tarjeta_layout.setSpacing(22)
        tarjeta_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.lbl_foto = QLabel()
        self.lbl_foto.setFixedSize(112, 112)
        self.lbl_foto.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tarjeta_layout.addWidget(self.lbl_foto, alignment=Qt.AlignmentFlag.AlignCenter)

        self.lbl_nombre = QLabel()
        self.lbl_nombre.setObjectName("lblNombre")
        self.lbl_nombre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tarjeta_layout.addWidget(self.lbl_nombre)

        # Divisor sutil entre el nombre y las estadísticas de configuración
        divisor = QFrame()
        divisor.setFrameShape(QFrame.Shape.HLine)
        divisor.setObjectName("divisor")
        tarjeta_layout.addWidget(divisor)

        # Fila de mini-estadísticas: Idioma | Tema | Fuente
        fila_stats = QHBoxLayout()
        fila_stats.setSpacing(0)
        self.stat_idioma = self._crear_stat("Idioma")
        self.stat_tema = self._crear_stat("Tema")
        self.stat_fuente = self._crear_stat("Fuente")
        fila_stats.addLayout(self.stat_idioma["layout"])
        fila_stats.addWidget(self._crear_divisor_vertical())
        fila_stats.addLayout(self.stat_tema["layout"])
        fila_stats.addWidget(self._crear_divisor_vertical())
        fila_stats.addLayout(self.stat_fuente["layout"])
        tarjeta_layout.addLayout(fila_stats)

        outer_layout.addWidget(self.tarjeta_perfil)

    def _crear_stat(self, etiqueta: str) -> dict:
        """Crea una mini-columna de estadística (etiqueta arriba, valor abajo)."""
        layout = QVBoxLayout()
        layout.setSpacing(2)
        lbl_etiqueta = QLabel(etiqueta)
        lbl_etiqueta.setObjectName("statLabel")
        lbl_etiqueta.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_valor = QLabel("—")
        lbl_valor.setObjectName("statValor")
        lbl_valor.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_etiqueta)
        layout.addWidget(lbl_valor)
        return {"layout": layout, "valor": lbl_valor}

    def _crear_divisor_vertical(self) -> QFrame:
        divisor = QFrame()
        divisor.setFrameShape(QFrame.Shape.VLine)
        divisor.setObjectName("divisorVertical")
        return divisor

    def resizeEvent(self, event):
        """Escala la tarjeta de perfil junto con la ventana, dentro de un rango
        razonable, para que no se vea diminuta cuando la ventana está maximizada
        ni demasiado ancha en una ventana pequeña."""
        super().resizeEvent(event)
        ancho_objetivo = int(self.width() * 0.42)
        ancho_final = max(460, min(680, ancho_objetivo))
        self.tarjeta_perfil.setFixedWidth(ancho_final)

    def agregar_accion_simulada(self, menu, nombre: str):
        """Crea acciones simuladas que muestran un mensaje informativo al hacer clic."""
        accion = QAction(f"{nombre} (Simulado)", self)
        accion.triggered.connect(lambda: QMessageBox.information(
            self, "Opción simulada", f"La función '{nombre}' es simulada según los requerimientos de la guía."
        ))
        menu.addAction(accion)

    def abrir_settings(self):
        dialog = SettingsDialog(self.config, self.guardar_nueva_config, self)
        dialog.exec()

    def guardar_nueva_config(self, nueva_config: dict) -> tuple[bool, str, bool]:
        exito, msg, backup_ok = ConfigManager.guardar_configuracion(nueva_config)
        if exito:
            self.config = nueva_config
            self.aplicar_configuracion_ui()
        return exito, msg, backup_ok

    def obtener_pixmap_circular(self, ruta_imagen: str, tamano: int) -> QPixmap:
        """Carga una imagen y la recorta en forma circular."""
        original = QPixmap(ruta_imagen)
        if original.isNull():
            return QPixmap()

        scaled = original.scaled(
            tamano, tamano,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )

        out_pixmap = QPixmap(tamano, tamano)
        out_pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(out_pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        path = QPainterPath()
        path.addEllipse(0, 0, tamano, tamano)
        painter.setClipPath(path)

        x = (scaled.width() - tamano) // 2
        y = (scaled.height() - tamano) // 2
        painter.drawPixmap(0, 0, scaled, x, y, tamano, tamano)
        painter.end()

        return out_pixmap

    def aplicar_configuracion_ui(self):
        """Aplica estilos, foto circular y textos actualizados."""
        tamano_fuente = self.config["tamano_fuente"]

        self.lbl_nombre.setFont(QFont("Segoe UI", max(tamano_fuente, 13), QFont.Weight.DemiBold))
        self.lbl_nombre.setText(self.config["nombre_usuario"])

        self.stat_idioma["valor"].setText(self.config["idioma"])
        self.stat_tema["valor"].setText(self.config["tema_interfaz"].capitalize())
        self.stat_fuente["valor"].setText(f"{tamano_fuente} pt")

        es_oscuro = self.config["tema_interfaz"] == "oscuro"
        gradiente_fondo = GRADIENT_OSCURO if es_oscuro else GRADIENT_CLARO
        color_texto_valor = self.config["color_letra"]
        color_texto_muted = COLOR_TEXT_MUTED if es_oscuro else "#5B6472"
        panel_bg = COLOR_PANEL if es_oscuro else "#FFFFFF"
        panel_borde = COLOR_PANEL_BORDE if es_oscuro else "#DDE1E8"

        self.setStyleSheet(f"""
            QMainWindow {{ background: {gradiente_fondo}; }}
            QMenuBar {{
                background-color: {self.config['color_menu']};
                color: {self.config['color_letra']};
                font-size: 10.5pt;
                font-weight: 600;
                padding: 4px;
            }}
            QMenuBar::item {{
                padding: 6px 12px;
                border-radius: 4px;
                background: transparent;
            }}
            QMenuBar::item:selected {{
                background-color: rgba(255, 255, 255, 0.12);
            }}
            QMenu {{
                background-color: {self.config['color_menu']};
                color: {self.config['color_letra']};
                border: 1px solid rgba(255, 255, 255, 0.1);
            }}
            QMenu::item:selected {{
                background-color: rgba(255, 255, 255, 0.12);
            }}
            QFrame#tarjetaPerfil {{
                background-color: {panel_bg};
                border: 1px solid {panel_borde};
                border-top: 3px solid {COLOR_ACCENT};
                border-radius: 14px;
            }}
            QFrame#divisor {{
                background-color: {panel_borde};
                max-height: 1px;
                border: none;
            }}
            QFrame#divisorVertical {{
                background-color: {panel_borde};
                max-width: 1px;
                border: none;
                margin: 2px 18px;
            }}
            QLabel#lblNombre {{
                color: {color_texto_valor};
            }}
            QLabel#statLabel {{
                color: {color_texto_muted};
                font-size: 8.5pt;
            }}
            QLabel#statValor {{
                color: {color_texto_valor};
                font-size: 10.5pt;
                font-weight: 600;
            }}
        """)

        foto_path = self.config["foto_perfil"]
        if foto_path and os.path.exists(foto_path):
            pixmap_circular = self.obtener_pixmap_circular(foto_path, 112)
            if not pixmap_circular.isNull():
                self.lbl_foto.setText("")
                self.lbl_foto.setStyleSheet(
                    f"border: 2px solid {COLOR_ACCENT}; border-radius: 56px;"
                )
                self.lbl_foto.setPixmap(pixmap_circular)
            else:
                self.mostrar_placeholder_foto()
        else:
            self.mostrar_placeholder_foto()

    def mostrar_placeholder_foto(self):
        """Muestra un contenedor circular vacío cuando no hay foto elegida."""
        self.lbl_foto.setPixmap(QPixmap())
        self.lbl_foto.setText("Sin foto")
        self.lbl_foto.setStyleSheet(
            f"border: 2px dashed {COLOR_TEXT_MUTED}; "
            f"border-radius: 56px; "
            f"color: {COLOR_TEXT_MUTED};"
        )