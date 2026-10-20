from decimal import Decimal

from peewee import (
    AutoField,
    BooleanField,
    CharField,
    DateField,
    DecimalField,
    ForeignKeyField,
    IntegerField,
    Model,
    TextField,
)

from datos.conexion import conectar


base_datos = conectar()


class BaseModel(Model):
    """Modelo base que comparte conexión y operaciones comunes."""

    class Meta:
        database = base_datos

    def guardar(self):
        self.save()
        return self

    def eliminar(self):
        return self.delete_instance()

    def existe(self):
        id_registro = self.get_id()
        if id_registro is None:
            return False
        return self.__class__.get_or_none(id_registro) is not None

    def nombre_tabla(self):
        return self._meta.table_name


class Propietario(BaseModel):
    id_propietario = AutoField()
    rut = CharField(max_length=12, unique=True)
    nombre = CharField(max_length=80)
    telefono = CharField(max_length=20, null=True)
    correo = CharField(max_length=120, null=True)
    habilitado = BooleanField(default=True)

    class Meta:
        table_name = "propietarios"

    def validar(self):
        if not self.rut or not self.rut.strip():
            raise ValueError("El RUT del propietario es obligatorio.")
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre del propietario es obligatorio.")
        return True

    def actualizar_contacto(self, telefono, correo):
        self.telefono = telefono.strip() if telefono else None
        self.correo = correo.strip() if correo else None
        return self

    def activar(self):
        self.habilitado = True
        return self

    def desactivar(self):
        self.habilitado = False
        return self

    def resumen(self):
        return f"{self.nombre} | RUT: {self.rut}"

    def __str__(self):
        return self.resumen()


class Marca(BaseModel):
    id_marca = AutoField()
    nombre = CharField(max_length=50, unique=True)
    habilitado = BooleanField(default=True)

    class Meta:
        table_name = "marcas"

    def validar(self):
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre de la marca es obligatorio.")
        return True

    def renombrar(self, nombre):
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre de la marca no puede estar vacío.")
        self.nombre = nombre
        return self

    def activar(self):
        self.habilitado = True
        return self

    def desactivar(self):
        self.habilitado = False
        return self

    def resumen(self):
        return f"Marca: {self.nombre}"

    def __str__(self):
        return self.nombre


class ModeloVehiculo(BaseModel):
    id_modelo = AutoField()
    marca = ForeignKeyField(
        Marca,
        backref="modelos",
        column_name="marca_id",
        on_delete="RESTRICT",
    )
    nombre = CharField(max_length=60)
    habilitado = BooleanField(default=True)

    class Meta:
        table_name = "modelos"
        indexes = ((('marca', 'nombre'), True),)

    def validar(self):
        if self.marca is None:
            raise ValueError("El modelo debe estar asociado a una marca.")
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre del modelo es obligatorio.")
        return True

    def renombrar(self, nombre):
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre del modelo no puede estar vacío.")
        self.nombre = nombre
        return self

    def activar(self):
        self.habilitado = True
        return self

    def desactivar(self):
        self.habilitado = False
        return self

    def resumen(self):
        return f"{self.marca.nombre} {self.nombre}"

    def __str__(self):
        return self.resumen()


class TipoVehiculo(BaseModel):
    id_tipo_vehiculo = AutoField()
    nombre = CharField(max_length=40, unique=True)
    habilitado = BooleanField(default=True)

    class Meta:
        table_name = "tipos_vehiculo"

    def validar(self):
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre del tipo de vehículo es obligatorio.")
        return True

    def renombrar(self, nombre):
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El tipo de vehículo no puede estar vacío.")
        self.nombre = nombre
        return self

    def activar(self):
        self.habilitado = True
        return self

    def desactivar(self):
        self.habilitado = False
        return self

    def resumen(self):
        return f"Tipo de vehículo: {self.nombre}"

    def __str__(self):
        return self.nombre


