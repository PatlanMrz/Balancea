# 📖 Guía de Uso - Balancea v1.0

## 🚀 Inicio Rápido

### Primera vez usando Balancea

1. **Ejecuta la aplicación**: `python app.py`
2. **Agrega tu primera transacción**:
   - Ve a la pestaña "💳 Transacciones"
   - Completa el formulario
   - Haz clic en "➕ Agregar"
3. **Visualiza tus finanzas**:
   - Dashboard: Resumen general
   - Análisis: Gráficas detalladas

---

## 📊 Dashboard

El Dashboard muestra un resumen completo de tus finanzas:

### Tarjetas Principales
- **Balance Total**: Ingresos - Gastos
- **Total Ingresos**: Suma de todos los ingresos
- **Total Gastos**: Suma de todos los gastos
- **Tasa de Ahorro**: Porcentaje de ahorro sobre ingresos

### Estadísticas del Mes
- Ingresos, gastos y balance del mes actual
- Número de transacciones registradas

### Comparativa con Mes Anterior
- Cambio en ingresos, gastos y balance
- Porcentajes de variación
- Colores: 🟢 Verde (positivo) | 🔴 Rojo (negativo)

### Top 5 Gastos
- Los 5 gastos más grandes registrados
- Útil para identificar gastos importantes

---

## 💳 Gestión de Transacciones

### Agregar Transacción

1. Selecciona la **fecha**
2. Escribe una **descripción** clara (mín. 3 caracteres)
3. Ingresa el **monto** (solo números positivos)
4. Selecciona el **tipo**: Ingreso o Gasto
5. Elige una **categoría**
6. Haz clic en **"➕ Agregar"**

💡 **Tip**: La descripción te ayudará a buscar transacciones después

### Editar Transacción

1. Haz clic en la transacción que deseas editar
2. Los datos se cargarán en el formulario
3. Modifica lo necesario
4. Haz clic en **"✏️ Editar"**

### Eliminar Transacción

1. Selecciona la transacción
2. Haz clic en **"🗑️ Eliminar"**
3. Confirma la eliminación

⚠️ **Advertencia**: La eliminación es permanente

---

## 🔍 Búsqueda y Filtros

### Buscar Transacciones
- Escribe en el campo de búsqueda
- La búsqueda es en tiempo real
- Busca por descripción

### Filtros Disponibles
1. **Por Tipo**: Todos, Ingreso, Gasto
2. **Por Categoría**: Todas las categorías disponibles

### Limpiar Filtros
- Haz clic en **"🔄 Limpiar Filtros"**
- Restaura la vista completa

---

## ⚙️ Gestión de Categorías

### Abrir Gestor de Categorías
- Haz clic en **"⚙️ Categorías"**

### Agregar Categoría
1. Selecciona el tipo (Ingreso/Gasto)
2. Haz clic en **"➕ Agregar"**
3. Escribe el nombre
4. Confirma

### Editar Categoría
1. Selecciona la categoría de la lista
2. Haz clic en **"✏️ Editar"**
3. Escribe el nuevo nombre
4. Confirma

### Eliminar Categoría
1. Selecciona la categoría
2. Haz clic en **"🗑️ Eliminar"**
3. Confirma

### Restaurar Categorías por Defecto
- Haz clic en **"🔄 Restaurar por defecto"**
- Elimina todas las personalizaciones

---

## 📈 Análisis y Gráficas

### Gráficas Disponibles

#### 1. Gráfica de Pastel
- Muestra gastos por categoría
- Porcentaje de cada categoría
- Identifica en qué gastas más

#### 2. Gráfica de Barras
- Compara ingresos vs gastos por mes
- Verde: Ingresos | Rojo: Gastos
- Visualiza tendencias mensuales

#### 3. Gráfica de Línea
- Tendencia de gastos en el tiempo
- Identifica patrones
- Área sombreada bajo la curva

### Actualizar Gráficas
- Haz clic en **"🔄 Actualizar Gráficas"**
- Se actualizan automáticamente al agregar/editar/eliminar

---

## 📥 Exportar Datos

### Exportar a CSV
1. Haz clic en **"📥 Exportar CSV"**
2. Selecciona la ubicación
3. Guarda el archivo

### Usos del CSV Exportado
- Respaldo de datos
- Análisis en Excel
- Compartir con contador
- Importar en otras apps

---

## ⌨️ Atajos de Teclado

| Atajo | Acción |
|-------|--------|
| **F1** | Mostrar ayuda |
| **F5** | Actualizar dashboard |
| **Ctrl+Q** | Salir de la aplicación |
| **Delete** | Eliminar transacción seleccionada |
| **Esc** | Limpiar formulario |

💡 Presiona **F1** en cualquier momento para ver los atajos

---

## 💡 Consejos y Buenas Prácticas

### Para Mejores Resultados

1. **Sé consistente con las descripciones**
   - Usa nombres similares para gastos recurrentes
   - Ejemplo: "Supermercado Walmart" en lugar de solo "Compras"

2. **Registra transacciones regularmente**
   - Idealmente diariamente o semanalmente
   - Evita acumular muchas transacciones

3. **Usa categorías específicas**
   - Crea categorías personalizadas para tu caso
   - Ejemplo: "Gimnasio" en lugar de solo "Salud"

4. **Revisa el dashboard semanalmente**
   - Identifica patrones de gasto
   - Ajusta tu presupuesto según necesites

5. **Exporta respaldos regularmente**
   - Al menos una vez al mes
   - Guarda en la nube o disco externo

### Interpretando las Estadísticas

- **Tasa de Ahorro < 20%**: Considera reducir gastos
- **Tasa de Ahorro 20-30%**: Rango saludable
- **Tasa de Ahorro > 30%**: Excelente manejo financiero

- **Balance Negativo**: Gastas más de lo que ganas
- **Balance Positivo**: Estás ahorrando

---

## ❓ Preguntas Frecuentes

### ¿Dónde se guardan mis datos?
En la carpeta `datos/` del proyecto:
- `transacciones.csv` - Tus transacciones
- `categorias.json` - Categorías personalizadas

### ¿Puedo usar Balancea en múltiples computadoras?
Sí, copia la carpeta `datos/` a otra computadora con Balancea instalado.

### ¿Los datos están seguros?
Los datos se guardan localmente en tu computadora. No se envían a internet.

### ¿Qué pasa si elimino una transacción por error?
No hay función de deshacer. Haz respaldos regulares con "Exportar CSV".

### ¿Puedo importar datos de otras apps?
Actualmente no. Esta función se agregará en futuras versiones.

---

## 🐛 Solución de Problemas

### La aplicación no inicia
```bash
# Verifica que Python esté instalado
python --version

# Reinstala dependencias
pip install -r requirements.txt
```

### No aparecen las gráficas
- Verifica que matplotlib esté instalado
- Asegúrate de tener transacciones registradas

### Error al guardar datos
- Verifica permisos de escritura en la carpeta `datos/`
- Cierra otras apps que puedan estar usando los archivos

### Las categorías no aparecen
- Haz clic en "⚙️ Categorías" y "🔄 Restaurar por defecto"

---

## 📞 Soporte

Si encuentras algún problema:
1. Revisa esta guía
2. Verifica los logs en la consola
3. Contacta al desarrollador

---

## 🎯 Próximas Características (Semana 2+)

- 💬 **Asistente IA con Ollama**
- 🔔 **Alertas inteligentes**
- 🎯 **Metas de ahorro**
- 📄 **Reportes en PDF**
- 📊 **Presupuestos por categoría**

---

**Versión**: 1.0.0  
**Última actualización**: Noviembre 2024