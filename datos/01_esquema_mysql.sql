CREATE DATABASE IF NOT EXISTS control_vehiculos
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE control_vehiculos;

CREATE TABLE IF NOT EXISTS propietarios (
    id_propietario INTEGER AUTO_INCREMENT,
    rut VARCHAR(12) NOT NULL,
    nombre VARCHAR(80) NOT NULL,
    telefono VARCHAR(20) NULL,
    correo VARCHAR(120) NULL,
    habilitado TINYINT NOT NULL DEFAULT 1,
    CONSTRAINT pk_propietarios PRIMARY KEY (id_propietario),
    CONSTRAINT uq_propietarios_rut UNIQUE (rut)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS marcas (
    id_marca INTEGER AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    habilitado TINYINT NOT NULL DEFAULT 1,
    CONSTRAINT pk_marcas PRIMARY KEY (id_marca),
    CONSTRAINT uq_marcas_nombre UNIQUE (nombre)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS modelos (
    id_modelo INTEGER AUTO_INCREMENT,
    marca_id INTEGER NOT NULL,
    nombre VARCHAR(60) NOT NULL,
    habilitado TINYINT NOT NULL DEFAULT 1,
    CONSTRAINT pk_modelos PRIMARY KEY (id_modelo),
    CONSTRAINT uq_modelos_marca_nombre UNIQUE (marca_id, nombre),
    CONSTRAINT fk_modelos_marcas FOREIGN KEY (marca_id)
        REFERENCES marcas (id_marca)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS tipos_vehiculo (
    id_tipo_vehiculo INTEGER AUTO_INCREMENT,
    nombre VARCHAR(40) NOT NULL,
    habilitado TINYINT NOT NULL DEFAULT 1,
    CONSTRAINT pk_tipos_vehiculo PRIMARY KEY (id_tipo_vehiculo),
    CONSTRAINT uq_tipos_vehiculo_nombre UNIQUE (nombre)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS vehiculos (
    id_vehiculo INTEGER AUTO_INCREMENT,
    patente VARCHAR(10) NOT NULL,
    vin VARCHAR(17) NOT NULL,
    propietario_id INTEGER NOT NULL,
    tipo_vehiculo_id INTEGER NOT NULL,
    modelo_id INTEGER NOT NULL,
    anio INTEGER NOT NULL,
    color VARCHAR(30) NOT NULL,
    kilometraje INTEGER NOT NULL DEFAULT 0,
    estado VARCHAR(20) NOT NULL DEFAULT 'ACTIVO',
    CONSTRAINT pk_vehiculos PRIMARY KEY (id_vehiculo),
    CONSTRAINT uq_vehiculos_patente UNIQUE (patente),
    CONSTRAINT uq_vehiculos_vin UNIQUE (vin),
    CONSTRAINT fk_vehiculos_propietarios FOREIGN KEY (propietario_id)
        REFERENCES propietarios (id_propietario),
    CONSTRAINT fk_vehiculos_tipos FOREIGN KEY (tipo_vehiculo_id)
        REFERENCES tipos_vehiculo (id_tipo_vehiculo),
    CONSTRAINT fk_vehiculos_modelos FOREIGN KEY (modelo_id)
        REFERENCES modelos (id_modelo)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS talleres (
    id_taller INTEGER AUTO_INCREMENT,
    nombre VARCHAR(80) NOT NULL,
    direccion VARCHAR(120) NULL,
    telefono VARCHAR(20) NULL,
    habilitado TINYINT NOT NULL DEFAULT 1,
    CONSTRAINT pk_talleres PRIMARY KEY (id_taller)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS mecanicos (
    id_mecanico INTEGER AUTO_INCREMENT,
    taller_id INTEGER NOT NULL,
    rut VARCHAR(12) NOT NULL,
    nombre VARCHAR(80) NOT NULL,
    especialidad VARCHAR(60) NULL,
    habilitado TINYINT NOT NULL DEFAULT 1,
    CONSTRAINT pk_mecanicos PRIMARY KEY (id_mecanico),
    CONSTRAINT uq_mecanicos_rut UNIQUE (rut),
    CONSTRAINT fk_mecanicos_talleres FOREIGN KEY (taller_id)
        REFERENCES talleres (id_taller)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS tipos_mantencion (
    id_tipo_mantencion INTEGER AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    descripcion VARCHAR(150) NULL,
    intervalo_km INTEGER NULL,
    intervalo_meses INTEGER NULL,
    habilitado TINYINT NOT NULL DEFAULT 1,
    CONSTRAINT pk_tipos_mantencion PRIMARY KEY (id_tipo_mantencion),
    CONSTRAINT uq_tipos_mantencion_nombre UNIQUE (nombre)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS mantenciones (
    id_mantencion INTEGER AUTO_INCREMENT,
    vehiculo_id INTEGER NOT NULL,
    taller_id INTEGER NOT NULL,
    tipo_mantencion_id INTEGER NOT NULL,
    fecha_ingreso DATE NOT NULL,
    tipo_trabajo VARCHAR(20) NOT NULL,
    kilometraje INTEGER NOT NULL,
    observaciones TEXT NULL,
    costo_mano_obra DECIMAL(10, 2) NOT NULL DEFAULT 0,
    costo_repuestos DECIMAL(10, 2) NOT NULL DEFAULT 0,
    costo_total DECIMAL(10, 2) NOT NULL DEFAULT 0,
    estado VARCHAR(20) NOT NULL DEFAULT 'PENDIENTE',
    CONSTRAINT pk_mantenciones PRIMARY KEY (id_mantencion),
    CONSTRAINT fk_mantenciones_vehiculos FOREIGN KEY (vehiculo_id)
        REFERENCES vehiculos (id_vehiculo),
    CONSTRAINT fk_mantenciones_talleres FOREIGN KEY (taller_id)
        REFERENCES talleres (id_taller),
    CONSTRAINT fk_mantenciones_tipos FOREIGN KEY (tipo_mantencion_id)
        REFERENCES tipos_mantencion (id_tipo_mantencion)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS repuestos (
    id_repuesto INTEGER AUTO_INCREMENT,
    codigo VARCHAR(30) NOT NULL,
    nombre VARCHAR(80) NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    precio_unitario DECIMAL(10, 2) NOT NULL DEFAULT 0,
    habilitado TINYINT NOT NULL DEFAULT 1,
    CONSTRAINT pk_repuestos PRIMARY KEY (id_repuesto),
    CONSTRAINT uq_repuestos_codigo UNIQUE (codigo)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS mantencion_repuesto (
    id_mantencion_repuesto INTEGER AUTO_INCREMENT,
    mantencion_id INTEGER NOT NULL,
    repuesto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    precio_unitario DECIMAL(10, 2) NOT NULL,
    CONSTRAINT pk_mantencion_repuesto PRIMARY KEY (id_mantencion_repuesto),
    CONSTRAINT uq_mantencion_repuesto UNIQUE (mantencion_id, repuesto_id),
    CONSTRAINT fk_mantencion_repuesto_mantenciones FOREIGN KEY (mantencion_id)
        REFERENCES mantenciones (id_mantencion),
    CONSTRAINT fk_mantencion_repuesto_repuestos FOREIGN KEY (repuesto_id)
        REFERENCES repuestos (id_repuesto)
) ENGINE=InnoDB;
