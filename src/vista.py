import json

def cargar_datos():
    try:
        with open("src/usuarios.json", "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return []

def mostrar_interfaz_visual():
    datos = cargar_datos()
    
    print("\n" + "="*50)
    print("      PANEL DE CONTROL - FRONTEND v2.0")
    print("="*50)
    
    if not datos:
        print(" [!] No hay datos para mostrar.")
        return

    # 1. Dibujar la Tabla
    print(f"{'NOMBRE':<15} | {'EDAD':<5} | {'CATEGORÍA':<10}")
    print("-" * 50)
    for u in datos:
        print(f"{u['nombre']:<15} | {u['edad']:<5} | {u['categoria']:<10}")
    
    # 2. SECCIÓN DE ESTADÍSTICAS (La nueva inteligencia)
    print("-" * 50)
    
    # Extraemos todas las edades para operar con ellas
    edades = [u['edad'] for u in datos]
    promedio = sum(edades) / len(edades)
    joven = min(edades)
    viejo = max(edades)
    
    print(f"📊 ESTADÍSTICAS DEL GRUPO:")
    print(f" > Edad Promedio: {promedio:.1f} años")
    print(f" > Edad Mínima:   {joven} años")
    print(f" > Edad Máxima:   {viejo} años")
    print("="*50 + "\n")

if __name__ == "__main__":
    mostrar_interfaz_visual()