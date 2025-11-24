"""
BALANCEA - Gestor de Finanzas Personales con IA
Aplicación principal con interfaz Tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
from pathlib import Path

# Importar configuración
try:
    import config
except ImportError:
    # Si no existe config.py, usar valores por defecto
    class config:
        APP_NOMBRE = "Balancea"
        APP_VERSION = "1.0.0"
        APP_DESCRIPCION = "Gestor de Finanzas Personales"
        VENTANA_ANCHO = 1200
        VENTANA_ALTO = 700
        VENTANA_MIN_ANCHO = 900
        VENTANA_MIN_ALTO = 600
        COLORES = {
            'primario': '#2C3E50',
            'secundario': '#3498DB',
            'exito': '#27AE60',
            'peligro': '#E74C3C',
            'fondo': '#ECF0F1'
        }

# Importar módulos de la interfaz
from interfaz.pestañas import GestorPestañas
from interfaz.panel_dashboard import PanelDashboard
from interfaz.panel_transacciones import PanelTransacciones
from interfaz.panel_resultados import PanelResultados
from interfaz.panel_chat import PanelChat
from interfaz.panel_alertas import PanelAlertas
from interfaz.panel_metas import PanelMetas
from interfaz.panel_presupuestos import PanelPresupuestos

# Importar gestores de datos
from datos.gestor_transacciones import GestorTransacciones

# Importar utilidades
try:
    from utils.helpers import AtajosUtil, DialogosUtil
    from utils.ventana_bienvenida import mostrar_ventana_bienvenida
    from utils.tooltip import crear_tooltip
except ImportError:
    # Si no existen las utilidades, crear clases dummy
    class AtajosUtil:
        @staticmethod
        def mostrar_ayuda_atajos(parent):
            messagebox.showinfo("Atajos", "F1: Ayuda\nF5: Actualizar\nCtrl+Q: Salir")


    class DialogosUtil:
        pass


    def mostrar_ventana_bienvenida(parent, gestor_datos):
        pass  # No hacer nada si no existe


    def crear_tooltip(widget, texto):
        pass  # No hacer nada si no existe


class BalanceaApp:
    """Aplicación principal de Balancea"""

    def __init__(self, root):
        self.root = root
        self.root.title(f"{config.APP_NOMBRE} - Cargando...")
        self.root.geometry(f"{config.VENTANA_ANCHO}x{config.VENTANA_ALTO}")

        # Intentar configurar tamaño mínimo
        try:
            self.root.minsize(config.VENTANA_MIN_ANCHO, config.VENTANA_MIN_ALTO)
        except:
            pass

        # Configurar estilo
        self.configurar_estilo()

        # Mostrar splash screen de carga
        self.mostrar_splash()

        # Inicializar aplicación después de 100ms
        self.root.after(100, self.inicializar_app)

    def mostrar_splash(self):
        """Muestra pantalla de carga"""
        self.splash_frame = ttk.Frame(self.root)
        self.splash_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        ttk.Label(self.splash_frame, text="💰 BALANCEA",
                  font=('Arial', 24, 'bold'),
                  foreground='#3498DB').pack(pady=20)

        ttk.Label(self.splash_frame, text="Cargando...",
                  font=('Arial', 12)).pack(pady=10)

        self.progress = ttk.Progressbar(self.splash_frame, mode='indeterminate', length=300)
        self.progress.pack(pady=10)
        self.progress.start(10)

    def inicializar_app(self):
        """Inicializa la aplicación"""
        # Inicializar gestor de datos
        self.gestor_datos = GestorTransacciones()

        # Ocultar splash
        self.progress.stop()
        self.splash_frame.destroy()

        # Crear interfaz
        self.crear_interfaz()

        # Configurar atajos
        self.configurar_atajos()

        # Configurar cierre
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_aplicacion)

        # Actualizar título
        self.root.title(f"{config.APP_NOMBRE} - {config.APP_DESCRIPCION}")

        # Mostrar ventana de bienvenida
        self.root.after(500, lambda: mostrar_ventana_bienvenida(self.root, self.gestor_datos))

        # Mostrar mensaje en título
        self.root.after(100, lambda: self.mostrar_bienvenida())

    def configurar_estilo(self):
        """Configura el estilo visual de la aplicación"""
        style = ttk.Style()
        style.theme_use('clam')

        # Usar colores de config
        self.color_primario = config.COLORES['primario']
        self.color_secundario = config.COLORES['secundario']
        self.color_exito = config.COLORES['exito']
        self.color_peligro = config.COLORES['peligro']
        self.color_fondo = config.COLORES['fondo']

        # Configurar estilos
        style.configure('Header.TLabel',
                        font=('Arial', 14, 'bold'),
                        foreground=self.color_primario)

        style.configure('Title.TLabel',
                        font=('Arial', 18, 'bold'),
                        foreground=self.color_secundario)

        self.root.configure(bg=self.color_fondo)

    def configurar_atajos(self):
        """Configura los atajos de teclado"""
        # Atajos globales
        self.root.bind('<F1>', lambda e: self.mostrar_ayuda())
        self.root.bind('<F5>', lambda e: self.actualizar_dashboard())
        self.root.bind('<Control-q>', lambda e: self.cerrar_aplicacion())
        self.root.bind('<Control-h>', lambda e: self.mostrar_bienvenida_manual())

    def mostrar_bienvenida_manual(self):
        """Muestra la ventana de bienvenida manualmente"""
        mostrar_ventana_bienvenida(self.root, self.gestor_datos)

    def mostrar_bienvenida(self):
        """Muestra mensaje de bienvenida"""
        total_trans = len(self.gestor_datos.transacciones)
        if total_trans == 0:
            self.root.title(f"{config.APP_NOMBRE} - Sin transacciones")
        else:
            self.root.title(f"{config.APP_NOMBRE} - {total_trans} transacciones")

    def mostrar_ayuda(self):
        """Muestra ventana de ayuda con atajos"""
        AtajosUtil.mostrar_ayuda_atajos(self.root)

    def crear_interfaz(self):
        """Crea la interfaz principal con pestañas"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Título de la aplicación
        titulo = ttk.Label(main_frame,
                           text="💰 BALANCEA",
                           style='Title.TLabel')
        titulo.grid(row=0, column=0, pady=(0, 10), sticky=tk.W)

        # Frame de botones de acción rápida
        frame_acciones = ttk.Frame(main_frame)
        frame_acciones.grid(row=0, column=1, pady=(0, 10), sticky=tk.E)

        btn_demo = ttk.Button(frame_acciones, text="🎲 Generar Demo",
                              command=self.generar_datos_demo)
        btn_demo.pack(side=tk.LEFT, padx=5)
        crear_tooltip(btn_demo, "Genera datos de demostración para probar la app")

        btn_ayuda = ttk.Button(frame_acciones, text="📖 Ayuda (F1)",
                               command=self.mostrar_ayuda)
        btn_ayuda.pack(side=tk.LEFT, padx=5)
        crear_tooltip(btn_ayuda, "Muestra los atajos de teclado disponibles")

        btn_optimizar = ttk.Button(frame_acciones, text="🔧 Optimizar",
                                   command=self.optimizar_sistema)
        btn_optimizar.pack(side=tk.LEFT, padx=5)
        crear_tooltip(btn_optimizar, "Optimiza y limpia el sistema")

        # Crear notebook (pestañas)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Bind para detectar cambio de pestaña
        self.notebook.bind('<<NotebookTabChanged>>', self.cambiar_pestaña)

        # Crear paneles
        self.crear_paneles()

    def crear_paneles(self):
        """Crea todos los paneles de la aplicación"""
        # Panel Dashboard (resumen)
        self.panel_dashboard = PanelDashboard(
            self.notebook,
            self.gestor_datos
        )
        self.notebook.add(self.panel_dashboard, text="📊 Dashboard")

        # Panel Transacciones
        self.panel_transacciones = PanelTransacciones(
            self.notebook,
            self.gestor_datos,
            self.actualizar_dashboard
        )
        self.notebook.add(self.panel_transacciones, text="💳 Transacciones")

        # Panel Metas
        self.panel_metas = PanelMetas(
            self.notebook,
            self.gestor_datos
        )
        self.notebook.add(self.panel_metas, text="🎯 Metas")

        # Panel Presupuestos
        self.panel_presupuestos = PanelPresupuestos(
            self.notebook,
            self.gestor_datos
        )
        self.notebook.add(self.panel_presupuestos, text="💰 Presupuestos")

        # Panel Resultados (gráficas)
        self.panel_resultados = PanelResultados(
            self.notebook,
            self.gestor_datos
        )
        self.notebook.add(self.panel_resultados, text="📈 Análisis")

        # Panel Chat Financiero
        self.panel_chat = PanelChat(
            self.notebook,
            self.gestor_datos
        )
        self.notebook.add(self.panel_chat, text="💬 Asistente IA")

        # Panel Alertas
        self.panel_alertas = PanelAlertas(
            self.notebook,
            self.gestor_datos
        )
        self.notebook.add(self.panel_alertas, text="🔔 Alertas")

    def actualizar_dashboard(self):
        """Actualiza el dashboard con nuevos datos"""
        self.panel_dashboard.actualizar_datos()
        self.panel_resultados.actualizar_graficas()
        self.panel_alertas.actualizar_alertas()

        # Actualizar título
        total_trans = len(self.gestor_datos.transacciones)
        self.root.title(f"{config.APP_NOMBRE} - {total_trans} transacciones")

    def cambiar_pestaña(self, event=None):
        """Maneja el cambio de pestaña para actualizar datos"""
        pestaña_actual = self.notebook.index(self.notebook.select())

        # Actualizar según la pestaña
        if pestaña_actual == 0:  # Dashboard
            self.panel_dashboard.actualizar_datos()
        elif pestaña_actual == 2:  # Metas
            self.panel_metas.actualizar_metas()
        elif pestaña_actual == 3:  # Presupuestos
            self.panel_presupuestos.actualizar_presupuestos()
        elif pestaña_actual == 4:  # Análisis
            self.panel_resultados.actualizar_graficas()
        elif pestaña_actual == 6:  # Alertas
            self.panel_alertas.actualizar_alertas()

    def cerrar_aplicacion(self):
        """Cierra la aplicación de forma segura"""
        if messagebox.askokcancel("Salir", "¿Deseas cerrar Balancea?"):
            # Guardar datos antes de cerrar
            self.gestor_datos.guardar_datos()
            self.root.destroy()

    def generar_datos_demo(self):
        """Genera datos de demostración"""
        if len(self.gestor_datos.transacciones) > 0:
            respuesta = messagebox.askyesnocancel(
                "Generar Datos Demo",
                "Ya tienes transacciones registradas.\n\n"
                "¿Deseas agregar datos de demostración adicionales?\n\n"
                "• SÍ: Agregar datos demo a los existentes\n"
                "• NO: Eliminar todo y crear datos demo nuevos\n"
                "• CANCELAR: No hacer nada"
            )

            if respuesta is None:  # Cancelar
                return
            elif respuesta is False:  # NO - Limpiar todo
                if messagebox.askokcancel("Confirmar",
                                          "Esto ELIMINARÁ todas tus transacciones, metas y presupuestos actuales.\n\n¿Estás seguro?"):
                    # Limpiar datos
                    self.gestor_datos.transacciones = []
                    self.gestor_datos.guardar_datos()
                else:
                    return

        # Generar demo
        from utils.generador_demo import GeneradorDemo

        generador = GeneradorDemo(self.gestor_datos)
        resultado = generador.generar_demo_completa()

        # Actualizar todas las vistas
        self.actualizar_dashboard()

        messagebox.showinfo(
            "¡Datos Demo Generados!",
            f"Se generaron:\n\n"
            f"✅ {resultado['transacciones']} transacciones\n"
            f"✅ {resultado['metas']} metas\n"
            f"✅ {resultado['presupuestos']} presupuestos\n\n"
            f"Explora las diferentes pestañas para ver los datos."
        )

    def optimizar_sistema(self):
        """Optimiza el sistema"""
        from utils.optimizador import Optimizador

        if messagebox.askyesno("Optimizar Sistema",
                               "Esto hará:\n\n"
                               "• Crear backup de datos\n"
                               "• Eliminar duplicados\n"
                               "• Corregir IDs\n"
                               "• Limpiar backups antiguos\n\n"
                               "¿Continuar?"):
            optimizador = Optimizador(self.gestor_datos)
            resultados = optimizador.optimizar_todo()

            mensaje = f"""✅ Optimización Completa

📦 Backup creado: {resultados['backup']['timestamp']}

🧹 Duplicados eliminados: {resultados['duplicados_eliminados']}
🔢 IDs corregidos: {resultados['ids_corregidos']}
🗑️ Backups antiguos limpiados: {resultados['backups_antiguos_eliminados']}

📊 Estadísticas:
• Transacciones: {resultados['estadisticas']['transacciones']}
• Total Ingresos: ${resultados['estadisticas']['total_ingresos']:,.2f}
• Total Gastos: ${resultados['estadisticas']['total_gastos']:,.2f}
"""

            messagebox.showinfo("Optimización Completa", mensaje)
            self.actualizar_dashboard()


def main():
    """Función principal"""
    root = tk.Tk()
    app = BalanceaApp(root)
    root.app = app
    root.mainloop()

if __name__ == "__main__":
    main()
