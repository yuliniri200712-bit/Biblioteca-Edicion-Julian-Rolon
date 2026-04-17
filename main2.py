import gestion_libros
import buscar_libros
import prestamos
import reportes
import auditoria

def menu():
    while True:
        print("\n==========================================")
        print("GESTOR DE INVENTARIO PARA BIBLIOTECA VIRTUAL")
        print("==========================================")
        print("1. Registrar un nuevo libro")
        print("2. Ver el inventario de libros")
        print("3. Buscar un libro")
        print("4. Prestar un libro")
        print("5. Devolver un libro")
        print("6. Generar un reporte del inventario")
        print("7. Auditoría de consistencia")
        print("8. Salir")
        
        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            gestion_libros.registrar_libro()
        elif opcion == "2":
            gestion_libros.ver_inventario()
        elif opcion == "3":
            buscar_libros.buscar_libro()
        elif opcion == "4":
            prestamos.prestar_libro()
        elif opcion == "5":
            prestamos.devolver_libro()
        elif opcion == "6":
            reportes.generar_reporte()
        elif opcion == "7":
            auditoria.auditoria_estados()    
        elif opcion == "8":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu()