"""
Helpers
Funciones auxiliares y utilidades
"""

import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import locale


class FormatoUtil:
    """Utilidades para formateo de datos"""

    @staticmethod
    def formatear_moneda(monto):
        """Formatea un número como moneda"""
        return f"${monto:,.2f}"

    @staticmethod
    def formatear_fecha(fecha_str):
        """Formatea una fecha de YYYY-MM-DD a formato legible"""
        try:
            fecha = datetime.strptime(fecha_str, '%Y-%m-%d')
            return fecha.strftime('%d/%m/%Y')
        except:
            return fecha_str

    @staticmethod
    def formatear_porcentaje(valor):
        """Formatea un número como porcentaje"""
        return f"{valor:.1f}%"

    @staticmethod
    def abreviar_numero(numero):
        """Abrevia números grandes (1000 -> 1K, 1000000 -> 1M)"""
        if numero >= 1000000:
            return f"${numero / 1000000:.1f}M"
        elif numero >= 1000:
            return f"${numero / 1000:.1f}K"
        else:
            return f"${numero:.2f}"


class FechaUtil:
    """Utilidades para manejo de fechas"""

    @staticmethod
    def obtener_rango_mes_actual():
        """Retorna el rango de fechas del mes actual"""
        hoy = datetime.now()
        inicio_mes = hoy.replace(day=1)

        # Último día del mes
        if hoy.month == 12:
            fin_mes = hoy.replace(year=hoy.year + 1, month=1, day=1) - timedelta(days=1)
        else:
            fin_mes = hoy.replace(month=hoy.month + 1, day=1) - timedelta(days=1)

        return inicio_mes.strftime('%Y-%m-%d'), fin_mes.strftime('%Y-%m-%d')

    @staticmethod
    def obtener_rango_mes_anterior():
        """Retorna el rango de fechas del mes anterior"""
        hoy = datetime.now()
        inicio_mes_actual = hoy.replace(day=1)
        fin_mes_anterior = inicio_mes_actual - timedelta(days=1)
        inicio_mes_anterior = fin_mes_anterior.replace(day=1)

        return inicio_mes_anterior.strftime('%Y-%m-%d'), fin_mes_anterior.strftime('%Y-%m-%d')

    @staticmethod
    def obtener_rango_semana_actual():
        """Retorna el rango de fechas de la semana actual"""
        hoy = datetime.now()
        inicio_semana = hoy - timedelta(days=hoy.weekday())
        fin_semana = inicio_semana + timedelta(days=6)

        return inicio_semana.strftime('%Y-%m-%d'), fin_semana.strftime('%Y-%m-%d')

    @staticmethod
    def obtener_rango_ultimo_mes():
        """Retorna el rango de los últimos 30 días"""
        hoy = datetime.now()
        hace_30_dias = hoy - timedelta(days=30)

        return hace_30_dias.strftime('%Y-%m-%d'), hoy.strftime('%Y-%m-%d')


