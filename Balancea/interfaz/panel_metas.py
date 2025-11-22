"""
Panel de Metas Financieras
Gestión y seguimiento de objetivos de ahorro
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry
from datos.gestor_metas import GestorMetas


class PanelMetas(ttk.Frame):
    """Panel para gestionar metas financieras"""

    # ✅ Agregar constante
    MAX_DESCRIPCION_CARACTERES = 80

    def __init__(self, parent, gestor_datos):
        super().__init__(parent)
        self.gestor_datos = gestor_datos
        self.gestor_metas = GestorMetas()
        self.meta_seleccionada = None

        self.crear_interfaz()
        self.actualizar_metas()

    def crear_interfaz(self):
        """Crea la interfaz del panel"""
        # Título y resumen
        frame_header = ttk.Frame(self)
        frame_header.pack(fill=tk.X, padx=10, pady=10)

        titulo = ttk.Label(frame_header, text="🎯 Metas Financieras",
                           font=('Arial', 16, 'bold'))
        titulo.pack(side=tk.LEFT)

        self.lbl_resumen = ttk.Label(frame_header,
                                     text="0 metas activas",
                                     font=('Arial', 11))
        self.lbl_resumen.pack(side=tk.RIGHT, padx=10)

        # === FORMULARIO ===
        frame_form = ttk.LabelFrame(self, text="Nueva Meta", padding="10")
        frame_form.pack(fill=tk.X, padx=10, pady=5)

        # Nombre de la meta
        ttk.Label(frame_form, text="Nombre:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_nombre = ttk.Entry(frame_form, width=30)
        self.entry_nombre.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # Monto objetivo
        ttk.Label(frame_form, text="Monto Objetivo:").grid(row=0, column=2, sticky=tk.W, pady=5)
        self.entry_monto = ttk.Entry(frame_form, width=15)
        self.entry_monto.grid(row=0, column=3, sticky=(tk.W, tk.E), padx=5, pady=5)

        # Fecha límite
        ttk.Label(frame_form, text="Fecha Límite:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_fecha = DateEntry(frame_form, width=15,
                                     background='darkblue', foreground='white',
                                     borderwidth=2, date_pattern='yyyy-mm-dd')
        self.entry_fecha.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # REEMPLÁZALA POR:
        ttk.Label(frame_form, text="Descripción:").grid(row=1, column=2, sticky=tk.W, pady=5)

        # Frame con contador
        desc_frame_meta = ttk.Frame(frame_form)
        desc_frame_meta.grid(row=1, column=3, sticky=(tk.W, tk.E), padx=5, pady=5)

        self.entry_desc = ttk.Entry(desc_frame_meta, width=30)
        self.entry_desc.pack(side=tk.TOP, fill=tk.X)

        # Contador de caracteres
        self.lbl_contador_meta = ttk.Label(desc_frame_meta,
                                           text=f"0/{self.MAX_DESCRIPCION_CARACTERES}",
                                           font=('Arial', 8),
                                           foreground='gray')
        self.lbl_contador_meta.pack(side=tk.TOP, anchor=tk.E)

        # Bind para actualizar contador
        self.entry_desc.bind('<KeyPress>', self.actualizar_contador_meta)
        self.entry_desc.bind('<KeyRelease>', self.actualizar_contador_meta)

        # Botones
        frame_btns = ttk.Frame(frame_form)
        frame_btns.grid(row=2, column=0, columnspan=4, pady=10)

        self.btn_agregar = ttk.Button(frame_btns, text="➕ Agregar Meta",
                                      command=self.agregar_meta)
        self.btn_agregar.pack(side=tk.LEFT, padx=5)

        self.btn_editar = ttk.Button(frame_btns, text="✏️ Editar",
                                     command=self.editar_meta, state=tk.DISABLED)
        self.btn_editar.pack(side=tk.LEFT, padx=5)

        self.btn_eliminar = ttk.Button(frame_btns, text="🗑️ Eliminar",
                                       command=self.eliminar_meta, state=tk.DISABLED)
        self.btn_eliminar.pack(side=tk.LEFT, padx=5)

        self.btn_limpiar = ttk.Button(frame_btns, text="🔄 Limpiar",
                                      command=self.limpiar_formulario)
        self.btn_limpiar.pack(side=tk.LEFT, padx=5)

        frame_form.columnconfigure(1, weight=1)
        frame_form.columnconfigure(3, weight=1)

        # === LISTA DE METAS ===
        frame_lista = ttk.LabelFrame(self, text="Mis Metas", padding="10")
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Canvas con scroll
        canvas = tk.Canvas(frame_lista, bg='#ECF0F1', highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=canvas.yview)
        self.frame_metas = ttk.Frame(canvas)

        self.frame_metas.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.frame_metas, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def actualizar_contador_meta(self, event=None):
        """Actualiza el contador de caracteres en descripción de meta"""
        self.after(1, self._actualizar_contador_meta_interno)

    def _actualizar_contador_meta_interno(self):
        """Función interna para actualizar contador de meta"""
        texto = self.entry_desc.get()
        longitud = len(texto)

        # Actualizar contador
        self.lbl_contador_meta.config(text=f"{longitud}/{self.MAX_DESCRIPCION_CARACTERES}")

        # Cambiar color según longitud
        if longitud > self.MAX_DESCRIPCION_CARACTERES:
            self.lbl_contador_meta.config(foreground='red', font=('Arial', 9, 'bold'))
            # Truncar automáticamente
            self.entry_desc.delete(self.MAX_DESCRIPCION_CARACTERES, tk.END)
            # Sonido de advertencia
            self.bell()
        elif longitud > self.MAX_DESCRIPCION_CARACTERES * 0.9:  # 72 caracteres
            self.lbl_contador_meta.config(foreground='orange', font=('Arial', 8, 'bold'))
        elif longitud > self.MAX_DESCRIPCION_CARACTERES * 0.7:  # 56 caracteres
            self.lbl_contador_meta.config(foreground='#F39C12', font=('Arial', 8))
        else:
            self.lbl_contador_meta.config(foreground='gray', font=('Arial', 8))

    def agregar_meta(self):
        """Agrega una nueva meta"""
        nombre = self.entry_nombre.get().strip()
        monto = self.entry_monto.get().strip()
        fecha = self.entry_fecha.get_date().strftime('%Y-%m-%d')
        desc = self.entry_desc.get().strip()

        if not nombre:
            messagebox.showwarning("Advertencia", "Ingresa un nombre para la meta")
            return

        # ✅ Validar longitud de descripción
        if len(desc) > self.MAX_DESCRIPCION_CARACTERES:
            messagebox.showwarning("Advertencia",
                                   f"La descripción es muy larga\n\nMáximo: {self.MAX_DESCRIPCION_CARACTERES} caracteres\nActual: {len(desc)}")
            return

        try:
            monto_float = float(monto)
            if monto_float <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Advertencia", "Ingresa un monto válido")
            return

        # Truncar por si acaso
        if len(desc) > self.MAX_DESCRIPCION_CARACTERES:
            desc = desc[:self.MAX_DESCRIPCION_CARACTERES]

        self.gestor_metas.agregar_meta(nombre, monto_float, fecha, desc)
        self.actualizar_metas()
        self.limpiar_formulario()
        messagebox.showinfo("Éxito", f"Meta '{nombre}' agregada correctamente")

    def editar_meta(self):
        """Edita la meta seleccionada"""
        if not self.meta_seleccionada:
            return

        nombre = self.entry_nombre.get().strip()
        monto = self.entry_monto.get().strip()
        fecha = self.entry_fecha.get_date().strftime('%Y-%m-%d')
        desc = self.entry_desc.get().strip()

        if not nombre or not monto:
            messagebox.showwarning("Advertencia", "Completa todos los campos")
            return

        # ✅ Validar longitud de descripción
        if len(desc) > self.MAX_DESCRIPCION_CARACTERES:
            messagebox.showwarning("Advertencia",
                                   f"La descripción es muy larga\n\nMáximo: {self.MAX_DESCRIPCION_CARACTERES} caracteres")
            return

        try:
            monto_float = float(monto)
        except ValueError:
            messagebox.showwarning("Advertencia", "Monto inválido")
            return

        # Truncar por si acaso
        if len(desc) > self.MAX_DESCRIPCION_CARACTERES:
            desc = desc[:self.MAX_DESCRIPCION_CARACTERES]

        self.gestor_metas.editar_meta(self.meta_seleccionada['id'],
                                      nombre, monto_float, fecha, desc)
        self.actualizar_metas()
        self.limpiar_formulario()
        messagebox.showinfo("Éxito", "Meta editada correctamente")

    def eliminar_meta(self):
        """Elimina la meta seleccionada"""
        if not self.meta_seleccionada:
            return

        if messagebox.askyesno("Confirmar",
                               f"¿Eliminar la meta '{self.meta_seleccionada['nombre']}'?"):
            self.gestor_metas.eliminar_meta(self.meta_seleccionada['id'])
            self.actualizar_metas()
            self.limpiar_formulario()
            messagebox.showinfo("Éxito", "Meta eliminada")

    def limpiar_formulario(self):
        """Limpia el formulario"""
        self.entry_nombre.delete(0, tk.END)
        self.entry_monto.delete(0, tk.END)
        self.entry_desc.delete(0, tk.END)
        self.entry_fecha.set_date(datetime.now())
        self.meta_seleccionada = None
        self.btn_editar.config(state=tk.DISABLED)
        self.btn_eliminar.config(state=tk.DISABLED)

        # ✅ Resetear contador
        if hasattr(self, 'lbl_contador_meta'):
            self.lbl_contador_meta.config(
                text=f"0/{self.MAX_DESCRIPCION_CARACTERES}",
                foreground='gray',
                font=('Arial', 8)
            )

    def actualizar_metas(self):
        """Actualiza la visualización de metas"""
        # Limpiar frame
        for widget in self.frame_metas.winfo_children():
            widget.destroy()

        # Actualizar resumen
        resumen = self.gestor_metas.obtener_resumen()
        self.lbl_resumen.config(
            text=f"{resumen['activas']} activas | {resumen['completadas']} completadas | {resumen['progreso_general']:.0f}% total"
        )

        # Metas activas
        metas_activas = self.gestor_metas.obtener_metas_activas()
        if metas_activas:
            lbl_activas = ttk.Label(self.frame_metas, text="📌 Metas Activas",
                                    font=('Arial', 12, 'bold'))
            lbl_activas.pack(anchor=tk.W, pady=(10, 5))

            for meta in metas_activas:
                self.crear_tarjeta_meta(meta)

        # Metas completadas
        metas_completadas = self.gestor_metas.obtener_metas_completadas()
        if metas_completadas:
            lbl_completadas = ttk.Label(self.frame_metas, text="✅ Metas Completadas",
                                        font=('Arial', 12, 'bold'))
            lbl_completadas.pack(anchor=tk.W, pady=(20, 5))

            for meta in metas_completadas:
                self.crear_tarjeta_meta(meta)

        # Sin metas
        if not metas_activas and not metas_completadas:
            lbl_vacio = ttk.Label(self.frame_metas,
                                  text="🎯 No tienes metas registradas\n\nAgrega tu primera meta financiera arriba",
                                  font=('Arial', 11),
                                  justify=tk.CENTER)
            lbl_vacio.pack(expand=True, pady=50)

    def crear_tarjeta_meta(self, meta):
        """Crea una tarjeta visual para una meta"""
        # Frame principal
        frame = tk.Frame(self.frame_metas, bg='white',
                         relief=tk.RAISED, borderwidth=1)
        frame.pack(fill=tk.X, padx=5, pady=5)

        # Frame interno
        frame_int = tk.Frame(frame, bg='white', padx=15, pady=10)
        frame_int.pack(fill=tk.X)

        # Nombre y monto
        frame_top = tk.Frame(frame_int, bg='white')
        frame_top.pack(fill=tk.X)

        lbl_nombre = tk.Label(frame_top, text=meta['nombre'],
                              font=('Arial', 12, 'bold'),
                              bg='white', fg='#2C3E50')
        lbl_nombre.pack(side=tk.LEFT)

        progreso = self.gestor_metas.obtener_progreso(meta['id'])
        lbl_monto = tk.Label(frame_top,
                             text=f"${meta['monto_actual']:,.2f} / ${meta['monto_objetivo']:,.2f}",
                             font=('Arial', 11),
                             bg='white', fg='#7F8C8D')
        lbl_monto.pack(side=tk.RIGHT)

        # Barra de progreso
        progress = ttk.Progressbar(frame_int, length=400, mode='determinate', value=progreso)
        progress.pack(fill=tk.X, pady=10)

        # Info adicional
        frame_info = tk.Frame(frame_int, bg='white')
        frame_info.pack(fill=tk.X)

        # Progreso
        lbl_prog = tk.Label(frame_info, text=f"{progreso:.1f}%",
                            font=('Arial', 10, 'bold'),
                            bg='white',
                            fg='#27AE60' if progreso >= 50 else '#F39C12')
        lbl_prog.pack(side=tk.LEFT)

        # Días restantes
        dias = self.gestor_metas.calcular_dias_restantes(meta['id'])
        if dias is not None:
            if dias < 0:
                texto_dias = f"⏰ Vencida hace {abs(dias)} días"
                color_dias = '#E74C3C'
            elif dias == 0:
                texto_dias = "⏰ ¡Hoy es el último día!"
                color_dias = '#E74C3C'
            elif dias <= 7:
                texto_dias = f"⏰ {dias} días restantes"
                color_dias = '#F39C12'
            else:
                texto_dias = f"📅 {dias} días restantes"
                color_dias = '#7F8C8D'

            lbl_dias = tk.Label(frame_info, text=texto_dias,
                                font=('Arial', 9),
                                bg='white', fg=color_dias)
            lbl_dias.pack(side=tk.LEFT, padx=10)

        # Descripción
        if meta['descripcion']:
            lbl_desc = tk.Label(frame_info, text=meta['descripcion'],
                                font=('Arial', 9, 'italic'),
                                bg='white', fg='#95A5A6')
            lbl_desc.pack(side=tk.LEFT, padx=10)

        # Botones
        frame_btns = tk.Frame(frame_int, bg='white')
        frame_btns.pack(fill=tk.X, pady=(10, 0))

        btn_aporte = ttk.Button(frame_btns, text="💰 Agregar Aporte",
                                command=lambda m=meta: self.agregar_aporte(m))
        btn_aporte.pack(side=tk.LEFT, padx=5)

        btn_editar = ttk.Button(frame_btns, text="✏️",
                                command=lambda m=meta: self.cargar_meta(m),
                                width=3)
        btn_editar.pack(side=tk.LEFT)

    def cargar_meta(self, meta):
        """Carga una meta en el formulario para editar"""
        self.meta_seleccionada = meta
        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, meta['nombre'])
        self.entry_monto.delete(0, tk.END)
        self.entry_monto.insert(0, str(meta['monto_objetivo']))
        self.entry_desc.delete(0, tk.END)
        self.entry_desc.insert(0, meta['descripcion'])

        if meta['fecha_limite']:
            fecha_obj = datetime.strptime(meta['fecha_limite'], '%Y-%m-%d')
            self.entry_fecha.set_date(fecha_obj)

        self.btn_editar.config(state=tk.NORMAL)
        self.btn_eliminar.config(state=tk.NORMAL)

    def agregar_aporte(self, meta):
        """Agrega un aporte a una meta"""
        ventana = tk.Toplevel(self)
        ventana.title("Agregar Aporte")
        ventana.geometry("400x200")
        ventana.transient(self)
        ventana.grab_set()

        frame = ttk.Frame(ventana, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text=f"Meta: {meta['nombre']}",
                  font=('Arial', 12, 'bold')).pack(pady=10)

        ttk.Label(frame, text=f"Actual: ${meta['monto_actual']:,.2f}").pack()
        ttk.Label(frame, text=f"Objetivo: ${meta['monto_objetivo']:,.2f}").pack(pady=(0, 20))

        ttk.Label(frame, text="Monto del aporte:").pack()
        entry_aporte = ttk.Entry(frame, width=20, font=('Arial', 11))
        entry_aporte.pack(pady=10)
        entry_aporte.focus()

        def guardar_aporte():
            try:
                aporte = float(entry_aporte.get())
                if aporte <= 0:
                    raise ValueError

                self.gestor_metas.agregar_aporte(meta['id'], aporte)
                self.actualizar_metas()
                ventana.destroy()

                nuevo_progreso = self.gestor_metas.obtener_progreso(meta['id'])
                if nuevo_progreso >= 100:
                    messagebox.showinfo("🎉 ¡Meta Completada!",
                                        f"¡Felicitaciones! Completaste tu meta '{meta['nombre']}'")
                else:
                    messagebox.showinfo("Éxito", f"Aporte de ${aporte:,.2f} agregado")
            except ValueError:
                messagebox.showwarning("Advertencia", "Ingresa un monto válido")

        ttk.Button(frame, text="💰 Agregar Aporte",
                   command=guardar_aporte).pack(pady=10)

        ventana.bind('<Return>', lambda e: guardar_aporte())