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

# Diccionario de traducción según la opción elegida en Settings
TRADUCCIONES = {
    "es-ES": {
        "menu_archivo": "Archivo",
        "menu_edicion": "Edición",
        "menu_ver": "Ver",
        "menu_settings": "Settings",
        "accion_nuevo": "Nuevo",
        "accion_abrir": "Abrir",
        "accion_salir": "Salir",
        "accion_deshacer": "Deshacer",
        "accion_rehacer": "Rehacer",
        "accion_zoom_in": "Zoom In",
        "accion_zoom_out": "Zoom Out",
        "accion_configurar": "Configurar...",
        "stat_idioma": "Idioma",
        "stat_tema": "Tema",
        "stat_fuente": "Fuente",
        "msg_simulado": "La función '{}' es simulada según los requerimientos de la guía."
    },
    "en-US": {
        "menu_archivo": "File",
        "menu_edicion": "Edit",
        "menu_ver": "View",
        "menu_settings": "Settings",
        "accion_nuevo": "New",
        "accion_abrir": "Open",
        "accion_salir": "Exit",
        "accion_deshacer": "Undo",
        "accion_rehacer": "Redo",
        "accion_zoom_in": "Zoom In",
        "accion_zoom_out": "Zoom Out",
        "accion_configurar": "Configure...",
        "stat_idioma": "Language",
        "stat_tema": "Theme",
        "stat_fuente": "Font Size",
        "msg_simulado": "The '{}' feature is simulated as per project requirements."
    }
}


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

        # 1. Menú Archivo
        self.menu_archivo = menu_bar.addMenu("")
        self.action_nuevo = self.agregar_accion_simulada(self.menu_archivo, "accion_nuevo")
        self.action_abrir = self.agregar_accion_simulada(self.menu_archivo, "accion_abrir")
        self.menu_archivo.addSeparator()
        self.action_salir = QAction("", self)
        self.action_salir.triggered.connect(self.close)
        self.menu_archivo.addAction(self.action_salir)

        # 2. Menú Edición
        self.menu_edicion = menu_bar.addMenu("")
        self.action_deshacer = self.agregar_accion_simulada(self.menu_edicion, "accion_deshacer")
        self.action_rehacer = self.agregar_accion_simulada(self.menu_edicion, "accion_rehacer")

        # 3. Menú Ver
        self.menu_ver = menu_bar.addMenu("")
        self.action_zoom_in = self.agregar_accion_simulada(self.menu_ver, "accion_zoom_in")
        self.action_zoom_out = self.agregar_accion_simulada(self.menu_ver, "accion_zoom_out")

        # 4. Menú Settings
        self.menu_settings = menu_bar.addMenu("")
        self.action_configurar = QAction("", self)
        self.action_configurar.triggered.connect(self.abrir_settings)
        self.menu_settings.addAction(self.action_configurar)

        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        outer_layout = QVBoxLayout(self.central_widget)
        outer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Tarjeta de perfil
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

        divisor = QFrame()
        divisor.setFrameShape(QFrame.Shape.HLine)
        divisor.setObjectName("divisor")
        tarjeta_layout.addWidget(divisor)

        # Fila de mini-estadísticas
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
        return {"layout": layout, "etiqueta": lbl_etiqueta, "valor": lbl_valor}

    def _crear_divisor_vertical(self) -> QFrame:
        divisor = QFrame()
        divisor.setFrameShape(QFrame.Shape.VLine)
        divisor.setObjectName("divisorVertical")
        return divisor

    def resizeEvent(self, event):
        super().resizeEvent(event)
        ancho_objetivo = int(self.width() * 0.42)
        ancho_final = max(460, min(680, ancho_objetivo))
        self.tarjeta_perfil.setFixedWidth(ancho_final)

    def agregar_accion_simulada(self, menu, clave_traduccion: str) -> QAction:
        """Crea una acción simulada que responde en el idioma seleccionado."""
        accion = QAction("", self)
        accion.triggered.connect(lambda: self.mostrar_mensaje_simulado(clave_traduccion))
        menu.addAction(accion)
        return accion

    def mostrar_mensaje_simulado(self, clave_traduccion: str):
        idioma = self.config.get("idioma", "es-ES")
        traduccion = TRADUCCIONES.get(idioma, TRADUCCIONES["es-ES"])
        nombre_accion = traduccion.get(clave_traduccion, "Acción")
        QMessageBox.information(
            self,
            "Opción simulada",
            traduccion["msg_simulado"].format(nombre_accion)
        )

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
        """Aplica estilos, traducción dinámica y textos actualizados."""
        idioma = self.config.get("idioma", "es-ES")
        traduccion = TRADUCCIONES.get(idioma, TRADUCCIONES["es-ES"])

        # Actualizar textos de los Menús
        self.menu_archivo.setTitle(traduccion["menu_archivo"])
        self.action_nuevo.setText(f"{traduccion['accion_nuevo']} (Simulado)")
        self.action_abrir.setText(f"{traduccion['accion_abrir']} (Simulado)")
        self.action_salir.setText(traduccion["accion_salir"])

        self.menu_edicion.setTitle(traduccion["menu_edicion"])
        self.action_deshacer.setText(f"{traduccion['accion_deshacer']} (Simulado)")
        self.action_rehacer.setText(f"{traduccion['accion_rehacer']} (Simulado)")

        self.menu_ver.setTitle(traduccion["menu_ver"])
        self.action_zoom_in.setText(f"{traduccion['accion_zoom_in']} (Simulado)")
        self.action_zoom_out.setText(f"{traduccion['accion_zoom_out']} (Simulado)")

        self.menu_settings.setTitle(traduccion["menu_settings"])
        self.action_configurar.setText(traduccion["accion_configurar"])

        # Actualizar etiquetas de la tarjeta de perfil
        self.stat_idioma["etiqueta"].setText(traduccion["stat_idioma"])
        self.stat_tema["etiqueta"].setText(traduccion["stat_tema"])
        self.stat_fuente["etiqueta"].setText(traduccion["stat_fuente"])

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