class AtajosUtil:
    """Utilidades para atajos de teclado"""

    @staticmethod
    def configurar_atajos(ventana, callbacks):
        """
        Configura atajos de teclado para la ventana
        callbacks: dict con formato {'atajo': funcion}
        Ejemplo: {'<Control-s>': guardar_funcion}
        """
        for atajo, callback in callbacks.items():
            ventana.bind(atajo, callback)

    @staticmethod
    def obtener_atajos_disponibles():
        """Retorna un diccionario con los atajos disponibles"""
        return {
            'Ctrl+N': 'Nueva transacción',
            'Ctrl+S': 'Guardar',
            'Ctrl+F': 'Buscar',
            'Ctrl+E': 'Exportar',
            'Delete': 'Eliminar selección',
            'F5': 'Actualizar',
            'Esc': 'Cancelar/Limpiar'
        }

    @staticmethod
    def mostrar_ayuda_atajos(parent):
        """Muestra una ventana con los atajos disponibles"""
        ventana = tk.Toplevel(parent)
        ventana.title("Atajos de Teclado")
        ventana.geometry("400x300")
        ventana.transient(parent)

        titulo = tk.Label(ventana, text="⌨️ Atajos de Teclado",
                          font=('Arial', 14, 'bold'))
        titulo.pack(pady=20)

        frame = tk.Frame(ventana, padx=20, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        atajos = AtajosUtil.obtener_atajos_disponibles()

        for i, (atajo, descripcion) in enumerate(atajos.items()):
            tk.Label(frame, text=atajo, font=('Arial', 10, 'bold'),
                     anchor=tk.W, width=15).grid(row=i, column=0, sticky=tk.W, pady=5)
            tk.Label(frame, text=descripcion, anchor=tk.W).grid(row=i, column=1, sticky=tk.W, pady=5)

        btn_cerrar = tk.Button(ventana, text="Cerrar", command=ventana.destroy)
        btn_cerrar.pack(pady=10)


class DialogosUtil:
    """Utilidades para diálogos y mensajes"""

    @staticmethod
    def confirmar_eliminacion(elemento="este elemento"):
        """Muestra diálogo de confirmación para eliminación"""
        return messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Estás seguro de que deseas eliminar {elemento}?\n\nEsta acción no se puede deshacer."
        )

    @staticmethod
    def mostrar_exito(mensaje):
        """Muestra mensaje de éxito"""
        messagebox.showinfo("✓ Éxito", mensaje)

    @staticmethod
    def mostrar_error(mensaje):
        """Muestra mensaje de error"""
        messagebox.showerror("✗ Error", mensaje)

    @staticmethod
    def mostrar_advertencia(mensaje):
        """Muestra mensaje de advertencia"""
        messagebox.showwarning("⚠ Advertencia", mensaje)

    @staticmethod
    def mostrar_info(mensaje):
        """Muestra mensaje informativo"""
        messagebox.showinfo("ℹ Información", mensaje)


class ColorUtil:
    """Utilidades para colores y temas"""

    # Paleta de colores
    COLORES = {
        'primario': '#2C3E50',
        'secundario': '#3498DB',
        'exito': '#27AE60',
        'peligro': '#E74C3C',
        'advertencia': '#F39C12',
        'info': '#3498DB',
        'fondo': '#ECF0F1',
        'texto': '#2C3E50',
        'gris': '#95A5A6'
    }

    @staticmethod
    def obtener_color(nombre):
        """Obtiene un color de la paleta"""
        return ColorUtil.COLORES.get(nombre, '#000000')

    @staticmethod
    def color_segun_valor(valor, positivo_es_bueno=True):
        """Retorna un color según si el valor es positivo o negativo"""
        if valor > 0:
            return ColorUtil.COLORES['exito'] if positivo_es_bueno else ColorUtil.COLORES['peligro']
        elif valor < 0:
            return ColorUtil.COLORES['peligro'] if positivo_es_bueno else ColorUtil.COLORES['exito']
        else:
            return ColorUtil.COLORES['gris']


class EstadisticasUtil:
    """Utilidades para cálculos estadísticos"""

    @staticmethod
    def calcular_promedio(lista_valores):
        """Calcula el promedio de una lista"""
        if not lista_valores:
            return 0
        return sum(lista_valores) / len(lista_valores)

    @staticmethod
    def calcular_mediana(lista_valores):
        """Calcula la mediana de una lista"""
        if not lista_valores:
            return 0
        valores_ordenados = sorted(lista_valores)
        n = len(valores_ordenados)
        if n % 2 == 0:
            return (valores_ordenados[n // 2 - 1] + valores_ordenados[n // 2]) / 2
        else:
            return valores_ordenados[n // 2]

    @staticmethod
    def calcular_variacion_porcentual(valor_actual, valor_anterior):
        """Calcula la variación porcentual entre dos valores"""
        if valor_anterior == 0:
            return 0 if valor_actual == 0 else 100
        return ((valor_actual - valor_anterior) / abs(valor_anterior)) * 100