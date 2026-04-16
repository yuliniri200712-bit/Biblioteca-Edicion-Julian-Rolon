from gestion_libros import cargar_libros, guardar_libros

def prestar_libro():
    libros = cargar_libros()
    titulo = input("\nIngrese el título del libro que desea prestar: ")
    
    for libro in libros:
        if libro['titulo'].lower() == titulo.lower():
            if libro['estado'] == "Disponible":
                usuario = input("Ingrese el nombre del usuario: ")
                libro['estado'] = "Prestado"
                libro['prestado_a'] = usuario
                guardar_libros(libros)
                print(f'\nLibro "{libro["titulo"]}" prestado a {usuario}.')
            else:
                print("\nEl libro ya se encuentra prestado.")
            return
    print("\nLibro no encontrado.")

def devolver_libro():
    libros = cargar_libros()
    titulo = input("\nIngrese el título del libro que desea devolver: ")
    
    for libro in libros:
        if libro['titulo'].lower() == titulo.lower():
            libro['estado'] = "Disponible"
            libro['prestado_a'] = None
            guardar_libros(libros)
            print(f'\nLibro "{libro["titulo"]}" ha sido devuelto y está disponible nuevamente.')
            return
    print("\nLibro no encontrado.")