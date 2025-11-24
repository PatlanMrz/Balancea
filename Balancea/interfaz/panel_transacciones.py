"""
Panel de Transacciones - CORREGIDO
Límite de caracteres y truncado de descripciones largas
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from tkcalendar import DateEntry
import csv


class PanelTransacciones(ttk.Frame):
    """Panel para gestionar transacciones"""

    # ✅ FIX: Constantes para límites
    MAX_DESCRIPCION_CARACTERES = 50
    MAX_DESCRIPCION_DISPLAY = 50  # Para mostrar en lista

    def __init__(self, parent, gestor_datos, callback_actualizar):
        super().__init__(parent)
        self.gestor_datos = gestor_datos
        self.callback_actualizar = callback_actualizar
        self.transaccion_seleccionada = None

        self.crear_interfaz()
        self.cargar_transacciones()

    def crear_interfaz(self):
        """Crea la interfaz del panel"""
        # === SECCIÓN BÚSQUEDA Y FILTROS ===
        frame_busqueda = ttk.LabelFrame(self, text="🔍 Búsqueda y Filtros", padding="10")
        frame_busqueda.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

        # Búsqueda
        ttk.Label(frame_busqueda, text="Buscar:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.busqueda_var = tk.StringVar()
        self.busqueda_var.trace('w', self.aplicar_filtros)
        busqueda_entry = ttk.Entry(frame_busqueda, textvariable=self.busqueda_var, width=25)
        busqueda_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # Filtro por Tipo
        ttk.Label(frame_busqueda, text="Tipo:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.filtro_tipo_var = tk.StringVar()
        filtro_tipo = ttk.Combobox(frame_busqueda, textvariable=self.filtro_tipo_var,
                                   values=['Todos', 'Ingreso', 'Gasto'],
                                   state='readonly', width=12)
        filtro_tipo.set('Todos')
        filtro_tipo.grid(row=0, column=3, sticky=(tk.W, tk.E), padx=5, pady=5)
        filtro_tipo.bind('<<ComboboxSelected>>', self.on_cambio_tipo_filtro)

        # Filtro por Categoría
        ttk.Label(frame_busqueda, text="Categoría:").grid(row=0, column=4, sticky=tk.W, padx=5, pady=5)
        self.filtro_categoria_var = tk.StringVar()
        self.filtro_categoria_combo = ttk.Combobox(frame_busqueda,
                                                   textvariable=self.filtro_categoria_var,
                                                   state='readonly', width=15)
        self.filtro_categoria_combo.set('Todas')
        self.filtro_categoria_combo.grid(row=0, column=5, sticky=(tk.W, tk.E), padx=5, pady=5)
        self.filtro_categoria_combo.bind('<<ComboboxSelected>>', lambda e: self.aplicar_filtros())

        # Botones de acción
        btn_limpiar_filtros = ttk.Button(frame_busqueda, text="🔄 Limpiar Filtros",
                                         command=self.limpiar_filtros)
        btn_limpiar_filtros.grid(row=0, column=6, padx=5, pady=5)

        btn_exportar = ttk.Button(frame_busqueda, text="📥 Exportar CSV",
                                 command=self.exportar_transacciones)
        btn_exportar.grid(row=0, column=7, padx=5, pady=5)

        btn_gestionar_cat = ttk.Button(frame_busqueda, text="⚙️ Categorías",
                                       command=self.gestionar_categorias)
        btn_gestionar_cat.grid(row=0, column=8, padx=5, pady=5)

        # === SECCIÓN FORMULARIO ===
        frame_formulario = ttk.LabelFrame(self, text="Nueva Transacción", padding="10")
        frame_formulario.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)

        # Fecha
        ttk.Label(frame_formulario, text="Fecha:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.fecha_entry = DateEntry(frame_formulario, width=15,
                                     background='darkblue', foreground='white',
                                     borderwidth=2, date_pattern='yyyy-mm-dd')
        self.fecha_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # Descripción con límite de caracteres
        ttk.Label(frame_formulario, text="Descripción:").grid(row=0, column=2, sticky=tk.W, pady=5)

        # ✅ FIX: Frame para descripción con contador
        desc_frame = ttk.Frame(frame_formulario)
        desc_frame.grid(row=0, column=3, sticky=(tk.W, tk.E), padx=5, pady=5)

        self.descripcion_entry = ttk.Entry(desc_frame, width=30)
        self.descripcion_entry.pack(side=tk.TOP, fill=tk.X)

        # Contador de caracteres
        self.lbl_contador = ttk.Label(desc_frame, text=f"0/{self.MAX_DESCRIPCION_CARACTERES}",
                                      font=('Arial', 8), foreground='gray')
        self.lbl_contador.pack(side=tk.TOP, anchor=tk.E)

        # Bind para actualizar contador y validar
        self.descripcion_entry.bind('<KeyPress>', self.actualizar_contador_descripcion)
        self.descripcion_entry.bind('<KeyRelease>', self.actualizar_contador_descripcion)

        # Monto
        ttk.Label(frame_formulario, text="Monto:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.monto_entry = ttk.Entry(frame_formulario, width=15)
        self.monto_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # Tipo (Ingreso/Gasto)
        ttk.Label(frame_formulario, text="Tipo:").grid(row=1, column=2, sticky=tk.W, pady=5)
        self.tipo_var = tk.StringVar()
        self.tipo_combo = ttk.Combobox(frame_formulario, textvariable=self.tipo_var,
                                       values=['Ingreso', 'Gasto'], state='readonly', width=15)
        self.tipo_combo.grid(row=1, column=3, sticky=(tk.W, tk.E), padx=5, pady=5)
        self.tipo_combo.bind('<<ComboboxSelected>>', self.actualizar_categorias)

        # Categoría
        ttk.Label(frame_formulario, text="Categoría:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.categoria_var = tk.StringVar()
        self.categoria_combo = ttk.Combobox(frame_formulario, textvariable=self.categoria_var,
                                           state='readonly', width=20)
        self.categoria_combo.grid(row=2, column=1, columnspan=3, sticky=(tk.W, tk.E), padx=5, pady=5)

        # Botones de acción
        frame_botones = ttk.Frame(frame_formulario)
        frame_botones.grid(row=3, column=0, columnspan=4, pady=10)

        self.btn_agregar = ttk.Button(frame_botones, text="➕ Agregar", command=self.agregar_transaccion)
        self.btn_agregar.pack(side=tk.LEFT, padx=5)

        self.btn_editar = ttk.Button(frame_botones, text="✏️ Editar", command=self.editar_transaccion, state=tk.DISABLED)
        self.btn_editar.pack(side=tk.LEFT, padx=5)

        self.btn_eliminar = ttk.Button(frame_botones, text="🗑️ Eliminar", command=self.eliminar_transaccion, state=tk.DISABLED)
        self.btn_eliminar.pack(side=tk.LEFT, padx=5)

        self.btn_limpiar = ttk.Button(frame_botones, text="🔄 Limpiar", command=self.limpiar_formulario)
        self.btn_limpiar.pack(side=tk.LEFT, padx=5)

        # === SECCIÓN LISTA DE TRANSACCIONES ===
        self.frame_lista = ttk.LabelFrame(self, text="Historial de Transacciones", padding="10")
        self.frame_lista.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

        # Configurar grid para expandir
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.frame_lista.columnconfigure(0, weight=1)
        self.frame_lista.rowconfigure(0, weight=1)

        # Crear Treeview
        columnas = ('Fecha', 'Descripción', 'Monto', 'Tipo', 'Categoría')
        self.tree = ttk.Treeview(self.frame_lista, columns=columnas, show='headings', height=12)

        # Configurar columnas
        self.tree.heading('Fecha', text='Fecha')
        self.tree.heading('Descripción', text='Descripción')
        self.tree.heading('Monto', text='Monto')
        self.tree.heading('Tipo', text='Tipo')
        self.tree.heading('Categoría', text='Categoría')

        self.tree.column('Fecha', width=100)
        self.tree.column('Descripción', width=250)
        self.tree.column('Monto', width=100)
        self.tree.column('Tipo', width=100)
        self.tree.column('Categoría', width=150)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.frame_lista, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Frame de estado vacío (oculto inicialmente)
        self.empty_state_frame = ttk.Frame(self)
        # No se empaqueta aún; se mostrará cuando no haya transacciones

        # Bind para selección
        self.tree.bind('<<TreeviewSelect>>', self.seleccionar_transaccion)

        # Actualizar categorías en filtro
        self.actualizar_filtro_categorias()

    # ✅ FIX: Nueva función para actualizar contador
    def actualizar_contador_descripcion(self, event=None):
        """Actualiza el contador de caracteres y limita la entrada EN TIEMPO REAL"""
        # Usar after() para ejecutar después de que la tecla se procese
        self.after(1, self._actualizar_contador_interno)

    def _actualizar_contador_interno(self):
        """Función interna para actualizar contador"""
        texto = self.descripcion_entry.get()
        longitud = len(texto)

        # Actualizar contador
        self.lbl_contador.config(text=f"{longitud}/{self.MAX_DESCRIPCION_CARACTERES}")

        # Cambiar color según longitud
        if longitud > self.MAX_DESCRIPCION_CARACTERES:
            self.lbl_contador.config(foreground='red', font=('Arial', 9, 'bold'))
            # Truncar automáticamente
            self.descripcion_entry.delete(self.MAX_DESCRIPCION_CARACTERES, tk.END)
            # Sonido de advertencia (opcional)
            self.bell()
        elif longitud > self.MAX_DESCRIPCION_CARACTERES * 0.9:  # 180 caracteres
            self.lbl_contador.config(foreground='orange', font=('Arial', 8, 'bold'))
        elif longitud > self.MAX_DESCRIPCION_CARACTERES * 0.7:  # 140 caracteres
            self.lbl_contador.config(foreground='#F39C12', font=('Arial', 8))
        else:
            self.lbl_contador.config(foreground='gray', font=('Arial', 8))

    # ✅ FIX: Función para truncar descripciones en display
    def truncar_descripcion(self, descripcion):
        """Trunca descripción para mostrar en lista"""
        if len(descripcion) > self.MAX_DESCRIPCION_DISPLAY:
            return descripcion[:self.MAX_DESCRIPCION_DISPLAY] + "..."
        return descripcion

    def actualizar_categorias(self, event=None):
        """Actualiza las categorías según el tipo seleccionado"""
        tipo = self.tipo_var.get()
        if tipo:
            categorias = self.gestor_datos.categorias.get(tipo, [])
            self.categoria_combo['values'] = categorias
            if categorias:
                self.categoria_combo.current(0)

    def actualizar_filtro_categorias(self):
        """Actualiza el combo de filtro de categorías según el tipo seleccionado en filtros"""
        tipo_sel = self.filtro_tipo_var.get()
        if tipo_sel in ('Ingreso', 'Gasto'):
            categorias = self.gestor_datos.categorias.get(tipo_sel, [])
            self.filtro_categoria_combo['values'] = ['Todas'] + categorias
        else:
            # Sin tipo seleccionado: mostrar todas
            todas_categorias = []
            for categorias in self.gestor_datos.categorias.values():
                todas_categorias.extend(categorias)
            self.filtro_categoria_combo['values'] = ['Todas'] + todas_categorias

        # Si la categoría actual no está en la lista, resetear a 'Todas'
        actual = self.filtro_categoria_var.get()
        if actual not in self.filtro_categoria_combo['values']:
            self.filtro_categoria_var.set('Todas')

    def aplicar_filtros(self, *args):
        """Aplica los filtros de búsqueda"""
        # Limpiar árbol
        for item in self.tree.get_children():
            self.tree.delete(item)

        transacciones = self.obtener_transacciones_filtradas()

        if not transacciones:
            return  # lista vacía

        # Mostrar resultados ordenados
        transacciones = sorted(transacciones, key=lambda x: x['fecha'], reverse=True)
        for t in transacciones:
            monto_formato = f"${t['monto']:,.2f}"
            descripcion_display = self.truncar_descripcion(t['descripcion'])
            self.tree.insert('', tk.END, values=(
            t['fecha'],
            descripcion_display,
            monto_formato,
            t['tipo'],
            t['categoria']
            ))

    def limpiar_filtros(self):
        """Limpia todos los filtros"""
        self.busqueda_var.set('')
        self.filtro_tipo_var.set('Todos')
        self.actualizar_filtro_categorias()
        self.filtro_categoria_var.set('Todas')
        self.cargar_transacciones()

    def exportar_transacciones(self):
        """Exporta a CSV SOLO las transacciones que coinciden con los filtros activos"""
        archivo = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Exportar transacciones filtradas"
        )

        if not archivo:
            return

        filas = self.obtener_transacciones_filtradas()
        try:
            with open(archivo, 'w', newline='', encoding='utf-8') as f:
                campos = ['id', 'fecha', 'descripcion', 'monto', 'tipo', 'categoria']
                writer = csv.DictWriter(f, fieldnames=campos)
                writer.writeheader()
                writer.writerows(filas)
            messagebox.showinfo("Éxito", f"Transacciones filtradas exportadas a:\n{archivo}")
        except Exception as e:
            print(f"Error al exportar: {e}")
            messagebox.showerror("Error", "No se pudo exportar el archivo")

    def gestionar_categorias(self):
        """Abre ventana para gestionar categorías"""
        VentanaCategorias(self, self.gestor_datos)

    def agregar_transaccion(self):
        """Agrega una nueva transacción"""
        if not self.validar_campos():
            return

        fecha = self.fecha_entry.get_date().strftime('%Y-%m-%d')
        descripcion = self.descripcion_entry.get().strip()
        monto = float(self.monto_entry.get())
        tipo = self.tipo_var.get()
        categoria = self.categoria_var.get()

        # ✅ FIX: Validación extra de longitud
        if len(descripcion) > self.MAX_DESCRIPCION_CARACTERES:
            descripcion = descripcion[:self.MAX_DESCRIPCION_CARACTERES]

        self.gestor_datos.agregar_transaccion(fecha, descripcion, monto, tipo, categoria)

        self.cargar_transacciones()
        self.limpiar_formulario()
        self.callback_actualizar()

        messagebox.showinfo("Éxito", "Transacción agregada correctamente")

    def editar_transaccion(self):
        """Edita la transacción seleccionada"""
        if not self.transaccion_seleccionada:
            return

        if not self.validar_campos():
            return

        fecha = self.fecha_entry.get_date().strftime('%Y-%m-%d')
        descripcion = self.descripcion_entry.get().strip()
        monto = float(self.monto_entry.get())
        tipo = self.tipo_var.get()
        categoria = self.categoria_var.get()

        # ✅ FIX: Validación extra de longitud
        if len(descripcion) > self.MAX_DESCRIPCION_CARACTERES:
            descripcion = descripcion[:self.MAX_DESCRIPCION_CARACTERES]

        self.gestor_datos.editar_transaccion(
            self.transaccion_seleccionada['id'],
            fecha, descripcion, monto, tipo, categoria
        )

        self.cargar_transacciones()
        self.limpiar_formulario()
        self.callback_actualizar()

        messagebox.showinfo("Éxito", "Transacción editada correctamente")

    def eliminar_transaccion(self):
        """Elimina la transacción seleccionada"""
        if not self.transaccion_seleccionada:
            return

        if messagebox.askyesno("Confirmar", "¿Deseas eliminar esta transacción?"):
            self.gestor_datos.eliminar_transaccion(self.transaccion_seleccionada['id'])
            self.cargar_transacciones()
            self.limpiar_formulario()
            self.callback_actualizar()
            messagebox.showinfo("Éxito", "Transacción eliminada")

    def seleccionar_transaccion(self, event):
        """Maneja la selección de una transacción en la lista"""
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            valores = item['values']

            # Buscar la transacción completa (con descripción sin truncar)
            for t in self.gestor_datos.transacciones:
                if (t['fecha'] == valores[0] and
                    float(t['monto']) == float(valores[2].replace('$', '').replace(',', ''))):
                    self.transaccion_seleccionada = t
                    break

            self.cargar_datos_formulario()
            self.btn_editar.config(state=tk.NORMAL)
            self.btn_eliminar.config(state=tk.NORMAL)

    def cargar_datos_formulario(self):
        """Carga los datos de la transacción seleccionada en el formulario"""
        if self.transaccion_seleccionada:
            fecha_obj = datetime.strptime(self.transaccion_seleccionada['fecha'], '%Y-%m-%d')
            self.fecha_entry.set_date(fecha_obj)
            self.descripcion_entry.delete(0, tk.END)
            self.descripcion_entry.insert(0, self.transaccion_seleccionada['descripcion'])
            self.actualizar_contador_descripcion()  # ✅ Actualizar contador
            self.monto_entry.delete(0, tk.END)
            self.monto_entry.insert(0, str(self.transaccion_seleccionada['monto']))
            self.tipo_var.set(self.transaccion_seleccionada['tipo'])
            self.actualizar_categorias()
            self.categoria_var.set(self.transaccion_seleccionada['categoria'])

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.fecha_entry.set_date(datetime.now())
        self.descripcion_entry.delete(0, tk.END)
        self.actualizar_contador_descripcion()  # ✅ Resetear contador
        self.monto_entry.delete(0, tk.END)
        self.tipo_var.set('')
        self.categoria_var.set('')
        self.transaccion_seleccionada = None
        self.btn_editar.config(state=tk.DISABLED)
        self.btn_eliminar.config(state=tk.DISABLED)

    def validar_campos(self):
        """Valida que los campos estén completos - CON FEEDBACK VISUAL"""
        descripcion = self.descripcion_entry.get().strip()

        # Reset de estilos
        self.descripcion_entry.config(style='TEntry')

        if not descripcion:
            self.descripcion_entry.config(background='#FFE5E5')  # Rojo claro
            messagebox.showwarning("Advertencia", "❌ Ingresa una descripción")
            self.descripcion_entry.focus()
            return False

        if len(descripcion) < 3:
            self.descripcion_entry.config(background='#FFE5E5')
            messagebox.showwarning("Advertencia", "❌ La descripción debe tener al menos 3 caracteres")
            self.descripcion_entry.focus()
            return False

        # ✅ Validación de longitud máxima (no debería pasar, pero por si acaso)
        if len(descripcion) > self.MAX_DESCRIPCION_CARACTERES:
            self.descripcion_entry.config(background='#FFE5E5')
            messagebox.showwarning("Advertencia",
                                   f"❌ La descripción es demasiado larga\n\nMáximo: {self.MAX_DESCRIPCION_CARACTERES} caracteres\nActual: {len(descripcion)} caracteres")
            self.descripcion_entry.focus()
            return False

        # Restablecer color normal
        self.descripcion_entry.config(background='white')

        try:
            monto = float(self.monto_entry.get())
            if monto <= 0:
                raise ValueError
        except ValueError:
            self.monto_entry.config(background='#FFE5E5')
            messagebox.showwarning("Advertencia", "❌ Ingresa un monto válido")
            self.monto_entry.focus()
            # Restaurar después de 2 segundos
            self.after(2000, lambda: self.monto_entry.config(background='white'))
            return False

        self.monto_entry.config(background='white')

        if not self.tipo_var.get():
            messagebox.showwarning("Advertencia", "❌ Selecciona un tipo")
            self.tipo_combo.focus()
            return False

        if not self.categoria_var.get():
            messagebox.showwarning("Advertencia", "❌ Selecciona una categoría")
            self.categoria_combo.focus()
            return False

        return True

    def cargar_transacciones(self):
        """Carga todas las transacciones en el Treeview - CON MENSAJE VACÍO"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        transacciones = sorted(self.gestor_datos.transacciones,
                               key=lambda x: x['fecha'], reverse=True)

        # ✅ FIX: Mostrar mensaje si no hay transacciones
        if not transacciones:
            # Ocultar la lista y mostrar estado vacío a pantalla completa del panel
            try:
                self.frame_lista.grid_remove()
            except Exception:
                pass

            # Limpiar y construir el estado vacío si es necesario
            for w in self.empty_state_frame.winfo_children():
                w.destroy()

            lbl_icono = ttk.Label(self.empty_state_frame, text="💳", font=('Arial', 48))
            lbl_icono.pack(pady=10)

            lbl_titulo = ttk.Label(self.empty_state_frame,
                                   text="No hay transacciones registradas",
                                   font=('Arial', 14, 'bold'),
                                   foreground='#2C3E50')
            lbl_titulo.pack(pady=5)

            lbl_mensaje = ttk.Label(self.empty_state_frame,
                                    text="Comienza tu registro financiero agregando\ntu primera transacción con el formulario superior",
                                    font=('Arial', 10),
                                    foreground='#7F8C8D',
                                    justify=tk.CENTER)
            lbl_mensaje.pack(pady=10)

            # Tips
            frame_tips = ttk.Frame(self.empty_state_frame)
            frame_tips.pack(pady=15)

            lbl_tips_titulo = ttk.Label(frame_tips,
                                        text="💡 Consejos rápidos:",
                                        font=('Arial', 10, 'bold'),
                                        foreground='#3498DB')
            lbl_tips_titulo.pack(anchor=tk.W, padx=20)

            tips = [
                "• Registra tus gastos diariamente",
                "• Sé específico en las descripciones",
                "• Usa las categorías correctas"
            ]
            for tip in tips:
                ttk.Label(frame_tips, text=tip, font=('Arial', 9)).pack(anchor=tk.W, padx=20, pady=2)

            # Empaquetar el estado vacío ocupando todo
            self.empty_state_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        else:
            # Mostrar la lista y ocultar el estado vacío
            try:
                self.empty_state_frame.grid_forget()
            except Exception:
                pass
            self.frame_lista.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

            # Mostrar transacciones normalmente
            for t in transacciones:
                monto_formato = f"${t['monto']:,.2f}"
                descripcion_display = self.truncar_descripcion(t['descripcion'])

                self.tree.insert('', tk.END, values=(
                    t['fecha'],
                    descripcion_display,
                    monto_formato,
                    t['tipo'],
                    t['categoria']
                ))

    # ✅ Agregar función helper para demo
    def on_cambio_tipo_filtro(self, event=None):
        """Handler cuando cambia el tipo en filtros: actualiza categorías y aplica filtros"""
        self.actualizar_filtro_categorias()
        self.aplicar_filtros()

    def obtener_transacciones_filtradas(self):
        """Retorna la lista de transacciones que coinciden con los filtros actuales"""
        termino = self.busqueda_var.get().lower()
        tipo_filtro = self.filtro_tipo_var.get()
        categoria_filtro = self.filtro_categoria_var.get()

        transacciones = self.gestor_datos.transacciones.copy()

        if termino:
            transacciones = [t for t in transacciones if termino in t['descripcion'].lower()]
        if tipo_filtro and tipo_filtro != 'Todos':
            transacciones = [t for t in transacciones if t['tipo'] == tipo_filtro]
        if categoria_filtro and categoria_filtro != 'Todas':
            transacciones = [t for t in transacciones if t['categoria'] == categoria_filtro]

        return transacciones

    def generar_demo_desde_transacciones(self):
        """Genera datos demo desde transacciones"""
        if messagebox.askyesno("Generar Demo",
                               "¿Deseas generar transacciones de demostración?\n\n" +
                               "Esto agregará aproximadamente 60 transacciones de ejemplo."):
            from utils.generador_demo import GeneradorDemo

            generador = GeneradorDemo(self.gestor_datos)
            num_trans = generador.generar_transacciones_demo(60)

            # Actualizar vista
            self.cargar_transacciones()
            self.callback_actualizar()

            messagebox.showinfo("✅ Demo Generado",
                                f"Se generaron {num_trans} transacciones de demostración.\n\n" +
                                "Explora el Dashboard y Análisis para ver los datos.")


