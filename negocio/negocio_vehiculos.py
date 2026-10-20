from peewee import IntegrityError

from datos.auxiliar import (
    entero_positivo,
    normalizar_patente,
    normalizar_vin,
    texto_obligatorio,
    validar_anio,
)
from datos.modelos.models import (
    ModeloVehiculo,
    Propietario,
    TipoVehiculo,
    Vehiculo,
)
from datos.repositorio import vehiculo_repositorio as repositorio


def listar_vehiculos():
    return repositorio.listar_vehiculos()


def obtener_vehiculo(id_vehiculo):
    id_vehiculo = entero_positivo(id_vehiculo, "ID del vehículo")
    vehiculo = repositorio.obtener_vehiculo(id_vehiculo)
    if vehiculo is None:
        raise ValueError("No existe un vehículo con ese ID.")
    return vehiculo


def crear_vehiculo(datos):
    propietario = Propietario.get_or_none(
        Propietario.id_propietario == entero_positivo(
            datos["propietario_id"], "ID del propietario"
        )
    )
    tipo = TipoVehiculo.get_or_none(
        TipoVehiculo.id_tipo_vehiculo == entero_positivo(
            datos["tipo_vehiculo_id"], "ID del tipo de vehículo"
        )
    )
    modelo = ModeloVehiculo.get_or_none(
        ModeloVehiculo.id_modelo == entero_positivo(
            datos["modelo_id"], "ID del modelo"
        )
    )
    if propietario is None or tipo is None or modelo is None:
        raise ValueError("Selecciona un propietario, tipo y modelo existentes.")

    vehiculo = Vehiculo(
        patente=normalizar_patente(datos["patente"]),
        vin=normalizar_vin(datos["vin"]),
        propietario=propietario,
        tipo=tipo,
        modelo=modelo,
        anio=validar_anio(datos["anio"]),
        color=texto_obligatorio(datos["color"], "Color"),
        kilometraje=entero_positivo(
            datos["kilometraje"], "Kilometraje", permitir_cero=True
        ),
        estado="ACTIVO",
    )
    vehiculo.validar()
    try:
        return repositorio.guardar_vehiculo(vehiculo)
    except IntegrityError as error:
        raise ValueError(repositorio.traducir_error_integridad(error)) from error


def actualizar_vehiculo(id_vehiculo, datos):
    vehiculo = obtener_vehiculo(id_vehiculo)
    propietario = Propietario.get_or_none(
        Propietario.id_propietario == entero_positivo(
            datos["propietario_id"], "ID del propietario"
        )
    )
    tipo = TipoVehiculo.get_or_none(
        TipoVehiculo.id_tipo_vehiculo == entero_positivo(
            datos["tipo_vehiculo_id"], "ID del tipo de vehículo"
        )
    )
    modelo = ModeloVehiculo.get_or_none(
        ModeloVehiculo.id_modelo == entero_positivo(
            datos["modelo_id"], "ID del modelo"
        )
    )
    if propietario is None or tipo is None or modelo is None:
        raise ValueError("Selecciona un propietario, tipo y modelo existentes.")

    vehiculo.patente = normalizar_patente(datos["patente"])
    vehiculo.vin = normalizar_vin(datos["vin"])
    vehiculo.propietario = propietario
    vehiculo.tipo = tipo
    vehiculo.modelo = modelo
    vehiculo.anio = validar_anio(datos["anio"])
    vehiculo.color = texto_obligatorio(datos["color"], "Color")
    vehiculo.kilometraje = entero_positivo(
        datos["kilometraje"], "Kilometraje", permitir_cero=True
    )
    vehiculo.estado = datos.get("estado", vehiculo.estado)
    try:
        return repositorio.actualizar_vehiculo(vehiculo)
    except IntegrityError as error:
        raise ValueError(repositorio.traducir_error_integridad(error)) from error


def eliminar_vehiculo(id_vehiculo):
    vehiculo = obtener_vehiculo(id_vehiculo)
    try:
        repositorio.eliminar_vehiculo(vehiculo)
    except IntegrityError as error:
        raise ValueError(
            "No se puede eliminar: el vehículo tiene mantenciones relacionadas."
        ) from error
    return True


def obtener_catalogos():
    return repositorio.obtener_catalogos()
