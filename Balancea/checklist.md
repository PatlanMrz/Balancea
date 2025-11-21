# ✅ CHECKLIST DE FUNCIONALIDADES - BALANCEA

## 📊 Dashboard
- [✅] Visualiza balance total correctamente
- [✅] Muestra total de ingresos
- [✅] Muestra total de gastos
- [✅] Calcula tasa de ahorro
- [✅] Estadísticas del mes actual
- [✅] Comparativa con mes anterior
- [✅] Top 5 gastos más grandes
- [✅] Resumen de metas
- [✅] Resumen de presupuestos
- [✅] Botón de exportar reporte funciona
  - En formato PDF el exporte es correcto, pero,
  - en excel la fecha se muestra como "##########" aunque en barra de fórmulas
  - sí aparece como "15/11/2025  12:00:00 a. m.", tal vez sea la versión que tengo
  - tengo la versión Excel2016.
- [✅] Scroll funciona correctamente

## 💳 Transacciones
* Mejorías: poder selccionar más de una transacción. 
* Al seleccionar una transacción ya establecida que no se pueda presionar el botón de  añadir.
* Cuando se busca una categoria o un tipo, al realizar alguna acción se reincia la sección de transacciones y creo que se debería de quedar así hasta que se limpie o se modifique el filtro.
* Si no hay transacciones me gustaría que hubiera algún mensaje como "añade tu primera transacción con el botón añadir"
- [✅] Agregar transacción funciona
- [✅] Editar transacción funciona
- [✅] Eliminar transacción funciona
- [✅] Búsqueda en tiempo real funciona
- [✅] Filtro por tipo funciona
- [✅] Filtro por categoría funciona
    - Funciona, pero, sería bueno que si ya se 
    - seleccionó el tipo (Gasto o Ingreso) en la categoría salga solo las categorías
    - de esté, ejemplo: si selecciono gasto que no slagan las categorías de ingreso.
- [✅] Limpiar filtros funciona
- [✅] Exportar CSV funciona
  - Funciona, solo que salen todas las transacciones, yo creí que el csv saldría
  - solo con categorías que se filtrarón
- [✅] Gestionar categorías funciona
- [✅] Validaciones de campos funcionan
- [✅] Mensajes de error son claros

## 🎯 Metas
Mejorías: en la sección de mis metas, se va hacia abajo incluyendo las metas completadas y hacia al lado todo se ve blanco no se si se podria que estuvieran al lado las metas compeltadas o algo que haga que ya no se vea esa falta de contenido.
El scroll no funciona con el mouse, solo cuando se presiona manualmente.
- [✅] Crear meta funciona
- [✅] Editar meta funciona
- [✅] Eliminar meta funciona
- [✅] Agregar aporte funciona
- [✅] Barra de progreso se actualiza
- [➖] Alertas de tiempo funcionan
    - No se mostro alguna alerta realmente, pero no se si era hacia el apartado de alertas
    - o en la misma pestaña, pero no se visualizaron alertas.
- [✅] Metas completadas se marcan
- [✅] Resumen general es correcto
- [✅] Días restantes se calculan bien
  - Si sale el tiempo y funciona hasta en los colores, lo malo, es que al completar una
  - meta, está sigue saliendo con el tiempo incluso si ya vencieron, se sigue mostrando
  - cuantos dias de vencida lleva.

## 💰 Presupuestos
* Mejoras: Pestaña está cortada, si son pocos presupuestos hacia abajo se ve en blaco, pero a los lados se sigue viendo en blanco.
* No funciona el scroll con el mouse, pero si al seleccionarlo.
* Cuando no hay presupuestos si se desplaza el scroll hacia arriba la pestaña de presupuestos se va hacia abajo dejando un cuadro en blanco
  - [✅] Crear presupuesto funciona
    - Si funciona, pero se ven cortada las opciones
- [✅] Editar presupuesto funciona
    - Si funciona, pero, el boton de guardar sale cortado, al expandir la pantalla manualmente si aparece y funciona correctamente
- [✅] Eliminar presupuesto funciona
- [✅] Sugerencias automáticas funcionan
- [✅] Porcentaje de uso es correcto
- [✅] Colores cambian según estado
- [✅] Alertas se generan correctamente
  - No se muestran alertas.
- [✅] Resumen general funciona
- [✅] Saldo restante es correcto

