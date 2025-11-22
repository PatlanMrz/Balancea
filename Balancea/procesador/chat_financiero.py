"""
Chat Financiero con IA
Versión optimizada con mejor manejo de errores
"""

import requests
import json
from datetime import datetime
from procesador.analizador import AnalizadorFinanciero


class ChatFinanciero:
    """Gestiona la conversación con IA incluyendo contexto financiero"""

    def __init__(self, gestor_datos, modelo="llama3.2:1b", url="http://localhost:11434/api/generate"):
        self.gestor_datos = gestor_datos
        self.analizador = AnalizadorFinanciero(gestor_datos)
        self.modelo = modelo
        self.url = url
        self.historial = []
        # ✅ Configuración optimizada
        self.timeout = 60  # Aumentado para modelos pesados
        self.max_tokens = 200  # Reducido para respuestas más rápidas

    def obtener_contexto_completo(self):
        """Obtiene contexto financiero detallado para el prompt"""
        # ✅ Permitir contexto mínimo incluso sin datos
        if not self.gestor_datos.transacciones:
            return """Eres un asistente financiero personal experto y amigable llamado 'Balancea AI'.

SITUACIÓN: El usuario aún no tiene transacciones registradas, pero puedes ayudarlo.

PUEDES HACER:
- Responder preguntas generales sobre finanzas personales
- Dar consejos sobre cómo empezar a gestionar sus finanzas
- Explicar conceptos financieros básicos (ahorro, inversión, presupuesto, etc.)
- Motivar al usuario a comenzar a registrar sus transacciones
- Responder dudas sobre cómo usar la aplicación Balancea
- Dar tips de educación financiera

INSTRUCCIONES:
- Responde en español de manera clara, concisa y amigable
- Da consejos prácticos sobre gestión financiera
- Si te preguntan sobre sus finanzas específicas, menciona que necesitas que registre transacciones primero
- Mantén las respuestas breves (máximo 3-4 párrafos)
- Usa emojis apropiados para hacer la conversación más amigable
- Sé empático y motivador
- Cuando sea relevante, sugiere usar el botón "Generar Demo" para explorar la app
"""

        try:
            balance = self.gestor_datos.obtener_balance()
            ingresos = self.gestor_datos.obtener_total_ingresos()
            gastos = self.gestor_datos.obtener_total_gastos()
            gastos_cat = self.gestor_datos.obtener_gastos_por_categoria()

            # Salud financiera
            salud = self.analizador.obtener_resumen_salud_financiera()

            # Alertas activas
            try:
                alertas = self.analizador.analizar_todo()
                alertas_texto = "\n".join([f"- {a['titulo']}: {a['mensaje']}" for a in alertas[:3]]) if alertas else "No hay alertas"
            except Exception as e:
                print(f"Error al obtener alertas: {e}")
                alertas = []
                alertas_texto = "Error al procesar alertas"

            contexto = f"""Eres un asistente financiero personal experto y amigable llamado 'Balancea AI'.

DATOS FINANCIEROS DEL USUARIO:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 Balance Total: ${balance:,.2f}
📈 Total Ingresos: ${ingresos:,.2f}
📉 Total Gastos: ${gastos:,.2f}
📊 Tasa de Ahorro: {salud.get('tasa_ahorro', 0):.1f}%
💚 Salud Financiera: {salud.get('nivel', 'N/A')} ({salud.get('puntuacion', 0)}/100)
📝 Transacciones Registradas: {len(self.gestor_datos.transacciones)}

DISTRIBUCIÓN DE GASTOS POR CATEGORÍA:
"""

            if gastos_cat:
                for cat, monto in sorted(gastos_cat.items(), key=lambda x: x[1], reverse=True)[:5]:
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

        except Exception as e:
            print(f"❌ Error al obtener contexto: {e}")
            import traceback
            traceback.print_exc()
            return "Eres un asistente financiero llamado Balancea AI. Responde de manera amigable y útil en español."

    def generar_respuesta(self, mensaje_usuario):
        """Genera respuesta usando Ollama - OPTIMIZADO"""
        # Detectar comandos especiales primero
        comando = self.detectar_comando(mensaje_usuario)

        if comando:
            respuesta_comando = self.obtener_contexto_comando(comando)
            if respuesta_comando:
                return {
                    'exito': True,
                    'respuesta': respuesta_comando,
                    'tipo': 'comando'
                }

        # ✅ Ya NO retornamos mensaje predefinido, dejamos que Ollama procese
        # (Comentado para permitir que Ollama responda incluso sin datos)

        # Obtener contexto completo
        try:
            contexto = self.obtener_contexto_completo()
        except Exception as e:
            print(f"❌ Error al obtener contexto: {e}")
            return {
                'exito': False,
                'error': "Error al procesar los datos financieros. Verifica tus transacciones.",
                'tipo': 'error'
            }

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
            # ✅ Payload optimizado
            payload = {
                "model": self.modelo,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": self.max_tokens,
                    "top_k": 40,
                    "top_p": 0.9,
                    "repeat_penalty": 1.1
                }
            }

            print(f"🤖 Enviando a Ollama (modelo: {self.modelo}, timeout: {self.timeout}s, max_tokens: {self.max_tokens})...")
            response = requests.post(self.url, json=payload, timeout=self.timeout)

            print(f"📡 Status Code: {response.status_code}")

            if response.status_code == 200:
                response_data = response.json()
                respuesta = response_data.get('response', '').strip()

                if not respuesta:
                    return {
                        'exito': False,
                        'error': "Ollama no generó respuesta. Verifica que el modelo esté cargado correctamente.",
                        'tipo': 'error'
                    }

                # Guardar en historial
                self.historial.append({'rol': 'usuario', 'mensaje': mensaje_usuario})
                self.historial.append({'rol': 'asistente', 'mensaje': respuesta})

                return {
                    'exito': True,
                    'respuesta': respuesta,
                    'tipo': 'ia'
                }
            elif response.status_code == 404:
                return {
                    'exito': False,
                    'error': f"""❌ Modelo '{self.modelo}' no encontrado

💡 Solución:
1. Abre una terminal
2. Ejecuta: ollama pull {self.modelo}
3. Espera a que descargue
4. Vuelve a intentar aquí

Si el modelo tarda mucho, prueba uno más ligero:
• ollama pull llama3.2:1b (más rápido)""",
                    'tipo': 'error'
                }
            elif response.status_code == 500:
                try:
                    error_data = response.json()
                    error_msg = error_data.get('error', 'Error desconocido')
                except:
                    error_msg = response.text[:200]

                print(f"❌ Error 500 de Ollama: {error_msg}")

                return {
                    'exito': False,
                    'error': f"""❌ Error interno de Ollama

Posibles causas:
1. Ollama no está ejecutándose correctamente
2. El modelo está corrupto o no cargó bien
3. Memoria insuficiente (RAM/VRAM)

💡 Soluciones:
• Reinicia Ollama: Cierra la terminal de ollama y ejecuta nuevamente: ollama serve
• Recarga el modelo: ollama pull {self.modelo}
• Prueba un modelo más ligero: ollama pull llama3.2:1b

Detalles: {error_msg[:100]}""",
                    'tipo': 'error'
                }
            else:
                return {
                    'exito': False,
                    'error': f"Error de Ollama (código {response.status_code}). Verifica el servicio.",
                    'tipo': 'error'
                }

        except requests.exceptions.ConnectionError:
            return {
                'exito': False,
                'error': """❌ No se pudo conectar a Ollama

💡 Solución:
1. Abre una terminal/CMD
2. Ejecuta: ollama serve
3. Espera a que se inicie (verás "Listening on...")
4. Vuelve a intentar aquí

Asegúrate de que Ollama esté instalado: https://ollama.ai""",
                'tipo': 'conexion'
            }
        except requests.exceptions.Timeout:
            return {
                'exito': False,
                'error': f"""⏱️ La solicitud tardó más de {self.timeout} segundos

Posibles causas:
• El modelo es muy pesado para tu hardware
• Ollama está sobrecargado
• Primera ejecución (carga inicial lenta)

💡 Soluciones:
• Espera un momento y vuelve a intentar
• Usa un modelo más ligero (llama3.2:1b)
• Aumenta la RAM disponible""",
                'tipo': 'timeout'
            }
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            import traceback
            traceback.print_exc()
            return {
                'exito': False,
                'error': f"Error inesperado: {str(e)}\n\nSi el problema persiste, contacta al desarrollador.",
                'tipo': 'error'
            }

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

    def obtener_contexto_comando(self, comando):
        """Obtiene contexto específico para comandos especiales"""
        try:
            if comando == "analisis":
                return self.generar_analisis_completo()
            elif comando == "alertas":
                return self.generar_resumen_alertas()
            elif comando == "consejos":
                return self.generar_consejos_personalizados()
            elif comando == "resumen":
                return self.generar_resumen_financiero()
        except Exception as e:
            print(f"Error en comando {comando}: {e}")
            return f"❌ Error al generar {comando}. Verifica tus datos."

        return None

    def generar_analisis_completo(self):
        """Genera análisis financiero completo"""
        if not self.gestor_datos.transacciones:
            return "⚠️ No hay transacciones para analizar. Agrega algunas primero en la pestaña 'Transacciones'."

        try:
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
Tasa de Ahorro: {salud.get('tasa_ahorro', 0):.1f}%

