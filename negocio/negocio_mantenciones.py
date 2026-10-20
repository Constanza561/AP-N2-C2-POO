from datetime import date
from decimal import Decimal

from peewee import IntegrityError

from datos.auxiliar import entero_positivo, texto_obligatorio, validar_monto
from datos.modelos.models import (
    Mantencion,
    MantencionRepuesto,
    Repuesto,
    Taller,
    TipoMantencion,
    Vehiculo,
)
from datos.repositorio import mantencion_repositorio as repositorio
from negocio.trabajos import MantencionPreventiva, Reparacion


def registrar_mantencion(datos):
    vehiculo = Vehiculo.get_or_none(
        Vehiculo.id_vehiculo
        == entero_positivo(datos["vehiculo_id"], "ID del vehículo")
    )
    taller = Taller.get_or_none(
        Taller.id_taller == entero_positivo(datos["taller_id"], "ID del taller")
    )
    tipo = TipoMantencion.get_or_none(
        TipoMantencion.id_tipo_mantencion
        == entero_positivo(datos["tipo_mantencion_id"], "ID del tipo de mantención")
    )
    if vehiculo is None or taller is None or tipo is None:
        raise ValueError("El vehículo, taller o tipo de mantención no existe.")

    tipo_trabajo = texto_obligatorio(datos["tipo_trabajo"], "Tipo de trabajo").upper()
    mano_obra = validar_monto(datos["costo_mano_obra"], "Costo de mano de obra")
    diagnostico = validar_monto(
        datos.get("costo_diagnostico", "0") or "0",
        "Costo de diagnóstico",
    )
    kilometraje = entero_positivo(
        datos["kilometraje"], "Kilometraje", permitir_cero=True
    )

    seleccion = {}
    for item in datos.get("repuestos", []):
        id_repuesto = entero_positivo(item["id_repuesto"], "ID del repuesto")
        cantidad = entero_positivo(item["cantidad"], "Cantidad")
        seleccion[id_repuesto] = seleccion.get(id_repuesto, 0) + cantidad

    if tipo_trabajo == "PREVENTIVA":
        clase_trabajo = MantencionPreventiva
    elif tipo_trabajo == "REPARACION":
        clase_trabajo = Reparacion
    else:
        raise ValueError("Tipo de trabajo: PREVENTIVA o REPARACION.")

    base_datos = vehiculo._meta.database
    try:
        with base_datos.atomic():
            repuestos = []
            costo_repuestos = Decimal("0")
            for id_repuesto, cantidad in seleccion.items():
                repuesto = Repuesto.get_or_none(
                    Repuesto.id_repuesto == id_repuesto
                )
                if repuesto is None or not repuesto.habilitado:
                    raise ValueError(f"No existe el repuesto con ID {id_repuesto}.")
                if repuesto.stock < cantidad:
                    raise ValueError(
                        f"Stock insuficiente para {repuesto.nombre}. "
                        f"Disponible: {repuesto.stock}."
                    )
                costo_repuestos += repuesto.precio_unitario * cantidad
                repuestos.append((repuesto, cantidad))

            if tipo_trabajo == "PREVENTIVA":
                calculador = clase_trabajo(mano_obra, costo_repuestos)
            else:
                calculador = clase_trabajo(
                    mano_obra,
                    costo_repuestos,
                    costo_diagnostico=diagnostico,
                )

            mantencion = Mantencion(
                vehiculo=vehiculo,
                taller=taller,
                tipo_mantencion=tipo,
                fecha_ingreso=date.today(),
                tipo_trabajo=tipo_trabajo,
                kilometraje=kilometraje,
                observaciones=(datos.get("observaciones") or "").strip() or None,
                costo_mano_obra=mano_obra + diagnostico,
                costo_repuestos=costo_repuestos,
                costo_total=calculador.calcular_costo(),
                estado="PENDIENTE",
            )
            repositorio.guardar_mantencion(mantencion)

            for repuesto, cantidad in repuestos:
                MantencionRepuesto.create(
                    mantencion=mantencion,
                    repuesto=repuesto,
                    cantidad=cantidad,
                    precio_unitario=repuesto.precio_unitario,
                )
                repuesto.stock -= cantidad
                repuesto.save()

            vehiculo.kilometraje = max(vehiculo.kilometraje, kilometraje)
            vehiculo.estado = "EN_MANTENCION"
            vehiculo.save()
            return mantencion
    except IntegrityError as error:
        raise ValueError("No se pudo guardar la mantención.") from error


def historial_por_vehiculo(id_vehiculo):
    id_vehiculo = entero_positivo(id_vehiculo, "ID del vehículo")
    if Vehiculo.get_or_none(Vehiculo.id_vehiculo == id_vehiculo) is None:
        raise ValueError("No existe un vehículo con ese ID.")
    return repositorio.historial_por_vehiculo(id_vehiculo)


def mantenciones_pendientes():
    return repositorio.listar_mantenciones_pendientes()


def completar_mantencion(id_mantencion):
    id_mantencion = entero_positivo(id_mantencion, "ID de la mantención")
    mantencion = repositorio.obtener_mantencion(id_mantencion)
    if mantencion is None:
        raise ValueError("No existe una mantención con ese ID.")
    if mantencion.estado == "COMPLETADA":
        raise ValueError("La mantención ya está completada.")

    base_datos = mantencion._meta.database
    with base_datos.atomic():
        mantencion.estado = "COMPLETADA"
        repositorio.actualizar_mantencion(mantencion)
        existen_pendientes = Mantencion.select().where(
            (Mantencion.vehiculo == mantencion.vehiculo_id)
            & (Mantencion.estado == "PENDIENTE")
        ).exists()
        if not existen_pendientes:
            vehiculo = mantencion.vehiculo
            vehiculo.estado = "ACTIVO"
            vehiculo.save()
    return mantencion


def obtener_catalogos_mantencion():
    return {
        "talleres": repositorio.listar_talleres(),
        "tipos": repositorio.listar_tipos_mantencion(),
        "repuestos": repositorio.listar_repuestos(),
    }
