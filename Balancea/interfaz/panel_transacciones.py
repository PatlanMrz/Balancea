"""
Panel de Transacciones
Permite agregar, editar y eliminar transacciones con búsqueda y filtros
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from tkcalendar import DateEntry


class PanelTransacciones(ttk.Frame):
    """Panel para gestionar transacciones"""

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
        filtro_tipo.bind('<<ComboboxSelected>>', lambda e: self.aplicar_filtros())

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

        # Descripción
        ttk.Label(frame_formulario, text="Descripción:").grid(row=0, column=2, sticky=tk.W, pady=5)
        self.descripcion_entry = ttk.Entry(frame_formulario, width=30)
        self.descripcion_entry.grid(row=0, column=3, sticky=(tk.W, tk.E), padx=5, pady=5)

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
        frame_lista = ttk.LabelFrame(self, text="Historial de Transacciones", padding="10")
        frame_lista.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

        # Configurar grid para expandir
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        frame_lista.columnconfigure(0, weight=1)
        frame_lista.rowconfigure(0, weight=1)

        # Crear Treeview
        columnas = ('Fecha', 'Descripción', 'Monto', 'Tipo', 'Categoría')
        self.tree = ttk.Treeview(frame_lista, columns=columnas, show='headings', height=12)

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
        scrollbar = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Bind para selección
        self.tree.bind('<<TreeviewSelect>>', self.seleccionar_transaccion)

        # Actualizar categorías en filtro
        self.actualizar_filtro_categorias()

    def actualizar_categorias(self, event=None):
        """Actualiza las categorías según el tipo seleccionado"""
        tipo = self.tipo_var.get()
        if tipo:
            categorias = self.gestor_datos.categorias.get(tipo, [])
            self.categoria_combo['values'] = categorias
            if categorias:
                self.categoria_combo.current(0)

    def actualizar_filtro_categorias(self):
        """Actualiza el combo de filtro de categorías"""
        todas_categorias = []
        for categorias in self.gestor_datos.categorias.values():
            todas_categorias.extend(categorias)
        self.filtro_categoria_combo['values'] = ['Todas'] + todas_categorias

    def aplicar_filtros(self, *args):
        """Aplica los filtros de búsqueda"""
        termino = self.busqueda_var.get().lower()
        tipo_filtro = self.filtro_tipo_var.get()
        categoria_filtro = self.filtro_categoria_var.get()

        # Limpiar árbol
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Obtener transacciones filtradas
        transacciones = self.gestor_datos.transacciones.copy()

        # Filtrar por búsqueda
        if termino:
            transacciones = [t for t in transacciones
                           if termino in t['descripcion'].lower()]

        # Filtrar por tipo
        if tipo_filtro != 'Todos':
            transacciones = [t for t in transacciones if t['tipo'] == tipo_filtro]

        # Filtrar por categoría
        if categoria_filtro != 'Todas':
            transacciones = [t for t in transacciones if t['categoria'] == categoria_filtro]

        # Mostrar resultados
        transacciones = sorted(transacciones, key=lambda x: x['fecha'], reverse=True)
        for t in transacciones:
            monto_formato = f"${t['monto']:,.2f}"
            self.tree.insert('', tk.END, values=(
                t['fecha'],
                t['descripcion'],
                monto_formato,
                t['tipo'],
                t['categoria']
            ))

    def limpiar_filtros(self):
        """Limpia todos los filtros"""
        self.busqueda_var.set('')
        self.filtro_tipo_var.set('Todos')
        self.filtro_categoria_var.set('Todas')
        self.cargar_transacciones()

    def exportar_transacciones(self):
        """Exporta transacciones a CSV"""
        archivo = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Exportar transacciones"
        )

        if archivo:
            if self.gestor_datos.exportar_csv(archivo):
                messagebox.showinfo("Éxito", f"Transacciones exportadas a:\n{archivo}")
            else:
                messagebox.showerror("Error", "No se pudo exportar el archivo")

    def gestionar_categorias(self):
        """Abre ventana para gestionar categorías"""
        VentanaCategorias(self, self.gestor_datos)

    def agregar_transaccion(self):
        """Agrega una nueva transacción"""
        if not self.validar_campos():
            return

        fecha = self.fecha_entry.get_date().strftime('%Y-%m-%d')
        descripcion = self.descripcion_entry.get()
        monto = float(self.monto_entry.get())
        tipo = self.tipo_var.get()
        categoria = self.categoria_var.get()

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
        descripcion = self.descripcion_entry.get()
        monto = float(self.monto_entry.get())
        tipo = self.tipo_var.get()
        categoria = self.categoria_var.get()

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

            for t in self.gestor_datos.transacciones:
                if (t['fecha'] == valores[0] and
                    t['descripcion'] == valores[1] and
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
            self.monto_entry.delete(0, tk.END)
            self.monto_entry.insert(0, str(self.transaccion_seleccionada['monto']))
            self.tipo_var.set(self.transaccion_seleccionada['tipo'])
            self.actualizar_categorias()
            self.categoria_var.set(self.transaccion_seleccionada['categoria'])

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.fecha_entry.set_date(datetime.now())
        self.descripcion_entry.delete(0, tk.END)
        self.monto_entry.delete(0, tk.END)
        self.tipo_var.set('')
        self.categoria_var.set('')
        self.transaccion_seleccionada = None
        self.btn_editar.config(state=tk.DISABLED)
        self.btn_eliminar.config(state=tk.DISABLED)

    def validar_campos(self):
        """Valida que los campos estén completos"""
        if not self.descripcion_entry.get():
            messagebox.showwarning("Advertencia", "Ingresa una descripción")
            return False

        try:
            monto = float(self.monto_entry.get())
            if monto <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Advertencia", "Ingresa un monto válido")
            return False

        if not self.tipo_var.get():
            messagebox.showwarning("Advertencia", "Selecciona un tipo")
            return False

        if not self.categoria_var.get():
            messagebox.showwarning("Advertencia", "Selecciona una categoría")
            return False

        return True

    def cargar_transacciones(self):
        """Carga todas las transacciones en el Treeview"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        transacciones = sorted(self.gestor_datos.transacciones,
                              key=lambda x: x['fecha'], reverse=True)

        for t in transacciones:
            monto_formato = f"${t['monto']:,.2f}"
            self.tree.insert('', tk.END, values=(
                t['fecha'],
                t['descripcion'],
                monto_formato,
                t['tipo'],
                t['categoria']
            ))


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