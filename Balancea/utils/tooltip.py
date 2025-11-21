"""
Sistema de Tooltips
Muestra ayuda contextual al pasar el mouse
"""

import tkinter as tk


class Tooltip:
    """Crea tooltips para widgets"""

    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None

        # Bind events
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        """Muestra el tooltip"""
        if self.tooltip_window or not self.text:
            return

        # Calcular posición
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5

        # Crear ventana
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")

        # Crear label con el texto
        label = tk.Label(
            self.tooltip_window,
            text=self.text,
            background="#FFFFCC",
            foreground="#000000",
            relief=tk.SOLID,
            borderwidth=1,
            font=("Arial", 9),
            padx=5,
            pady=3
        )
        label.pack()

    def hide_tooltip(self, event=None):
        """Oculta el tooltip"""
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


def crear_tooltip(widget, texto):
    """Función helper para crear tooltips fácilmente"""
    return Tooltip(widget, texto)