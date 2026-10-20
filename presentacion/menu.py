from peewee import IntegrityError, OperationalError

from negocio import negocio_mantenciones, negocio_vehiculos
from presentacion import presentacion_mantenciones, presentacion_vehiculos


def _leer_id(mensaje):
    return int(input(mensaje).strip())


def _mostrar_catalogos_vehiculo():
    catalogos = negocio_vehiculos.obtener_catalogos()
    print("\nPROPIETARIOS")
    for elemento in catalogos["propietarios"]:
        print(f"  {elemento.id_propietario}. {elemento.nombre}")
    print("TIPOS DE VEHÍCULO")
    for elemento in catalogos["tipos"]:
        print(f"  {elemento.id_tipo_vehiculo}. {elemento.nombre}")
    print("MODELOS")
    for elemento in catalogos["modelos"]:
        print(f"  {elemento.id_modelo}. {elemento.marca.nombre} {elemento.nombre}")


def _leer_datos_vehiculo(vehiculo=None):
    _mostrar_catalogos_vehiculo()
    if vehiculo is None:
        valores = {
            "patente": input("Patente: "),
            "vin": input("VIN (17 caracteres): "),
            "anio": input("Año: "),
            "color": input("Color: "),
            "kilometraje": input("Kilometraje: "),
        }
    else:
        valores = {
            "patente": input(f"Patente [{vehiculo.patente}]: ").strip()
            or vehiculo.patente,
            "vin": input(f"VIN [{vehiculo.vin}]: ").strip() or vehiculo.vin,
            "anio": input(f"Año [{vehiculo.anio}]: ").strip() or vehiculo.anio,
            "color": input(f"Color [{vehiculo.color}]: ").strip() or vehiculo.color,
            "kilometraje": input(
                f"Kilometraje [{vehiculo.kilometraje}]: "
            ).strip()
            or vehiculo.kilometraje,
        }

    propietarios_id = vehiculo.propietario.id_propietario if vehiculo else ""
    tipos_id = vehiculo.tipo.id_tipo_vehiculo if vehiculo else ""
    modelos_id = vehiculo.modelo.id_modelo if vehiculo else ""
    valores["propietario_id"] = input(
        f"ID propietario [{propietarios_id}]: "
    ).strip() or propietarios_id
    valores["tipo_vehiculo_id"] = input(
        f"ID tipo de vehículo [{tipos_id}]: "
    ).strip() or tipos_id
    valores["modelo_id"] = input(
        f"ID modelo [{modelos_id}]: "
    ).strip() or modelos_id
    return valores


def _registrar_vehiculo():
    nuevo = negocio_vehiculos.crear_vehiculo(_leer_datos_vehiculo())
    print(f"Vehículo registrado con ID {nuevo.id_vehiculo}.")


def _actualizar_vehiculo():
    id_vehiculo = _leer_id("ID del vehículo que desea actualizar: ")
    actual = negocio_vehiculos.obtener_vehiculo(id_vehiculo)
    datos = _leer_datos_vehiculo(actual)
    print(f"Estado actual: {actual.estado}")
    nuevo_estado = input(
        "Nuevo estado [ACTIVO/EN_MANTENCION/INACTIVO; Enter conserva]: "
    ).strip().upper()
    if nuevo_estado:
        datos["estado"] = nuevo_estado
    actualizado = negocio_vehiculos.actualizar_vehiculo(id_vehiculo, datos)
    print(f"Vehículo {actualizado.id_vehiculo} actualizado.")


def _eliminar_vehiculo():
    id_vehiculo = _leer_id("ID del vehículo que desea eliminar: ")
    vehiculo = negocio_vehiculos.obtener_vehiculo(id_vehiculo)
    confirmacion = input(
        f"¿Eliminar {vehiculo.patente}? Escriba SI para confirmar: "
    ).strip().upper()
    if confirmacion == "SI":
        negocio_vehiculos.eliminar_vehiculo(id_vehiculo)
        print("Vehículo eliminado.")
    else:
        print("Operación cancelada.")


