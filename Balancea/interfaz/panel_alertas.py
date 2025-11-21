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
        # Título
        titulo = ttk.Label(self, text="🔔 Centro de Alertas y Notificaciones",
                          font=('Arial', 16, 'bold'))
        titulo.grid(row=0, column=0, columnspan=2, pady=20)

        # Botón actualizar
        btn_actualizar = ttk.Button(self, text="🔄 Actualizar Alertas",
                                    command=self.actualizar_alertas)
        btn_actualizar.grid(row=0, column=2, padx=10, pady=20, sticky=tk.E)

        # === SALUD FINANCIERA ===
        frame_salud = ttk.LabelFrame(self, text="💚 Salud Financiera", padding="20")
        frame_salud.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), padx=20, pady=10)

        # Barra de progreso
        self.lbl_salud_titulo = ttk.Label(frame_salud,
                                         text="Calculando...",
                                         font=('Arial', 14, 'bold'))
        self.lbl_salud_titulo.pack(pady=10)

        self.progress_salud = ttk.Progressbar(frame_salud, length=400, mode='determinate')
        self.progress_salud.pack(pady=10)

        self.lbl_salud_desc = ttk.Label(frame_salud,
                                       text="",
                                       font=('Arial', 11))
        self.lbl_salud_desc.pack(pady=5)

        # === ALERTAS ===
        frame_alertas = ttk.LabelFrame(self, text="⚠️ Alertas Activas", padding="10")
        frame_alertas.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S),
                          padx=20, pady=10)

        # Canvas con scroll para alertas
        canvas = tk.Canvas(frame_alertas, bg='#ECF0F1', highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_alertas, orient="vertical", command=canvas.yview)
        self.frame_alertas_contenido = ttk.Frame(canvas)

        self.frame_alertas_contenido.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.frame_alertas_contenido, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Configurar expansión
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(2, weight=1)

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
            for alerta in alertas:
                self.crear_tarjeta_alerta(alerta)

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
        frame = ttk.Frame(self.frame_alertas_contenido)
        frame.pack(fill=tk.BOTH, expand=True, pady=50)

        label = ttk.Label(frame,
                         text="✅ ¡Todo en orden!\n\nNo hay alertas en este momento.\nTus finanzas están bajo control.",
                         font=('Arial', 12),
                         justify=tk.CENTER)
        label.pack()

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
                              wraplength=700,
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