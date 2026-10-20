from decouple import config
from peewee import MySQLDatabase


base_datos = None


def conectar():
    """Crea e inicializa la conexión MySQL de la aplicación."""
    global base_datos

    if base_datos is None:
        base_datos = MySQLDatabase(
            config("DB_NAME", default="control_vehiculos"),
            host=config("DB_HOST", default="localhost"),
            port=config("DB_PORT", default=3306, cast=int),
            user=config("DB_USER", default="root"),
            password=config("DB_PASSWORD", default=""),
            charset=config("DB_CHARSET", default="utf8mb4"),
        )

    return base_datos
