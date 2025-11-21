"""
Gestor de Presupuestos
Maneja presupuestos por categoría y seguimiento
"""

import json
import os
from datetime import datetime
from pathlib import Path


class GestorPresupuestos:
    """Gestiona presupuestos por categoría"""

    def __init__(self, gestor_datos, archivo_presupuestos="datos/presupuestos.json"):
        self.gestor_datos = gestor_datos
        self.archivo_presupuestos = archivo_presupuestos
        self.presupuestos = {}

        # Crear directorio si no existe
        Path("datos").mkdir(exist_ok=True)

        # Cargar presupuestos
        self.cargar_presupuestos()

    def cargar_presupuestos(self):
        """Carga presupuestos desde archivo JSON"""
        if not os.path.exists(self.archivo_presupuestos):
            self.presupuestos = {}
            return

        try:
            with open(self.archivo_presupuestos, 'r', encoding='utf-8') as f:
                self.presupuestos = json.load(f)
                print(f"✓ Presupuestos cargados")
        except Exception as e:
            print(f"Error al cargar presupuestos: {e}")
            self.presupuestos = {}

    def guardar_presupuestos(self):
        """Guarda presupuestos en archivo JSON"""
        try:
            with open(self.archivo_presupuestos, 'w', encoding='utf-8') as f:
                json.dump(self.presupuestos, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error al guardar presupuestos: {e}")
            return False

    def establecer_presupuesto(self, categoria, monto):
        """Establece o actualiza presupuesto para una categoría"""
        if monto <= 0:
            return False

        self.presupuestos[categoria] = {
            'monto': float(monto),
            'fecha_creacion': datetime.now().strftime('%Y-%m-%d'),
            'mes_actual': datetime.now().strftime('%Y-%m')
        }

        return self.guardar_presupuestos()

    def eliminar_presupuesto(self, categoria):
        """Elimina presupuesto de una categoría"""
        if categoria in self.presupuestos:
            del self.presupuestos[categoria]
            return self.guardar_presupuestos()
        return False

    def obtener_presupuesto(self, categoria):
        """Obtiene presupuesto de una categoría"""
        return self.presupuestos.get(categoria, None)

    def obtener_gasto_categoria_mes_actual(self, categoria):
        """Obtiene el gasto actual de una categoría en el mes"""
        fecha_actual = datetime.now()
        mes_actual = fecha_actual.month
        año_actual = fecha_actual.year

        gastos = [t for t in self.gestor_datos.transacciones
                  if t['tipo'] == 'Gasto'
                  and t['categoria'] == categoria
                  and datetime.strptime(t['fecha'], '%Y-%m-%d').month == mes_actual
                  and datetime.strptime(t['fecha'], '%Y-%m-%d').year == año_actual]

        return sum([g['monto'] for g in gastos])

    def obtener_porcentaje_uso(self, categoria):
        """Calcula el porcentaje usado del presupuesto"""
        presupuesto = self.obtener_presupuesto(categoria)
        if not presupuesto:
            return None

        gasto_actual = self.obtener_gasto_categoria_mes_actual(categoria)
        porcentaje = (gasto_actual / presupuesto['monto']) * 100

        return porcentaje

    def obtener_saldo_restante(self, categoria):
        """Obtiene el saldo restante del presupuesto"""
        presupuesto = self.obtener_presupuesto(categoria)
        if not presupuesto:
            return None

        gasto_actual = self.obtener_gasto_categoria_mes_actual(categoria)
        restante = presupuesto['monto'] - gasto_actual

        return restante

    def verificar_alerta(self, categoria):
        """Verifica si hay alertas para una categoría"""
        porcentaje = self.obtener_porcentaje_uso(categoria)

        if porcentaje is None:
            return None

        alertas = []

        if porcentaje >= 100:
            alertas.append({
                'tipo': 'peligro',
                'mensaje': f"¡Presupuesto de '{categoria}' EXCEDIDO! ({porcentaje:.1f}%)"
            })
        elif porcentaje >= 90:
            alertas.append({
                'tipo': 'peligro',
                'mensaje': f"Presupuesto de '{categoria}' casi agotado ({porcentaje:.1f}%)"
            })
        elif porcentaje >= 80:
            alertas.append({
                'tipo': 'advertencia',
                'mensaje': f"Presupuesto de '{categoria}' en {porcentaje:.1f}%"
            })
        elif porcentaje >= 50:
            alertas.append({
                'tipo': 'info',
                'mensaje': f"Presupuesto de '{categoria}' en {porcentaje:.1f}%"
            })

        return alertas

    def obtener_todas_alertas(self):
        """Obtiene todas las alertas de presupuestos"""
        alertas = []

        for categoria in self.presupuestos.keys():
            alertas_cat = self.verificar_alerta(categoria)
            if alertas_cat:
                alertas.extend(alertas_cat)

        return alertas

    def obtener_resumen(self):
        """Obtiene resumen de todos los presupuestos"""
        total_presupuestado = sum([p['monto'] for p in self.presupuestos.values()])

        total_gastado = 0
        for categoria in self.presupuestos.keys():
            total_gastado += self.obtener_gasto_categoria_mes_actual(categoria)

        porcentaje_uso_general = (total_gastado / total_presupuestado * 100) if total_presupuestado > 0 else 0

        return {
            'total_presupuestado': total_presupuestado,
            'total_gastado': total_gastado,
            'saldo_restante': total_presupuestado - total_gastado,
            'porcentaje_uso': porcentaje_uso_general,
            'categorias_con_presupuesto': len(self.presupuestos),
            'categorias_excedidas': len([c for c in self.presupuestos.keys()
                                         if self.obtener_porcentaje_uso(c) >= 100])
        }

    def obtener_categorias_sin_presupuesto(self):
        """Obtiene categorías de gasto sin presupuesto asignado"""
        todas_categorias = self.gestor_datos.categorias.get('Gasto', [])
        categorias_sin_presupuesto = [c for c in todas_categorias
                                      if c not in self.presupuestos]
        return categorias_sin_presupuesto

    def sugerir_presupuesto(self, categoria):
        """Sugiere un presupuesto basado en gastos históricos"""
        # Calcular promedio de los últimos 3 meses
        fecha_actual = datetime.now()

        gastos_historicos = []
        for i in range(3):
            mes = fecha_actual.month - i
            año = fecha_actual.year

            if mes <= 0:
                mes += 12
                año -= 1

            gastos_mes = [t['monto'] for t in self.gestor_datos.transacciones
                          if t['tipo'] == 'Gasto'
                          and t['categoria'] == categoria
                          and datetime.strptime(t['fecha'], '%Y-%m-%d').month == mes
                          and datetime.strptime(t['fecha'], '%Y-%m-%d').year == año]

            if gastos_mes:
                gastos_historicos.append(sum(gastos_mes))

        if gastos_historicos:
            promedio = sum(gastos_historicos) / len(gastos_historicos)
            # Agregar 10% de margen
            sugerencia = promedio * 1.1
            return round(sugerencia, 2)

        return None

    def resetear_mes_nuevo(self):
        """Verifica y resetea presupuestos para mes nuevo (opcional)"""
        mes_actual = datetime.now().strftime('%Y-%m')

        reseteos = 0
        for categoria, datos in self.presupuestos.items():
            if datos.get('mes_actual') != mes_actual:
                # Actualizar mes
                datos['mes_actual'] = mes_actual
                reseteos += 1

        if reseteos > 0:
            self.guardar_presupuestos()

        return reseteos