# 💰 Balancea - Gestor de Finanzas Personales

Sistema inteligente de gestión de finanzas personales con IA local (Ollama) y análisis predictivo.

## 🚀 Características

- ✅ **Dashboard Interactivo**: Visualización en tiempo real con métricas avanzadas
- ✅ **Gestión de Transacciones**: CRUD completo con búsqueda y filtros
- ✅ **Categorización Personalizable**: Crea y gestiona tus propias categorías
- ✅ **Gráficas Avanzadas**: Pastel, barras y líneas de tendencia
- ✅ **Asistente IA con Ollama**: Chat financiero inteligente con comandos especiales
- ✅ **Sistema de Alertas**: Detección automática de gastos inusuales
- ✅ **Análisis de Salud Financiera**: Puntuación 0-100 con recomendaciones
- ✅ **Comparativa Mensual**: Análisis vs mes anterior
- ✅ **Top 5 Gastos**: Identifica tus mayores gastos
- ✅ **Exportación CSV**: Respaldo de datos

## 📋 Requisitos

- Python 3.8 o superior
- Ollama instalado (para funciones de IA)
  - Modelo recomendado: `llama3.2:3b-instruct-fp16`

## 🔧 Instalación

### 1. Clonar el repositorio

```bash
cd Balancea
```

### 2. Crear entorno virtual (recomendado)

```bash
python -m venv venv

# En Windows
venv\Scripts\activate

# En Mac/Linux
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación

```bash
python app.py
```

## 📁 Estructura del Proyecto

```
Balancea/
├── app.py                      # Aplicación principal
├── requirements.txt            # Dependencias
│
├── datos/                      # Gestión de datos
│   ├── gestor_transacciones.py
│   └── transacciones.csv       # Se genera automáticamente
│
├── interfaz/                   # Componentes UI
│   ├── panel_dashboard.py
│   ├── panel_transacciones.py
│   ├── panel_resultados.py
│   ├── panel_chat.py
│   └── panel_alertas.py
│
├── procesador/                 # Lógica de IA (próximamente)
├── utils/                      # Utilidades (próximamente)
└── tests/                      # Pruebas (próximamente)
```

## 🎯 Uso Básico

### Agregar una Transacción

1. Ve a la pestaña "💳 Transacciones"
2. Completa el formulario:
   - Fecha
   - Descripción
   - Monto
   - Tipo (Ingreso/Gasto)
   - Categoría
3. Haz clic en "➕ Agregar"

### Editar/Eliminar Transacciones

1. Selecciona una transacción de la lista
2. Los datos se cargarán en el formulario
3. Modifica y haz clic en "✏️ Editar"
4. O haz clic en "🗑️ Eliminar" para eliminarla

### Ver Dashboard

- La pestaña "📊 Dashboard" muestra:
  - Balance total
  - Total de ingresos
  - Total de gastos
  - Estadísticas adicionales

## 🗓️ Roadmap

- [x] **Semana 1**: Base sólida (Días 1-2 completados)
- [ ] **Día 3**: Gráficas con Matplotlib
- [ ] **Semana 2**: Integración con Ollama
- [ ] **Semana 3**: Features avanzadas
- [ ] **Semana 4**: Preparación final

## 🛠️ Tecnologías

- **Python 3.8+**
- **Tkinter** - Interfaz gráfica
- **Pandas** - Manipulación de datos
- **Matplotlib** - Gráficas
- **Ollama** - IA local
- **Scikit-learn** - Machine Learning

## 📝 Notas de Desarrollo

- Día 1-2: ✅ Estructura base + CRUD de transacciones
- Los datos se guardan en CSV automáticamente
- La aplicación crea el archivo de datos si no existe

## 👨‍💻 Autor

Proyecto desarrollado como sistema de gestión financiera personal.

## 📄 Licencia

Este proyecto es de uso educativo.