"""
Panel de Resultados
Muestra gráficas y análisis visuales
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
from datetime import datetime
import calendar


class PanelResultados(ttk.Frame):
    """Panel de gráficas y análisis"""

    def __init__(self, parent, gestor_datos):
        super().__init__(parent)
        self.gestor_datos = gestor_datos

        # Configurar estilo de matplotlib
        plt.style.use('seaborn-v0_8-darkgrid')

        self.crear_interfaz()
        self.actualizar_graficas()

    def crear_interfaz(self):
        """Crea la interfaz del panel"""
        # Título
        titulo = ttk.Label(self, text="📈 Análisis Visual de Finanzas",
                          font=('Arial', 16, 'bold'))
        titulo.grid(row=0, column=0, columnspan=2, pady=10)

        # Botón de actualizar
        btn_actualizar = ttk.Button(self, text="🔄 Actualizar Gráficas",
                                    command=self.actualizar_graficas)
        btn_actualizar.grid(row=0, column=2, padx=10, pady=10, sticky=tk.E)

        # Frame para las gráficas (3 gráficas en grid)
        self.frame_graficas = ttk.Frame(self)
        self.frame_graficas.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configurar expansión
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(1, weight=1)

        # Placeholder para los canvas
        self.canvas_pastel = None
        self.canvas_barras = None
        self.canvas_linea = None

    def actualizar_graficas(self):
        """Actualiza todas las gráficas"""
        # Limpiar gráficas anteriores
        for widget in self.frame_graficas.winfo_children():
            widget.destroy()

        # Verificar si hay datos
        if not self.gestor_datos.transacciones:
            self.mostrar_mensaje_sin_datos()
            return

        # Crear las 3 gráficas
        self.crear_grafica_pastel()
        self.crear_grafica_barras()
        self.crear_grafica_linea()

    def mostrar_mensaje_sin_datos(self):
        """Muestra mensaje cuando no hay datos"""
        mensaje = ttk.Label(self.frame_graficas,
                           text="📊 No hay transacciones para mostrar\n\nAgrega transacciones en la pestaña 'Transacciones'",
                           font=('Arial', 14),
                           justify=tk.CENTER)
        mensaje.pack(expand=True, pady=50)

    def crear_grafica_pastel(self):
        """Crea gráfica de pastel de gastos por categoría"""
        gastos_cat = self.gestor_datos.obtener_gastos_por_categoria()

        if not gastos_cat:
            return

        # Crear figura
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        # Datos para el pastel
        categorias = list(gastos_cat.keys())
        valores = list(gastos_cat.values())

        # Colores personalizados
        colores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8',
                   '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B739', '#52B788']

        # Crear gráfica de pastel
        wedges, texts, autotexts = ax.pie(valores, labels=categorias, autopct='%1.1f%%',
                                           colors=colores[:len(categorias)],
                                           startangle=90)

        # Mejorar apariencia
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(9)
            autotext.set_weight('bold')

        ax.set_title('Gastos por Categoría', fontsize=12, fontweight='bold', pad=20)

        # Integrar en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.frame_graficas)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.canvas_pastel = canvas

    def crear_grafica_barras(self):
        """Crea gráfica de barras comparando ingresos vs gastos"""
        # Obtener datos
        df = self.gestor_datos.obtener_dataframe()

        if df.empty:
            return

        # Agrupar por mes
        df['mes'] = df['fecha'].dt.to_period('M')

        # Separar ingresos y gastos
        ingresos_mes = df[df['tipo'] == 'Ingreso'].groupby('mes')['monto'].sum()
        gastos_mes = df[df['tipo'] == 'Gasto'].groupby('mes')['monto'].sum()

        # Crear figura
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        # Obtener todos los meses únicos
        todos_meses = sorted(set(ingresos_mes.index) | set(gastos_mes.index))

        # Preparar datos para la gráfica
        x = range(len(todos_meses))
        ingresos_valores = [ingresos_mes.get(mes, 0) for mes in todos_meses]
        gastos_valores = [gastos_mes.get(mes, 0) for mes in todos_meses]

        # Crear barras
        ancho = 0.35
        ax.bar([i - ancho/2 for i in x], ingresos_valores, ancho,
               label='Ingresos', color='#27AE60', alpha=0.8)
        ax.bar([i + ancho/2 for i in x], gastos_valores, ancho,
               label='Gastos', color='#E74C3C', alpha=0.8)

        # Configurar ejes
        ax.set_xlabel('Mes', fontweight='bold')
        ax.set_ylabel('Monto ($)', fontweight='bold')
        ax.set_title('Ingresos vs Gastos por Mes', fontsize=12, fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels([str(mes) for mes in todos_meses], rotation=45, ha='right')
        ax.legend()
        ax.grid(True, alpha=0.3)

        # Ajustar diseño
        fig.tight_layout()

        # Integrar en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.frame_graficas)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=1, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.canvas_barras = canvas

    def crear_grafica_linea(self):
        """Crea gráfica de línea de tendencia de gastos"""
        # Obtener solo gastos
        df = self.gestor_datos.obtener_dataframe()

        if df.empty:
            return

        gastos_df = df[df['tipo'] == 'Gasto'].copy()

        if gastos_df.empty:
            return

        # Agrupar por fecha
        gastos_diarios = gastos_df.groupby('fecha')['monto'].sum().sort_index()

        # Crear figura
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        # Crear línea
        ax.plot(gastos_diarios.index, gastos_diarios.values,
               marker='o', linestyle='-', linewidth=2,
               markersize=6, color='#E74C3C', alpha=0.7)

        # Llenar área bajo la curva
        ax.fill_between(gastos_diarios.index, gastos_diarios.values,
                        alpha=0.3, color='#E74C3C')

        # Configurar ejes
        ax.set_xlabel('Fecha', fontweight='bold')
        ax.set_ylabel('Gastos ($)', fontweight='bold')
        ax.set_title('Tendencia de Gastos', fontsize=12, fontweight='bold', pad=20)
        ax.grid(True, alpha=0.3)

        # Rotar etiquetas de fecha
        fig.autofmt_xdate()

        # Ajustar diseño
        fig.tight_layout()

        # Integrar en Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.frame_graficas)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=2, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.canvas_linea = canvas

        # Configurar expansión del grid
        self.frame_graficas.columnconfigure(0, weight=1)
        self.frame_graficas.columnconfigure(1, weight=1)
        self.frame_graficas.columnconfigure(2, weight=1)
        self.frame_graficas.rowconfigure(0, weight=1)