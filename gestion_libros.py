import json
import os

DATA_PATH = "data/libros.json"

def asegurar_ruta():
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(DATA_PATH):
        with open(DATA_PATH, "w") as f:
            json.dump([], f)

def cargar_libros():
    asegurar_ruta()
    with open(DATA_PATH, "r") as f:
        return json.load(f)

def guardar_libros(libros):
    with open(DATA_PATH, "w") as f:
        json.dump(libros, f, indent=4)

def registrar_libro():
    libros = cargar_libros()
    print("\n--- Registrar Nuevo Libro ---")
    titulo = input("Ingrese el título del libro: ")
    
    if any(l['titulo'].lower() == titulo.lower() for l in libros):
        print(f'Error: El libro "{titulo}" ya existe.')
        return

    autor = input("Ingrese el nombre del autor: ")
    genero = input("Ingrese el género del libro: ")
    try:
        anio = int(input("Ingrese el año de publicación: "))
    except ValueError:
        print("Año no válido. Registro cancelado.")
        return

    nuevo_libro = {
        "titulo": titulo,
        "autor": autor,
        "genero": genero,
        "anio_publicacion": anio,
        "estado": "Disponible",
        "prestado_a": None
    }
    
    libros.append(nuevo_libro)
    guardar_libros(libros)
    print(f'\nLibro "{titulo}" registrado exitosamente.')

def ver_inventario():
    libros = cargar_libros()
    if not libros:
        print("\nEl inventario está vacío.")
        return

    print("\n" + "="*85)
    print(f"{'Título':<25} | {'Autor':<20} | {'Género':<15} | {'Estado':<20}")
    print("="*85)
    for l in libros:
        estado_str = l['estado'] if l['estado'] == "Disponible" else f"Prestado a {l['prestado_a']}"
        print(f"{l['titulo']:<25} | {l['autor']:<20} | {l['genero']:<15} | {estado_str:<20}")
    print("="*85)