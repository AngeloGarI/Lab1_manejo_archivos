import os
import json
import shutil
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
_CORE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(_CORE_DIR)

CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
BACKUP_FILE = os.path.join(BASE_DIR, "config.bak")
TEMP_FILE = os.path.join(BASE_DIR, "config.tmp")

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
    Manejo de errores, persistencia y backups.
    """

    @staticmethod
    def validar_estructura(data: dict) -> bool:
        """
        Mira que el diccionario tenga todas las llaves requeridas con el tipo esperado.
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
        # Archivo ausente
        if not os.path.exists(CONFIG_FILE):
            logging.info("Archivo config.json ausente. Usando configuración por defecto.")
            return DEFAULT_CONFIG.copy(), "Archivo ausente. Se cargaron valores por defecto."

        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Estructura inválida o incompleta
            if not cls.validar_estructura(data):
                raise ValueError("El esquema de datos del archivo JSON es inválido.")

            logging.info("Configuración cargada exitosamente.")
            return data, "Configuración cargada con éxito."

        except PermissionError:
            logging.error("Sin permisos de lectura sobre config.json.")
            return DEFAULT_CONFIG.copy(), "Error: sin permisos de lectura. Se usaron valores por defecto."

        except (json.JSONDecodeError, ValueError) as e:
            logging.error(f"Archivo de configuración corrupto o mal formado: {e}")
            return DEFAULT_CONFIG.copy(), "Archivo corrupto o inválido. Se restauraron valores por defecto."

        except Exception as e:
            logging.critical(f"Error inesperado al cargar configuración: {e}")
            return DEFAULT_CONFIG.copy(), f"Error inesperado: {str(e)}"

    @classmethod
    def guardar_configuracion(cls, nueva_config: dict) -> tuple[bool, str, bool]:
        """
        Guarda la configuración usando escritura atómica (.tmp -> .json) y genera un backup (.bak).

        Retorna (exito, mensaje, backup_ok):
          - exito: si el guardado del archivo principal fue correcto.
          - mensaje: texto para mostrar al usuario.
          - backup_ok: si el respaldo se creó correctamente (puede ser False aunque exito sea True).
        """
        if not cls.validar_estructura(nueva_config):
            return False, "Error: la configuración a guardar tiene datos o formatos inválidos.", False

        backup_ok = True

        # 1. Respaldo (.bak) de la configuración previa, si existe un archivo activo
        if os.path.exists(CONFIG_FILE):
            try:
                shutil.copy2(CONFIG_FILE, BACKUP_FILE)
                logging.info(f"Respaldo creado con éxito en '{BACKUP_FILE}'.")
            except Exception as e:
                backup_ok = False
                logging.warning(f"No se pudo crear el archivo de respaldo: {e}")

        try:
            # 2. Escritura segura en archivo temporal (.tmp) en UTF-8
            with open(TEMP_FILE, "w", encoding="utf-8") as f:
                json.dump(nueva_config, f, ensure_ascii=False, indent=4)
                f.flush()
                os.fsync(f.fileno())  # fuerza la escritura a disco antes de renombrar

            # 3. Reemplazo atómico del archivo final
            os.replace(TEMP_FILE, CONFIG_FILE)
            logging.info("Configuración guardada y reemplazada atómicamente.")

            if backup_ok:
                return True, "Configuración guardada y respaldada correctamente.", True
            else:
                return True, "Configuración guardada, pero no se pudo crear el respaldo (.bak).", False

        except PermissionError:
            logging.error("Sin permisos de escritura en la ruta de trabajo.")
            if os.path.exists(TEMP_FILE):
                os.remove(TEMP_FILE)
            return False, "Error: sin permisos de escritura para guardar los cambios.", backup_ok

        except Exception as e:
            logging.error(f"Error crítico al guardar configuración: {e}")
            if os.path.exists(TEMP_FILE):
                os.remove(TEMP_FILE)
            return False, f"Fallo al guardar: {str(e)}", backup_ok