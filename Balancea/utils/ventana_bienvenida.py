"""
Ventana de Bienvenida
Muestra consejos y estado inicial
"""

import tkinter as tk
from tkinter import ttk


def mostrar_ventana_bienvenida(parent, gestor_datos):
    """Muestra ventana de bienvenida con tips"""

    total_trans = len(gestor_datos.transacciones)

    print(f"DEBUG: Total transacciones: {total_trans}")  # Para debug

    # Mostrar si hay menos de 10 transacciones (cambiado de 5 a 10)
    if total_trans < 10:
        ventana = tk.Toplevel(parent)
        ventana.title("¡Bienvenido a Balancea!")
        ventana.geometry("600x450")

        # Hacer que esté sobre la ventana principal
        ventana.transient(parent)

        # Centrar ventana
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() // 2) - (600 // 2)
        y = (ventana.winfo_screenheight() // 2) - (450 // 2)
        ventana.geometry(f"600x450+{x}+{y}")

        # Frame principal
        frame = ttk.Frame(ventana, padding="30")
        frame.pack(fill=tk.BOTH, expand=True)

        # Título
        titulo = tk.Label(frame,
                         text="💰 ¡Bienvenido a Balancea!",
                         font=('Arial', 20, 'bold'),
                         fg='#3498DB')
        titulo.pack(pady=(0, 20))

        # Subtítulo dinámico
        if total_trans == 0:
            subtitulo_text = "Comienza tu viaje hacia la libertad financiera"
        elif total_trans == 1:
            subtitulo_text = "¡Excelente! Ya tienes tu primera transacción"
        else:
            subtitulo_text = f"Tienes {total_trans} transacciones registradas"

        subtitulo = tk.Label(frame,
                           text=subtitulo_text,
                           font=('Arial', 12))
        subtitulo.pack(pady=(0, 30))

        # Tips
        tips_frame = ttk.LabelFrame(frame, text="🎯 Primeros Pasos", padding="20")
        tips_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        tips = [
            "1️⃣ Agrega tus transacciones en la pestaña 'Transacciones'",
            "2️⃣ Visualiza tus gastos en 'Análisis' con gráficas",
            "3️⃣ Revisa tu 'Dashboard' para ver tu balance",
            "4️⃣ Consulta 'Alertas' para recibir consejos",
            "5️⃣ Usa el 'Asistente IA' para preguntas personalizadas"
        ]

        for tip in tips:
            lbl = tk.Label(tips_frame, text=tip, font=('Arial', 11),
                          anchor=tk.W, justify=tk.LEFT)
            lbl.pack(fill=tk.X, pady=8)

        # Consejo del día
        consejo_frame = ttk.Frame(frame)
        consejo_frame.pack(fill=tk.X, pady=20)

        if total_trans == 0:
            consejo_text = "💡 Consejo: Comienza agregando tus gastos del día de hoy"
        else:
            consejo_text = "💡 Consejo: Registra tus transacciones diariamente\npara obtener análisis más precisos"

        consejo = tk.Label(consejo_frame,
                          text=consejo_text,
                          font=('Arial', 10, 'italic'),
                          fg='#7F8C8D',
                          justify=tk.CENTER)
        consejo.pack()

        # Botones
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)

        btn_empezar = ttk.Button(btn_frame, text="¡Empezar! 🚀",
                                command=ventana.destroy,
                                width=15)
        btn_empezar.pack(side=tk.LEFT, padx=5)

        # Focus en el botón
        btn_empezar.focus_set()

        # Cerrar con Enter o Escape
        ventana.bind('<Return>', lambda e: ventana.destroy())
        ventana.bind('<Escape>', lambda e: ventana.destroy())

        # Traer al frente
        ventana.lift()
        ventana.focus_force()

        print("✓ Ventana de bienvenida mostrada")
    else:
        print(f"ℹ Ventana de bienvenida no mostrada (tienes {total_trans} transacciones)")