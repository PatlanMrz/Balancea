"""
Analizador de Patrones y Tendencias
Detecta anomalías y genera insights
"""

from datetime import datetime, timedelta
from statistics import mean, median
import calendar


class AnalizadorFinanciero:
    """Analiza patrones financieros y genera alertas"""

    def __init__(self, gestor_datos):
        self.gestor_datos = gestor_datos

    def analizar_todo(self):
        """Ejecuta todos los análisis y retorna alertas"""
        alertas = []

        # Solo analizar si hay datos
        if not self.gestor_datos.transacciones:
            return []

        # Detectar balance negativo
        alerta_balance = self.detectar_balance_negativo()
        if alerta_balance:
            alertas.append(alerta_balance)

        # Detectar gastos inusuales
        alertas_gastos = self.detectar_gastos_inusuales()
        alertas.extend(alertas_gastos)

        # Analizar categoría con más gastos
        alerta_categoria = self.analizar_categoria_maxima()
        if alerta_categoria:
            alertas.append(alerta_categoria)

        # Comparar con mes anterior
        alerta_comparativa = self.comparar_con_mes_anterior()
        if alerta_comparativa:
            alertas.append(alerta_comparativa)

        # Analizar tendencia de gastos
        alerta_tendencia = self.analizar_tendencia()
        if alerta_tendencia:
            alertas.append(alerta_tendencia)

        # Generar recomendaciones
        recomendaciones = self.generar_recomendaciones()
        alertas.extend(recomendaciones)

        return alertas

    def detectar_balance_negativo(self):
        """Detecta si el balance es negativo"""
        balance = self.gestor_datos.obtener_balance()

        if balance < 0:
            return {
                'tipo': 'peligro',
                'titulo': '⚠️ Balance Negativo',
                'mensaje': f'Tu balance actual es negativo: ${balance:,.2f}. Estás gastando más de lo que ganas.',
                'severidad': 'alta',
                'categoria': 'balance'
            }

        return None

    def detectar_gastos_inusuales(self):
        """Detecta gastos que sean significativamente mayores al promedio"""
        alertas = []

        gastos = [t for t in self.gestor_datos.transacciones if t['tipo'] == 'Gasto']

        if len(gastos) < 3:
            return alertas

        # Calcular promedio y mediana
        montos = [g['monto'] for g in gastos]
        promedio = mean(montos)
        mediana_valor = median(montos)

        # Detectar gastos que sean 2x el promedio
        umbral = promedio * 2

        for gasto in gastos:
            if gasto['monto'] >= umbral:
                alertas.append({
                    'tipo': 'advertencia',
                    'titulo': '💸 Gasto Inusual Detectado',
                    'mensaje': f"Gasto de ${gasto['monto']:,.2f} en '{gasto['descripcion']}' es {gasto['monto'] / promedio:.1f}x mayor que tu promedio (${promedio:,.2f})",
                    'severidad': 'media',
                    'categoria': 'gasto_inusual',
                    'detalles': gasto
                })

        return alertas[:3]  # Máximo 3 alertas

    def analizar_categoria_maxima(self):
        """Analiza la categoría con más gastos"""
        gastos_cat = self.gestor_datos.obtener_gastos_por_categoria()

        if not gastos_cat:
            return None

        total_gastos = self.gestor_datos.obtener_total_gastos()
        max_cat = max(gastos_cat, key=gastos_cat.get)
        max_monto = gastos_cat[max_cat]
        porcentaje = (max_monto / total_gastos * 100) if total_gastos > 0 else 0

        if porcentaje > 40:  # Si una categoría representa más del 40%
            return {
                'tipo': 'info',
                'titulo': '📊 Categoría Dominante',
                'mensaje': f"'{max_cat}' representa el {porcentaje:.1f}% de tus gastos totales (${max_monto:,.2f}). Considera diversificar o revisar esta categoría.",
                'severidad': 'baja',
                'categoria': 'concentracion'
            }

        return None

    def comparar_con_mes_anterior(self):
        """Compara gastos con el mes anterior"""
        fecha_actual = datetime.now()

        # Transacciones mes actual
        trans_mes_actual = [t for t in self.gestor_datos.transacciones
                            if datetime.strptime(t['fecha'], '%Y-%m-%d').month == fecha_actual.month
                            and datetime.strptime(t['fecha'], '%Y-%m-%d').year == fecha_actual.year]

        # Mes anterior
        primer_dia_mes = fecha_actual.replace(day=1)
        ultimo_dia_mes_anterior = primer_dia_mes - timedelta(days=1)
        mes_anterior = ultimo_dia_mes_anterior.month
        año_anterior = ultimo_dia_mes_anterior.year

        trans_mes_anterior = [t for t in self.gestor_datos.transacciones
                              if datetime.strptime(t['fecha'], '%Y-%m-%d').month == mes_anterior
                              and datetime.strptime(t['fecha'], '%Y-%m-%d').year == año_anterior]

        if not trans_mes_anterior:
            return None

        gastos_actual = sum([t['monto'] for t in trans_mes_actual if t['tipo'] == 'Gasto'])
        gastos_anterior = sum([t['monto'] for t in trans_mes_anterior if t['tipo'] == 'Gasto'])

        if gastos_anterior == 0:
            return None

        variacion = ((gastos_actual - gastos_anterior) / gastos_anterior) * 100

        if variacion > 20:  # Aumento de más del 20%
            return {
                'tipo': 'advertencia',
                'titulo': '📈 Aumento en Gastos',
                'mensaje': f"Tus gastos aumentaron un {variacion:.1f}% respecto al mes anterior. Mes anterior: ${gastos_anterior:,.2f}, Mes actual: ${gastos_actual:,.2f}",
                'severidad': 'media',
                'categoria': 'tendencia'
            }
        elif variacion < -20:  # Reducción de más del 20%
            return {
                'tipo': 'exito',
                'titulo': '🎉 Reducción en Gastos',
                'mensaje': f"¡Excelente! Redujiste tus gastos un {abs(variacion):.1f}% respecto al mes anterior. Sigue así.",
                'severidad': 'baja',
                'categoria': 'mejora'
            }

        return None

    def analizar_tendencia(self):
        """Analiza la tendencia de gastos en los últimos días"""
        if len(self.gestor_datos.transacciones) < 5:
            return None

        # Últimos 7 días
        hace_7_dias = datetime.now() - timedelta(days=7)

        gastos_recientes = [t for t in self.gestor_datos.transacciones
                            if t['tipo'] == 'Gasto'
                            and datetime.strptime(t['fecha'], '%Y-%m-%d') >= hace_7_dias]

        if len(gastos_recientes) < 3:
            return None

        total_reciente = sum([g['monto'] for g in gastos_recientes])
        promedio_diario = total_reciente / 7

        # Calcular promedio histórico
        todos_gastos = [t for t in self.gestor_datos.transacciones if t['tipo'] == 'Gasto']
        if len(todos_gastos) < 10:
            return None

        fechas_unicas = set([t['fecha'] for t in todos_gastos])
        dias_totales = len(fechas_unicas)
        promedio_historico = sum([g['monto'] for g in todos_gastos]) / dias_totales

        if promedio_diario > promedio_historico * 1.5:
            return {
                'tipo': 'advertencia',
                'titulo': '📊 Gastos Elevados Últimamente',
                'mensaje': f"En los últimos 7 días gastas ${promedio_diario:.2f}/día, que es {promedio_diario / promedio_historico:.1f}x tu promedio normal (${promedio_historico:.2f}/día)",
                'severidad': 'media',
                'categoria': 'tendencia'
            }

        return None

    def generar_recomendaciones(self):
        """Genera recomendaciones basadas en los datos"""
        recomendaciones = []

        balance = self.gestor_datos.obtener_balance()
        ingresos = self.gestor_datos.obtener_total_ingresos()
        gastos = self.gestor_datos.obtener_total_gastos()

        if ingresos == 0:
            return recomendaciones

        # Calcular tasa de ahorro
        tasa_ahorro = (balance / ingresos * 100)

        if tasa_ahorro < 10:
            recomendaciones.append({
                'tipo': 'consejo',
                'titulo': '💡 Consejo de Ahorro',
                'mensaje': f"Tu tasa de ahorro es del {tasa_ahorro:.1f}%. Intenta ahorrar al menos el 20% de tus ingresos. Considera reducir gastos no esenciales.",
                'severidad': 'baja',
                'categoria': 'recomendacion'
            })
        elif tasa_ahorro >= 30:
            recomendaciones.append({
                'tipo': 'exito',
                'titulo': '🌟 ¡Excelente Gestión!',
                'mensaje': f"Tu tasa de ahorro es del {tasa_ahorro:.1f}%. ¡Estás haciendo un trabajo fantástico! Sigue así.",
                'severidad': 'baja',
                'categoria': 'felicitacion'
            })

        # Analizar categorías con potencial de ahorro
        gastos_cat = self.gestor_datos.obtener_gastos_por_categoria()
        if gastos_cat:
            for categoria in ['Entretenimiento', 'Comida', 'Transporte']:
                if categoria in gastos_cat:
                    monto = gastos_cat[categoria]
                    porcentaje = (monto / gastos * 100) if gastos > 0 else 0

                    if porcentaje > 25:
                        recomendaciones.append({
                            'tipo': 'consejo',
                            'titulo': f'💰 Oportunidad en {categoria}',
                            'mensaje': f"Gastas ${monto:,.2f} ({porcentaje:.1f}%) en {categoria}. Reducir un 10% aquí te ahorraría ${monto * 0.1:,.2f}",
                            'severidad': 'baja',
                            'categoria': 'oportunidad'
                        })
                        break  # Solo una recomendación de este tipo

        return recomendaciones[:2]  # Máximo 2 recomendaciones

    def obtener_resumen_salud_financiera(self):
        """Genera un resumen del estado de salud financiera"""
        balance = self.gestor_datos.obtener_balance()
        ingresos = self.gestor_datos.obtener_total_ingresos()
        gastos = self.gestor_datos.obtener_total_gastos()

        if ingresos == 0:
            return {
                'puntuacion': 0,
                'nivel': 'Sin datos',
                'color': '#95A5A6'
            }

        tasa_ahorro = (balance / ingresos * 100)

        # Calcular puntuación (0-100)
        puntuacion = 0

        # 40 puntos por tasa de ahorro
        if tasa_ahorro >= 30:
            puntuacion += 40
        elif tasa_ahorro >= 20:
            puntuacion += 30
        elif tasa_ahorro >= 10:
            puntuacion += 20
        elif tasa_ahorro > 0:
            puntuacion += 10

        # 30 puntos por balance positivo
        if balance > 0:
            puntuacion += 30

        # 30 puntos por diversificación de gastos
        gastos_cat = self.gestor_datos.obtener_gastos_por_categoria()
        if gastos_cat:
            max_cat_pct = (max(gastos_cat.values()) / gastos * 100) if gastos > 0 else 100
            if max_cat_pct < 30:
                puntuacion += 30
            elif max_cat_pct < 50:
                puntuacion += 15

        # Determinar nivel y color
        if puntuacion >= 80:
            nivel = 'Excelente'
            color = '#27AE60'
        elif puntuacion >= 60:
            nivel = 'Buena'
            color = '#3498DB'
        elif puntuacion >= 40:
            nivel = 'Regular'
            color = '#F39C12'
        else:
            nivel = 'Necesita mejorar'
            color = '#E74C3C'

        return {
            'puntuacion': puntuacion,
            'nivel': nivel,
            'color': color,
            'tasa_ahorro': tasa_ahorro
        }