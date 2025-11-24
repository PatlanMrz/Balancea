"""
Panel de Alertas
Muestra notificaciones y alertas inteligentes
"""

import tkinter as tk
from tkinter import ttk
from procesador.analizador import AnalizadorFinanciero
from datos.gestor_presupuestos import GestorPresupuestos


class PanelAlertas(ttk.Frame):
    """Panel de alertas y notificaciones"""

    def __init__(self, parent, gestor_datos):
        super().__init__(parent)
        self.gestor_datos = gestor_datos
        self.analizador = AnalizadorFinanciero(gestor_datos)

        self.crear_interfaz()
        self.actualizar_alertas()

    def crear_interfaz(self):
        """Crea la interfaz del panel"""
        # Configurar expansión principal
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)  # La fila de alertas se expande

        # Título
        titulo = ttk.Label(self, text="🔔 Centro de Alertas y Notificaciones",
                        font=('Arial', 16, 'bold'))
        titulo.grid(row=0, column=0, columnspan=2, pady=20, sticky=tk.W)

        # Botón actualizar
        btn_actualizar = ttk.Button(self, text="🔄 Actualizar Alertas",
                                    command=self.actualizar_alertas)
        btn_actualizar.grid(row=0, column=1, padx=10, pady=20, sticky=tk.E)

        # === SALUD FINANCIERA ===
        frame_salud = ttk.LabelFrame(self, text="💚 Salud Financiera", padding="20")
        frame_salud.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=20, pady=10)

        # Barra de progreso
        self.lbl_salud_titulo = ttk.Label(frame_salud,
                                        text="Calculando...",
                                        font=('Arial', 14, 'bold'))
        self.lbl_salud_titulo.pack(pady=10)

        self.progress_salud = ttk.Progressbar(frame_salud, length=400, mode='determinate')
        self.progress_salud.pack(pady=10, fill=tk.X, padx=20)

        self.lbl_salud_desc = ttk.Label(frame_salud,
                                    text="",
                                    font=('Arial', 11))
        self.lbl_salud_desc.pack(pady=5)

        # === ALERTAS ===
        frame_alertas = ttk.LabelFrame(self, text="⚠️ Alertas Activas", padding="10")
        frame_alertas.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S),
                        padx=20, pady=10)
        
        # Configurar expansión del frame de alertas
        frame_alertas.columnconfigure(0, weight=1)
        frame_alertas.rowconfigure(0, weight=1)

        # Canvas con scroll para alertas
        self.canvas_alertas = tk.Canvas(frame_alertas, bg='#ECF0F1', highlightthickness=0)
        self.scrollbar_alertas = ttk.Scrollbar(frame_alertas, orient="vertical", command=self.canvas_alertas.yview)
        self.frame_alertas_contenido = ttk.Frame(self.canvas_alertas)

        self.frame_alertas_contenido.bind(
            "<Configure>",
            lambda e: self.canvas_alertas.configure(scrollregion=self.canvas_alertas.bbox("all"))
        )

        self.canvas_window = self.canvas_alertas.create_window((0, 0), window=self.frame_alertas_contenido, anchor="nw")
        self.canvas_alertas.configure(yscrollcommand=self.scrollbar_alertas.set)
        
        # Ajustar ancho del frame interno al canvas
        self.canvas_alertas.bind('<Configure>', 
                                lambda e: self.canvas_alertas.itemconfigure(self.canvas_window, width=e.width))

        self.canvas_alertas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.scrollbar_alertas.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Frame para estado vacío (inicialmente oculto)
        self.empty_state_frame = ttk.Frame(frame_alertas)
        
        # Scroll con rueda del ratón
        def _on_mousewheel_alertas(event):
            delta = 0
            if hasattr(event, 'delta') and event.delta != 0:
                delta = int(-1 * (event.delta / 120))
            elif getattr(event, 'num', None) == 4:
                delta = -3
            elif getattr(event, 'num', None) == 5:
                delta = 3
            if delta == 0 or not getattr(self, '_can_scroll_alertas', False):
                return
            first, last = self.canvas_alertas.yview()
            if delta < 0 and first <= 0.0:
                return
            if delta > 0 and last >= 1.0:
                return
            self.canvas_alertas.yview_scroll(delta, "units")

        self.canvas_alertas.bind('<Enter>', lambda e: (
            self.canvas_alertas.bind_all("<MouseWheel>", _on_mousewheel_alertas),
            self.canvas_alertas.bind_all("<Button-4>", _on_mousewheel_alertas),
            self.canvas_alertas.bind_all("<Button-5>", _on_mousewheel_alertas)
        ))
        self.canvas_alertas.bind('<Leave>', lambda e: (
            self.canvas_alertas.unbind_all("<MouseWheel>"),
            self.canvas_alertas.unbind_all("<Button-4>"),
            self.canvas_alertas.unbind_all("<Button-5>")
        ))

        self._can_scroll_alertas = False

    def actualizar_alertas(self):
        """Actualiza todas las alertas"""
        # Actualizar salud financiera
        self.actualizar_salud_financiera()

        # Limpiar alertas anteriores
        for widget in self.frame_alertas_contenido.winfo_children():
            widget.destroy()

        # Obtener nuevas alertas
        alertas = self.analizador.analizar_todo()

        if not alertas:
            self.mostrar_sin_alertas()
        else:
            # Ocultar estado vacío y mostrar canvas
            try:
                self.empty_state_frame.grid_remove()
            except Exception:
                pass
            
            self.canvas_alertas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
            self.scrollbar_alertas.grid(row=0, column=1, sticky=(tk.N, tk.S))

            for alerta in alertas:
                self.crear_tarjeta_alerta(alerta)

            self._update_scroll_state_alertas()

    def actualizar_salud_financiera(self):
        """Actualiza el indicador de salud financiera"""
        salud = self.analizador.obtener_resumen_salud_financiera()

        self.lbl_salud_titulo.config(
            text=f"Salud Financiera: {salud['nivel']} ({salud['puntuacion']}/100)",
            foreground=salud['color']
        )

        self.progress_salud['value'] = salud['puntuacion']

        if salud['puntuacion'] > 0:
            self.lbl_salud_desc.config(
                text=f"Tasa de ahorro: {salud['tasa_ahorro']:.1f}% | "
                    f"Continúa mejorando tus finanzas"
            )
        else:
            self.lbl_salud_desc.config(text="Agrega transacciones para calcular tu salud financiera")

    def mostrar_sin_alertas(self):
        """Muestra mensaje cuando no hay alertas"""
            # Ocultar canvas y scrollbar
        try:
            self.canvas_alertas.grid_remove()
            self.scrollbar_alertas.grid_remove()
        except Exception:
            pass

        # Limpiar estado vacío
        for widget in self.empty_state_frame.winfo_children():
            widget.destroy()

        # Configurar el frame vacío para que ocupe todo el espacio
        self.empty_state_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Frame interno centrado
        frame_centro = ttk.Frame(self.empty_state_frame)
        frame_centro.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        ttk.Label(frame_centro, text="✅", font=('Arial', 48)).pack(pady=10)
        ttk.Label(frame_centro,
                text="¡Todo en orden!",
                font=('Arial', 14, 'bold')).pack(pady=5)
        ttk.Label(frame_centro,
                text="No hay alertas en este momento.\nTus finanzas están bajo control.",
                font=('Arial', 10),
                justify=tk.CENTER).pack(pady=5)

    def _update_scroll_state_alertas(self):
        """Actualiza el estado del scroll para alertas"""
        try:
            self.canvas_alertas.update_idletasks()
            bbox = self.canvas_alertas.bbox('all')
            if bbox:
                self.canvas_alertas.configure(scrollregion=bbox)
                content_h = bbox[3] - bbox[1]
            else:
                self.canvas_alertas.configure(scrollregion=(0, 0, 0, 0))
                content_h = 0
            
            view_h = self.canvas_alertas.winfo_height()
            self._can_scroll_alertas = content_h > view_h + 1
            
            if self._can_scroll_alertas:
                self.scrollbar_alertas.state(['!disabled'])
            else:
                self.scrollbar_alertas.state(['disabled'])
                self.canvas_alertas.yview_moveto(0.0)
        except Exception:
            pass

    def crear_tarjeta_alerta(self, alerta):
        """Crea una tarjeta visual para una alerta"""
        # Determinar color según tipo
        colores = {
            'peligro': '#E74C3C',
            'advertencia': '#F39C12',
            'info': '#3498DB',
            'exito': '#27AE60',
            'consejo': '#9B59B6'
        }

        color = colores.get(alerta['tipo'], '#95A5A6')

        # Frame de la tarjeta
        frame = tk.Frame(self.frame_alertas_contenido,
                        bg=color,
                        relief=tk.RAISED,
                        borderwidth=2)
        frame.pack(fill=tk.X, padx=10, pady=8)

        # Contenido interno con padding
        frame_interno = tk.Frame(frame, bg='white', padx=15, pady=12)
        frame_interno.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Título
        lbl_titulo = tk.Label(frame_interno,
                            text=alerta['titulo'],
                            font=('Arial', 12, 'bold'),
                            bg='white',
                            fg=color,
                            anchor=tk.W)
        lbl_titulo.pack(fill=tk.X)

        # Mensaje
        lbl_mensaje = tk.Label(frame_interno,
                            text=alerta['mensaje'],
                            font=('Arial', 10),
                            bg='white',
                            fg='#2C3E50',
                            anchor=tk.W,
                            wraplength=700,  # Se ajustará al ancho real
                            justify=tk.LEFT)
        lbl_mensaje.pack(fill=tk.X, pady=(5, 0))

        # Badge de severidad
        if alerta['severidad'] == 'alta':
            badge_text = "🔴 Prioridad Alta"
        elif alerta['severidad'] == 'media':
            badge_text = "🟡 Atención Requerida"
        else:
            badge_text = "🟢 Informativo"

        lbl_badge = tk.Label(frame_interno,
                            text=badge_text,
                            font=('Arial', 8),
                            bg='white',
                            fg='#7F8C8D')
        lbl_badge.pack(anchor=tk.W, pady=(5, 0))
        
        # Actualizar scroll después de agregar
        self.after(100, self._update_scroll_state_alertas)