from models import CAMPOS_ESTUDIANTE, Estudiante
from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import (
    crear_estudiante, obtener_todos, obtener_por_id, buscar_estudiantes,
    actualizar_estudiante, eliminar_estudiante, agregar_nota, estudiantes_en_comun
)


def pausa():
    input("\nPresione Enter para continuar...")


def mostrar_tabla(estudiantes):
    print(f"{'ID':<5}{'NOMBRE':<25}{'CARNET':<15}{'EMAIL':<28}{'PROMEDIO':<10}")
    print("-" * 85)
    for estudiante in estudiantes:
        print(f"{estudiante.id:<5}{estudiante.obtener_nombre_completo():<25}"
              f"{estudiante.carnet:<15}{estudiante.email:<28}{estudiante.obtener_promedio():<10.2f}")
    print("-" * 85)
    imprimir_info(f"Total: {len(estudiantes)} estudiante(s)")


# ---------- C · CREAR ----------
def opcion_crear():
    imprimir_titulo("CREAR NUEVO ESTUDIANTE")
    # Recorro la TUPLA de campos: si mañana agrego un campo al Modelo,
    # este formulario se actualiza solo.
    datos = {}
    for campo in CAMPOS_ESTUDIANTE:
        datos[campo] = input(f"{campo.capitalize()}: ")

    exito, mensaje = crear_estudiante(datos)          # desempaqueto la TUPLA que devuelve
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()

def opcion_agregar_nota():
    imprimir_titulo("AGREGAR NOTA A ESTUDIANTE")
    try:
        id_est = int(input("Id del estudiante: "))
        materia = input("Nombre de la materia: ").strip()
        nota = float(input("Nota (0 - 20): "))
    except ValueError:
        imprimir_error("Error en los datos ingresados (ID entero, nota numérica)")
        return pausa()

    exito, mensaje = agregar_nota(id_est, materia, nota)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()

def opcion_ver_promedio():
    imprimir_titulo("VER PROMEDIO DE ESTUDIANTE")
    try:
        id_est = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El ID debe ser un número entero")
        return pausa()

    est = obtener_por_id(id_est)
    if not est:
        imprimir_error(f"No existe un estudiante con id {id_est}")
    else:
        imprimir_info(f"Estudiante: {est.obtener_nombre_completo()} ({est.carnet})")
        print(f"  Promedio general: {est.obtener_promedio()}")
        if est.notas:
            print("  Notas por materia:")
            for mat, list_notas in est.notas.items():
                print(f"    - {mat}: {list_notas}")
        else:
            print("  No registra notas todavía.")
    pausa()

def opcion_materias_en_comun():
    imprimir_titulo("MATERIAS EN COMÚN ENTRE ESTUDIANTES")
    try:
        id_a = int(input("Id del primer estudiante: "))
        id_b = int(input("Id del segundo estudiante: "))
    except ValueError:
        imprimir_error("Los IDs deben ser números enteros")
        return pausa()

    comun, mensaje = estudiantes_en_comun(id_a, id_b)
    if comun is None:
        imprimir_error(mensaje)
    else:
        imprimir_info(mensaje)
        if comun:
            print(f"  Materias compartidas: {', '.join(sorted(comun))}")
        else:
            print("  No comparten ninguna materia en común.")
    pausa()
# ---------- R · LEER TODOS ----------
def opcion_ver_todos():
    imprimir_titulo("LISTA DE ESTUDIANTES")
    estudiantes = obtener_todos()
    if not estudiantes:
        imprimir_info("Todavía no hay estudiantes. Use la opción 1 para crear el primero.")
    else:
        mostrar_tabla(estudiantes)
    pausa()


# ---------- S · BUSCAR ----------
def opcion_buscar():
    imprimir_titulo("BUSCAR ESTUDIANTE")
    termino = input("Nombre, email, teléfono o ciudad: ")
    encontrados = buscar_estudiantes(termino)

    if not encontrados:
        imprimir_info(f"Ningún estudiante coincide con '{termino}'.")
    else:
        mostrar_tabla(encontrados)
    pausa()


# ---------- R · LEER UNO ----------
def opcion_ver_por_id():
    imprimir_titulo("VER ESTUDIANTE POR ID")
    try:
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    estudiante = obtener_por_id(id_estudiante)
    if not estudiante:
        imprimir_error(f"No existe un estudiante con id {id_estudiante}")
    else:
        for clave, valor in estudiante.a_diccionario().items():
            print(f"  {clave.capitalize():<12}: {valor}")
    pausa()


# ---------- U · ACTUALIZAR ----------
def opcion_actualizar():
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")
    try:
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    estudiante = obtener_por_id(id_estudiante)
    if not estudiante:
        imprimir_error(f"No existe un estudiante con id {id_estudiante}")
        return pausa()

    imprimir_info(f"Editando a {estudiante.obtener_nombre_completo()}")
    print("Deje en blanco el campo que no quiera cambiar.\n")

    # Armo un DICCIONARIO solo con lo que el usuario escribió
    cambios = {}
    for campo in CAMPOS_ESTUDIANTE:
        if campo not in("notas", "materias"):  
         actual = getattr(estudiante, campo)
         nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
         if nuevo:
             cambios[campo] = nuevo

    exito, mensaje = actualizar_estudiante(id_estudiante, cambios)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()


# ---------- D · ELIMINAR ----------
def opcion_eliminar():
    imprimir_titulo("ELIMINAR ESTUDIANTE")
    try:
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    estudiante = obtener_por_id(id_estudiante)
    if not estudiante:
        imprimir_error(f"No existe un estudiante con id {id_estudiante}")
        return pausa()

    imprimir_info(f"Se eliminará: {estudiante}")
    if confirmar("¿Confirma la eliminación?"):
        exito, mensaje = eliminar_estudiante(id_estudiante)
        if exito:
            imprimir_exito(mensaje)
        else:
            imprimir_error(mensaje)
    else:
        imprimir_info("Operación cancelada")
    pausa()



def salir():
    imprimir_info("¡Hasta luego! 👋")
    return "salir"


# DICCIONARIO de opciones: tecla -> (texto del menú, función)
OPCIONES = {
    "1": ("Crear estudiante", opcion_crear),
    "2": ("Ver todos", opcion_ver_todos),
    "3": ("Buscar", opcion_buscar),
    "4": ("Ver por id", opcion_ver_por_id),
    "5": ("Actualizar", opcion_actualizar),
    "6": ("Eliminar", opcion_eliminar),
    "7": ("Agregar nota", opcion_agregar_nota),
    "8": ("Ver promedio", opcion_ver_promedio),
    "9": ("Materias en común", opcion_materias_en_comun),
    "0": ("Salir", salir),
}



def mostrar_menu():
    imprimir_titulo("SISTEMA DE GESTIÓN DE ESTUDIANTES")
    for tecla, (texto, _funcion) in OPCIONES.items():
        print(f"  {tecla}. {texto}")
    print()


def main():
    while True:
        mostrar_menu()
        tecla = input("Seleccione una opción: ").strip()

        if tecla not in OPCIONES:          # búsqueda instantánea por clave
            imprimir_error("Opción no válida")
            pausa()
            continue

        _texto, funcion = OPCIONES[tecla]
        if funcion() == "salir":
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")