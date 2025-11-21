"""
Gestor de Transacciones
Maneja todas las operaciones CRUD de transacciones
"""

import csv
import os
from datetime import datetime
from pathlib import Path
import pandas as pd
from datos.config_categorias import GestorCategorias


class GestorTransacciones:
    """Gestiona las transacciones financieras"""

    def __init__(self, archivo_datos="datos/transacciones.csv"):
        self.archivo_datos = archivo_datos
        self.transacciones = []

        # Usar el gestor de categorías personalizable
        self.gestor_categorias = GestorCategorias()
        self.categorias = self.gestor_categorias.obtener_categorias()

        # Crear directorio de datos si no existe
        Path("datos").mkdir(exist_ok=True)

        # Cargar datos existentes
        self.cargar_datos()

    def obtener_categorias(self):
        """Retorna las categorías disponibles"""
        return self.gestor_categorias.obtener_categorias()

    def cargar_datos(self):
        """Carga transacciones desde el archivo CSV"""
        if not os.path.exists(self.archivo_datos):
            self.crear_archivo_datos()
            return

        try:
            # Verificar si el archivo está vacío
            if os.path.getsize(self.archivo_datos) == 0:
                self.crear_archivo_datos()
                return

            with open(self.archivo_datos, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.transacciones = list(reader)

                # Convertir montos a float y validar datos
                transacciones_validas = []
                for t in self.transacciones:
                    try:
                        t['monto'] = float(t['monto'])
                        # Validar que tenga todos los campos necesarios
                        if all(k in t for k in ['id', 'fecha', 'descripcion', 'monto', 'tipo', 'categoria']):
                            transacciones_validas.append(t)
                    except (ValueError, KeyError) as e:
                        print(f"Advertencia: Transacción inválida ignorada: {e}")
                        continue

                self.transacciones = transacciones_validas
                print(f"✓ {len(self.transacciones)} transacciones cargadas correctamente")

        except Exception as e:
            print(f"Error al cargar datos: {e}")
            self.transacciones = []

    def crear_archivo_datos(self):
        """Crea el archivo CSV con encabezados"""
        with open(self.archivo_datos, 'w', newline='', encoding='utf-8') as f:  # ✅ CORREGIDO
            campos = ['id', 'fecha', 'descripcion', 'monto', 'tipo', 'categoria']
            writer = csv.DictWriter(f, fieldnames=campos)
            writer.writeheader()

    def guardar_datos(self):
        """Guarda todas las transacciones en el archivo CSV"""
        try:
            with open(self.archivo_datos, 'w', newline='', encoding='utf-8') as f:
                campos = ['id', 'fecha', 'descripcion', 'monto', 'tipo', 'categoria']
                writer = csv.DictWriter(f, fieldnames=campos)
                writer.writeheader()
                writer.writerows(self.transacciones)
            return True
        except Exception as e:
            print(f"Error al guardar datos: {e}")
            return False

    def agregar_transaccion(self, fecha, descripcion, monto, tipo, categoria):
        """Agrega una nueva transacción"""
        nueva_transaccion = {
            'id': self.generar_id(),
            'fecha': fecha,
            'descripcion': descripcion,
            'monto': float(monto),
            'tipo': tipo,
            'categoria': categoria
        }

        self.transacciones.append(nueva_transaccion)
        self.guardar_datos()
        return nueva_transaccion

    def editar_transaccion(self, id_transaccion, fecha, descripcion, monto, tipo, categoria):
        """Edita una transacción existente"""
        for t in self.transacciones:
            if t['id'] == id_transaccion:
                t['fecha'] = fecha
                t['descripcion'] = descripcion
                t['monto'] = float(monto)
                t['tipo'] = tipo
                t['categoria'] = categoria
                self.guardar_datos()
                return True
        return False

    def eliminar_transaccion(self, id_transaccion):
        """Elimina una transacción"""
        self.transacciones = [t for t in self.transacciones if t['id'] != id_transaccion]
        self.guardar_datos()

    def generar_id(self):
        """Genera un ID único para la transacción"""
        if not self.transacciones:
            return "1"
        return str(max([int(t['id']) for t in self.transacciones]) + 1)

    def obtener_transacciones(self, filtro_tipo=None, filtro_categoria=None,
                             fecha_inicio=None, fecha_fin=None):
        """Obtiene transacciones con filtros opcionales"""
        resultado = self.transacciones.copy()

        if filtro_tipo:
            resultado = [t for t in resultado if t['tipo'] == filtro_tipo]

        if filtro_categoria:
            resultado = [t for t in resultado if t['categoria'] == filtro_categoria]

        if fecha_inicio:
            resultado = [t for t in resultado if t['fecha'] >= fecha_inicio]

        if fecha_fin:
            resultado = [t for t in resultado if t['fecha'] <= fecha_fin]

        return resultado

    def obtener_balance(self):
        """Calcula el balance total (ingresos - gastos)"""
        ingresos = sum([t['monto'] for t in self.transacciones if t['tipo'] == 'Ingreso'])
        gastos = sum([t['monto'] for t in self.transacciones if t['tipo'] == 'Gasto'])
        return ingresos - gastos

    def obtener_total_ingresos(self):
        """Calcula el total de ingresos"""
        return sum([t['monto'] for t in self.transacciones if t['tipo'] == 'Ingreso'])

    def obtener_total_gastos(self):
        """Calcula el total de gastos"""
        return sum([t['monto'] for t in self.transacciones if t['tipo'] == 'Gasto'])

    def obtener_gastos_por_categoria(self):
        """Obtiene gastos agrupados por categoría"""
        gastos = [t for t in self.transacciones if t['tipo'] == 'Gasto']
        categorias_dict = {}

        for gasto in gastos:
            cat = gasto['categoria']
            if cat in categorias_dict:
                categorias_dict[cat] += gasto['monto']
            else:
                categorias_dict[cat] = gasto['monto']

        return categorias_dict

    def obtener_dataframe(self):
        """Convierte las transacciones a DataFrame de pandas"""
        if not self.transacciones:
            return pd.DataFrame()

        df = pd.DataFrame(self.transacciones)
        df['fecha'] = pd.to_datetime(df['fecha'])
        df['monto'] = df['monto'].astype(float)
        return df

    def buscar_transacciones(self, termino_busqueda):
        """Busca transacciones por descripción"""
        termino = termino_busqueda.lower()
        return [t for t in self.transacciones
                if termino in t['descripcion'].lower()]

    def exportar_csv(self, archivo_destino):
        """Exporta transacciones a un archivo CSV"""
        try:
            with open(archivo_destino, 'w', newline='', encoding='utf-8') as f:
                campos = ['id', 'fecha', 'descripcion', 'monto', 'tipo', 'categoria']
                writer = csv.DictWriter(f, fieldnames=campos)
                writer.writeheader()
                writer.writerows(self.transacciones)
            return True
        except Exception as e:
            print(f"Error al exportar: {e}")
            return False