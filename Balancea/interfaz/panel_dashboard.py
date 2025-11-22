"""
Panel Dashboard
Muestra resumen general de finanzas con estadísticas avanzadas
CON SCROLL COMPLETO
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
import calendar
from utils.exportador import Exportador
from datos.gestor_metas import GestorMetas
from datos.gestor_presupuestos import GestorPresupuestos


class PanelDashboard(ttk.Frame):
    """Panel principal con resumen de finanzas"""

    def __init__(self, parent, gestor_datos):
        super().__init__(parent)
        self.gestor_datos = gestor_datos
        self.exportador = Exportador(gestor_datos)
        self.gestor_metas = GestorMetas()
        self.gestor_presupuestos = GestorPresupuestos(gestor_datos)

        self.crear_interfaz()
        self.actualizar_datos()

    def crear_interfaz(self):
        """Crea la interfaz del dashboard CON SCROLLBAR"""
        # Canvas con scrollbar para todo el dashboard
        canvas = tk.Canvas(self, bg='#ECF0F1', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)

        # Frame contenedor principal
        self.frame_contenido = ttk.Frame(canvas)

        # Configurar scroll region
        self.frame_contenido.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Crear ventana en canvas
        canvas.create_window((0, 0), window=self.frame_contenido, anchor="nw", width=canvas.winfo_reqwidth())
        canvas.configure(yscrollcommand=scrollbar.set)

        # Empaquetar canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Habilitar scroll con rueda del mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        def _bind_to_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)

        def _unbind_from_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")

        canvas.bind('<Enter>', _bind_to_mousewheel)
        canvas.bind('<Leave>', _unbind_from_mousewheel)

        # Configurar ancho del canvas
        canvas.bind('<Configure>', lambda e: canvas.itemconfig(canvas.create_window((0, 0), window=self.frame_contenido, anchor="nw"), width=e.width))

        # === CONTENIDO DEL DASHBOARD ===
        # Título y botón
        frame_header = ttk.Frame(self.frame_contenido)
        frame_header.grid(row=0, column=0, columnspan=4, pady=20, sticky=(tk.W, tk.E))
        frame_header.columnconfigure(0, weight=1)

        titulo = ttk.Label(frame_header, text="📊 Dashboard Financiero",
                          font=('Arial', 16, 'bold'))
        titulo.pack(side=tk.LEFT, padx=20)

        btn_actualizar = ttk.Button(frame_header, text="🔄 Actualizar",
                                    command=self.actualizar_datos)
        btn_actualizar.pack(side=tk.RIGHT, padx=5)

        btn_exportar = ttk.Button(frame_header, text="📄 Exportar Reporte",
                                 command=self.exportar_reporte)
        btn_exportar.pack(side=tk.RIGHT, padx=5)

        # === TARJETAS DE RESUMEN PRINCIPAL ===
        self.crear_tarjeta("Balance Total", "balance", 1, 0, "#3498DB")
        self.crear_tarjeta("Total Ingresos", "ingresos", 1, 1, "#27AE60")
        self.crear_tarjeta("Total Gastos", "gastos", 1, 2, "#E74C3C")
        self.crear_tarjeta("Tasa de Ahorro", "ahorro", 1, 3, "#9B59B6")

        # === ESTADÍSTICAS DEL MES ACTUAL ===
        frame_mes = ttk.LabelFrame(self.frame_contenido, text="📅 Mes Actual", padding="20")
        frame_mes.grid(row=2, column=0, columnspan=2, pady=20, padx=20, sticky=(tk.W, tk.E))

        self.lbl_mes_nombre = ttk.Label(frame_mes,
                                        text="",
                                        font=('Arial', 12, 'bold'))
        self.lbl_mes_nombre.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        self.lbl_ingresos_mes = ttk.Label(frame_mes,
                                         text="Ingresos del mes: $0.00",
                                         font=('Arial', 11))
        self.lbl_ingresos_mes.grid(row=1, column=0, sticky=tk.W, pady=5)

        self.lbl_gastos_mes = ttk.Label(frame_mes,
                                        text="Gastos del mes: $0.00",
                                        font=('Arial', 11))
        self.lbl_gastos_mes.grid(row=2, column=0, sticky=tk.W, pady=5)

        self.lbl_balance_mes = ttk.Label(frame_mes,
                                        text="Balance del mes: $0.00",
                                        font=('Arial', 11, 'bold'))
        self.lbl_balance_mes.grid(row=3, column=0, sticky=tk.W, pady=5)

        # === ESTADÍSTICAS GENERALES ===
        frame_stats = ttk.LabelFrame(self.frame_contenido, text="📈 Estadísticas Generales", padding="20")
        frame_stats.grid(row=2, column=2, columnspan=2, pady=20, padx=20, sticky=(tk.W, tk.E))

        self.lbl_total_trans = ttk.Label(frame_stats,
                                        text="Total de transacciones: 0",
                                        font=('Arial', 11))
        self.lbl_total_trans.grid(row=0, column=0, sticky=tk.W, pady=5)

        self.lbl_trans_mes = ttk.Label(frame_stats,
                                       text="Transacciones este mes: 0",
                                       font=('Arial', 11))
        self.lbl_trans_mes.grid(row=1, column=0, sticky=tk.W, pady=5)

        self.lbl_categoria_max = ttk.Label(frame_stats,
                                          text="Categoría top: N/A",
                                          font=('Arial', 11))
        self.lbl_categoria_max.grid(row=2, column=0, sticky=tk.W, pady=5)

        self.lbl_promedio = ttk.Label(frame_stats,
                                     text="Promedio diario: $0.00",
                                     font=('Arial', 11))
        self.lbl_promedio.grid(row=3, column=0, sticky=tk.W, pady=5)

        # === COMPARATIVA CON MES ANTERIOR ===
        frame_comparativa = ttk.LabelFrame(self.frame_contenido, text="🔄 Comparativa con Mes Anterior", padding="20")
        frame_comparativa.grid(row=3, column=0, columnspan=4, pady=20, padx=20, sticky=(tk.W, tk.E))

        self.lbl_comp_ingresos = ttk.Label(frame_comparativa,
                                          text="Ingresos: +$0.00 (0%)",
                                          font=('Arial', 11))
        self.lbl_comp_ingresos.grid(row=0, column=0, padx=20, pady=5)

        self.lbl_comp_gastos = ttk.Label(frame_comparativa,
                                        text="Gastos: +$0.00 (0%)",
                                        font=('Arial', 11))
        self.lbl_comp_gastos.grid(row=0, column=1, padx=20, pady=5)

        self.lbl_comp_balance = ttk.Label(frame_comparativa,
                                         text="Balance: +$0.00 (0%)",
                                         font=('Arial', 11, 'bold'))
        self.lbl_comp_balance.grid(row=0, column=2, padx=20, pady=5)

        # === TOP 5 GASTOS ===
        frame_top = ttk.LabelFrame(self.frame_contenido, text="💰 Top 5 Gastos Más Grandes", padding="20")
        frame_top.grid(row=4, column=0, columnspan=4, pady=20, padx=20, sticky=(tk.W, tk.E), ipadx=10, ipady=10)

        # Crear tabla para top 5
        columnas = ('Fecha', 'Descripción', 'Monto', 'Categoría')
        self.tree_top = ttk.Treeview(frame_top, columns=columnas, show='headings', height=5)

        self.tree_top.heading('Fecha', text='Fecha')
        self.tree_top.heading('Descripción', text='Descripción')
        self.tree_top.heading('Monto', text='Monto')
        self.tree_top.heading('Categoría', text='Categoría')

        self.tree_top.column('Fecha', width=100)
        self.tree_top.column('Descripción', width=300)
        self.tree_top.column('Monto', width=120)
        self.tree_top.column('Categoría', width=150)

        self.tree_top.pack(fill=tk.BOTH, expand=True)

        # === RESUMEN DE METAS ===
        frame_metas = ttk.LabelFrame(self.frame_contenido, text="🎯 Mis Metas", padding="20")
        frame_metas.grid(row=5, column=0, columnspan=2, pady=20, padx=20, sticky=(tk.W, tk.E))

        self.lbl_metas_resumen = ttk.Label(frame_metas, text="", font=('Arial', 11))
        self.lbl_metas_resumen.grid(row=0, column=0, sticky=tk.W, pady=5)

        self.lbl_metas_progreso = ttk.Label(frame_metas, text="", font=('Arial', 11))
        self.lbl_metas_progreso.grid(row=1, column=0, sticky=tk.W, pady=5)

        # === RESUMEN DE PRESUPUESTOS ===
        frame_presupuestos = ttk.LabelFrame(self.frame_contenido, text="💰 Mis Presupuestos", padding="20")
        frame_presupuestos.grid(row=5, column=2, columnspan=2, pady=20, padx=20, sticky=(tk.W, tk.E))

        self.lbl_presup_resumen = ttk.Label(frame_presupuestos, text="", font=('Arial', 11))
        self.lbl_presup_resumen.grid(row=0, column=0, sticky=tk.W, pady=5)

        self.lbl_presup_estado = ttk.Label(frame_presupuestos, text="", font=('Arial', 11))
        self.lbl_presup_estado.grid(row=1, column=0, sticky=tk.W, pady=5)

        # Espacio al final para que se vea todo
        ttk.Label(self.frame_contenido, text="").grid(row=6, column=0, pady=20)

        # Configurar expansión del grid
        self.frame_contenido.columnconfigure(0, weight=1)
        self.frame_contenido.columnconfigure(1, weight=1)
        self.frame_contenido.columnconfigure(2, weight=1)
        self.frame_contenido.columnconfigure(3, weight=1)

    def crear_tarjeta(self, titulo, nombre, fila, columna, color):
        """Crea una tarjeta de resumen"""
        frame = tk.Frame(self.frame_contenido, bg=color, relief=tk.RAISED, borderwidth=2)
        frame.grid(row=fila, column=columna, padx=15, pady=10, ipadx=25, ipady=15)

        lbl_titulo = tk.Label(frame, text=titulo,
                             font=('Arial', 11, 'bold'),
                             bg=color, fg='white')
        lbl_titulo.pack(pady=(5, 10))

        lbl_valor = tk.Label(frame, text="$0.00",
                            font=('Arial', 18, 'bold'),
                            bg=color, fg='white')
        lbl_valor.pack(pady=(0, 5))

        # Guardar referencia al label de valor
        setattr(self, f'lbl_{nombre}', lbl_valor)

    def actualizar_datos(self):
        """Actualiza todos los datos del dashboard - CON MENSAJE SIN DATOS"""
        # ✅ FIX: Verificar si hay transacciones y mostrar mensaje
        if not self.gestor_datos.transacciones:
            # Limpiar todo y mostrar mensaje
            self.lbl_balance.config(text="$0.00")
            self.lbl_ingresos.config(text="$0.00")
            self.lbl_gastos.config(text="$0.00")
            self.lbl_ahorro.config(text="0.0%")

            # Limpiar estadísticas
            self.lbl_mes_nombre.config(text="Sin datos del mes")
            self.lbl_ingresos_mes.config(text="Ingresos del mes: $0.00")
            self.lbl_gastos_mes.config(text="Gastos del mes: $0.00")
            self.lbl_balance_mes.config(text="Balance del mes: $0.00")

            self.lbl_total_trans.config(text="Total de transacciones: 0")
            self.lbl_trans_mes.config(text="Transacciones este mes: 0")
            self.lbl_categoria_max.config(text="Categoría top: N/A")
            self.lbl_promedio.config(text="Promedio diario: $0.00")

            # Limpiar comparativa
            self.lbl_comp_ingresos.config(text="Ingresos: $0.00 (0%)", foreground='gray')
            self.lbl_comp_gastos.config(text="Gastos: $0.00 (0%)", foreground='gray')
            self.lbl_comp_balance.config(text="Balance: $0.00 (0%)", foreground='gray')

            # Limpiar top 5
            for item in self.tree_top.get_children():
                self.tree_top.delete(item)

            # Limpiar metas y presupuestos
            self.lbl_metas_resumen.config(text="No hay metas configuradas")
            self.lbl_metas_progreso.config(text="💡 Ve a la pestaña Metas para crear una")
            self.lbl_presup_resumen.config(text="No hay presupuestos configurados")
            self.lbl_presup_estado.config(text="💡 Ve a la pestaña Presupuestos")

            # ✅ FIX: Crear frame con mensaje motivacional
            # Verificar si ya existe el frame de mensaje
            if not hasattr(self, 'frame_mensaje_vacio'):
                self.frame_mensaje_vacio = ttk.Frame(self.frame_contenido)

            # Limpiar y recrear mensaje
            for widget in self.frame_mensaje_vacio.winfo_children():
                widget.destroy()

            self.frame_mensaje_vacio.grid(row=6, column=0, columnspan=4, pady=50)

            # Mensaje principal
            lbl_icono = ttk.Label(self.frame_mensaje_vacio,
                                  text="📊",
                                  font=('Arial', 48))
            lbl_icono.pack(pady=10)

            lbl_titulo = ttk.Label(self.frame_mensaje_vacio,
                                   text="¡Bienvenido a Balancea!",
                                   font=('Arial', 20, 'bold'),
                                   foreground='#3498DB')
            lbl_titulo.pack(pady=10)

            lbl_mensaje = ttk.Label(self.frame_mensaje_vacio,
                                    text="Aún no tienes transacciones registradas.\nComienza tu viaje financiero agregando tu primera transacción.",
                                    font=('Arial', 12),
                                    justify=tk.CENTER)
            lbl_mensaje.pack(pady=10)

            # Botones de acción
            frame_botones = ttk.Frame(self.frame_mensaje_vacio)
            frame_botones.pack(pady=20)

            btn_agregar = ttk.Button(frame_botones,
                                     text="➕ Agregar Transacción",
                                     command=lambda: self.master.master.notebook.select(
                                         1))  # Ir a pestaña Transacciones
            btn_agregar.pack(side=tk.LEFT, padx=10)

            btn_demo = ttk.Button(frame_botones,
                                  text="🎲 Generar Datos Demo",
                                  command=self.generar_datos_demo_desde_dashboard)
            btn_demo.pack(side=tk.LEFT, padx=10)

            # Tips
            lbl_tips = ttk.Label(self.frame_mensaje_vacio,
                                 text="💡 Tip: Los datos demo te ayudarán a explorar todas las funciones de Balancea",
                                 font=('Arial', 9, 'italic'),
                                 foreground='#7F8C8D')
            lbl_tips.pack(pady=10)

            return  # Salir temprano

        # Si llegamos aquí, hay datos - ocultar mensaje si existe
        if hasattr(self, 'frame_mensaje_vacio'):
            self.frame_mensaje_vacio.grid_remove()

        # Obtener datos generales
        balance = self.gestor_datos.obtener_balance()
        ingresos = self.gestor_datos.obtener_total_ingresos()
        gastos = self.gestor_datos.obtener_total_gastos()

        # Calcular tasa de ahorro
        tasa_ahorro = (balance / ingresos * 100) if ingresos > 0 else 0

        # Actualizar tarjetas principales
        self.lbl_balance.config(text=f"${balance:,.2f}")
        self.lbl_ingresos.config(text=f"${ingresos:,.2f}")
        self.lbl_gastos.config(text=f"${gastos:,.2f}")
        self.lbl_ahorro.config(text=f"{tasa_ahorro:.1f}%")

        # Cambiar color del balance según sea positivo o negativo
        if balance < 0:
            self.lbl_balance.master.config(bg="#E74C3C")
        elif balance > 0:
            self.lbl_balance.master.config(bg="#27AE60")

        # Actualizar estadísticas del mes actual
        self.actualizar_mes_actual()

        # Actualizar estadísticas generales
        self.actualizar_estadisticas_generales()

        # Actualizar comparativa
        self.actualizar_comparativa()

        # Actualizar top 5 gastos
        self.actualizar_top_gastos()

        # Actualizar metas
        self.actualizar_resumen_metas()

        # Actualizar presupuestos
        self.actualizar_resumen_presupuestos()

    def actualizar_mes_actual(self):
        """Actualiza estadísticas del mes actual"""
        fecha_actual = datetime.now()
        mes_nombre = calendar.month_name[fecha_actual.month]
        self.lbl_mes_nombre.config(text=f"{mes_nombre} {fecha_actual.year}")

        # Filtrar transacciones del mes actual
        transacciones_mes = [t for t in self.gestor_datos.transacciones
                            if datetime.strptime(t['fecha'], '%Y-%m-%d').month == fecha_actual.month
                            and datetime.strptime(t['fecha'], '%Y-%m-%d').year == fecha_actual.year]

        ingresos_mes = sum([t['monto'] for t in transacciones_mes if t['tipo'] == 'Ingreso'])
        gastos_mes = sum([t['monto'] for t in transacciones_mes if t['tipo'] == 'Gasto'])
        balance_mes = ingresos_mes - gastos_mes

        self.lbl_ingresos_mes.config(text=f"Ingresos del mes: ${ingresos_mes:,.2f}")
        self.lbl_gastos_mes.config(text=f"Gastos del mes: ${gastos_mes:,.2f}")
        self.lbl_balance_mes.config(text=f"Balance del mes: ${balance_mes:,.2f}")

        # Transacciones del mes
        self.lbl_trans_mes.config(text=f"Transacciones este mes: {len(transacciones_mes)}")

    def actualizar_estadisticas_generales(self):
        """Actualiza estadísticas generales"""
        total_trans = len(self.gestor_datos.transacciones)
        self.lbl_total_trans.config(text=f"Total de transacciones: {total_trans}")

        # Categoría con más gastos
        gastos_cat = self.gestor_datos.obtener_gastos_por_categoria()
        if gastos_cat:
            max_cat = max(gastos_cat, key=gastos_cat.get)
            self.lbl_categoria_max.config(
                text=f"Categoría top: {max_cat} (${gastos_cat[max_cat]:,.2f})"
            )
        else:
            self.lbl_categoria_max.config(text="Categoría top: N/A")

        # Promedio de gasto diario
        gastos = self.gestor_datos.obtener_total_gastos()
        if gastos > 0 and total_trans > 0:
            fechas_unicas = set([t['fecha'] for t in self.gestor_datos.transacciones])
            dias = len(fechas_unicas) if fechas_unicas else 1
            promedio = gastos / dias
            self.lbl_promedio.config(text=f"Promedio diario: ${promedio:,.2f}")
        else:
            self.lbl_promedio.config(text="Promedio diario: $0.00")

    def actualizar_comparativa(self):
        """Actualiza comparativa con mes anterior"""
        fecha_actual = datetime.now()

        # Calcular mes anterior
        primer_dia_mes = fecha_actual.replace(day=1)
        ultimo_dia_mes_anterior = primer_dia_mes - timedelta(days=1)
        mes_anterior = ultimo_dia_mes_anterior.month
        año_anterior = ultimo_dia_mes_anterior.year

        # Transacciones mes actual
        trans_mes_actual = [t for t in self.gestor_datos.transacciones
                           if datetime.strptime(t['fecha'], '%Y-%m-%d').month == fecha_actual.month
                           and datetime.strptime(t['fecha'], '%Y-%m-%d').year == fecha_actual.year]

        # Transacciones mes anterior
        trans_mes_anterior = [t for t in self.gestor_datos.transacciones
                             if datetime.strptime(t['fecha'], '%Y-%m-%d').month == mes_anterior
                             and datetime.strptime(t['fecha'], '%Y-%m-%d').year == año_anterior]

        # Calcular totales
        ingresos_actual = sum([t['monto'] for t in trans_mes_actual if t['tipo'] == 'Ingreso'])
        gastos_actual = sum([t['monto'] for t in trans_mes_actual if t['tipo'] == 'Gasto'])
        balance_actual = ingresos_actual - gastos_actual

        ingresos_anterior = sum([t['monto'] for t in trans_mes_anterior if t['tipo'] == 'Ingreso'])
        gastos_anterior = sum([t['monto'] for t in trans_mes_anterior if t['tipo'] == 'Gasto'])
        balance_anterior = ingresos_anterior - gastos_anterior

        # Calcular diferencias
        diff_ingresos = ingresos_actual - ingresos_anterior
        diff_gastos = gastos_actual - gastos_anterior
        diff_balance = balance_actual - balance_anterior

        # Calcular porcentajes
        pct_ingresos = (diff_ingresos / ingresos_anterior * 100) if ingresos_anterior > 0 else 0
        pct_gastos = (diff_gastos / gastos_anterior * 100) if gastos_anterior > 0 else 0
        pct_balance = (diff_balance / abs(balance_anterior) * 100) if balance_anterior != 0 else 0

        # Actualizar labels
        signo_ing = "+" if diff_ingresos >= 0 else ""
        signo_gas = "+" if diff_gastos >= 0 else ""
        signo_bal = "+" if diff_balance >= 0 else ""

        self.lbl_comp_ingresos.config(
            text=f"Ingresos: {signo_ing}${diff_ingresos:,.2f} ({signo_ing}{pct_ingresos:.1f}%)",
            foreground="#27AE60" if diff_ingresos >= 0 else "#E74C3C"
        )

        self.lbl_comp_gastos.config(
            text=f"Gastos: {signo_gas}${diff_gastos:,.2f} ({signo_gas}{pct_gastos:.1f}%)",
            foreground="#E74C3C" if diff_gastos >= 0 else "#27AE60"
        )

        self.lbl_comp_balance.config(
            text=f"Balance: {signo_bal}${diff_balance:,.2f} ({signo_bal}{pct_balance:.1f}%)",
            foreground="#27AE60" if diff_balance >= 0 else "#E74C3C"
        )

    def actualizar_top_gastos(self):
        """Actualiza el top 5 de gastos más grandes"""
        # Limpiar árbol
        for item in self.tree_top.get_children():
            self.tree_top.delete(item)

        # Obtener gastos y ordenar
        gastos = [t for t in self.gestor_datos.transacciones if t['tipo'] == 'Gasto']
        gastos_ordenados = sorted(gastos, key=lambda x: x['monto'], reverse=True)[:5]

        # Mostrar top 5
        for gasto in gastos_ordenados:
            self.tree_top.insert('', tk.END, values=(
                gasto['fecha'],
                gasto['descripcion'],
                f"${gasto['monto']:,.2f}",
                gasto['categoria']
            ))

    def actualizar_resumen_metas(self):
        """Actualiza el resumen de metas en el dashboard"""
        resumen = self.gestor_metas.obtener_resumen()

        if resumen['total'] == 0:
            self.lbl_metas_resumen.config(text="No tienes metas configuradas")
            self.lbl_metas_progreso.config(text="💡 Ve a la pestaña Metas para crear una")
        else:
            self.lbl_metas_resumen.config(
                text=f"Total: {resumen['total']} metas | {resumen['activas']} activas | {resumen['completadas']} completadas"
            )

            color_progreso = '#27AE60' if resumen['progreso_general'] >= 50 else '#F39C12'
            self.lbl_metas_progreso.config(
                text=f"Progreso general: {resumen['progreso_general']:.1f}% | ${resumen['monto_total_actual']:,.2f} de ${resumen['monto_total_objetivo']:,.2f}",
                foreground=color_progreso
            )

    def actualizar_resumen_presupuestos(self):
        """Actualiza el resumen de presupuestos en el dashboard"""
        resumen = self.gestor_presupuestos.obtener_resumen()

        if resumen['categorias_con_presupuesto'] == 0:
            self.lbl_presup_resumen.config(text="No tienes presupuestos configurados")
            self.lbl_presup_estado.config(text="💡 Ve a la pestaña Presupuestos para crear uno")
        else:
            self.lbl_presup_resumen.config(
                text=f"{resumen['categorias_con_presupuesto']} categorías presupuestadas | Gastado: ${resumen['total_gastado']:,.2f} de ${resumen['total_presupuestado']:,.2f}"
            )

            if resumen['categorias_excedidas'] > 0:
                color_estado = '#E74C3C'
                texto_estado = f"⚠️ {resumen['categorias_excedidas']} categoría(s) excedida(s)"
            elif resumen['porcentaje_uso'] >= 80:
                color_estado = '#F39C12'
                texto_estado = f"🟡 Uso al {resumen['porcentaje_uso']:.1f}%"
            else:
                color_estado = '#27AE60'
                texto_estado = f"🟢 Uso al {resumen['porcentaje_uso']:.1f}% | Saldo: ${resumen['saldo_restante']:,.2f}"

            self.lbl_presup_estado.config(text=texto_estado, foreground=color_estado)

    def exportar_reporte(self):
        """Muestra diálogo para exportar reporte"""
        ventana = tk.Toplevel(self)
        ventana.title("Exportar Reporte")
        ventana.geometry("400x250")
        ventana.transient(self.winfo_toplevel())
        ventana.grab_set()

        # Centrar ventana
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() // 2) - 200
        y = (ventana.winfo_screenheight() // 2) - 125
        ventana.geometry(f"400x250+{x}+{y}")

        frame = ttk.Frame(ventana, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="📄 Exportar Reporte Financiero",
                 font=('Arial', 12, 'bold')).pack(pady=10)

        ttk.Label(frame, text="Selecciona el formato de exportación:").pack(pady=10)

        def exportar_pdf():
            archivo = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                title="Guardar Reporte PDF"
            )

            if archivo:
                ventana.destroy()
                if self.exportador.generar_reporte_pdf(archivo, incluir_graficas=True):
                    messagebox.showinfo("Éxito",
                                      f"Reporte PDF generado correctamente:\n{archivo}")
                else:
                    messagebox.showerror("Error", "No se pudo generar el reporte PDF")

        def exportar_excel():
            archivo = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                title="Guardar Reporte Excel"
            )

            if archivo:
                ventana.destroy()
                if self.exportador.exportar_excel(archivo):
                    messagebox.showinfo("Éxito",
                                      f"Reporte Excel generado correctamente:\n{archivo}")
                else:
                    messagebox.showerror("Error", "No se pudo generar el reporte Excel")

        ttk.Button(frame, text="📄 Exportar como PDF",
                  command=exportar_pdf, width=25).pack(pady=10)

        ttk.Button(frame, text="📊 Exportar como Excel",
                  command=exportar_excel, width=25).pack(pady=10)

        ttk.Button(frame, text="Cancelar",
                  command=ventana.destroy, width=25).pack(pady=10)

    def generar_datos_demo_desde_dashboard(self):
        """Genera datos demo desde el dashboard"""
        # Esta función debe estar en la clase principal (app.py)
        # pero la llamamos desde aquí
        try:
            # Buscar la ventana principal
            app_window = self.winfo_toplevel()
            if hasattr(app_window, 'generar_datos_demo'):
                app_window.generar_datos_demo()
            else:
                messagebox.showinfo("Info", "Usa el botón '🎲 Generar Demo' en la parte superior de la ventana")
        except Exception as e:
            print(f"Error al generar demo: {e}")
            messagebox.showerror("Error", "No se pudo generar los datos demo")