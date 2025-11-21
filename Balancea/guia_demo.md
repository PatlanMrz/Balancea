# 🎯 GUÍA DE DEMOSTRACIÓN - BALANCEA

## ⏱️ Tiempo estimado: 8-10 minutos

---

## 📋 PREPARACIÓN (Antes de la demo)

1. **Generar datos demo**
   - Ejecutar: `python app.py`
   - Hacer clic en "🎲 Generar Demo"
   - Seleccionar "Eliminar todo y crear datos demo nuevos"

2. **Verificar Ollama**
   - Terminal: `ollama serve`
   - Verificar que esté corriendo

3. **Tener preparado**
   - Proyector/pantalla funcionando
   - Aplicación en pantalla completa
   - Ventana de bienvenida cerrada

---

## 🎬 SCRIPT DE DEMOSTRACIÓN

### **[0:00-1:00] INTRODUCCIÓN (1 min)**

> "Buenos días/tardes. Hoy les presentaré **Balancea**, un gestor de finanzas personales inteligente con IA local que desarrollé."

**Mostrar:**
- Ventana principal con pestañas visibles

> "Balancea ayuda a controlar gastos, establecer metas de ahorro, gestionar presupuestos y obtener insights financieros mediante inteligencia artificial, todo de manera local y privada."

---

### **[1:00-2:30] DASHBOARD (1.5 min)**

**Ir a: 📊 Dashboard**

> "Comenzamos en el Dashboard, que muestra un resumen completo de la situación financiera."

**Señalar:**
1. **Tarjetas principales** (arriba)
   - "Aquí vemos el balance total, ingresos, gastos y tasa de ahorro"

2. **Scroll hacia abajo - Estadísticas del mes**
   - "Tenemos estadísticas del mes actual y comparativa con el anterior"

3. **Top 5 Gastos** (hacer scroll)
   - "Y los 5 gastos más grandes para identificar dónde va el dinero"

4. **Resumen de Metas y Presupuestos**
   - "También vemos un resumen de metas y presupuestos activos"

**Acción:** Click en "📄 Exportar Reporte" → "PDF"
> "Podemos exportar todo esto a PDF profesional en cualquier momento"

---

### **[2:30-4:00] TRANSACCIONES (1.5 min)**

**Ir a: 💳 Transacciones**

> "En Transacciones gestionamos todo el registro de ingresos y gastos"

**Demostrar:**

1. **Búsqueda en tiempo real**
   - Escribir "super" en búsqueda
   - "La búsqueda filtra en tiempo real"

2. **Filtros**
   - Filtrar por tipo "Gasto"
   - Filtrar por categoría "Alimentación"
   - "Podemos combinar filtros para análisis específicos"

3. **Agregar transacción**
   - Click "Limpiar Filtros"
   - Completar formulario rápido:
     - Fecha: Hoy
     - Descripción: "Demo presentación"
     - Monto: 150
     - Tipo: Gasto
     - Categoría: Entretenimiento
   - Click "➕ Agregar"
   
   > "Agregar transacciones es muy simple y rápido"

4. **Categorías personalizables**
   - Click "⚙️ Categorías"
   - "Las categorías son completamente personalizables"
   - Cerrar ventana

---

### **[4:00-5:00] METAS (1 min)**

**Ir a: 🎯 Metas**

> "El sistema de metas ayuda a establecer objetivos de ahorro"

**Mostrar:**
- Tarjetas de metas con barras de progreso
- "Vemos el progreso visual, días restantes y estado de cada meta"

**Demostrar:**
- Click en "💰 Agregar Aporte" en cualquier meta
- Ingresar monto: 500
- "Agregar Aporte"
- "La barra se actualiza en tiempo real"

---

### **[5:00-6:00] PRESUPUESTOS (1 min)**

**Ir a: 💰 Presupuestos**

> "Los presupuestos ayudan a controlar gastos por categoría"

**Señalar:**
- Código de colores: Verde, Amarillo, Rojo
- "El sistema alerta automáticamente cuando nos acercamos o excedemos el presupuesto"

**Opcional (si hay tiempo):**
- Click "➕ Nuevo Presupuesto"
- "El sistema sugiere montos basados en historial"
- Cancelar

