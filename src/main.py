import json
from vista import mostrar_interfaz_visual

def cargar_datos_existentes():
    """Esta función le da memoria al programa al iniciar"""
    try:
        with open("src/usuarios.json", "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def guardar_en_json(datos_usuarios):
    with open("src/usuarios.json", "w", encoding="utf-8") as archivo:
        json.dump(datos_usuarios, archivo, indent=4, ensure_ascii=False)
    print("\n[SISTEMA]: Memoria actualizada correctamente.")

def iniciar_app():
    # --- LA MEJORA AQUÍ: Cargamos lo que ya existe ---
    registro_usuarios = cargar_datos_existentes()
    print(f"--- SISTEMA INICIADO: {len(registro_usuarios)} usuarios en memoria ---")
    
    while True:
        nombre = input("\nNombre (o 'salir'): ")
        
        if nombre.lower() == "salir":
            guardar_en_json(registro_usuarios)
            mostrar_interfaz_visual()
            break

        try:
            edad = int(input(f"Edad de {nombre}: "))
            cat = "Adulto" if edad >= 18 else "Menor"
            
            usuario = {
                "nombre": nombre, "edad": edad, 
                "categoria": cat, "dias": edad * 365
            }
            
            registro_usuarios.append(usuario) # Ahora se añade a la lista existente
            print(f"✅ {nombre} añadido a la cola de guardado.")
        except ValueError:
            print("❌ Error: Edad no válida.")

if __name__ == "__main__":
    iniciar_app()