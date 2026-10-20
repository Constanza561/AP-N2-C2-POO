from peewee import OperationalError

from datos.conexion import conectar
from datos.modelos.models import (
    Mantencion,
    MantencionRepuesto,
    Marca,
    Mecanico,
    ModeloVehiculo,
    Propietario,
    Repuesto,
    Taller,
    TipoMantencion,
    TipoVehiculo,
    Vehiculo,
)
from presentacion.menu import cargar_menu


MODELOS = [
    Propietario,
    Marca,
    ModeloVehiculo,
    TipoVehiculo,
    Vehiculo,
    Taller,
    Mecanico,
    TipoMantencion,
    Mantencion,
    Repuesto,
    MantencionRepuesto,
]


def inicializar_datos_demo():
    propietario, _ = Propietario.get_or_create(
        rut="11111111-1",
        defaults={
            "nombre": "Propietario Demo",
            "telefono": "900000000",
            "correo": "demo@ejemplo.cl",
        },
    )
    marca, _ = Marca.get_or_create(nombre="Toyota")
    modelo, _ = ModeloVehiculo.get_or_create(
        marca=marca,
        nombre="Corolla",
    )
    tipo_vehiculo, _ = TipoVehiculo.get_or_create(nombre="Automóvil")
    taller, _ = Taller.get_or_create(
        nombre="Taller Central",
        defaults={"direccion": "Av. Principal 100", "telefono": "900000001"},
    )
    TipoMantencion.get_or_create(
        nombre="Mantención preventiva",
        defaults={"descripcion": "Servicio periódico", "intervalo_km": 10000},
    )
    TipoMantencion.get_or_create(
        nombre="Reparación",
        defaults={"descripcion": "Reparación correctiva"},
    )
    Repuesto.get_or_create(
        codigo="FILTRO-DEMO",
        defaults={
            "nombre": "Filtro de aceite de demostración",
            "stock": 10,
            "precio_unitario": 5000,
        },
    )
    Vehiculo.get_or_create(
        patente="DEMO01",
        defaults={
            "vin": "JTDBR32E720123456",
            "propietario": propietario,
            "tipo": tipo_vehiculo,
            "modelo": modelo,
            "anio": 2020,
            "color": "Blanco",
            "kilometraje": 45000,
            "estado": "ACTIVO",
        },
    )


def iniciar():
    base_datos = conectar()
    try:
        base_datos.connect(reuse_if_open=True)
        base_datos.create_tables(MODELOS, safe=True)
        inicializar_datos_demo()
        cargar_menu()
    except OperationalError as error:
        print("No se pudo conectar con MySQL.")
        print("Revisa que MySQL esté iniciado, que exista la base de datos")
        print("y que los datos de conexión de .env sean correctos.")
        print(f"Detalle: {error}")
    finally:
        if not base_datos.is_closed():
            base_datos.close()


if __name__ == "__main__":
    iniciar()
