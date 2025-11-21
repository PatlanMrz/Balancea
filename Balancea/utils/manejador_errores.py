"""
Ventana de Bienvenida
Muestra consejos y estado inicial
"""

import tkinter as tk
from tkinter import ttk


def mostrar_ventana_bienvenida(parent, gestor_datos):
    """Muestra ventana de bienvenida con tips"""

    total_trans = len(gestor_datos.transacciones)

    # Si hay pocas transacciones, mostrar tips
    if total_trans < 5:
        ventana = tk.Toplevel(parent)
        ventana.title("¡Bienvenido a Balancea!")
        ventana.geometry("600x450")
        ventana.transient(parent)
        ventana.grab_set()

        # Centrar ventana
        ventana.update_idletasks()
        x = (ventana.winfo_screenwidth() // 2) - (600 // 2)
        y = (ventana.winfo_screenheight() // 2) - (450 // 2)
        ventana.geometry(f"+{x}+{y}")

        # Frame principal
        frame = ttk.Frame(ventana, padding="30")
        frame.pack(fill=tk.BOTH, expand=True)

        # Título
        titulo = tk.Label(frame,
                          text="💰 ¡Bienvenido a Balancea!",
                          font=('Arial', 20, 'bold'),
                          fg='#3498DB')
        titulo.pack(pady=(0, 20))

        # Subtítulo
        if total_trans == 0:
            subtitulo = tk.Label(frame,
                                 text="Comienza tu viaje hacia la libertad financiera",
                                 font=('Arial', 12))
            subtitulo.pack(pady=(0, 30))
        else:
            subtitulo = tk.Label(frame,
                                 text=f"Tienes {total_trans} transacción(es) registrada(s)",
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

        consejo = tk.Label(consejo_frame,
                           text="💡 Consejo: Registra tus transacciones diariamente\npara obtener análisis más precisos",
                           font=('Arial', 10, 'italic'),
                           fg='#7F8C8D',
                           justify=tk.CENTER)
        consejo.pack()

        # Botón cerrar
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)

        def cerrar_y_no_mostrar():
            # Aquí podrías guardar una preferencia para no mostrar de nuevo
            ventana.destroy()

        btn_empezar = ttk.Button(btn_frame, text="¡Empezar! 🚀",
                                 command=ventana.destroy)
        btn_empezar.pack(side=tk.LEFT, padx=5)

        btn_no_mostrar = ttk.Button(btn_frame, text="No mostrar de nuevo",
                                    command=cerrar_y_no_mostrar)
        btn_no_mostrar.pack(side=tk.LEFT, padx=5)