💚 Salud Financiera: {salud.get('nivel', 'N/A')} ({salud.get('puntuacion', 0)}/100 puntos)

"""

            # Agregar interpretación
            puntuacion = salud.get('puntuacion', 0)
            if puntuacion >= 80:
                analisis += "✨ ¡Excelente trabajo! Tus finanzas están en muy buen estado."
            elif puntuacion >= 60:
                analisis += "👍 Vas bien, pero hay áreas de oportunidad para mejorar."
            elif puntuacion >= 40:
                analisis += "⚠️ Atención necesaria. Considera revisar tus gastos."
            else:
                analisis += "🚨 Situación crítica. Necesitas hacer cambios importantes."

            return analisis
        except Exception as e:
            print(f"Error en análisis: {e}")
            return "❌ Error al generar análisis. Verifica tus datos."

    def generar_resumen_alertas(self):
        """Genera resumen de alertas"""
        try:
            alertas = self.analizador.analizar_todo()

            if not alertas:
                return "✅ ¡Todo en orden! No hay alertas activas en este momento."

            resumen = f"🔔 ALERTAS ACTIVAS ({len(alertas)}):\n\n"

            for i, alerta in enumerate(alertas[:5], 1):
                icono = {
                    'peligro': '🔴',
                    'advertencia': '🟡',
                    'info': '🔵',
                    'exito': '🟢',
                    'consejo': '💡'
                }.get(alerta['tipo'], '⚪')

                resumen += f"{icono} {alerta['titulo']}\n{alerta['mensaje']}\n\n"

            if len(alertas) > 5:
                resumen += f"... y {len(alertas) - 5} alertas más. Ve a la pestaña 'Alertas' para verlas todas."

            return resumen
        except Exception as e:
            print(f"Error en alertas: {e}")
            return "❌ Error al generar alertas."

    def generar_consejos_personalizados(self):
        """Genera consejos basados en el análisis"""
        if not self.gestor_datos.transacciones:
            return "📝 Primero registra algunas transacciones para recibir consejos personalizados."

        try:
            balance = self.gestor_datos.obtener_balance()
            gastos = self.gestor_datos.obtener_total_gastos()
            ingresos = self.gestor_datos.obtener_total_ingresos()
            gastos_cat = self.gestor_datos.obtener_gastos_por_categoria()

            consejos = "💡 CONSEJOS PERSONALIZADOS:\n\n"

            # Consejo sobre balance
            if balance < 0:
                consejos += "1️⃣ URGENTE: Tu balance es negativo. Prioriza reducir gastos inmediatamente.\n\n"
            elif ingresos > 0 and balance < ingresos * 0.1:
                consejos += "1️⃣ Intenta ahorrar al menos el 20% de tus ingresos mensuales.\n\n"

            # Consejo sobre categorías
            if gastos_cat and gastos > 0:
                max_cat = max(gastos_cat, key=gastos_cat.get)
                max_monto = gastos_cat[max_cat]
                porcentaje = (max_monto / gastos * 100)

                if porcentaje > 35:
                    consejos += f"2️⃣ Tu mayor gasto es '{max_cat}' ({porcentaje:.1f}%). Busca formas de optimizar esta categoría.\n\n"

            # Consejo general
            consejos += "3️⃣ Regla 50/30/20: 50% necesidades, 30% gustos, 20% ahorro.\n\n"
            consejos += "4️⃣ Revisa tus gastos semanalmente para mantener el control."

            return consejos
        except Exception as e:
            print(f"Error en consejos: {e}")
            return "❌ Error al generar consejos."

    def generar_resumen_financiero(self):
        """Genera resumen rápido de la situación"""
        if not self.gestor_datos.transacciones:
            return "📋 No hay datos para generar un resumen. Agrega transacciones primero."

        try:
            balance = self.gestor_datos.obtener_balance()
            ingresos = self.gestor_datos.obtener_total_ingresos()
            gastos = self.gestor_datos.obtener_total_gastos()
            salud = self.analizador.obtener_resumen_salud_financiera()

            return f"""📋 RESUMEN RÁPIDO

Balance: ${balance:,.2f}
Ingresos: ${ingresos:,.2f}
Gastos: ${gastos:,.2f}
Ahorro: {salud.get('tasa_ahorro', 0):.1f}%
Salud: {salud.get('nivel', 'N/A')}

{self._emoji_tendencia(balance)} Tendencia: {'Positiva' if balance > 0 else 'Requiere atención'}"""
        except Exception as e:
            print(f"Error en resumen: {e}")
            return "❌ Error al generar resumen."

    def _emoji_tendencia(self, balance):
        """Retorna emoji según la tendencia"""
        if balance > 0:
            return "📈"
        elif balance < 0:
            return "📉"
        return "➡️"

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