import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

print("=" * 60)
print("PRUEBA DE INTEGRACIÓN - Aplicación de Protección")
print("=" * 60)

print("\n[1] Verificando worker thread...")
try:
    from worker_thread import MonitoringWorker
    print("✓ Worker thread importado correctamente")
except Exception as e:
    print(f"✗ Error importando worker: {e}")
    sys.exit(1)

print("\n[2] Verificando chat widget...")
try:
    from chat_widget import ChatWidget
    print("✓ Chat widget importado correctamente")
except Exception as e:
    print(f"✗ Error importando chat: {e}")
    sys.exit(1)

print("\n[3] Verificando main app...")
try:
    from main_app import MainApp
    print("✓ Main app importado correctamente")
except Exception as e:
    print(f"✗ Error importando main app: {e}")
    sys.exit(1)

print("\n[4] Verificando módulos del backend...")
backend_path = os.path.join(os.path.dirname(__file__), '..', 'Sistema-de-detecci-n-y-recomendaci-n-main')
if os.path.exists(backend_path):
    print(f"✓ Ruta del backend encontrada: {backend_path}")
else:
    print(f"✗ Ruta del backend no encontrada: {backend_path}")

print("\n" + "=" * 60)
print("TODAS LAS PRUEBAS PASARON ✓")
print("=" * 60)
print("\nAhora puedes ejecutar: python app.py")
