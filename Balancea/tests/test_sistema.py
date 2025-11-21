"""
Tests del Sistema Balancea
Pruebas automáticas de funcionalidades
"""

import sys
import os

# Agregar directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datos.gestor_transacciones import GestorTransacciones
from datos.gestor_metas import GestorMetas
from datos.gestor_presupuestos import GestorPresupuestos
from procesador.analizador import AnalizadorFinanciero
from datetime import datetime


class TestSistema:
    """Suite de pruebas del sistema"""

    def __init__(self):
        self.tests_pasados = 0
        self.tests_fallidos = 0
        self.errores = []

    def test(self, nombre, funcion):
        """Ejecuta una prueba"""
        try:
            funcion()
            print(f"✅ {nombre}")
            self.tests_pasados += 1
            return True
        except AssertionError as e:
            print(f"❌ {nombre}: {str(e)}")
            self.tests_fallidos += 1
            self.errores.append(f"{nombre}: {str(e)}")
            return False
        except Exception as e:
            print(f"💥 {nombre}: Error inesperado - {str(e)}")
            self.tests_fallidos += 1
            self.errores.append(f"{nombre}: {str(e)}")
            return False

    def test_gestor_transacciones(self):
        """Pruebas del gestor de transacciones"""
        print("\n🧪 Testing Gestor de Transacciones...")

        # Crear gestor temporal
        gestor = GestorTransacciones("datos/test_transacciones.csv")
        gestor.transacciones = []

        # Test 1: Agregar transacción
        def test_agregar():
            trans = gestor.agregar_transaccion(
                datetime.now().strftime('%Y-%m-%d'),
                "Test compra",
                100.50,
                "Gasto",
                "Alimentación"
            )
            assert trans is not None, "Transacción no creada"
            assert trans['monto'] == 100.50, "Monto incorrecto"

        self.test("Agregar transacción", test_agregar)

        # Test 2: Obtener balance
        def test_balance():
            gestor.transacciones = []
            gestor.agregar_transaccion(
                datetime.now().strftime('%Y-%m-%d'),
                "Ingreso", 1000, "Ingreso", "Salario"
            )
            gestor.agregar_transaccion(
                datetime.now().strftime('%Y-%m-%d'),
                "Gasto", 300, "Gasto", "Alimentación"
            )
            balance = gestor.obtener_balance()
            assert balance == 700, f"Balance incorrecto: {balance}"

        self.test("Calcular balance", test_balance)

        # Test 3: Gastos por categoría
        def test_gastos_cat():
            gastos = gestor.obtener_gastos_por_categoria()
            assert 'Alimentación' in gastos, "Categoría no encontrada"
            assert gastos['Alimentación'] == 300, "Monto incorrecto"

        self.test("Gastos por categoría", test_gastos_cat)

        # Limpiar archivo de prueba
        if os.path.exists("datos/test_transacciones.csv"):
            os.remove("datos/test_transacciones.csv")

    def test_gestor_metas(self):
        """Pruebas del gestor de metas"""
        print("\n🎯 Testing Gestor de Metas...")

        gestor = GestorMetas("datos/test_metas.json")
        gestor.metas = []

        # Test 1: Crear meta
        def test_crear_meta():
            meta = gestor.agregar_meta(
                "Test Meta",
                10000,
                datetime.now().strftime('%Y-%m-%d'),
                "Meta de prueba"
            )
            assert meta is not None, "Meta no creada"
            assert meta['monto_objetivo'] == 10000, "Monto incorrecto"

        self.test("Crear meta", test_crear_meta)

        # Test 2: Agregar aporte
        def test_aporte():
            meta_id = gestor.metas[0]['id']
            gestor.agregar_aporte(meta_id, 5000)
            progreso = gestor.obtener_progreso(meta_id)
            assert progreso == 50, f"Progreso incorrecto: {progreso}"

        self.test("Agregar aporte a meta", test_aporte)

        # Test 3: Meta completada
        def test_completar():
            meta_id = gestor.metas[0]['id']
            gestor.agregar_aporte(meta_id, 5000)
            meta = gestor.obtener_meta_por_id(meta_id)
            assert meta['completada'] == True, "Meta no marcada como completada"

        self.test("Completar meta", test_completar)

        # Limpiar
        if os.path.exists("datos/test_metas.json"):
            os.remove("datos/test_metas.json")

    def test_gestor_presupuestos(self):
        """Pruebas del gestor de presupuestos"""
        print("\n💰 Testing Gestor de Presupuestos...")

        gestor_trans = GestorTransacciones("datos/test_trans_presup.csv")
        gestor_trans.transacciones = []

        gestor = GestorPresupuestos(gestor_trans, "datos/test_presupuestos.json")
        gestor.presupuestos = {}

        # Test 1: Establecer presupuesto
        def test_establecer():
            resultado = gestor.establecer_presupuesto("Alimentación", 5000)
            assert resultado == True, "No se pudo establecer presupuesto"
            assert "Alimentación" in gestor.presupuestos, "Presupuesto no guardado"

        self.test("Establecer presupuesto", test_establecer)

        # Test 2: Calcular porcentaje de uso
        def test_porcentaje():
            # Agregar gasto
            gestor_trans.agregar_transaccion(
                datetime.now().strftime('%Y-%m-%d'),
                "Supermercado", 2500, "Gasto", "Alimentación"
            )
            porcentaje = gestor.obtener_porcentaje_uso("Alimentación")
            assert porcentaje == 50, f"Porcentaje incorrecto: {porcentaje}"

        self.test("Calcular porcentaje de uso", test_porcentaje)

        # Limpiar
        for archivo in ["datos/test_presupuestos.json", "datos/test_trans_presup.csv"]:
            if os.path.exists(archivo):
                os.remove(archivo)

    def test_analizador(self):
        """Pruebas del analizador"""
        print("\n📊 Testing Analizador...")

        gestor = GestorTransacciones("datos/test_analisis.csv")
        gestor.transacciones = []

        # Agregar datos de prueba
        for i in range(5):
            gestor.agregar_transaccion(
                datetime.now().strftime('%Y-%m-%d'),
                f"Gasto {i}",
                100 + (i * 10),
                "Gasto",
                "Alimentación"
            )

        analizador = AnalizadorFinanciero(gestor)

        # Test 1: Detectar balance negativo
        def test_balance_negativo():
            alertas = analizador.analizar_todo()
            # Con solo gastos, debe detectar balance negativo
            tiene_alerta_balance = any(
                'balance' in a.get('categoria', '').lower()
                for a in alertas
            )
            assert tiene_alerta_balance, "No detectó balance negativo"

        self.test("Detectar balance negativo", test_balance_negativo)

        # Test 2: Salud financiera
        def test_salud():
            # Agregar ingreso
            gestor.agregar_transaccion(
                datetime.now().strftime('%Y-%m-%d'),
                "Salario", 10000, "Ingreso", "Salario"
            )
            salud = analizador.obtener_resumen_salud_financiera()
            assert 'puntuacion' in salud, "No calculó salud financiera"
            assert salud['puntuacion'] >= 0, "Puntuación inválida"

        self.test("Calcular salud financiera", test_salud)

        # Limpiar
        if os.path.exists("datos/test_analisis.csv"):
            os.remove("datos/test_analisis.csv")

    def ejecutar_todos(self):
        """Ejecuta todas las pruebas"""
        print("=" * 60)
        print("🧪 BALANCEA - SUITE DE PRUEBAS")
        print("=" * 60)

        self.test_gestor_transacciones()
        self.test_gestor_metas()
        self.test_gestor_presupuestos()
        self.test_analizador()

        # Resumen
        print("\n" + "=" * 60)
        print("📊 RESUMEN DE PRUEBAS")
        print("=" * 60)
        print(f"✅ Tests pasados: {self.tests_pasados}")
        print(f"❌ Tests fallidos: {self.tests_fallidos}")
        print(f"📈 Tasa de éxito: {(self.tests_pasados / (self.tests_pasados + self.tests_fallidos) * 100):.1f}%")

        if self.errores:
            print("\n❌ Errores encontrados:")
            for error in self.errores:
                print(f"  • {error}")
        else:
            print("\n🎉 ¡Todos los tests pasaron!")

        print("=" * 60)

        return self.tests_fallidos == 0


if __name__ == "__main__":
    tester = TestSistema()
    exito = tester.ejecutar_todos()

    sys.exit(0 if exito else 1)