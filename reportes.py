import json
import os
from gestion_libros import cargar_libros

REPORTE_DIR = "data/reportes"
REPORTE_PATH = os.path.join(REPORTE_DIR, "reporte_libros.json")

def generar_reporte():
    libros = cargar_libros()
    if not libros:
        print("\nNo hay datos para generar el reporte.")
        return

    if not os.path.exists(REPORTE_DIR):
        os.makedirs(REPORTE_DIR)

    reporte_dict = {}
    for l in libros:
        cat = l['genero']
        if cat not in reporte_dict:
            reporte_dict[cat] = []
        reporte_dict[cat].append({
            "titulo": l["titulo"],
            "autor": l["autor"],
            "estado": l["estado"] if l["estado"] == "Disponible" else f"Prestado a {l['prestado_a']}"
        })

    reporte_final = [{"categoria": k, "libros": v} for k, v in reporte_dict.items()]

    with open(REPORTE_PATH, "w") as f:
        json.dump(reporte_final, f, indent=4)

    print("\n" + "="*40)
    print("REPORTE DEL INVENTARIO DE LIBROS")
    print("="*40)
    for item in reporte_final:
        print(f"\n{item['categoria']}:")
        for lib in item['libros']:
            print(f"- {lib['titulo']} | Autor: {lib['autor']} | Estado: {lib['estado']}")
    
    print("\n" + "-"*40)
    input("Presione ENTER para continuar...")