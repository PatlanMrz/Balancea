"""
Validadores
Sistema de validación de datos
"""

import re
from datetime import datetime


class Validador:
    """Clase con métodos de validación"""

    @staticmethod
    def validar_monto(monto_str):
        """
        Valida que el monto sea un número válido y positivo
        Retorna: (es_valido, valor_float, mensaje_error)
        """
        try:
            # Remover espacios y caracteres especiales comunes
            monto_limpio = monto_str.strip().replace(',', '').replace('$', '')

            monto = float(monto_limpio)

            if monto <= 0:
                return False, 0, "El monto debe ser mayor a cero"

            if monto > 999999999:
                return False, 0, "El monto es demasiado grande"

            return True, monto, ""

        except ValueError:
            return False, 0, "El monto debe ser un número válido"

    @staticmethod
    def validar_descripcion(descripcion):
        """
        Valida que la descripción sea válida
        Retorna: (es_valido, descripcion_limpia, mensaje_error)
        """
        descripcion = descripcion.strip()

        if not descripcion:
            return False, "", "La descripción no puede estar vacía"

        if len(descripcion) < 3:
            return False, "", "La descripción debe tener al menos 3 caracteres"

        if len(descripcion) > 200:
            return False, "", "La descripción es demasiado larga (máx. 200 caracteres)"

        # Remover caracteres extraños pero permitir acentos y espacios
        if not re.match(r'^[\w\sáéíóúÁÉÍÓÚñÑ.,()-]+$', descripcion):
            return False, "", "La descripción contiene caracteres no permitidos"

        return True, descripcion, ""

    @staticmethod
    def validar_fecha(fecha_str):
        """
        Valida que la fecha sea válida
        Retorna: (es_valido, fecha_datetime, mensaje_error)
        """
        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d')

            # No permitir fechas futuras muy lejanas
            if fecha > datetime.now() + timedelta(days=365):
                return False, None, "La fecha no puede ser más de un año en el futuro"

            # No permitir fechas muy antiguas
            if fecha < datetime(1900, 1, 1):
                return False, None, "La fecha es demasiado antigua"

            return True, fecha, ""

        except ValueError:
            return False, None, "Formato de fecha inválido (usar YYYY-MM-DD)"

    @staticmethod
    def validar_categoria(categoria, tipo, categorias_disponibles):
        """
        Valida que la categoría exista para el tipo dado
        Retorna: (es_valido, mensaje_error)
        """
        if not tipo:
            return False, "Debe seleccionar un tipo primero"

        if tipo not in categorias_disponibles:
            return False, "Tipo de transacción inválido"

        if not categoria:
            return False, "Debe seleccionar una categoría"

        if categoria not in categorias_disponibles[tipo]:
            return False, "La categoría no es válida para este tipo"

        return True, ""

    @staticmethod
    def sanitizar_texto(texto):
        """Limpia y sanitiza un texto"""
        return texto.strip()


# Importar timedelta para validar_fecha
from datetime import timedelta