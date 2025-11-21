"""
Chat Financiero con IA
Sistema inteligente de conversación con contexto financiero
"""

import requests
import json
from datetime import datetime
from procesador.analizador import AnalizadorFinanciero


class ChatFinanciero:
    """Gestiona la conversación con IA incluyendo contexto financiero"""

    def __init__(self, gestor_datos, modelo="llama3.2:3b-instruct-fp16", url="http://localhost:11434/api/generate"):
        self.gestor_datos = gestor_datos
        self.analizador = AnalizadorFinanciero(gestor_datos)
        self.modelo = modelo
        self.url = url
        self.historial = []

    def obtener_contexto_completo(self):
        """Obtiene contexto financiero detallado para el prompt"""
        balance = self.gestor_datos.obtener_balance()
        ingresos = self.gestor_datos.obtener_total_ingresos()
        gastos = self.gestor_datos.obtener_total_gastos()
        gastos_cat = self.gestor_datos.obtener_gastos_por_categoria()

        # Salud financiera
        salud = self.analizador.obtener_resumen_salud_financiera()

        # Alertas activas
        alertas = self.analizador.analizar_todo()
        alertas_texto = "\n".join([f"- {a['titulo']}: {a['mensaje']}" for a in alertas[:3]])

        contexto = f"""Eres un asistente financiero personal experto y amigable llamado 'Balancea AI'.

DATOS FINANCIEROS DEL USUARIO:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 Balance Total: ${balance:,.2f}
📈 Total Ingresos: ${ingresos:,.2f}
📉 Total Gastos: ${gastos:,.2f}
📊 Tasa de Ahorro: {salud['tasa_ahorro']:.1f}%
💚 Salud Financiera: {salud['nivel']} ({salud['puntuacion']}/100)
📝 Transacciones Registradas: {len(self.gestor_datos.transacciones)}

DISTRIBUCIÓN DE GASTOS POR CATEGORÍA:
"""

        if gastos_cat:
            for cat, monto in sorted(gastos_cat.items(), key=lambda x: x[1], reverse=True):
                porcentaje = (monto / gastos * 100) if gastos > 0 else 0
                contexto += f"\n  • {cat}: ${monto:,.2f} ({porcentaje:.1f}%)"
        else:
            contexto += "\n  (Sin gastos registrados)"

        if alertas:
            contexto += f"\n\n⚠️ ALERTAS ACTIVAS ({len(alertas)}):\n{alertas_texto}"

        contexto += """

INSTRUCCIONES:
- Responde en español de manera clara, concisa y amigable
- Usa los datos proporcionados para dar respuestas específicas
- Si el usuario pregunta sobre su situación financiera, usa los números exactos
- Da consejos prácticos y accionables
- Si no tienes suficiente información, menciona qué datos necesitas
- Mantén las respuestas breves (máximo 3-4 párrafos)
- Usa emojis apropiados para hacer la conversación más amigable
- Si detectas problemas en las finanzas, sé empático pero honesto
"""

        return contexto

    def obtener_contexto_comando(self, comando):
        """Obtiene contexto específico para comandos especiales"""
        if comando == "analisis":
            return self.generar_analisis_completo()
        elif comando == "alertas":
            return self.generar_resumen_alertas()
        elif comando == "consejos":
            return self.generar_consejos_personalizados()
        elif comando == "resumen":
            return self.generar_resumen_financiero()
        return None

    def generar_analisis_completo(self):
        """Genera análisis financiero completo"""
        balance = self.gestor_datos.obtener_balance()
        ingresos = self.gestor_datos.obtener_total_ingresos()
        gastos = self.gestor_datos.obtener_total_gastos()
        salud = self.analizador.obtener_resumen_salud_financiera()

        analisis = f"""📊 ANÁLISIS FINANCIERO COMPLETO

💰 Situación General:
━━━━━━━━━━━━━━━━━━━━
Balance: ${balance:,.2f}
Ingresos: ${ingresos:,.2f}
Gastos: ${gastos:,.2f}
Tasa de Ahorro: {salud['tasa_ahorro']:.1f}%

💚 Salud Financiera: {salud['nivel']} ({salud['puntuacion']}/100 puntos)

"""

        # Agregar interpretación
        if salud['puntuacion'] >= 80:
            analisis += "✨ ¡Excelente trabajo! Tus finanzas están en muy buen estado."
        elif salud['puntuacion'] >= 60:
            analisis += "👍 Vas bien, pero hay áreas de oportunidad para mejorar."
        elif salud['puntuacion'] >= 40:
            analisis += "⚠️ Atención necesaria. Considera revisar tus gastos."
        else:
            analisis += "🚨 Situación crítica. Necesitas hacer cambios importantes."

        return analisis

    def generar_resumen_alertas(self):
        """Genera resumen de alertas"""
        alertas = self.analizador.analizar_todo()

        if not alertas:
            return "✅ ¡Todo en orden! No hay alertas activas en este momento."

        resumen = f"🔔 ALERTAS ACTIVAS ({len(alertas)}):\n\n"

        for i, alerta in enumerate(alertas, 1):
            icono = {
                'peligro': '🔴',
                'advertencia': '🟡',
                'info': '🔵',
                'exito': '🟢',
                'consejo': '💡'
            }.get(alerta['tipo'], '⚪')

            resumen += f"{icono} {alerta['titulo']}\n{alerta['mensaje']}\n\n"

        return resumen

    def generar_consejos_personalizados(self):
        """Genera consejos basados en el análisis"""
        balance = self.gestor_datos.obtener_balance()
        gastos = self.gestor_datos.obtener_total_gastos()
        ingresos = self.gestor_datos.obtener_total_ingresos()
        gastos_cat = self.gestor_datos.obtener_gastos_por_categoria()

        consejos = "💡 CONSEJOS PERSONALIZADOS:\n\n"

        # Consejo sobre balance
        if balance < 0:
            consejos += "1️⃣ URGENTE: Tu balance es negativo. Prioriza reducir gastos inmediatamente.\n\n"
        elif balance < ingresos * 0.1:
            consejos += "1️⃣ Intenta ahorrar al menos el 20% de tus ingresos mensuales.\n\n"

        # Consejo sobre categorías
        if gastos_cat:
            max_cat = max(gastos_cat, key=gastos_cat.get)
            max_monto = gastos_cat[max_cat]
            porcentaje = (max_monto / gastos * 100) if gastos > 0 else 0

            if porcentaje > 35:
                consejos += f"2️⃣ Tu mayor gasto es '{max_cat}' ({porcentaje:.1f}%). Busca formas de optimizar esta categoría.\n\n"

        # Consejo general
        consejos += "3️⃣ Regla 50/30/20: 50% necesidades, 30% gustos, 20% ahorro.\n\n"
        consejos += "4️⃣ Revisa tus gastos semanalmente para mantener el control."

        return consejos

    def generar_resumen_financiero(self):
        """Genera resumen rápido de la situación"""
        balance = self.gestor_datos.obtener_balance()
        ingresos = self.gestor_datos.obtener_total_ingresos()
        gastos = self.gestor_datos.obtener_total_gastos()
        salud = self.analizador.obtener_resumen_salud_financiera()

        return f"""📋 RESUMEN RÁPIDO

Balance: ${balance:,.2f}
Ingresos: ${ingresos:,.2f}
Gastos: ${gastos:,.2f}
Ahorro: {salud['tasa_ahorro']:.1f}%
Salud: {salud['nivel']}

{self._emoji_tendencia(balance)} Tendencia: {'Positiva' if balance > 0 else 'Requiere atención'}"""

    def _emoji_tendencia(self, balance):
        """Retorna emoji según la tendencia"""
        if balance > 0:
            return "📈"
        elif balance < 0:
            return "📉"
        return "➡️"

    def detectar_comando(self, mensaje):
        """Detecta si el mensaje es un comando especial"""
        mensaje_lower = mensaje.lower().strip()

        comandos = {
            '/analisis': 'analisis',
            '/alertas': 'alertas',
            '/consejos': 'consejos',
            '/resumen': 'resumen',
            'análisis completo': 'analisis',
            'muestra alertas': 'alertas',
            'dame consejos': 'consejos',
            'resumen rápido': 'resumen'
        }

        for patron, comando in comandos.items():
            if patron in mensaje_lower:
                return comando

        return None

    def generar_respuesta(self, mensaje_usuario, timeout=30):
        """Genera respuesta usando Ollama"""
        # Detectar comandos especiales
        comando = self.detectar_comando(mensaje_usuario)

        if comando:
            respuesta_comando = self.obtener_contexto_comando(comando)
            if respuesta_comando:
                return {
                    'exito': True,
                    'respuesta': respuesta_comando,
                    'tipo': 'comando'
                }

        # Obtener contexto completo
        contexto = self.obtener_contexto_completo()

        # Construir historial de conversación
        historial_texto = ""
        for msg in self.historial[-4:]:  # Últimos 4 mensajes
            rol = "Usuario" if msg['rol'] == 'usuario' else "Asistente"
            historial_texto += f"{rol}: {msg['mensaje']}\n"

        # Construir prompt completo
        prompt = f"""{contexto}

HISTORIAL RECIENTE:
{historial_texto if historial_texto else "(Nueva conversación)"}

Usuario: {mensaje_usuario}

Asistente (responde de forma útil y específica basándote en los datos):"""

        try:
            # Hacer petición a Ollama
            payload = {
                "model": self.modelo,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 300  # Limitar longitud de respuesta
                }
            }

            response = requests.post(self.url, json=payload, timeout=timeout)

            if response.status_code == 200:
                respuesta = response.json().get('response', '').strip()

                # Guardar en historial
                self.historial.append({'rol': 'usuario', 'mensaje': mensaje_usuario})
                self.historial.append({'rol': 'asistente', 'mensaje': respuesta})

                return {
                    'exito': True,
                    'respuesta': respuesta,
                    'tipo': 'ia'
                }
            else:
                return {
                    'exito': False,
                    'error': f"Error de Ollama (código {response.status_code})",
                    'tipo': 'error'
                }

        except requests.exceptions.Timeout:
            return {
                'exito': False,
                'error': "La solicitud tardó demasiado. Intenta de nuevo.",
                'tipo': 'timeout'
            }
        except Exception as e:
            return {
                'exito': False,
                'error': str(e),
                'tipo': 'error'
            }

    def limpiar_historial(self):
        """Limpia el historial de conversación"""
        self.historial = []

    def obtener_comandos_disponibles(self):
        """Retorna lista de comandos disponibles"""
        return [
            "/analisis - Análisis financiero completo",
            "/alertas - Ver todas las alertas activas",
            "/consejos - Obtener consejos personalizados",
            "/resumen - Resumen rápido de tu situación"
        ]