---

### **[6:00-7:00] ANÁLISIS (1 min)**

**Ir a: 📈 Análisis**

> "El panel de análisis muestra visualizaciones de los datos"

**Mostrar (scroll):**
1. **Gráfica de Pastel**
   - "Distribución de gastos por categoría"

2. **Gráfica de Barras**
   - "Comparativa de ingresos vs gastos por mes"

3. **Gráfica de Línea**
   - "Tendencia de gastos en el tiempo"

---

### **[7:00-8:30] ASISTENTE IA (1.5 min) ⭐**

**Ir a: 💬 Asistente IA**

> "Esta es una de las características más innovadoras: un asistente financiero con IA local usando Ollama"

**Verificar:** Estado debe ser 🟢 Ollama conectado

**Demostrar:**

1. **Comando rápido**
   - Click en "📊 Análisis Completo"
   - "El asistente analiza todos los datos y genera un reporte completo"
   - *Esperar respuesta (10-15 seg)*

2. **Pregunta natural**
   - Escribir: "¿En qué categoría gasto más y cómo puedo reducir ese gasto?"
   - *Esperar respuesta*
   - "Responde de manera contextual basándose en MIS datos reales"

> "Todo esto funciona localmente, sin enviar datos a la nube, garantizando privacidad total"

---

### **[8:30-9:30] ALERTAS Y CIERRE (1 min)**

**Ir a: 🔔 Alertas**

> "Finalmente, el sistema de alertas identifica automáticamente:"

**Señalar:**
- Indicador de salud financiera
- Diferentes tipos de alertas
- "Balance negativo, gastos inusuales, presupuestos excedidos, todo automático"

**Regresar a Dashboard**

---

## 🎤 CIERRE (30 seg)

> "En resumen, Balancea ofrece:"
> 
> 1. **Control completo** de finanzas personales
> 2. **Visualizaciones claras** del dinero
> 3. **Metas y presupuestos** para planificación
> 4. **IA local** para insights inteligentes
> 5. **Reportes profesionales** en PDF
> 
> "Todo desarrollado en Python con Tkinter para la interfaz, Ollama para IA, y Matplotlib para visualizaciones."
>
> "¿Alguna pregunta?"

---

## ❓ PREGUNTAS FRECUENTES (Preparación)

### **"¿Qué pasa si no tengo Ollama?"**
> "La aplicación funciona completamente sin Ollama. El chat simplemente no estará disponible, pero todas las demás funciones operan normalmente."

### **"¿Los datos están seguros?"**
> "Sí, todo se guarda localmente en archivos CSV y JSON. No hay conexión a internet ni servicios externos, excepto Ollama que también es local."

### **"¿Se puede usar en múltiples dispositivos?"**
> "Sí, copiando la carpeta 'datos' entre dispositivos se sincronizan todas las transacciones, metas y presupuestos."

### **"¿Por qué usar IA local?"**
> "Privacidad. Los datos financieros son sensibles y mantenerlos locales garantiza que nadie más tenga acceso."

### **"¿Cuánto tarda en generar los reportes?"**
> "Los reportes PDF se generan en 2-3 segundos típicamente."

---

## ✅ CHECKLIST PRE-DEMO

- [✅] Ollama corriendo (`ollama serve`)
- [ ] Datos demo generados
- [ ] Ventana de bienvenida cerrada
- [ ] Proyector funcionando
- [ ] Aplicación en pantalla completa
- [ ] Cronómetro preparado (8-10 min)
- [ ] Script revisado
- [ ] Respuestas a preguntas preparadas
- [ ] Backup de datos por si algo falla

---

## 💡 TIPS PARA LA DEMO

1. **Practica el flujo** al menos 2 veces antes
2. **Habla con confianza** - conoces el sistema
3. **No te apresures** - es mejor terminar en 8 min que apurarse
4. **Si algo falla** - mantén la calma, explica qué debería pasar
5. **Interactúa** - pregunta "¿Se ve bien?" para engagement
6. **Destaca lo único** - IA local, privacidad, todo en uno

---

**¡Mucha suerte! 🚀**