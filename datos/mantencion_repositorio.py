from datos.modelos.models import Mantencion, Taller, TipoMantencion, Vehiculo


def listar_talleres():
    return list(Taller.select().where(Taller.habilitado == True))


def listar_tipos_mantencion():
    return list(
        TipoMantencion.select().where(TipoMantencion.habilitado == True)
    )


def listar_repuestos():
    from datos.modelos.models import Repuesto

    return list(Repuesto.select().where(Repuesto.habilitado == True))


def obtener_mantencion(id_mantencion):
    return Mantencion.get_or_none(Mantencion.id_mantencion == id_mantencion)


def guardar_mantencion(mantencion):
    mantencion.save(force_insert=True)
    return mantencion


def actualizar_mantencion(mantencion):
    mantencion.save()
    return mantencion


def historial_por_vehiculo(id_vehiculo):
    return list(
        Mantencion.select(Mantencion, Taller, TipoMantencion)
        .join(Taller)
        .switch(Mantencion)
        .join(TipoMantencion)
        .where(Mantencion.vehiculo == id_vehiculo)
        .order_by(Mantencion.fecha_ingreso.desc())
    )


def listar_mantenciones_pendientes():
    return list(
        Mantencion.select(Mantencion, Vehiculo, TipoMantencion, Taller)
        .join(Vehiculo)
        .switch(Mantencion)
        .join(TipoMantencion)
        .switch(Mantencion)
        .join(Taller)
        .where(Mantencion.estado == "PENDIENTE")
        .order_by(Mantencion.fecha_ingreso)
    )
