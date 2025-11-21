"""
Script para verificar que todos los imports funcionen
Ejecuta: python verificar_imports.py
"""

print("🔍 Verificando imports...\n")

imports_exitosos = []
imports_fallidos = []

# Lista de imports a verificar
imports_a_verificar = [
    ("config", "Configuración"),
    ("datos.gestor_transacciones", "Gestor de Transacciones"),
    ("datos.gestor_metas", "Gestor de Metas"),
    ("datos.config_categorias", "Configuración de Categorías"),
    ("interfaz.panel_dashboard", "Panel Dashboard"),
    ("interfaz.panel_transacciones", "Panel Transacciones"),
    ("interfaz.panel_metas", "Panel Metas"),
    ("interfaz.panel_resultados", "Panel Resultados"),
    ("interfaz.panel_chat", "Panel Chat"),
    ("interfaz.panel_alertas", "Panel Alertas"),
    ("procesador.analizador", "Analizador"),
    ("procesador.chat_financiero", "Chat Financiero"),
    ("utils.helpers", "Helpers"),
    ("utils.validadores", "Validadores"),
    ("utils.ventana_bienvenida", "Ventana Bienvenida"),
]

for modulo, nombre in imports_a_verificar:
    try:
        __import__(modulo)
        print(f"✅ {nombre}: OK")
        imports_exitosos.append(nombre)
    except ImportError as e:
        print(f"❌ {nombre}: FALTA - {e}")
        imports_fallidos.append((nombre, str(e)))
    except Exception as e:
        print(f"⚠️  {nombre}: ERROR - {e}")
        imports_fallidos.append((nombre, str(e)))

print("\n" + "="*50)
print(f"\n📊 Resumen:")
print(f"✅ Exitosos: {len(imports_exitosos)}/{len(imports_a_verificar)}")
print(f"❌ Fallidos: {len(imports_fallidos)}/{len(imports_a_verificar)}")

if imports_fallidos:
    print("\n⚠️  Módulos faltantes o con errores:")
    for nombre, error in imports_fallidos:
        print(f"  • {nombre}")
        print(f"    └─ {error}")
    print("\n💡 Crea los archivos faltantes antes de ejecutar la app.")
else:
    print("\n🎉 ¡Todos los módulos están disponibles!")
    print("✅ Puedes ejecutar: python app.py")

print("\n" + "="*50)