## 📈 Análisis
- [✅] Gráfica de pastel se genera
- [✅] Gráfica de barras se genera
- [✅] Gráfica de línea se genera
- [✅] Actualizar gráficas funciona
- [✅] Gráficas muestran datos correctos
- [✅] Sin datos muestra mensaje apropiado

## 💬 Asistente IA
- [✅] Conexión con Ollama funciona
- [❌] Chat responde preguntas
  - Aparece Error: Error de Ollama (código 500)
- [➖] Comandos especiales funcionan (/analisis, /alertas, etc.)
    - No funciona: Cual es mi balance actual y como van mis finanzas este mes, en ambas aparece: Error: Error de Ollama (código 500)
- [✅] Contexto financiero se incluye
- [✅] Historial de conversación funciona
- [✅] Limpiar chat funciona
- [✅] Botones de acciones rápidas funcionan
- [❌] Manejo de errores funciona

## 🔔 Alertas
- [✅] Alertas de balance negativo
- [✅] Alertas de gastos inusuales
- [❌] Alertas de presupuestos
- [✅] Salud financiera se calcula
- [✅] Barra de progreso de salud
- [✅] Tarjetas de alertas se muestran
- [✅] Colores según severidad
- [✅] Actualizar alertas funciona

## 📄 Reportes
- [✅] Exportar PDF funciona
- [✅] PDF incluye resumen
- [✅] PDF incluye transacciones
- [✅] PDF incluye gráficas 
  - Solo la de pastel.
- [✅] PDF incluye top gastos
- [✅] Exportar Excel funciona
- [✅] Excel incluye todas las hojas
- [❌] Formato es profesional
  - Para mí parece solo como si se colocaran los datos sin más no se ve profesional para mí o puede ser lo mismo de la versión de Excel2016

## ⚙️ General
- [✅] Ventana de bienvenida aparece
- [✅] Generar datos demo funciona
- [ ] Atajos de teclado funcionan (F1, F5, Ctrl+Q, Ctrl+H)
  - ctrl + h no muestra algo. también la ventana de ayuda aparece cortada, al momento de expandirla manualmente aparece el botón de cerrar.
- [✅] Cambio de pestañas actualiza datos
- [✅] Splash screen al cargar
- [✅] Datos se guardan correctamente
- [✅] Datos se cargan correctamente
- [❌] No hay errores en consola
  - Cuando se quiere platicar con ollama y no hay datos aparecen errores en la terminal.
- [✅] Rendimiento es aceptable
- [✅] Interfaz es responsiva

## 🐛 Bugs Conocidos
_(Agregar aquí cualquier bug que encuentres)_
- Los que mencione son ejemplos de algunos que he visualizado en esta prueba de testeo.


## 📱 Testing en Diferentes Escenarios

### Sin Datos
- [❌] Dashboard muestra mensaje apropiado
  - no se muestra algún mensaje.
- [✅] Análisis muestra mensaje apropiado
- [✅] Alertas muestra mensaje apropiado
- [✅] No hay crashes
  - De momento no he experimentado.

### Con Muchos Datos (500+ transacciones)
- [✅] Carga en tiempo razonable (<3 segundos)
- [✅] Scroll funciona bien
- [✅] Gráficas se generan correctamente
- [✅] No hay lag en la interfaz

### Datos Extremos
- [✅] Maneja montos muy grandes ($1,000,000+)
- [✅] Maneja montos decimales correctamente
- [✅] Maneja fechas antiguas
- [❌] Maneja descripciones largas
  - En transacciones se despliega hacia los lados la descripción de la transacción si es muy larga aplazando todo, hasta la barra de progreso, llegando a un punto en el que no se puede ver lo que continua, yo creo que es bueno que se ponga un limite de unas 200 palabras como máximo.
- [✅] Maneja caracteres especiales
  - De momento probe con los acentos y funciona bien.

## 🎯 Criterios de Aceptación para Demo

- [✅] ✅ Todas las funcionalidades principales funcionan
- [✅] ✅ No hay errores críticos
- [✅] ✅ La interfaz es intuitiva
- [✅] ✅ Los datos se persisten correctamente
- [✅] ✅ El rendimiento es aceptable
- [✅] ✅ Los reportes se generan correctamente
- [➖] ✅ El chat con IA funciona
- [✅] ✅ Las alertas son útiles
- [✅] ✅ La documentación está completa

---

**Fecha de revisión**: 20/11/2025
**Revisado por**: Patlan Marinez Cesar Eduardo

**Estado**: [ ] En Proceso [ ] Completo [✅] Con Issues