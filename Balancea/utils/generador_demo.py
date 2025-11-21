"""
Generador de Datos de Demostración
Crea transacciones, metas y presupuestos de ejemplo
"""

import random
from datetime import datetime, timedelta


class GeneradorDemo:
    """Genera datos de demostración realistas"""

    def __init__(self, gestor_datos):
        self.gestor_datos = gestor_datos

        # Plantillas de transacciones por categoría
        self.plantillas = {
            'Alimentación': [
                'Supermercado Walmart', 'Supermercado Soriana', 'Mercado local',
                'Restaurante comida rápida', 'Cafetería Starbucks', 'Tacos al pastor',
                'Pizza Dominos', 'Subway sandwich', 'Despensa mensual'
            ],
            'Transporte': [
                'Gasolina', 'Uber', 'Taxi', 'Estacionamiento', 'Servicio de auto',
                'Peaje carretera', 'DiDi', 'Transporte público', 'Mantenimiento auto'
            ],
            'Entretenimiento': [
                'Netflix', 'Spotify', 'Cine', 'Videojuegos', 'Salida con amigos',
                'Concierto', 'Teatro', 'Amazon Prime', 'Disney+'
            ],
            'Servicios': [
                'Luz CFE', 'Agua', 'Internet', 'Teléfono', 'Gas',
                'Streaming', 'Gym', 'Seguro', 'Renta'
            ],
            'Salud': [
                'Farmacia', 'Doctor', 'Dentista', 'Medicamentos', 'Vitaminas',
                'Análisis clínicos', 'Consulta médica', 'Seguro médico'
            ],
            'Educación': [
                'Colegiatura', 'Libros', 'Cursos online', 'Material escolar',
                'Udemy curso', 'Coursera', 'Papelería', 'Universidad'
            ],
            'Ropa': [
                'Zara', 'H&M', 'Nike', 'Adidas', 'Liverpool', 'Palacio de Hierro',
                'Mercado de ropa', 'Zapatos', 'Ropa deportiva'
            ],
            'Hogar': [
                'Muebles', 'Decoración', 'Limpieza hogar', 'Home Depot',
                'Reparaciones', 'Electrodomésticos', 'Jardinería', 'Pintura'
            ],
            'Salario': [
                'Sueldo mensual', 'Pago quincenal', 'Salario'
            ],
            'Freelance': [
                'Proyecto freelance', 'Trabajo extra', 'Consultoría',
                'Diseño web', 'Programación'
            ]
        }

    def generar_transacciones_demo(self, num_dias=60):
        """Genera transacciones de demostración de los últimos N días"""
        transacciones_generadas = 0

        # Generar transacciones diarias
        for i in range(num_dias):
            fecha = datetime.now() - timedelta(days=i)
            fecha_str = fecha.strftime('%Y-%m-%d')

            # Generar 1-4 transacciones por día
            num_trans_dia = random.randint(1, 4)

            for _ in range(num_trans_dia):
                # 80% gastos, 20% ingresos (más realista)
                if random.random() < 0.8:
                    # Gasto
                    categoria = random.choice(list(self.plantillas.keys()))

                    # Saltar categorías de ingresos
                    while categoria in ['Salario', 'Freelance']:
                        categoria = random.choice(list(self.plantillas.keys()))

                    descripcion = random.choice(self.plantillas[categoria])

                    # Montos realistas según categoría
                    rangos_monto = {
                        'Alimentación': (50, 800),
                        'Transporte': (30, 500),
                        'Entretenimiento': (100, 600),
                        'Servicios': (200, 2000),
                        'Salud': (100, 1500),
                        'Educación': (200, 3000),
                        'Ropa': (200, 2000),
                        'Hogar': (100, 3000)
                    }

                    rango = rangos_monto.get(categoria, (50, 500))
                    monto = round(random.uniform(*rango), 2)

                    self.gestor_datos.agregar_transaccion(
                        fecha_str, descripcion, monto, 'Gasto', categoria
                    )
                    transacciones_generadas += 1

                else:
                    # Ingreso (principalmente salarios)
                    if random.random() < 0.7:  # 70% salario
                        categoria = 'Salario'
                        descripcion = 'Sueldo mensual'
                        monto = round(random.uniform(8000, 20000), 2)
                    else:  # 30% freelance
                        categoria = 'Freelance'
                        descripcion = random.choice(self.plantillas['Freelance'])
                        monto = round(random.uniform(2000, 8000), 2)

                    # Solo agregar ingresos cada 15 días aprox
                    if i % 15 == 0:
                        self.gestor_datos.agregar_transaccion(
                            fecha_str, descripcion, monto, 'Ingreso', categoria
                        )
                        transacciones_generadas += 1

        return transacciones_generadas

    def generar_metas_demo(self):
        """Genera metas de demostración"""
        from datos.gestor_metas import GestorMetas

        gestor_metas = GestorMetas()

        metas_demo = [
            {
                'nombre': 'Fondo de Emergencia',
                'monto_objetivo': 50000,
                'monto_actual': 15000,
                'fecha_limite': (datetime.now() + timedelta(days=180)).strftime('%Y-%m-%d'),
                'descripcion': 'Ahorro para imprevistos'
            },
            {
                'nombre': 'Vacaciones 2025',
                'monto_objetivo': 25000,
                'monto_actual': 8000,
                'fecha_limite': (datetime.now() + timedelta(days=150)).strftime('%Y-%m-%d'),
                'descripcion': 'Viaje a la playa'
            },
            {
                'nombre': 'Laptop Nueva',
                'monto_objetivo': 15000,
                'monto_actual': 12000,
                'fecha_limite': (datetime.now() + timedelta(days=60)).strftime('%Y-%m-%d'),
                'descripcion': 'Para trabajo y estudios'
            }
        ]

        for meta in metas_demo:
            nueva_meta = gestor_metas.agregar_meta(
                meta['nombre'],
                meta['monto_objetivo'],
                meta['fecha_limite'],
                meta['descripcion']
            )
            # Actualizar monto actual
            gestor_metas.actualizar_monto(nueva_meta['id'], meta['monto_actual'])

        return len(metas_demo)

    def generar_presupuestos_demo(self):
        """Genera presupuestos de demostración"""
        from datos.gestor_presupuestos import GestorPresupuestos

        gestor_presup = GestorPresupuestos(self.gestor_datos)

        presupuestos_demo = {
            'Alimentación': 5000,
            'Transporte': 2000,
            'Entretenimiento': 1500,
            'Servicios': 3000,
            'Salud': 1000,
            'Educación': 2000
        }

        for categoria, monto in presupuestos_demo.items():
            gestor_presup.establecer_presupuesto(categoria, monto)

        return len(presupuestos_demo)

    def generar_demo_completa(self):
        """Genera demostración completa con todo"""
        resultado = {
            'transacciones': 0,
            'metas': 0,
            'presupuestos': 0
        }

        # Generar transacciones
        resultado['transacciones'] = self.generar_transacciones_demo(60)

        # Generar metas
        resultado['metas'] = self.generar_metas_demo()

        # Generar presupuestos
        resultado['presupuestos'] = self.generar_presupuestos_demo()

        return resultado