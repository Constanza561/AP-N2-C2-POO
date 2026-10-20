from negocio import negocio_mantenciones


def mostrar_historial(id_vehiculo):
    historial = negocio_mantenciones.historial_por_vehiculo(id_vehiculo)
    if not historial:
        print("No hay mantenciones registradas para este vehículo.")
        return

    print("\nHISTORIAL DE MANTENCIONES")
    print("-" * 32)
    for mantencion in historial:
        print(f"ID: {mantencion.id_mantencion}")
        print(f"Fecha: {mantencion.fecha_ingreso}")
        print(
            f"Tipo: {mantencion.tipo_trabajo} — "
            f"{mantencion.tipo_mantencion.nombre}"
        )
        print(f"Taller: {mantencion.taller.nombre}")
        print(f"Kilometraje: {mantencion.kilometraje:,} km")
        print(f"Estado: {mantencion.estado}")
        print(f"Costo total: ${mantencion.costo_total:,.0f}")
        print(f"Observaciones: {mantencion.observaciones or 'Sin observaciones'}")
        for detalle in mantencion.repuestos_utilizados:
            print(
                f"Repuesto: {detalle.repuesto.nombre} "
                f"| cantidad: {detalle.cantidad} "
                f"| precio: ${detalle.precio_unitario:,.0f}"
            )
        print("-" * 32)


def mostrar_pendientes():
    pendientes = negocio_mantenciones.mantenciones_pendientes()
    if not pendientes:
        print("No hay mantenciones pendientes.")
        return

    print("\nMANTENCIONES PENDIENTES")
    print("-" * 32)
    for mantencion in pendientes:
        print(f"ID: {mantencion.id_mantencion}")
        print(f"Vehículo: {mantencion.vehiculo.patente}")
        print(f"Trabajo: {mantencion.tipo_trabajo}")
        print(f"Fecha: {mantencion.fecha_ingreso}")
        print(f"Estado: {mantencion.estado}")
        print("-" * 32)
