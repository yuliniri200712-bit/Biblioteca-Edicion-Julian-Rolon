import json
import os
from datetime import datetime, timedelta
from gestion_libros import cargar_libros, guardar_libros
import config

ESTADISTICAS_PATH = config.ruta_absoluta/"data/reportes/estadisticas.csv"

def prestar_con_fecha():
    """Versión mejorada de préstamo que incluye fecha de devolución."""
    libros = cargar_libros()
    titulo = input("\nIngrese el título del libro: ")
    
    for libro in libros:
        if libro['titulo'].lower() == titulo.lower():
            if libro['estado'] == "Disponible":
                usuario = input("Nombre del usuario: ")
                # Calculamos 7 días para la devolución
                fecha_hoy = datetime.now()
                fecha_entrega = fecha_hoy + timedelta(days=7)
                
                libro['estado'] = "Prestado"
                libro['prestado_a'] = usuario
                libro['fecha_prestamo'] = fecha_hoy.strftime("%Y-%m-%d %H:%M")
                libro['fecha_limite'] = fecha_entrega.strftime("%Y-%m-%d")
                
                guardar_libros(libros)
                print(f'\nÉxito: "{libro["titulo"]}" prestado hasta el {libro["fecha_limite"]}.')
            else:
                print("\nEl libro ya está ocupado.")
            return
    print("\nLibro no encontrado.")

def ver_estadisticas():
    """Muestra un resumen rápido del inventario."""
    libros = cargar_libros()
    if not libros:
        return print("No hay libros registrados.")

    total = len(libros)
    prestados = len([l for l in libros if l['estado'] != "Disponible"])
    disponibles = total - prestados
    
    print("\n" + " stats ".center(30, "="))
    print(f"Total de ejemplares: {total}")
    print(f"Libros en préstamo:  {prestados}")
    print(f"Libros disponibles: {disponibles}")
    print("="*30)

def reservar_libro():
    """Permite poner un libro en reserva si ya está prestado."""
    libros = cargar_libros()
    titulo = input("\nIngrese el título del libro que desea reservar: ")
    
    for libro in libros:
        if libro['titulo'].lower() == titulo.lower():
            if libro['estado'] == "Prestado":
                usuario = input("Ingrese su nombre para la reserva: ")
                
                # Añadimos el campo 'reserva' si no existe
                libro['reservado_por'] = usuario
                guardar_libros(libros)
                
                print(f'\nReserva confirmada: Avisaremos a {usuario} cuando "{libro["titulo"]}" sea devuelto.')
            elif libro['estado'] == "Disponible":
                print("\nEl libro está disponible ahora mismo. ¡Puedes usar la opción de préstamo!")
            else:
                print(f"\nEl libro ya tiene una reserva activa por: {libro.get('reservado_por', 'Alguien más')}")
            return
    print("\nLibro no encontrado en el sistema.")        