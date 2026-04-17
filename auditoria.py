import json
import os
from gestion_libros import cargar_libros
import config

REPORT_PATH = config.ruta_absoluta / "data/reportes/reporte_auditoria_estados.json"
REPORTES_DIR = config.ruta_absoluta / "data/reportes"


ESTADOS_VALIDOS = {"Disponible", "Prestado"}


def asegurar_ruta_reporte():
    """Crea el directorio de reportes usando la ruta absoluta del proyecto."""
    os.makedirs(REPORTES_DIR, exist_ok=True)


def _normalizar_estado(estado):
    """
    Intenta reconocer un estado escrito de forma incorrecta (ej: 'disponible',
    'PRESTADO', 'Prestado ', etc.) para dar un mensaje de error más claro.
    Devuelve el valor tal como está en el JSON; no lo corrige.
    """
    if estado is None:
        return None
    mapa = {e.lower(): e for e in ESTADOS_VALIDOS}
    return mapa.get(str(estado).strip().lower())  


def _validar_libro(libro):
    """
    Valida un libro y devuelve una lista de inconsistencias encontradas.
    Un libro puede tener más de una inconsistencia simultáneamente.
    """
    errores = []
    estado_raw = libro.get("estado")
    usuario = libro.get("prestado_a")
    usuario_vacio = usuario is None or str(usuario).strip() == ""

    estado_reconocido = _normalizar_estado(estado_raw)

    
    if estado_raw not in ESTADOS_VALIDOS:
        errores.append("ESTADO_INVALIDO")
        
        estado_efectivo = estado_reconocido  
    else:
        estado_efectivo = estado_raw

    
    if estado_efectivo == "Prestado" and usuario_vacio:
        errores.append("PRESTADO_SIN_USUARIO")

    elif estado_efectivo == "Disponible" and not usuario_vacio:
        errores.append("DISPONIBLE_CON_USUARIO")

    return errores


def auditoria_estados():
    """
    Lee libros.json, detecta inconsistencias y genera
    data/reportes/reporte_auditoria_estados.json sin modificar el inventario.
    """
    libros = cargar_libros()

    inconsistencias = []
    conteo_por_tipo = {
        "ESTADO_INVALIDO": 0,
        "PRESTADO_SIN_USUARIO": 0,
        "DISPONIBLE_CON_USUARIO": 0,
    }

    for libro in libros:
        errores = _validar_libro(libro)
        if errores:
            for tipo in errores:
                conteo_por_tipo[tipo] += 1

            inconsistencias.append(
                {
                    "titulo": libro.get("titulo"),
                    "autor": libro.get("autor"),
                    "estado": libro.get("estado"),
                    "prestado_a": libro.get("prestado_a"),
                    "tipo_inconsistencia": errores if len(errores) > 1 else errores[0],
                }
            )

    total_inconsistencias = len(inconsistencias)

    resumen = {
        "total_revisados": len(libros),
        "total_inconsistencias": total_inconsistencias,
        "conteo_por_tipo": conteo_por_tipo,
    }

    reporte_final = {"resumen": resumen, "detalles": inconsistencias}

    
    asegurar_ruta_reporte()
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(reporte_final, f, indent=4, ensure_ascii=False)

   
    print("\n" + "=" * 50)
    print("     AUDITORÍA DE CONSISTENCIA DE ESTADOS")
    print("=" * 50)
    print(f"  Libros revisados       : {resumen['total_revisados']}")
    print(f"  Libros con problemas   : {total_inconsistencias}")
    print(f"   ESTADO_INVALIDO     : {conteo_por_tipo['ESTADO_INVALIDO']}")
    print(f"   PRESTADO_SIN_USUARIO: {conteo_por_tipo['PRESTADO_SIN_USUARIO']}")
    print(f"   DISPONIBLE_CON_USR  : {conteo_por_tipo['DISPONIBLE_CON_USUARIO']}")

    if inconsistencias:
        print("\n  Detalle de inconsistencias:")
        print("  " + "-" * 46)
        for inc in inconsistencias:
            titulo = inc["titulo"] or "(sin título)"
            tipo = (
                ", ".join(inc["tipo_inconsistencia"])
                if isinstance(inc["tipo_inconsistencia"], list)
                else inc["tipo_inconsistencia"]
            )
            print(f"  • {titulo[:30]:<30} → {tipo}")
    else:
        print("\n   No se encontraron inconsistencias.")

    print("=" * 50)
    print(f"\n  Reporte guardado en:\n  {REPORT_PATH}\n")