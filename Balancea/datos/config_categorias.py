"""
Configuración de Categorías
Gestiona las categorías personalizables
"""

import json
import os
from pathlib import Path


class GestorCategorias:
    """Gestiona las categorías de ingresos y gastos"""

    def __init__(self, archivo_config="datos/categorias.json"):
        self.archivo_config = archivo_config
        self.categorias = self.cargar_categorias()

    def cargar_categorias(self):
        """Carga las categorías desde el archivo JSON"""
        # Crear directorio si no existe
        Path("datos").mkdir(exist_ok=True)

        # Si no existe el archivo, crear con categorías por defecto
        if not os.path.exists(self.archivo_config):
            return self.crear_categorias_defecto()

        try:
            with open(self.archivo_config, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error al cargar categorías: {e}")
            return self.crear_categorias_defecto()

    def crear_categorias_defecto(self):
        """Crea las categorías por defecto"""
        categorias_defecto = {
            'Ingreso': [
                'Salario',
                'Freelance',
                'Inversiones',
                'Regalo',
                'Bono',
                'Otro Ingreso'
            ],
            'Gasto': [
                'Alimentación',
                'Transporte',
                'Servicios',
                'Entretenimiento',
                'Salud',
                'Educación',
                'Ropa',
                'Hogar',
                'Tecnología',
                'Viajes',
                'Otro Gasto'
            ]
        }
        self.guardar_categorias(categorias_defecto)
        return categorias_defecto

    def guardar_categorias(self, categorias=None):
        """Guarda las categorías en el archivo JSON"""
        if categorias is None:
            categorias = self.categorias

        try:
            with open(self.archivo_config, 'w', encoding='utf-8') as f:
                json.dump(categorias, f, ensure_ascii=False, indent=2)
            self.categorias = categorias
            return True
        except Exception as e:
            print(f"Error al guardar categorías: {e}")
            return False

    def agregar_categoria(self, tipo, nombre_categoria):
        """Agrega una nueva categoría"""
        if tipo not in self.categorias:
            return False

        if nombre_categoria in self.categorias[tipo]:
            return False  # Ya existe

        self.categorias[tipo].append(nombre_categoria)
        return self.guardar_categorias()

    def eliminar_categoria(self, tipo, nombre_categoria):
        """Elimina una categoría"""
        if tipo not in self.categorias:
            return False

        if nombre_categoria not in self.categorias[tipo]:
            return False

        self.categorias[tipo].remove(nombre_categoria)
        return self.guardar_categorias()

    def editar_categoria(self, tipo, nombre_anterior, nombre_nuevo):
        """Edita el nombre de una categoría"""
        if tipo not in self.categorias:
            return False

        if nombre_anterior not in self.categorias[tipo]:
            return False

        if nombre_nuevo in self.categorias[tipo]:
            return False  # El nuevo nombre ya existe

        index = self.categorias[tipo].index(nombre_anterior)
        self.categorias[tipo][index] = nombre_nuevo
        return self.guardar_categorias()

    def obtener_categorias(self, tipo=None):
        """Obtiene las categorías"""
        if tipo:
            return self.categorias.get(tipo, [])
        return self.categorias

    def restaurar_defecto(self):
        """Restaura las categorías por defecto"""
        self.categorias = self.crear_categorias_defecto()
        return True