def _registrar_mantencion():
    vehiculos = negocio_vehiculos.listar_vehiculos()
    print("\nVEHÍCULOS")
    for vehiculo in vehiculos:
        print(f"  {vehiculo.id_vehiculo}. {vehiculo.patente} — {vehiculo.modelo}")

    catalogos = negocio_mantenciones.obtener_catalogos_mantencion()
    print("\nTALLERES")
    for taller in catalogos["talleres"]:
        print(f"  {taller.id_taller}. {taller.nombre}")
    print("TIPOS DE MANTENCIÓN")
    for tipo in catalogos["tipos"]:
        print(f"  {tipo.id_tipo_mantencion}. {tipo.nombre}")
    print("REPUESTOS DISPONIBLES")
    for repuesto in catalogos["repuestos"]:
        print(
            f"  {repuesto.id_repuesto}. {repuesto.nombre} "
            f"| stock: {repuesto.stock} | ${repuesto.precio_unitario:,.0f}"
        )

    seleccion_repuestos = []
    while True:
        id_repuesto = input(
            "ID del repuesto (Enter para terminar): "
        ).strip()
        if not id_repuesto:
            break
        cantidad = input("Cantidad: ").strip()
        seleccion_repuestos.append(
            {"id_repuesto": id_repuesto, "cantidad": cantidad}
        )

    datos = {
        "vehiculo_id": input("ID del vehículo: "),
        "taller_id": input("ID del taller: "),
        "tipo_mantencion_id": input("ID del tipo de mantención: "),
        "tipo_trabajo": input("Tipo de trabajo [PREVENTIVA/REPARACION]: "),
        "kilometraje": input("Kilometraje de ingreso: "),
        "costo_mano_obra": input("Costo de mano de obra: "),
        "costo_diagnostico": input("Costo de diagnóstico [0]: ") or "0",
        "observaciones": input("Observaciones (opcional): "),
        "repuestos": seleccion_repuestos,
    }
    mantencion = negocio_mantenciones.registrar_mantencion(datos)
    print(
        f"Mantención {mantencion.id_mantencion} registrada. "
        f"Total: ${mantencion.costo_total:,.0f}."
    )


def _completar_mantencion():
    id_mantencion = _leer_id("ID de la mantención completada: ")
    mantencion = negocio_mantenciones.completar_mantencion(id_mantencion)
    print(f"Mantención {mantencion.id_mantencion} marcada como COMPLETADA.")


def mostrar_menu():
    print("\nCONTROL DE VEHÍCULOS Y MANTENCIONES")
    print("1. Listar vehículos")
    print("2. Consultar vehículo por ID")
    print("3. Registrar vehículo")
    print("4. Actualizar vehículo")
    print("5. Eliminar vehículo")
    print("6. Registrar mantención")
    print("7. Consultar historial de mantenciones")
    print("8. Ver mantenciones pendientes")
    print("9. Marcar mantención como completada")
    print("0. Salir")


def cargar_menu():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()
        try:
            if opcion == "1":
                presentacion_vehiculos.mostrar_vehiculos()
            elif opcion == "2":
                vehiculo = negocio_vehiculos.obtener_vehiculo(
                    _leer_id("ID del vehículo: ")
                )
                presentacion_vehiculos.mostrar_vehiculo(vehiculo)
            elif opcion == "3":
                _registrar_vehiculo()
            elif opcion == "4":
                _actualizar_vehiculo()
            elif opcion == "5":
                _eliminar_vehiculo()
            elif opcion == "6":
                _registrar_mantencion()
            elif opcion == "7":
                presentacion_mantenciones.mostrar_historial(
                    _leer_id("ID del vehículo: ")
                )
            elif opcion == "8":
                presentacion_mantenciones.mostrar_pendientes()
            elif opcion == "9":
                _completar_mantencion()
            elif opcion == "0":
                print("Aplicación finalizada.")
                break
            else:
                print("Opción inválida. Intente nuevamente.")
        except ValueError as error:
            print(f"No se pudo completar la operación: {error}")
        except IntegrityError:
            print("La operación no se pudo completar por una relación existente.")
        except OperationalError as error:
            print(f"Error de base de datos: {error}")
        except KeyboardInterrupt:
            print("\nAplicación finalizada.")
            break
