"""
Optimizador del Sistema
Limpieza y optimización de datos
"""

import os
import json
from datetime import datetime, timedelta


class Optimizador:
    """Optimiza y limpia el sistema"""

    def __init__(self, gestor_datos):
        self.gestor_datos = gestor_datos

    def limpiar_transacciones_duplicadas(self):
        """Elimina transacciones duplicadas"""
        transacciones_unicas = []
        vistos = set()

        for t in self.gestor_datos.transacciones:
            # Crear firma única
            firma = f"{t['fecha']}_{t['descripcion']}_{t['monto']}_{t['tipo']}"

            if firma not in vistos:
                transacciones_unicas.append(t)
                vistos.add(firma)

        duplicados = len(self.gestor_datos.transacciones) - len(transacciones_unicas)
        self.gestor_datos.transacciones = transacciones_unicas

        if duplicados > 0:
            self.gestor_datos.guardar_datos()

        return duplicados

    def limpiar_transacciones_antiguas(self, dias=365):
        """Elimina transacciones más antiguas de X días"""
        fecha_limite = datetime.now() - timedelta(days=dias)

        trans_nuevas = [
            t for t in self.gestor_datos.transacciones
            if datetime.strptime(t['fecha'], '%Y-%m-%d') > fecha_limite
        ]

        eliminados = len(self.gestor_datos.transacciones) - len(trans_nuevas)
        self.gestor_datos.transacciones = trans_nuevas

        if eliminados > 0:
            self.gestor_datos.guardar_datos()

        return eliminados

    def corregir_ids_transacciones(self):
        """Corrige IDs de transacciones para que sean secuenciales"""
        for i, trans in enumerate(self.gestor_datos.transacciones, 1):
            trans['id'] = str(i)

        self.gestor_datos.guardar_datos()
        return len(self.gestor_datos.transacciones)

    def crear_backup(self):
        """Crea un backup de todos los datos"""
        from pathlib import Path

        backup_dir = Path("datos/backups")
        backup_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Backup de transacciones
        backup_trans = backup_dir / f"transacciones_{timestamp}.csv"
        if os.path.exists("datos/transacciones.csv"):
            import shutil
            shutil.copy("datos/transacciones.csv", backup_trans)

        # Backup de metas
        backup_metas = backup_dir / f"metas_{timestamp}.json"
        if os.path.exists("datos/metas.json"):
            import shutil
            shutil.copy("datos/metas.json", backup_metas)

        # Backup de presupuestos
        backup_presup = backup_dir / f"presupuestos_{timestamp}.json"
        if os.path.exists("datos/presupuestos.json"):
            import shutil
            shutil.copy("datos/presupuestos.json", backup_presup)

        return {
            'transacciones': str(backup_trans),
            'metas': str(backup_metas),
            'presupuestos': str(backup_presup),
            'timestamp': timestamp
        }

    def limpiar_backups_antiguos(self, mantener=5):
        """Mantiene solo los N backups más recientes"""
        from pathlib import Path

        backup_dir = Path("datos/backups")
        if not backup_dir.exists():
            return 0

        # Obtener todos los backups
        backups = sorted(backup_dir.glob("*.csv")) + sorted(backup_dir.glob("*.json"))
        backups = sorted(backups, key=lambda x: x.stat().st_mtime, reverse=True)

        # Eliminar antiguos
        eliminados = 0
        for backup in backups[mantener:]:
            backup.unlink()
            eliminados += 1

        return eliminados

    def obtener_estadisticas_sistema(self):
        """Obtiene estadísticas del sistema"""
        import sys

        stats = {
            'transacciones': len(self.gestor_datos.transacciones),
            'tamaño_csv': 0,
            'version_python': sys.version,
            'fecha_transaccion_mas_antigua': None,
            'fecha_transaccion_mas_reciente': None,
            'categorias_usadas': set(),
            'total_ingresos': self.gestor_datos.obtener_total_ingresos(),
            'total_gastos': self.gestor_datos.obtener_total_gastos()
        }

        # Tamaño de archivo
        if os.path.exists("datos/transacciones.csv"):
            stats['tamaño_csv'] = os.path.getsize("datos/transacciones.csv")

        # Fechas
        if self.gestor_datos.transacciones:
            fechas = sorted([t['fecha'] for t in self.gestor_datos.transacciones])
            stats['fecha_transaccion_mas_antigua'] = fechas[0]
            stats['fecha_transaccion_mas_reciente'] = fechas[-1]

            # Categorías
            stats['categorias_usadas'] = set([t['categoria'] for t in self.gestor_datos.transacciones])

        return stats

    def optimizar_todo(self):
        """Ejecuta todas las optimizaciones"""
        resultados = {}

        # Backup primero
        resultados['backup'] = self.crear_backup()

        # Limpiar duplicados
        resultados['duplicados_eliminados'] = self.limpiar_transacciones_duplicadas()

        # Corregir IDs
        resultados['ids_corregidos'] = self.corregir_ids_transacciones()

        # Limpiar backups antiguos
        resultados['backups_antiguos_eliminados'] = self.limpiar_backups_antiguos()

        # Estadísticas
        resultados['estadisticas'] = self.obtener_estadisticas_sistema()

        return resultados