"""
Panel de Presupuestos
Gestión y seguimiento de presupuestos por categoría
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datos.gestor_presupuestos import GestorPresupuestos


class PanelPresupuestos(ttk.Frame):
    """Panel para gestionar presupuestos"""

    def __init__(self, parent, gestor_datos):
        super().__init__(parent)
        self.gestor_datos = gestor_datos
        self.gestor_presupuestos = GestorPresupuestos(gestor_datos)

        # Resetear mes si es necesario
        self.gestor_presupuestos.resetear_mes_nuevo()

        self.crear_interfaz()
        self.actualizar_presupuestos()

    def crear_interfaz(self):
        """Crea la interfaz del panel"""
        # === ENCABEZADO ===
        frame_header = ttk.Frame(self)
        frame_header.pack(fill=tk.X, padx=20, pady=10)

        titulo = ttk.Label(frame_header, text="💰 Presupuestos por Categoría",
                        font=('Arial', 16, 'bold'))
        titulo.pack(side=tk.LEFT)

        btn_actualizar = ttk.Button(frame_header, text="🔄 Actualizar",
                                    command=self.actualizar_presupuestos)
        btn_actualizar.pack(side=tk.RIGHT, padx=5)

        btn_agregar = ttk.Button(frame_header, text="➕ Nuevo Presupuesto",
                                command=self.agregar_presupuesto)
        btn_agregar.pack(side=tk.RIGHT, padx=5)

        # === RESUMEN GENERAL ===
        frame_resumen = ttk.LabelFrame(self, text="📊 Resumen General", padding="20")
        frame_resumen.pack(fill=tk.X, padx=20, pady=10)

        self.lbl_presupuestado = ttk.Label(frame_resumen, text="", font=('Arial', 11))
        self.lbl_presupuestado.grid(row=0, column=0, sticky=tk.W, pady=5)

        self.lbl_gastado = ttk.Label(frame_resumen, text="", font=('Arial', 11))
        self.lbl_gastado.grid(row=0, column=1, sticky=tk.W, padx=20, pady=5)

        self.lbl_restante = ttk.Label(frame_resumen, text="", font=('Arial', 11, 'bold'))
        self.lbl_restante.grid(row=0, column=2, sticky=tk.W, padx=20, pady=5)

        # === PRESUPUESTOS ACTIVOS === (mismo patrón que Metas)
        self.frame_lista = ttk.LabelFrame(self, text="💼 Mis Presupuestos", padding="10")
        self.frame_lista.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Contenedor con scroll interno para tarjetas - SIMPLIFICADO
        self.canvas_pres = tk.Canvas(self.frame_lista, bg='#ECF0F1', highlightthickness=0)
        self.scrollbar_pres = ttk.Scrollbar(self.frame_lista, orient="vertical", command=self.canvas_pres.yview)
        self.frame_presupuestos = ttk.Frame(self.canvas_pres)

        # Ajustar scrollregion al contenido de tarjetas
        self.frame_presupuestos.bind(
            "<Configure>",
            lambda e: self.canvas_pres.configure(scrollregion=self.canvas_pres.bbox("all"))
        )

        self.canvas_pres_window = self.canvas_pres.create_window((0, 0), window=self.frame_presupuestos, anchor="nw")
        self.canvas_pres.configure(yscrollcommand=self.scrollbar_pres.set)
        
        # Ajustar ancho del frame interno al canvas
        self.canvas_pres.bind('<Configure>', 
                            lambda e: self.canvas_pres.itemconfigure(self.canvas_pres_window, width=e.width))

        self.canvas_pres.pack(side="left", fill="both", expand=True)
        self.scrollbar_pres.pack(side="right", fill="y")

        # Scroll con rueda en la sección 'Mis Presupuestos'
        def _on_mousewheel_pres(event):
            delta = 0
            if hasattr(event, 'delta') and event.delta != 0:
                delta = int(-1 * (event.delta / 120))
            elif getattr(event, 'num', None) == 4:
                delta = -3
            elif getattr(event, 'num', None) == 5:
                delta = 3
            if delta == 0 or not getattr(self, '_can_scroll_pres', False):
                return
            first, last = self.canvas_pres.yview()
            if delta < 0 and first <= 0.0:
                return
            if delta > 0 and last >= 1.0:
                return
            self.canvas_pres.yview_scroll(delta, "units")

        self.canvas_pres.bind('<Enter>', lambda e: (
            self.canvas_pres.bind_all("<MouseWheel>", _on_mousewheel_pres),
            self.canvas_pres.bind_all("<Button-4>", _on_mousewheel_pres),
            self.canvas_pres.bind_all("<Button-5>", _on_mousewheel_pres)
        ))
        self.canvas_pres.bind('<Leave>', lambda e: (
            self.canvas_pres.unbind_all("<MouseWheel>"),
            self.canvas_pres.unbind_all("<Button-4>"),
            self.canvas_pres.unbind_all("<Button-5>")
        ))

        self._can_scroll_pres = False

        # Frame de estado vacío dentro de la sección lista
        self.empty_state_frame = ttk.Frame(self.frame_lista)

    def actualizar_presupuestos(self):
        """Actualiza la visualización de presupuestos"""
        # Limpiar frame
        for widget in self.frame_presupuestos.winfo_children():
            widget.destroy()

        # Actualizar resumen
        resumen = self.gestor_presupuestos.obtener_resumen()
        self.lbl_presupuestado.config(
            text=f"💵 Presupuestado: ${resumen['total_presupuestado']:,.2f}"
        )
        self.lbl_gastado.config(
            text=f"💸 Gastado: ${resumen['total_gastado']:,.2f}"
        )

        color_restante = '#27AE60' if resumen['saldo_restante'] >= 0 else '#E74C3C'
        self.lbl_restante.config(
            text=f"💰 Restante: ${resumen['saldo_restante']:,.2f}",
            foreground=color_restante
        )

        # Mostrar presupuestos
        if self.gestor_presupuestos.presupuestos:
            # Ocultar estado vacío
            try:
                self.empty_state_frame.pack_forget()
            except Exception:
                pass
            
            # Asegurar que canvas esté visible
            self.canvas_pres.pack(side="left", fill="both", expand=True)
            self.scrollbar_pres.pack(side="right", fill="y")

            for categoria in sorted(self.gestor_presupuestos.presupuestos.keys()):
                self.crear_tarjeta_presupuesto(categoria)

            self._update_scroll_state()
        else:
            self.mostrar_sin_presupuestos()

        # Recalcular scroll
        self._update_scroll_state()

    def mostrar_sin_presupuestos(self):
        """Muestra mensaje cuando no hay presupuestos ocupando toda la sección 'Mis Presupuestos'"""
        # Ocultar completamente el canvas y scrollbar de presupuestos
        try:
            self.canvas_pres.pack_forget()
            self.scrollbar_pres.pack_forget()
        except Exception:
            pass

        # Limpiar estado vacío
        for w in self.empty_state_frame.winfo_children():
            w.destroy()

        # Hacer que el estado vacío ocupe TODO el espacio disponible
        self.empty_state_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame interno centrado
        frame_centro = ttk.Frame(self.empty_state_frame)
        frame_centro.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        ttk.Label(frame_centro, text="💰", font=('Arial', 48)).pack(pady=10)
        ttk.Label(frame_centro,
                text="No tienes presupuestos configurados",
                font=('Arial', 14, 'bold')).pack(pady=5)
        ttk.Label(frame_centro,
                text="Haz clic en '➕ Nuevo Presupuesto' para comenzar",
                font=('Arial', 10)).pack(pady=5)

        # Forzar actualización de la geometría
        self.empty_state_frame.update_idletasks()

    def crear_tarjeta_presupuesto(self, categoria):
        """Crea una tarjeta visual para un presupuesto"""
        presupuesto = self.gestor_presupuestos.obtener_presupuesto(categoria)
        gasto_actual = self.gestor_presupuestos.obtener_gasto_categoria_mes_actual(categoria)
        porcentaje = self.gestor_presupuestos.obtener_porcentaje_uso(categoria)
        saldo = self.gestor_presupuestos.obtener_saldo_restante(categoria)

        # Determinar color según porcentaje
        if porcentaje >= 100:
            color_borde = '#E74C3C'
            color_barra = '#E74C3C'
        elif porcentaje >= 80:
            color_borde = '#F39C12'
            color_barra = '#F39C12'
        else:
            color_borde = '#3498DB'
            color_barra = '#27AE60'

        # Frame principal
        frame = tk.Frame(self.frame_presupuestos, bg=color_borde,
                        relief=tk.RAISED, borderwidth=2)
        frame.pack(fill=tk.X, pady=8)

        # Frame interno
        frame_int = tk.Frame(frame, bg='white', padx=15, pady=12)
        frame_int.pack(fill=tk.X, padx=2, pady=2)

        # Fila 1: Categoría y montos
        frame_top = tk.Frame(frame_int, bg='white')
        frame_top.pack(fill=tk.X)

        # Categoría
        lbl_categoria = tk.Label(frame_top, text=f"📁 {categoria}",
                                font=('Arial', 12, 'bold'),
                                bg='white', fg='#2C3E50')
        lbl_categoria.pack(side=tk.LEFT)

        # Monto
        lbl_monto = tk.Label(frame_top,
                            text=f"${gasto_actual:,.2f} / ${presupuesto['monto']:,.2f}",
                            font=('Arial', 11),
                            bg='white', fg='#7F8C8D')
        lbl_monto.pack(side=tk.RIGHT)

        # Barra de progreso
        frame_barra = tk.Frame(frame_int, bg='white')
        frame_barra.pack(fill=tk.X, pady=10)

        progress = ttk.Progressbar(frame_barra, length=500, mode='determinate',
                                  value=min(porcentaje, 100))
        progress.pack(fill=tk.X)

        # Fila 3: Info adicional
        frame_info = tk.Frame(frame_int, bg='white')
        frame_info.pack(fill=tk.X)

        # Porcentaje
        color_porcentaje = color_barra
        lbl_porcentaje = tk.Label(frame_info,
                                  text=f"{porcentaje:.1f}%",
                                  font=('Arial', 10, 'bold'),
                                  bg='white', fg=color_porcentaje)
        lbl_porcentaje.pack(side=tk.LEFT)

        # Saldo
        signo_saldo = "" if saldo < 0 else "+"
        color_saldo = '#E74C3C' if saldo < 0 else '#27AE60'
        lbl_saldo = tk.Label(frame_info,
                            text=f"Saldo: {signo_saldo}${saldo:,.2f}",
                            font=('Arial', 10),
                            bg='white', fg=color_saldo)
        lbl_saldo.pack(side=tk.LEFT, padx=20)

        # Estado
        if porcentaje >= 100:
            estado_text = "🔴 EXCEDIDO"
            estado_color = '#E74C3C'
        elif porcentaje >= 80:
            estado_text = "🟡 CUIDADO"
            estado_color = '#F39C12'
        else:
            estado_text = "🟢 BIEN"
            estado_color = '#27AE60'

        lbl_estado = tk.Label(frame_info, text=estado_text,
                             font=('Arial', 9, 'bold'),
                             bg='white', fg=estado_color)
        lbl_estado.pack(side=tk.RIGHT)

        # Botones
        frame_btns = tk.Frame(frame_int, bg='white')
        frame_btns.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(frame_btns, text="✏️ Editar",
                  command=lambda c=categoria: self.editar_presupuesto(c),
                  width=12).pack(side=tk.LEFT, padx=5)

        ttk.Button(frame_btns, text="🗑️ Eliminar",
                  command=lambda c=categoria: self.eliminar_presupuesto(c),
                  width=12).pack(side=tk.LEFT)

    def agregar_presupuesto(self):
        """Muestra diálogo para agregar presupuesto"""
        ventana = tk.Toplevel(self)
        ventana.title("Nuevo Presupuesto")
        ventana.transient(self.winfo_toplevel())
        ventana.grab_set()

        # Tamaño y mínimos para que no se corten botones
        ventana.geometry("500x360")
        try:
            ventana.minsize(480, 340)
            ventana.resizable(True, True)
        except Exception:
            pass

        # Centrar
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() // 2) - (ventana.winfo_width() // 2)
        y = (ventana.winfo_screenheight() // 2) - (ventana.winfo_height() // 2)
        ventana.geometry(f"{ventana.winfo_width()}x{ventana.winfo_height()}+{x}+{y}")

        frame = ttk.Frame(ventana, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="➕ Nuevo Presupuesto",
                 font=('Arial', 14, 'bold')).pack(pady=10)

        # Categoría
        ttk.Label(frame, text="Categoría:").pack(anchor=tk.W, pady=(10, 0))

        categorias_sin_presupuesto = self.gestor_presupuestos.obtener_categorias_sin_presupuesto()

        if not categorias_sin_presupuesto:
            ttk.Label(frame,
                     text="Todas las categorías ya tienen presupuesto",
                     foreground='#E74C3C').pack(pady=10)
            ttk.Button(frame, text="Cerrar", command=ventana.destroy).pack(pady=10)
            return

        combo_cat = ttk.Combobox(frame, values=categorias_sin_presupuesto,
                                state='readonly', width=30)
        combo_cat.pack(fill=tk.X, pady=5)
        combo_cat.current(0)

        # Monto
        ttk.Label(frame, text="Monto mensual:").pack(anchor=tk.W, pady=(10, 0))
        entry_monto = ttk.Entry(frame, width=30)
        entry_monto.pack(fill=tk.X, pady=5)

        # Sugerencia
        def mostrar_sugerencia():
            categoria = combo_cat.get()
            if categoria:
                sugerencia = self.gestor_presupuestos.sugerir_presupuesto(categoria)
                if sugerencia:
                    lbl_sugerencia.config(
                        text=f"💡 Sugerencia basada en historial: ${sugerencia:,.2f}"
                    )
                    entry_monto.delete(0, tk.END)
                    entry_monto.insert(0, str(sugerencia))
                else:
                    lbl_sugerencia.config(text="💡 Sin historial suficiente")

        combo_cat.bind('<<ComboboxSelected>>', lambda e: mostrar_sugerencia())

        lbl_sugerencia = ttk.Label(frame, text="",
                                   font=('Arial', 9, 'italic'),
                                   foreground='#7F8C8D')
        lbl_sugerencia.pack(pady=5)

        # Botones
        frame_btns = ttk.Frame(frame)
        frame_btns.pack(pady=20, fill=tk.X)

        def guardar():
            categoria = combo_cat.get()
            monto_str = entry_monto.get().strip()

            if not categoria or not monto_str:
                messagebox.showwarning("Advertencia", "Completa todos los campos")
                return

            try:
                monto = float(monto_str)
                if monto <= 0:
                    raise ValueError

                if self.gestor_presupuestos.establecer_presupuesto(categoria, monto):
                    ventana.destroy()
                    self.actualizar_presupuestos()
                    messagebox.showinfo("Éxito",
                                      f"Presupuesto de ${monto:,.2f} establecido para {categoria}")
                else:
                    messagebox.showerror("Error", "No se pudo guardar el presupuesto")
            except ValueError:
                messagebox.showwarning("Advertencia", "Ingresa un monto válido")

        ttk.Button(frame_btns, text="💾 Guardar", command=guardar).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_btns, text="Cancelar", command=ventana.destroy).pack(side=tk.LEFT, padx=5)

        # Mostrar sugerencia inicial
        mostrar_sugerencia()

    def editar_presupuesto(self, categoria):
        """Edita un presupuesto existente"""
        presupuesto_actual = self.gestor_presupuestos.obtener_presupuesto(categoria)

        ventana = tk.Toplevel(self)
        ventana.title(f"Editar Presupuesto - {categoria}")
        ventana.transient(self.winfo_toplevel())
        ventana.grab_set()

        # Tamaño y mínimos para evitar recortes
        ventana.geometry("480x260")
        try:
            ventana.minsize(460, 240)
            ventana.resizable(True, True)
        except Exception:
            pass

        frame = ttk.Frame(ventana, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text=f"Editar Presupuesto: {categoria}",
                 font=('Arial', 12, 'bold')).pack(pady=10)

        ttk.Label(frame, text=f"Presupuesto actual: ${presupuesto_actual['monto']:,.2f}").pack(pady=5)

        ttk.Label(frame, text="Nuevo monto:").pack(pady=5)
        entry_monto = ttk.Entry(frame, width=20)
        entry_monto.insert(0, str(presupuesto_actual['monto']))
        entry_monto.pack(pady=5)
        entry_monto.select_range(0, tk.END)
        entry_monto.focus()

        def guardar():
            try:
                monto = float(entry_monto.get())
                if monto <= 0:
                    raise ValueError

                if self.gestor_presupuestos.establecer_presupuesto(categoria, monto):
                    ventana.destroy()
                    self.actualizar_presupuestos()
                    messagebox.showinfo("Éxito", "Presupuesto actualizado")
            except ValueError:
                messagebox.showwarning("Advertencia", "Monto inválido")

        ttk.Button(frame, text="💾 Guardar", command=guardar).pack(pady=10)
        ventana.bind('<Return>', lambda e: guardar())

    def eliminar_presupuesto(self, categoria):
        """Elimina un presupuesto"""
        if messagebox.askyesno("Confirmar",
                              f"¿Eliminar el presupuesto de '{categoria}'?"):
            if self.gestor_presupuestos.eliminar_presupuesto(categoria):
                self.actualizar_presupuestos()
                messagebox.showinfo("Éxito", "Presupuesto eliminado")

    def _update_scroll_state(self):
        """Recalcula el scroll SOLO de la sección 'Mis Presupuestos'."""
        try:
            # Si la lista está visible, actualizar su scroll interno
            if self.canvas_pres.winfo_ismapped():
                self.canvas_pres.update_idletasks()
                bbox = self.canvas_pres.bbox('all')
                if bbox:
                    self.canvas_pres.configure(scrollregion=bbox)
                    content_h = bbox[3] - bbox[1]
                else:
                    self.canvas_pres.configure(scrollregion=(0, 0, 0, 0))
                    content_h = 0
                view_h = self.canvas_pres.winfo_height()
                self._can_scroll_pres = content_h > view_h + 1
                if self._can_scroll_pres:
                    self.scrollbar_pres.state(['!disabled'])
                else:
                    self.scrollbar_pres.state(['disabled'])
                    self.canvas_pres.yview_moveto(0.0)
            else:
                # Lista oculta: deshabilitar scroll
                self._can_scroll_pres = False
                self.scrollbar_pres.state(['disabled'])
        except Exception:
            pass