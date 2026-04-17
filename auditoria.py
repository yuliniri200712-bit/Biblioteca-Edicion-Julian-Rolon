import json
import os
from gestion_libros import cargar_libros
import config
REPORT_PATH = config.ruta_absoluta/"data/reportes/reporte_auditoria_estados.json"

def asegurar_ruta_reporte():
    if not os.path.exists("data/reportes"):
        os.makedirs("data/reportes")

def auditoria_estados():
    libros = cargar_libros()
    inconsistencias = []
    resumen = {
        "total_revisados": len(libros),
        "total_inconsistencias": 0,
        "conteo_por_tipo": {
            "ESTADO_INVALIDO": 0,
            "PRESTADO_SIN_USUARIO": 0,
            "DISPONIBLE_CON_USUARIO": 0
        }
    }

    estados_validos = ["Disponible", "Prestado"]

    for l in libros:
        error = None
        estado = l.get('estado')
        usuario = l.get('prestado_a')

       
        if estado not in estados_validos:
            error = "ESTADO_INVALIDO"
        
        
        elif estado == "Prestado" and (usuario is None or str(usuario).strip() == ""):
            error = "PRESTADO_SIN_USUARIO"
        
       
        elif estado == "Disponible" and (usuario is not None and str(usuario).strip() != ""):
            error = "DISPONIBLE_CON_USUARIO"

        if error:
            inconsistencias.append({
                "titulo": l.get('titulo'),
                "autor": l.get('autor'),
                "estado": estado,
                "prestado_a": usuario,
                "tipo_inconsistencia": error
            })
            resumen["total_inconsistencias"] += 1
            resumen["conteo_por_tipo"][error] += 1

    
    asegurar_ruta_reporte()
    reporte_final = {
        "resumen": resumen,
        "detalles": inconsistencias
    }

    with open(REPORT_PATH, "w") as f:
        json.dump(reporte_final, f, indent=4)

    print(f"\nAuditoría completada. Se encontraron {resumen['total_inconsistencias']} inconsistencias.")
    print(f"Reporte generado en: {REPORT_PATH}")