class Vehiculo(BaseModel):
    id_vehiculo = AutoField()
    patente = CharField(max_length=10, unique=True)
    vin = CharField(max_length=17, unique=True)
    propietario = ForeignKeyField(
        Propietario,
        backref="vehiculos",
        column_name="propietario_id",
        on_delete="RESTRICT",
    )
    tipo = ForeignKeyField(
        TipoVehiculo,
        backref="vehiculos",
        column_name="tipo_vehiculo_id",
        on_delete="RESTRICT",
    )
    modelo = ForeignKeyField(
        ModeloVehiculo,
        backref="vehiculos",
        column_name="modelo_id",
        on_delete="RESTRICT",
    )
    anio = IntegerField()
    color = CharField(max_length=30)
    kilometraje = IntegerField(default=0)
    estado = CharField(max_length=20, default="ACTIVO")

    class Meta:
        table_name = "vehiculos"

    def validar(self):
        from datos.auxiliar import (
            entero_positivo,
            normalizar_patente,
            normalizar_vin,
            texto_obligatorio,
            validar_anio,
        )

        self.patente = normalizar_patente(self.patente)
        self.vin = normalizar_vin(self.vin)
        self.anio = validar_anio(self.anio)
        self.kilometraje = entero_positivo(
            self.kilometraje,
            "Kilometraje",
            permitir_cero=True,
        )
        self.color = texto_obligatorio(self.color, "Color")
        if self.estado not in {"ACTIVO", "EN_MANTENCION", "INACTIVO"}:
            raise ValueError("Estado no válido para el vehículo.")
        return True

    def actualizar_kilometraje(self, kilometraje):
        from datos.auxiliar import entero_positivo

        nuevo = entero_positivo(kilometraje, "Kilometraje", permitir_cero=True)
        if nuevo < self.kilometraje:
            raise ValueError("El kilometraje no puede disminuir.")
        self.kilometraje = nuevo
        return self

    def iniciar_mantencion(self):
        if self.estado == "INACTIVO":
            raise ValueError("No se puede mantener un vehículo inactivo.")
        self.estado = "EN_MANTENCION"
        return self

    def finalizar_mantencion(self):
        self.estado = "ACTIVO"
        return self

    def esta_disponible(self):
        return self.estado == "ACTIVO"

    def identificacion(self):
        return f"{self.patente} | {self.modelo} | {self.anio}"

    def __str__(self):
        return self.identificacion()


class Taller(BaseModel):
    id_taller = AutoField()
    nombre = CharField(max_length=80)
    direccion = CharField(max_length=120, null=True)
    telefono = CharField(max_length=20, null=True)
    habilitado = BooleanField(default=True)

    class Meta:
        table_name = "talleres"

    def validar(self):
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre del taller es obligatorio.")
        return True

    def activar(self):
        self.habilitado = True
        return self

    def desactivar(self):
        self.habilitado = False
        return self

    def actualizar_contacto(self, direccion, telefono):
        self.direccion = direccion.strip() if direccion else None
        self.telefono = telefono.strip() if telefono else None
        return self

    def ficha(self):
        return f"{self.nombre} | {self.direccion or 'Sin dirección'}"

    def __str__(self):
        return self.nombre


class Mecanico(BaseModel):
    id_mecanico = AutoField()
    taller = ForeignKeyField(
        Taller,
        backref="mecanicos",
        column_name="taller_id",
        on_delete="RESTRICT",
    )
    rut = CharField(max_length=12, unique=True)
    nombre = CharField(max_length=80)
    especialidad = CharField(max_length=60, null=True)
    habilitado = BooleanField(default=True)

    class Meta:
        table_name = "mecanicos"

    def validar(self):
        if not self.rut or not self.rut.strip():
            raise ValueError("El RUT del mecánico es obligatorio.")
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre del mecánico es obligatorio.")
        if self.taller is None:
            raise ValueError("El mecánico debe pertenecer a un taller.")
        return True

    def activar(self):
        self.habilitado = True
        return self

    def desactivar(self):
        self.habilitado = False
        return self

    def cambiar_especialidad(self, especialidad):
        especialidad = especialidad.strip()
        if not especialidad:
            raise ValueError("La especialidad no puede estar vacía.")
        self.especialidad = especialidad
        return self

    def ficha(self):
        return f"{self.nombre} | {self.especialidad or 'Sin especialidad'}"

    def __str__(self):
        return self.ficha()


class TipoMantencion(BaseModel):
    id_tipo_mantencion = AutoField()
    nombre = CharField(max_length=50, unique=True)
    descripcion = CharField(max_length=150, null=True)
    intervalo_km = IntegerField(null=True)
    intervalo_meses = IntegerField(null=True)
    habilitado = BooleanField(default=True)

    class Meta:
        table_name = "tipos_mantencion"

    def validar(self):
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre del tipo de mantención es obligatorio.")
        if self.intervalo_km is not None and self.intervalo_km <= 0:
            raise ValueError("El intervalo de kilometraje debe ser positivo.")
        if self.intervalo_meses is not None and self.intervalo_meses <= 0:
            raise ValueError("El intervalo de meses debe ser positivo.")
        return True

    def requiere_programacion(self):
        return self.intervalo_km is not None or self.intervalo_meses is not None

    def actualizar_intervalos(self, kilometros=None, meses=None):
        if kilometros is not None and kilometros <= 0:
            raise ValueError("El intervalo de kilometraje debe ser positivo.")
        if meses is not None and meses <= 0:
            raise ValueError("El intervalo de meses debe ser positivo.")
        self.intervalo_km = kilometros
        self.intervalo_meses = meses
        return self

    def activar(self):
        self.habilitado = True
        return self

    def desactivar(self):
        self.habilitado = False
        return self

    def resumen(self):
        return f"{self.nombre} | cada {self.intervalo_km or '—'} km"

    def __str__(self):
        return self.nombre


