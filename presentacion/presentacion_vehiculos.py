from negocio import negocio_vehiculos


def mostrar_vehiculos():
    vehiculos = negocio_vehiculos.listar_vehiculos()
    if not vehiculos:
        print("No hay vehículos registrados.")
        return

    print("\nVEHÍCULOS REGISTRADOS")
    print("-" * 32)
    for vehiculo in vehiculos:
        print(f"ID: {vehiculo.id_vehiculo}")
        print(f"Patente: {vehiculo.patente}")
        print(f"VIN: {vehiculo.vin}")
        print(f"Vehículo: {vehiculo.modelo}")
        print(f"Tipo: {vehiculo.tipo.nombre}")
        print(f"Propietario: {vehiculo.propietario.nombre}")
        print(f"Año: {vehiculo.anio} | Color: {vehiculo.color}")
        print(f"Kilometraje: {vehiculo.kilometraje:,} km")
        print(f"Estado: {vehiculo.estado}")
        print("-" * 32)


def mostrar_vehiculo(vehiculo):
    print("\nDETALLE DEL VEHÍCULO")
    print("-" * 32)
    print(f"ID: {vehiculo.id_vehiculo}")
    print(f"Patente: {vehiculo.patente}")
    print(f"VIN: {vehiculo.vin}")
    print(f"Vehículo: {vehiculo.modelo}")
    print(f"Tipo: {vehiculo.tipo.nombre}")
    print(f"Propietario: {vehiculo.propietario.nombre}")
    print(f"Año: {vehiculo.anio} | Color: {vehiculo.color}")
    print(f"Kilometraje: {vehiculo.kilometraje:,} km")
    print(f"Estado: {vehiculo.estado}")
    print("-" * 32)
