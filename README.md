---
```markdown
# Laboratorio No. 1: Aplicación de Escritorio con Gestión de Configuración de Usuario

**Universidad:** Universidad Rafael Landívar, Campus San Alberto Hurtado, S.J. de Quetzaltenango  
**Facultad:** Ingeniería en Informática y Sistemas  
**Curso:** Manejo e Implementación de Archivos  
**Fecha:** Septiembre de 2026  

---

## 📌 Descripción del Proyecto
Aplicación de escritorio desarrollada en **Python** utilizando **PyQt6** para la interfaz gráfica. El objetivo principal es la **gestión y persistencia robusta de archivos de configuración** de usuario mediante lectura, escritura atómica, respaldo automático (`.bak`) y tolerancia a fallos.

---

## 🛠️ Tecnologías Utilizadas
* **Lenguaje:** Python 3.x
* **GUI Framework:** PyQt6
* **Formato de Almacenamiento:** JSON (`config.json`)
* **Librerías Nativas:** `os`, `json`, `shutil`, `logging`, `sys`

---

## 📂 Estructura del Repositorio
```text
lab1_archivos/
│
├── core/
│   ├── __init__.py
│   └── config_manager.py  # Lógica de persistencia, atomicidad (.tmp), backups (.bak) y UTF-8
│
├── gui/
│   ├── __init__.py
│   ├── main_window.py     # Ventana principal con tarjeta de perfil y menús
│   └── settings_dialog.py # Diálogo de configuración de usuario
│
├── config.json            # Archivo de configuración activo (se crea automáticamente)
├── config.bak             # Archivo de respaldo automático de la versión previa
├── main.py                # Punto de entrada de la aplicación
└── README.md              # Documentación del proyecto

```

---

## 🚀 Requisitos e Instalación

1. **Clonar el repositorio:**
```bash
   git clone https://github.com/AngeloGarI/Lab1_manejo_archivos.git
   cd lab1_archivos 

```


2. **Instalar dependencias:**
Asegúrate de tener instalada la librería PyQt6:
```bash
   pip install PyQt6

```


3. **Ejecutar la aplicación:**
```bash
   python main.py

```



---

## 🛡️ Mecanismos de Persistencia y Seguridad

* **Escritura Atómica (`config.tmp` → `config.json`):** Los cambios se escriben primero en un borrador temporal y se vacían físicamente al disco usando `os.fsync()`. Posteriormente se reemplaza el archivo final con `os.replace()` para prevenir corrupción por cierres abruptos.
* **Respaldo Automático (`config.bak`):** Se genera una copia del estado previo aceptado antes de aplicar nuevos cambios.
* **Manejo de Errores:** Tolerancia completa ante archivos ausentes, corruptos/inválidos o falta de permisos de lectura/escritura (recuperación mediante `DEFAULT_CONFIG`).
* **Codificación UTF-8:** Soporte garantizado para diacríticos (tildes, `ñ`) y rutas del sistema mediante `encoding="utf-8"`.

```

```