class Mantencion(BaseModel):
    id_mantencion = AutoField()
    vehiculo = ForeignKeyField(
        Vehiculo,
        backref="mantenciones",
        column_name="vehiculo_id",
        on_delete="RESTRICT",
    )
    taller = ForeignKeyField(
        Taller,
        backref="mantenciones",
        column_name="taller_id",
        on_delete="RESTRICT",
    )
    tipo_mantencion = ForeignKeyField(
        TipoMantencion,
        backref="mantenciones",
        column_name="tipo_mantencion_id",
        on_delete="RESTRICT",
    )
    fecha_ingreso = DateField()
    tipo_trabajo = CharField(max_length=20)
    kilometraje = IntegerField()
    observaciones = TextField(null=True)
    costo_mano_obra = DecimalField(max_digits=10, decimal_places=2, default=0)
    costo_repuestos = DecimalField(max_digits=10, decimal_places=2, default=0)
    costo_total = DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = CharField(max_length=20, default="PENDIENTE")

    class Meta:
        table_name = "mantenciones"

    def validar(self):
        if self.tipo_trabajo not in {"PREVENTIVA", "REPARACION"}:
            raise ValueError("El tipo de trabajo debe ser PREVENTIVA o REPARACION.")
        if self.kilometraje < 0:
            raise ValueError("El kilometraje no puede ser negativo.")
        if self.costo_mano_obra < 0 or self.costo_repuestos < 0:
            raise ValueError("Los costos no pueden ser negativos.")
        return True

    def calcular_costo_total(self):
        self.costo_total = Decimal(self.costo_mano_obra) + Decimal(
            self.costo_repuestos
        )
        return self.costo_total

    def completar(self):
        if self.estado == "COMPLETADA":
            raise ValueError("La mantención ya está completada.")
        self.estado = "COMPLETADA"
        return self

    def cancelar(self, motivo):
        if self.estado == "COMPLETADA":
            raise ValueError("No se puede cancelar una mantención completada.")
        self.estado = "CANCELADA"
        self.observaciones = motivo.strip() if motivo else self.observaciones
        return self

    def resumen(self):
        return (
            f"Mantención {self.id_mantencion} | {self.fecha_ingreso} | "
            f"{self.tipo_trabajo} | {self.estado}"
        )

    def __str__(self):
        return self.resumen()


class Repuesto(BaseModel):
    id_repuesto = AutoField()
    codigo = CharField(max_length=30, unique=True)
    nombre = CharField(max_length=80)
    stock = IntegerField(default=0)
    precio_unitario = DecimalField(max_digits=10, decimal_places=2, default=0)
    habilitado = BooleanField(default=True)

    class Meta:
        table_name = "repuestos"

    def validar(self):
        if not self.codigo or not self.codigo.strip():
            raise ValueError("El código del repuesto es obligatorio.")
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre del repuesto es obligatorio.")
        if self.stock < 0 or self.precio_unitario < 0:
            raise ValueError("El stock y el precio no pueden ser negativos.")
        return True

    def actualizar_stock(self, cantidad):
        if cantidad < 0:
            raise ValueError("El stock no puede ser negativo.")
        self.stock = cantidad
        return self

    def retirar_stock(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser positiva.")
        if cantidad > self.stock:
            raise ValueError("No existe suficiente stock disponible.")
        self.stock -= cantidad
        return self

    def ingresar_stock(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser positiva.")
        self.stock += cantidad
        return self

    def subtotal(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser positiva.")
        return self.precio_unitario * cantidad

    def __str__(self):
        return f"{self.nombre} | stock: {self.stock}"


class MantencionRepuesto(BaseModel):
    id_mantencion_repuesto = AutoField()
    mantencion = ForeignKeyField(
        Mantencion,
        backref="repuestos_utilizados",
        column_name="mantencion_id",
        on_delete="RESTRICT",
    )
    repuesto = ForeignKeyField(
        Repuesto,
        backref="uso_en_mantenciones",
        column_name="repuesto_id",
        on_delete="RESTRICT",
    )
    cantidad = IntegerField()
    precio_unitario = DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        table_name = "mantencion_repuesto"
        indexes = ((('mantencion', 'repuesto'), True),)

    def validar(self):
        if self.cantidad <= 0:
            raise ValueError("La cantidad de repuestos debe ser positiva.")
        if self.precio_unitario < 0:
            raise ValueError("El precio unitario no puede ser negativo.")
        return True

    def calcular_subtotal(self):
        return self.precio_unitario * self.cantidad

    def cambiar_cantidad(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad de repuestos debe ser positiva.")
        self.cantidad = cantidad
        return self

    def cambiar_precio(self, precio):
        precio = Decimal(str(precio))
        if precio < 0:
            raise ValueError("El precio unitario no puede ser negativo.")
        self.precio_unitario = precio
        return self

    def resumen(self):
        return f"{self.repuesto.nombre} x {self.cantidad}"

    def __str__(self):
        return self.resumen()
