import os
import json
import shutil
import logging

logging.basicConfig(level=logging.INFO, format = "%(asctime)s - %(levelname)s - %(message)s")
CONFIG_FILE = "config.json"
BACKUP_FILE = "backup.bak"
TEMP_FILE = "config.tmp"

DEFAULT_CONFIG = {
    "nombre_usuario": "Usuario Inicial",
    "tema_interfaz": "oscuro",
    "idioma": "es-ES",
    "tamano_fuente": 12,
    "color_menu": "#1f2937",
    "color_letra": "#ffffff",
    "foto_perfil": ""
}

class ConfigManager:
    """
    Manejo de errores, persistencia y backups
    """

    @staticmethod
    def validar_estructura(data: dict) -> bool:
        """
        Mira que el diccionario tenga todas las llaves requeridas
        """
        if not isinstance(data, dict):
            return False

        tipos_esperados = {
            "nombre_usuario": str,
            "tema_interfaz": str,
            "idioma": str,
            "tamano_fuente": int,
            "color_menu": str,
            "color_letra": str,
            "foto_perfil": str
        }

        for clave, tipo in tipos_esperados.items():
            if clave not in data or not isinstance(data[clave], tipo):
                logging.warning(f"Validación fallida: clave '{clave}' ausente o tipo incorrecto.")
                return False
        return True

    @classmethod
    def cargar_configuracion(cls) -> tuple[dict, str]:
        """
        Carga la configuración desde config.json.
        Retorna (config_dict, estado_mensaje).
        En caso de error (ausente, corrupto, sin permisos), cae de forma segura a DEFAULT_CONFIG.
        """
        #Archivo Ausente
        if not os.path.exists(CONFIG_FILE):
            logging.info("Archivo config.json ausente. Creando/Usando configuración por defecto.")
            return DEFAULT_CONFIG.copy(), "Archivo ausente. Se cargaron valores por defecto."

        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            #Estructura Inválida o Incompleta
            if not cls.validar_estructura(data):
                raise ValueError("El esquema de datos del archivo JSON es inválido.")

            logging.info("Configuración cargada exitosamente.")
            return data, "Configuración cargada con éxito."

        except PermissionError:
            # Sin Permisos de Lectura
            logging.error("Sin permisos de lectura sobre config.json.")
            return DEFAULT_CONFIG.copy(), "Error: Sin permisos de lectura. Se usaron valores por defecto."

        except (json.JSONDecodeError, ValueError) as e:
            # Archivo Corrupto / JSON mal formado
            logging.error(f"Archivo de configuración corrupto o mal formado: {e}")
            return DEFAULT_CONFIG.copy(), "Archivo corrupto o inválido. Se restauraron valores por defecto."

        except Exception as e:
            # Red de seguridad para cualquier otro error imprevisto
            logging.critical(f"Error inesperado al cargar configuración: {e}")
            return DEFAULT_CONFIG.copy(), f"Error inesperado: {str(e)}"

    @classmethod
    def guardar_configuracion(cls, nueva_config: dict) -> tuple[dict, str]:
        """
        Guarda la configuración usando escritura atómica (.tmp -> .json) y genera un backup (.bak).
        Retorna (éxito: bool, mensaje: str).
        """
