"""
Configuración de la Aplicación
Constantes y configuraciones globales
"""

# Información de la aplicación
APP_NOMBRE = "Balancea"
APP_VERSION = "1.0.0"
APP_AUTOR = "Tu Nombre"
APP_DESCRIPCION = "Gestor de Finanzas Personales con IA"

# Configuración de ventana
VENTANA_ANCHO = 1200
VENTANA_ALTO = 700
VENTANA_MIN_ANCHO = 900
VENTANA_MIN_ALTO = 600

# Colores del tema
COLORES = {
    'primario': '#2C3E50',
    'secundario': '#3498DB',
    'exito': '#27AE60',
    'peligro': '#E74C3C',
    'advertencia': '#F39C12',
    'info': '#3498DB',
    'fondo': '#ECF0F1',
    'texto': '#2C3E50',
    'gris': '#95A5A6',
    'morado': '#9B59B6',
    'naranja': '#E67E22',
    'turquesa': '#1ABC9C'
}

# Rutas de archivos
RUTA_DATOS = "datos/"
RUTA_TRANSACCIONES = "datos/transacciones.csv"
RUTA_CATEGORIAS = "datos/categorias.json"
RUTA_CONFIGURACION = "datos/config.json"
RUTA_BACKUPS = "datos/backups/"

# Configuración de gráficas
GRAFICAS_DPI = 100
GRAFICAS_ESTILO = 'seaborn-v0_8-darkgrid'
GRAFICAS_COLORES = [
    '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8',
    '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B739', '#52B788'
]

# Límites y validaciones
MONTO_MINIMO = 0.01
MONTO_MAXIMO = 999999999
DESCRIPCION_MIN_CARACTERES = 3
DESCRIPCION_MAX_CARACTERES = 200

# Configuración de exportación
FORMATOS_EXPORTACION = [
    ("CSV files", "*.csv"),
    ("Excel files", "*.xlsx"),
    ("PDF files", "*.pdf"),
    ("All files", "*.*")
]

# Atajos de teclado
ATAJOS = {
    'nueva_transaccion': '<Control-n>',
    'guardar': '<Control-s>',
    'buscar': '<Control-f>',
    'exportar': '<Control-e>',
    'eliminar': '<Delete>',
    'actualizar': '<F5>',
    'cancelar': '<Escape>',
    'ayuda': '<F1>'
}

# Mensajes de la aplicación
MENSAJES = {
    'bienvenida': f'Bienvenido a {APP_NOMBRE} v{APP_VERSION}',
    'sin_datos': 'No hay transacciones registradas',
    'exito_agregar': 'Transacción agregada correctamente',
    'exito_editar': 'Transacción editada correctamente',
    'exito_eliminar': 'Transacción eliminada correctamente',
    'exito_exportar': 'Datos exportados correctamente',
    'error_validacion': 'Por favor verifica los datos ingresados',
    'error_guardar': 'Error al guardar los datos',
    'error_cargar': 'Error al cargar los datos'
}

# Configuración de Ollama (para futuro)
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODELO = "llama3.2:latest"
OLLAMA_TIMEOUT = 30

# Configuración de alertas
ALERTA_GASTO_INUSUAL_PORCENTAJE = 150  # 150% del promedio
ALERTA_BALANCE_NEGATIVO = True
ALERTA_PRESUPUESTO_EXCEDIDO = True

# Configuración de backups
BACKUP_AUTOMATICO = True
BACKUP_FRECUENCIA_DIAS = 7
BACKUP_MAX_ARCHIVOS = 10