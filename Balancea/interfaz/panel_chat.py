# ===== interfaz/panel_chat.py =====
"""
Panel de Chat Financiero MEJORADO
Interacción con IA (Ollama) con contexto avanzado
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
from procesador.chat_financiero import ChatFinanciero


class PanelChat(ttk.Frame):
    """Panel de chat con asistente IA mejorado"""

    def __init__(self, parent, gestor_datos):
        super().__init__(parent)
        self.gestor_datos = gestor_datos
        self.chat = ChatFinanciero(gestor_datos)

        self.crear_interfaz()
        self.verificar_ollama()

    def crear_interfaz(self):
        """Crea la interfaz del chat"""
        # Frame superior con título y estado
        frame_header = ttk.Frame(self)
        frame_header.pack(fill=tk.X, padx=10, pady=10)

        # Título
        titulo = ttk.Label(frame_header, text="💬 Asistente Financiero IA",
                           font=('Arial', 16, 'bold'))
        titulo.pack(side=tk.LEFT)

        # Botones de header
        btn_comandos = ttk.Button(frame_header, text="📋 Comandos",
                                  command=self.mostrar_comandos)
        btn_comandos.pack(side=tk.RIGHT, padx=5)

        btn_verificar = ttk.Button(frame_header, text="🔄 Verificar",
                                   command=self.verificar_ollama)
        btn_verificar.pack(side=tk.RIGHT, padx=5)

        # Estado de Ollama
        frame_estado = ttk.Frame(self)
        frame_estado.pack(fill=tk.X, padx=10, pady=(0, 5))

        self.lbl_estado = ttk.Label(frame_estado,
                                    text="🔴 Verificando Ollama...",
                                    font=('Arial', 10))
        self.lbl_estado.pack(side=tk.LEFT)

        # Área de chat
        frame_chat = ttk.LabelFrame(self, text="Conversación", padding="10")
        frame_chat.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # ScrolledText para el historial
        self.text_chat = scrolledtext.ScrolledText(
            frame_chat,
            wrap=tk.WORD,
            width=80,
            height=18,
            font=('Arial', 10),
            state=tk.DISABLED
        )
        self.text_chat.pack(fill=tk.BOTH, expand=True)

        # Configurar tags para colores
        self.text_chat.tag_config('usuario', foreground='#2C3E50', font=('Arial', 10, 'bold'))
        self.text_chat.tag_config('asistente', foreground='#27AE60')
        self.text_chat.tag_config('comando', foreground='#3498DB', font=('Arial', 10, 'bold'))
        self.text_chat.tag_config('sistema', foreground='#95A5A6', font=('Arial', 9, 'italic'))
        self.text_chat.tag_config('error', foreground='#E74C3C', font=('Arial', 9, 'italic'))

        # Frame de entrada
        frame_entrada = ttk.Frame(self)
        frame_entrada.pack(fill=tk.X, padx=10, pady=10)

        # Entry de mensaje
        self.entry_mensaje = ttk.Entry(frame_entrada, font=('Arial', 11))
        self.entry_mensaje.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.entry_mensaje.bind('<Return>', lambda e: self.enviar_mensaje())
        self.entry_mensaje.focus()

        # Botón enviar
        self.btn_enviar = ttk.Button(frame_entrada, text="📤 Enviar",
                                     command=self.enviar_mensaje)
        self.btn_enviar.pack(side=tk.LEFT, padx=5)

        # Botón limpiar
        btn_limpiar = ttk.Button(frame_entrada, text="🗑️ Limpiar",
                                 command=self.limpiar_chat)
        btn_limpiar.pack(side=tk.LEFT)

        # Sugerencias rápidas con comandos especiales
        frame_sugerencias = ttk.LabelFrame(self, text="💡 Acciones Rápidas", padding="10")
        frame_sugerencias.pack(fill=tk.X, padx=10, pady=5)

        sugerencias = [
            ("📊 Análisis Completo", "/analisis"),
            ("🔔 Ver Alertas", "/alertas"),
            ("💡 Dame Consejos", "/consejos"),
            ("📋 Resumen Rápido", "/resumen"),
            ("💰 ¿Cuál es mi balance?", "¿Cuál es mi balance actual?"),
            ("📈 ¿Cómo van mis finanzas?", "¿Cómo van mis finanzas este mes?")
        ]

        for i, (texto, comando) in enumerate(sugerencias):
            btn = ttk.Button(frame_sugerencias, text=texto,
                             command=lambda c=comando: self.enviar_comando(c))
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5, sticky=(tk.W, tk.E))

        for i in range(3):
            frame_sugerencias.columnconfigure(i, weight=1)

        # Mensaje de bienvenida
        self.agregar_mensaje_sistema("¡Hola! Soy tu asistente financiero mejorado. 🤖")
        self.agregar_mensaje_sistema("Puedo ayudarte con análisis detallados, alertas y consejos personalizados.")
        self.agregar_mensaje_sistema(
            "💡 Tip: Usa los botones de Acciones Rápidas o escribe '/comandos' para ver todos los comandos disponibles.")

    def verificar_ollama(self):
        """Verifica si Ollama está disponible"""

        def verificar():
            try:
                import requests
                response = requests.get("http://localhost:11434/api/tags", timeout=2)
                if response.status_code == 200:
                    self.lbl_estado.config(
                        text=f"🟢 Ollama conectado - Modelo: {self.chat.modelo}",
                        foreground='#27AE60'
                    )
                    self.btn_enviar.config(state=tk.NORMAL)
                else:
                    raise Exception()
            except Exception:
                self.lbl_estado.config(
                    text="🔴 Ollama no disponible - Ejecuta 'ollama serve' en terminal",
                    foreground='#E74C3C'
                )
                self.btn_enviar.config(state=tk.DISABLED)

        thread = threading.Thread(target=verificar)
        thread.daemon = True
        thread.start()

    def mostrar_comandos(self):
        """Muestra ventana con comandos disponibles"""
        ventana = tk.Toplevel(self)
        ventana.title("Comandos Disponibles")
        ventana.geometry("500x400")
        ventana.transient(self)

        titulo = ttk.Label(ventana, text="📋 Comandos Disponibles",
                           font=('Arial', 14, 'bold'))
        titulo.pack(pady=20)

        frame = ttk.Frame(ventana, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        comandos = self.chat.obtener_comandos_disponibles()

        for i, cmd in enumerate(comandos):
            ttk.Label(frame, text=cmd, font=('Arial', 11)).pack(anchor=tk.W, pady=5)

        ttk.Label(frame, text="\n💡 También puedes hacer preguntas normales como:",
                  font=('Arial', 10, 'italic')).pack(anchor=tk.W, pady=10)

        ejemplos = [
            "• ¿Cuánto gasté este mes?",
            "• ¿En qué categoría gasto más?",
            "• Dame tips para ahorrar",
            "• ¿Cómo está mi salud financiera?"
        ]

        for ej in ejemplos:
            ttk.Label(frame, text=ej, font=('Arial', 9)).pack(anchor=tk.W, pady=2)

        btn_cerrar = ttk.Button(ventana, text="Cerrar", command=ventana.destroy)
        btn_cerrar.pack(pady=10)

    def enviar_comando(self, comando):
        """Envía un comando o pregunta predefinida"""
        self.entry_mensaje.delete(0, tk.END)
        self.entry_mensaje.insert(0, comando)
        self.enviar_mensaje()

    def enviar_mensaje(self):
        """Envía un mensaje al chat"""
        mensaje = self.entry_mensaje.get().strip()
        if not mensaje:
            return

        # Mostrar mensaje del usuario
        self.agregar_mensaje_usuario(mensaje)
        self.entry_mensaje.delete(0, tk.END)

        # Deshabilitar botón mientras procesa
        self.btn_enviar.config(state=tk.DISABLED, text="⏳ Pensando...")

        # Obtener respuesta en hilo separado
        thread = threading.Thread(target=self.procesar_mensaje, args=(mensaje,))
        thread.daemon = True
        thread.start()

    def procesar_mensaje(self, mensaje):
        """Procesa el mensaje y obtiene respuesta"""
        resultado = self.chat.generar_respuesta(mensaje)

        if resultado['exito']:
            if resultado['tipo'] == 'comando':
                self.agregar_mensaje_comando(resultado['respuesta'])
            else:
                self.agregar_mensaje_asistente(resultado['respuesta'])
        else:
            self.agregar_mensaje_error(f"Error: {resultado['error']}")

        # Rehabilitar botón
        self.btn_enviar.config(state=tk.NORMAL, text="📤 Enviar")

    def agregar_mensaje_usuario(self, mensaje):
        """Agrega mensaje del usuario al chat"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M")
        self.text_chat.config(state=tk.NORMAL)
        self.text_chat.insert(tk.END, f"\n[{timestamp}] Tú: ", 'usuario')
        self.text_chat.insert(tk.END, f"{mensaje}\n")
        self.text_chat.config(state=tk.DISABLED)
        self.text_chat.see(tk.END)

    def agregar_mensaje_asistente(self, mensaje):
        """Agrega mensaje del asistente al chat"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M")
        self.text_chat.config(state=tk.NORMAL)
        self.text_chat.insert(tk.END, f"\n[{timestamp}] Asistente: ", 'asistente')
        self.text_chat.insert(tk.END, f"{mensaje}\n")
        self.text_chat.config(state=tk.DISABLED)
        self.text_chat.see(tk.END)

    def agregar_mensaje_comando(self, mensaje):
        """Agrega resultado de comando al chat"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M")
        self.text_chat.config(state=tk.NORMAL)
        self.text_chat.insert(tk.END, f"\n[{timestamp}] 📊 ", 'comando')
        self.text_chat.insert(tk.END, f"{mensaje}\n")
        self.text_chat.config(state=tk.DISABLED)
        self.text_chat.see(tk.END)

    def agregar_mensaje_sistema(self, mensaje):
        """Agrega mensaje del sistema al chat"""
        self.text_chat.config(state=tk.NORMAL)
        self.text_chat.insert(tk.END, f"\n💡 {mensaje}\n", 'sistema')
        self.text_chat.config(state=tk.DISABLED)
        self.text_chat.see(tk.END)

    def agregar_mensaje_error(self, mensaje):
        """Agrega mensaje de error al chat"""
        self.text_chat.config(state=tk.NORMAL)
        self.text_chat.insert(tk.END, f"\n❌ {mensaje}\n", 'error')
        self.text_chat.config(state=tk.DISABLED)
        self.text_chat.see(tk.END)

    def limpiar_chat(self):
        """Limpia el historial del chat"""
        self.text_chat.config(state=tk.NORMAL)
        self.text_chat.delete(1.0, tk.END)
        self.text_chat.config(state=tk.DISABLED)
        self.chat.limpiar_historial()
        self.agregar_mensaje_sistema("Chat limpiado. ¿En qué puedo ayudarte?")

# ===== Los demás archivos permanecen igual =====