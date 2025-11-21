"""
Gestor de Metas Financieras
Maneja objetivos de ahorro y seguimiento
"""

import json
import os
from datetime import datetime
from pathlib import Path


class GestorMetas:
    """Gestiona las metas financieras del usuario"""

    def __init__(self, archivo_metas="datos/metas.json"):
        self.archivo_metas = archivo_metas
        self.metas = []

        # Crear directorio si no existe
        Path("datos").mkdir(exist_ok=True)

        # Cargar metas existentes
        self.cargar_metas()

    def cargar_metas(self):
        """Carga las metas desde el archivo JSON"""
        if not os.path.exists(self.archivo_metas):
            self.metas = []
            return

        try:
            with open(self.archivo_metas, 'r', encoding='utf-8') as f:
                self.metas = json.load(f)
                print(f"✓ {len(self.metas)} metas cargadas")
        except Exception as e:
            print(f"Error al cargar metas: {e}")
            self.metas = []

    def guardar_metas(self):
        """Guarda las metas en el archivo JSON"""
        try:
            with open(self.archivo_metas, 'w', encoding='utf-8') as f:
                json.dump(self.metas, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error al guardar metas: {e}")
            return False

    def agregar_meta(self, nombre, monto_objetivo, fecha_limite=None, descripcion=""):
        """Agrega una nueva meta financiera"""
        nueva_meta = {
            'id': self.generar_id(),
            'nombre': nombre,
            'monto_objetivo': float(monto_objetivo),
            'monto_actual': 0.0,
            'fecha_creacion': datetime.now().strftime('%Y-%m-%d'),
            'fecha_limite': fecha_limite,
            'descripcion': descripcion,
            'completada': False,
            'fecha_completada': None
        }

        self.metas.append(nueva_meta)
        self.guardar_metas()
        return nueva_meta

    def editar_meta(self, id_meta, nombre, monto_objetivo, fecha_limite, descripcion):
        """Edita una meta existente"""
        for meta in self.metas:
            if meta['id'] == id_meta:
                meta['nombre'] = nombre
                meta['monto_objetivo'] = float(monto_objetivo)
                meta['fecha_limite'] = fecha_limite
                meta['descripcion'] = descripcion
                self.guardar_metas()
                return True
        return False

    def eliminar_meta(self, id_meta):
        """Elimina una meta"""
        self.metas = [m for m in self.metas if m['id'] != id_meta]
        self.guardar_metas()

    def actualizar_monto(self, id_meta, monto_actual):
        """Actualiza el monto actual de una meta"""
        for meta in self.metas:
            if meta['id'] == id_meta:
                meta['monto_actual'] = float(monto_actual)

                # Verificar si se completó
                if meta['monto_actual'] >= meta['monto_objetivo'] and not meta['completada']:
                    meta['completada'] = True
                    meta['fecha_completada'] = datetime.now().strftime('%Y-%m-%d')
                elif meta['monto_actual'] < meta['monto_objetivo'] and meta['completada']:
                    meta['completada'] = False
                    meta['fecha_completada'] = None

                self.guardar_metas()
                return True
        return False

    def agregar_aporte(self, id_meta, monto_aporte):
        """Agrega un aporte a una meta"""
        for meta in self.metas:
            if meta['id'] == id_meta:
                meta['monto_actual'] += float(monto_aporte)

                # Verificar si se completó
                if meta['monto_actual'] >= meta['monto_objetivo'] and not meta['completada']:
                    meta['completada'] = True
                    meta['fecha_completada'] = datetime.now().strftime('%Y-%m-%d')

                self.guardar_metas()
                return True
        return False

    def obtener_progreso(self, id_meta):
        """Obtiene el progreso de una meta (0-100)"""
        for meta in self.metas:
            if meta['id'] == id_meta:
                if meta['monto_objetivo'] == 0:
                    return 0
                progreso = (meta['monto_actual'] / meta['monto_objetivo']) * 100
                return min(progreso, 100)  # Máximo 100%
        return 0

    def obtener_metas_activas(self):
        """Obtiene metas no completadas"""
        return [m for m in self.metas if not m['completada']]

    def obtener_metas_completadas(self):
        """Obtiene metas completadas"""
        return [m for m in self.metas if m['completada']]

    def obtener_meta_por_id(self, id_meta):
        """Obtiene una meta específica por ID"""
        for meta in self.metas:
            if meta['id'] == id_meta:
                return meta
        return None

    def calcular_dias_restantes(self, id_meta):
        """Calcula días restantes para una meta"""
        meta = self.obtener_meta_por_id(id_meta)
        if not meta or not meta['fecha_limite']:
            return None

        try:
            fecha_limite = datetime.strptime(meta['fecha_limite'], '%Y-%m-%d')
            hoy = datetime.now()
            dias = (fecha_limite - hoy).days
            return dias
        except:
            return None

    def obtener_alerta_meta(self, id_meta):
        """Genera alerta según el estado de la meta"""
        meta = self.obtener_meta_por_id(id_meta)
        if not meta:
            return None

        progreso = self.obtener_progreso(id_meta)
        dias_restantes = self.calcular_dias_restantes(id_meta)

        alertas = []

        # Meta completada
        if meta['completada']:
            alertas.append({
                'tipo': 'exito',
                'mensaje': f"🎉 ¡Meta '{meta['nombre']}' completada!"
            })

        # Progreso importante alcanzado
        elif progreso >= 75:
            alertas.append({
                'tipo': 'exito',
                'mensaje': f"¡Casi lo logras! {progreso:.1f}% de '{meta['nombre']}'"
            })
        elif progreso >= 50:
            alertas.append({
                'tipo': 'info',
                'mensaje': f"¡Mitad del camino! {progreso:.1f}% de '{meta['nombre']}'"
            })
        elif progreso >= 25:
            alertas.append({
                'tipo': 'info',
                'mensaje': f"Buen progreso: {progreso:.1f}% de '{meta['nombre']}'"
            })

        # Alertas de tiempo
        if dias_restantes is not None:
            if dias_restantes < 0:
                alertas.append({
                    'tipo': 'peligro',
                    'mensaje': f"⚠️ Meta '{meta['nombre']}' venció hace {abs(dias_restantes)} días"
                })
            elif dias_restantes <= 7:
                alertas.append({
                    'tipo': 'advertencia',
                    'mensaje': f"⏰ Quedan {dias_restantes} días para '{meta['nombre']}'"
                })
            elif dias_restantes <= 30:
                alertas.append({
                    'tipo': 'info',
                    'mensaje': f"📅 {dias_restantes} días restantes para '{meta['nombre']}'"
                })

        return alertas if alertas else None

    def generar_id(self):
        """Genera un ID único para la meta"""
        if not self.metas:
            return "1"
        return str(max([int(m['id']) for m in self.metas]) + 1)

    def obtener_resumen(self):
        """Obtiene resumen de todas las metas"""
        total = len(self.metas)
        activas = len(self.obtener_metas_activas())
        completadas = len(self.obtener_metas_completadas())

        monto_total_objetivo = sum([m['monto_objetivo'] for m in self.metas])
        monto_total_actual = sum([m['monto_actual'] for m in self.metas])

        progreso_general = (monto_total_actual / monto_total_objetivo * 100) if monto_total_objetivo > 0 else 0

        return {
            'total': total,
            'activas': activas,
            'completadas': completadas,
            'monto_total_objetivo': monto_total_objetivo,
            'monto_total_actual': monto_total_actual,
            'progreso_general': progreso_general
        }