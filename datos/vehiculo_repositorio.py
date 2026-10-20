from peewee import IntegrityError

from datos.modelos.models import (
    Marca,
    ModeloVehiculo,
    Propietario,
    TipoVehiculo,
    Vehiculo,
)


def listar_vehiculos():
    consulta = (
        Vehiculo.select(
            Vehiculo,
            Propietario,
            TipoVehiculo,
            ModeloVehiculo,
            Marca,
        )
        .join(Propietario)
        .switch(Vehiculo)
        .join(TipoVehiculo)
        .switch(Vehiculo)
        .join(ModeloVehiculo)
        .join(Marca)
        .order_by(Vehiculo.id_vehiculo)
    )
    return list(consulta)


def obtener_vehiculo(id_vehiculo):
    return Vehiculo.get_or_none(Vehiculo.id_vehiculo == id_vehiculo)


def guardar_vehiculo(vehiculo):
    vehiculo.validar()
    vehiculo.save(force_insert=True)
    return vehiculo


def actualizar_vehiculo(vehiculo):
    vehiculo.validar()
    vehiculo.save()
    return vehiculo


def eliminar_vehiculo(vehiculo):
    return vehiculo.delete_instance()


def obtener_catalogos():
    return {
        "propietarios": list(Propietario.select().where(Propietario.habilitado == True)),
        "tipos": list(TipoVehiculo.select().where(TipoVehiculo.habilitado == True)),
        "modelos": list(
            ModeloVehiculo.select(ModeloVehiculo, Marca)
            .join(Marca)
            .where(ModeloVehiculo.habilitado == True)
        ),
    }


def traducir_error_integridad(error):
    mensaje = str(error).lower()
    if "patente" in mensaje:
        return "Ya existe un vehículo con esa patente."
    if "vin" in mensaje:
        return "Ya existe un vehículo con ese VIN."
    return "No se pudo completar la operación por una relación o dato duplicado."
