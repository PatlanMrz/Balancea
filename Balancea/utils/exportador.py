"""
Exportador de Reportes
Genera reportes en PDF y Excel
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from datetime import datetime
import matplotlib.pyplot as plt
from io import BytesIO
import pandas as pd


class Exportador:
    """Clase para exportar reportes en diferentes formatos"""

    def __init__(self, gestor_datos):
        self.gestor_datos = gestor_datos
        self.styles = getSampleStyleSheet()

    def generar_reporte_pdf(self, archivo_destino, incluir_graficas=True):
        """Genera un reporte completo en PDF"""
        try:
            # Crear documento
            doc = SimpleDocTemplate(archivo_destino, pagesize=letter,
                                    rightMargin=72, leftMargin=72,
                                    topMargin=72, bottomMargin=18)

            # Contenedor de elementos
            elementos = []

            # Agregar encabezado
            elementos.extend(self._crear_encabezado())

            # Agregar resumen financiero
            elementos.extend(self._crear_resumen_financiero())

            # Agregar tabla de transacciones recientes
            elementos.extend(self._crear_tabla_transacciones())

            # Agregar gráficas si se solicita
            if incluir_graficas and len(self.gestor_datos.transacciones) > 0:
                elementos.append(PageBreak())
                elementos.extend(self._crear_seccion_graficas())

            # Agregar top gastos
            elementos.extend(self._crear_top_gastos())

            # Agregar pie de página
            elementos.extend(self._crear_pie_pagina())

            # Construir PDF
            doc.build(elementos)
            return True

        except Exception as e:
            print(f"Error al generar PDF: {e}")
            return False

    def _crear_encabezado(self):
        """Crea el encabezado del reporte"""
        elementos = []

        # Título
        titulo_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#3498DB'),
            spaceAfter=30,
            alignment=TA_CENTER
        )

        elementos.append(Paragraph("💰 BALANCEA", titulo_style))
        elementos.append(Paragraph("Reporte Financiero", self.styles['Heading2']))

        # Fecha del reporte
        fecha_style = ParagraphStyle(
            'FechaStyle',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.grey,
            alignment=TA_RIGHT
        )
        fecha_actual = datetime.now().strftime('%d/%m/%Y %H:%M')
        elementos.append(Paragraph(f"Generado: {fecha_actual}", fecha_style))
        elementos.append(Spacer(1, 20))

        return elementos

    def _crear_resumen_financiero(self):
        """Crea la sección de resumen financiero"""
        elementos = []

        # Título de sección
        elementos.append(Paragraph("📊 Resumen Financiero", self.styles['Heading2']))
        elementos.append(Spacer(1, 12))

        # Obtener datos
        balance = self.gestor_datos.obtener_balance()
        ingresos = self.gestor_datos.obtener_total_ingresos()
        gastos = self.gestor_datos.obtener_total_gastos()
        tasa_ahorro = (balance / ingresos * 100) if ingresos > 0 else 0

        # Crear tabla de resumen
        datos_resumen = [
            ['Concepto', 'Monto'],
            ['Total Ingresos', f'${ingresos:,.2f}'],
            ['Total Gastos', f'${gastos:,.2f}'],
            ['Balance', f'${balance:,.2f}'],
            ['Tasa de Ahorro', f'{tasa_ahorro:.1f}%'],
            ['Total Transacciones', str(len(self.gestor_datos.transacciones))]
        ]

        tabla = Table(datos_resumen, colWidths=[3 * inch, 2 * inch])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 3), (-1, 3), 'Helvetica-Bold'),
            ('TEXTCOLOR', (1, 3), (1, 3),
             colors.green if balance >= 0 else colors.red),
        ]))

        elementos.append(tabla)
        elementos.append(Spacer(1, 20))

        return elementos

    def _crear_tabla_transacciones(self):
        """Crea tabla con las últimas transacciones"""
        elementos = []

        elementos.append(Paragraph("💳 Últimas 10 Transacciones", self.styles['Heading2']))
        elementos.append(Spacer(1, 12))

        # Obtener últimas 10 transacciones
        trans = sorted(self.gestor_datos.transacciones,
                       key=lambda x: x['fecha'], reverse=True)[:10]

        if not trans:
            elementos.append(Paragraph("No hay transacciones registradas", self.styles['Normal']))
            return elementos

        # Crear tabla
        datos_tabla = [['Fecha', 'Descripción', 'Tipo', 'Monto']]

        for t in trans:
            datos_tabla.append([
                t['fecha'],
                t['descripcion'][:30] + '...' if len(t['descripcion']) > 30 else t['descripcion'],
                t['tipo'],
                f"${t['monto']:,.2f}"
            ])

        tabla = Table(datos_tabla, colWidths=[1 * inch, 2.5 * inch, 1 * inch, 1.2 * inch])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (3, 0), (3, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
        ]))

        elementos.append(tabla)
        elementos.append(Spacer(1, 20))

        return elementos

    def _crear_seccion_graficas(self):
        """Crea sección con gráficas"""
        elementos = []

        elementos.append(Paragraph("📈 Análisis Visual", self.styles['Heading2']))
        elementos.append(Spacer(1, 12))

        # Gráfica de gastos por categoría
        img_gastos = self._generar_grafica_gastos_categoria()
        if img_gastos:
            elementos.append(img_gastos)
            elementos.append(Spacer(1, 12))

        return elementos

    def _generar_grafica_gastos_categoria(self):
        """Genera gráfica de pastel de gastos por categoría"""
        gastos_cat = self.gestor_datos.obtener_gastos_por_categoria()

        if not gastos_cat:
            return None

        # Crear gráfica
        fig, ax = plt.subplots(figsize=(6, 4))

        categorias = list(gastos_cat.keys())
        valores = list(gastos_cat.values())

        colores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8',
                   '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B739', '#52B788']

        ax.pie(valores, labels=categorias, autopct='%1.1f%%',
               colors=colores[:len(categorias)], startangle=90)
        ax.set_title('Distribución de Gastos por Categoría', fontweight='bold')

        # Guardar en buffer
        buffer = BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        plt.close()

        # Crear imagen para el PDF
        img = Image(buffer, width=5 * inch, height=3.5 * inch)
        return img

    def _crear_top_gastos(self):
        """Crea sección de top gastos"""
        elementos = []

        elementos.append(Paragraph("💰 Top 5 Gastos Más Grandes", self.styles['Heading2']))
        elementos.append(Spacer(1, 12))

        gastos = [t for t in self.gestor_datos.transacciones if t['tipo'] == 'Gasto']
        top_gastos = sorted(gastos, key=lambda x: x['monto'], reverse=True)[:5]

        if not top_gastos:
            elementos.append(Paragraph("No hay gastos registrados", self.styles['Normal']))
            return elementos

        datos_tabla = [['#', 'Descripción', 'Categoría', 'Fecha', 'Monto']]

        for i, gasto in enumerate(top_gastos, 1):
            datos_tabla.append([
                str(i),
                gasto['descripcion'][:25] + '...' if len(gasto['descripcion']) > 25 else gasto['descripcion'],
                gasto['categoria'],
                gasto['fecha'],
                f"${gasto['monto']:,.2f}"
            ])

        tabla = Table(datos_tabla, colWidths=[0.4 * inch, 2 * inch, 1.2 * inch, 1 * inch, 1.1 * inch])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E74C3C')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (0, 0), (0, -1), 'CENTER'),
            ('ALIGN', (4, 0), (4, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
        ]))

        elementos.append(tabla)
        elementos.append(Spacer(1, 20))

        return elementos

    def _crear_pie_pagina(self):
        """Crea pie de página del reporte"""
        elementos = []

        elementos.append(Spacer(1, 30))

        pie_style = ParagraphStyle(
            'PieStyle',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_CENTER
        )

        elementos.append(Paragraph("─────────────────────────────", pie_style))
        elementos.append(Paragraph("Generado por Balancea - Gestor de Finanzas Personales", pie_style))
        elementos.append(Paragraph(f"© {datetime.now().year} - Reporte confidencial", pie_style))

        return elementos

    def exportar_excel(self, archivo_destino):
        """Exporta transacciones a Excel"""
        try:
            df = self.gestor_datos.obtener_dataframe()

            if df.empty:
                return False

            # Crear escritor de Excel
            with pd.ExcelWriter(archivo_destino, engine='openpyxl') as writer:
                # Hoja de transacciones
                df.to_excel(writer, sheet_name='Transacciones', index=False)

                # Hoja de resumen
                resumen_data = {
                    'Concepto': ['Total Ingresos', 'Total Gastos', 'Balance', 'Total Transacciones'],
                    'Valor': [
                        self.gestor_datos.obtener_total_ingresos(),
                        self.gestor_datos.obtener_total_gastos(),
                        self.gestor_datos.obtener_balance(),
                        len(self.gestor_datos.transacciones)
                    ]
                }
                df_resumen = pd.DataFrame(resumen_data)
                df_resumen.to_excel(writer, sheet_name='Resumen', index=False)

                # Hoja de gastos por categoría
                gastos_cat = self.gestor_datos.obtener_gastos_por_categoria()
                if gastos_cat:
                    df_categorias = pd.DataFrame(list(gastos_cat.items()),
                                                 columns=['Categoría', 'Monto'])
                    df_categorias = df_categorias.sort_values('Monto', ascending=False)
                    df_categorias.to_excel(writer, sheet_name='Por Categoría', index=False)

            return True

        except Exception as e:
            print(f"Error al exportar a Excel: {e}")
            return False