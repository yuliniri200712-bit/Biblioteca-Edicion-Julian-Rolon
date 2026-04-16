from gestion_libros import cargar_libros

def buscar_libro():
    libros = cargar_libros()
    criterio = input("\nIngrese un criterio de búsqueda (título, autor o género): ").lower()
    
    encontrados = [l for l in libros if criterio in l['titulo'].lower() or 
                   criterio in l['autor'].lower() or 
                   criterio in l['genero'].lower()]

    if encontrados:
        print(f'\nLibros encontrados para "{criterio}":')
        for l in encontrados:
            print(f"- {l['titulo']} | Autor: {l['autor']} | Estado: {l['estado']}")
    else:
        print("\nNo se encontraron coincidencias.")