class VentanaCategorias(tk.Toplevel):
    """Ventana para gestionar categorías"""

    def __init__(self, parent, gestor_datos):
        super().__init__(parent)
        self.gestor_datos = gestor_datos
        self.title("Gestionar Categorías")
        self.geometry("500x400")
        self.transient(parent)
        self.grab_set()

        self.crear_interfaz()

    def crear_interfaz(self):
        """Crea la interfaz de gestión de categorías"""
        # Título
        titulo = ttk.Label(self, text="⚙️ Gestionar Categorías",
                          font=('Arial', 14, 'bold'))
        titulo.pack(pady=10)

        # Frame principal
        frame = ttk.Frame(self, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        # Tipo
        ttk.Label(frame, text="Tipo:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.tipo_var = tk.StringVar()
        tipo_combo = ttk.Combobox(frame, textvariable=self.tipo_var,
                                 values=['Ingreso', 'Gasto'], state='readonly')
        tipo_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        tipo_combo.bind('<<ComboboxSelected>>', self.cargar_categorias)

        # Lista de categorías
        ttk.Label(frame, text="Categorías:").grid(row=1, column=0, sticky=tk.NW, pady=5)

        list_frame = ttk.Frame(frame)
        list_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

        self.lista = tk.Listbox(list_frame, height=10)
        self.lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.lista.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.lista.configure(yscrollcommand=scrollbar.set)

        # Botones
        frame_botones = ttk.Frame(frame)
        frame_botones.grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Button(frame_botones, text="➕ Agregar",
                  command=self.agregar_categoria).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="✏️ Editar",
                  command=self.editar_categoria).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="🗑️ Eliminar",
                  command=self.eliminar_categoria).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botones, text="🔄 Restaurar por defecto",
                  command=self.restaurar_defecto).pack(side=tk.LEFT, padx=5)

        # Configurar expansión
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(1, weight=1)

    def cargar_categorias(self, event=None):
        """Carga las categorías del tipo seleccionado"""
        self.lista.delete(0, tk.END)
        tipo = self.tipo_var.get()
        if tipo:
            categorias = self.gestor_datos.gestor_categorias.obtener_categorias(tipo)
            for cat in categorias:
                self.lista.insert(tk.END, cat)

    def agregar_categoria(self):
        """Agrega una nueva categoría"""
        tipo = self.tipo_var.get()
        if not tipo:
            messagebox.showwarning("Advertencia", "Selecciona un tipo")
            return

        nombre = tk.simpledialog.askstring("Nueva Categoría",
                                          f"Nombre de la nueva categoría de {tipo}:")
        if nombre:
            if self.gestor_datos.gestor_categorias.agregar_categoria(tipo, nombre):
                self.gestor_datos.categorias = self.gestor_datos.gestor_categorias.obtener_categorias()
                self.cargar_categorias()
                messagebox.showinfo("Éxito", "Categoría agregada")
            else:
                messagebox.showerror("Error", "No se pudo agregar la categoría")

    def editar_categoria(self):
        """Edita la categoría seleccionada"""
        tipo = self.tipo_var.get()
        if not tipo:
            messagebox.showwarning("Advertencia", "Selecciona un tipo")
            return

        seleccion = self.lista.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una categoría")
            return

        categoria_actual = self.lista.get(seleccion[0])
        nuevo_nombre = tk.simpledialog.askstring("Editar Categoría",
                                                 "Nuevo nombre:",
                                                 initialvalue=categoria_actual)
        if nuevo_nombre:
            if self.gestor_datos.gestor_categorias.editar_categoria(tipo, categoria_actual, nuevo_nombre):
                self.gestor_datos.categorias = self.gestor_datos.gestor_categorias.obtener_categorias()
                self.cargar_categorias()
                messagebox.showinfo("Éxito", "Categoría editada")
            else:
                messagebox.showerror("Error", "No se pudo editar la categoría")

    def eliminar_categoria(self):
        """Elimina la categoría seleccionada"""
        tipo = self.tipo_var.get()
        if not tipo:
            messagebox.showwarning("Advertencia", "Selecciona un tipo")
            return

        seleccion = self.lista.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una categoría")
            return

        categoria = self.lista.get(seleccion[0])
        if messagebox.askyesno("Confirmar", f"¿Eliminar la categoría '{categoria}'?"):
            if self.gestor_datos.gestor_categorias.eliminar_categoria(tipo, categoria):
                self.gestor_datos.categorias = self.gestor_datos.gestor_categorias.obtener_categorias()
                self.cargar_categorias()
                messagebox.showinfo("Éxito", "Categoría eliminada")
            else:
                messagebox.showerror("Error", "No se pudo eliminar la categoría")

    def restaurar_defecto(self):
        """Restaura las categorías por defecto"""
        if messagebox.askyesno("Confirmar", "¿Restaurar categorías por defecto?\nEsto eliminará las categorías personalizadas."):
            self.gestor_datos.gestor_categorias.restaurar_defecto()
            self.gestor_datos.categorias = self.gestor_datos.gestor_categorias.obtener_categorias()
            self.cargar_categorias()
            messagebox.showinfo("Éxito", "Categorías restauradas")


# Importar para usar en VentanaCategorias
import tkinter.simpledialog