USE control_vehiculos;

INSERT INTO propietarios (
    rut,
    nombre,
    telefono,
    correo
)
VALUES (
    '11111111-1',
    'Propietario Demo',
    '900000000',
    'demo@ejemplo.cl'
)
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre);

INSERT INTO marcas (nombre)
VALUES ('Toyota')
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre);

INSERT INTO modelos (marca_id, nombre)
SELECT id_marca, 'Corolla'
FROM marcas
WHERE nombre = 'Toyota'
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre);

INSERT INTO tipos_vehiculo (nombre)
VALUES ('Automóvil')
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre);

INSERT INTO talleres (
    nombre,
    direccion,
    telefono
)
SELECT
    'Taller Central',
    'Av. Principal 100',
    '900000001'
WHERE NOT EXISTS (
    SELECT 1
    FROM talleres
    WHERE nombre = 'Taller Central'
);

INSERT INTO tipos_mantencion (
    nombre,
    descripcion,
    intervalo_km,
    intervalo_meses
)
VALUES (
    'Mantención preventiva',
    'Servicio periódico',
    10000,
    6
)
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre);

INSERT INTO tipos_mantencion (nombre, descripcion)
VALUES ('Reparación', 'Reparación correctiva')
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre);

INSERT INTO repuestos (
    codigo,
    nombre,
    stock,
    precio_unitario
)
VALUES (
    'FILTRO-DEMO',
    'Filtro de aceite de demostración',
    10,
    5000.00
)
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre);

INSERT INTO vehiculos (
    patente,
    vin,
    propietario_id,
    tipo_vehiculo_id,
    modelo_id,
    anio,
    color,
    kilometraje,
    estado
)
SELECT
    'DEMO01',
    'JTDBR32E720123456',
    propietarios.id_propietario,
    tipos_vehiculo.id_tipo_vehiculo,
    modelos.id_modelo,
    2020,
    'Blanco',
    45000,
    'ACTIVO'
FROM propietarios
JOIN tipos_vehiculo
    ON tipos_vehiculo.nombre = 'Automóvil'
JOIN marcas
    ON marcas.nombre = 'Toyota'
JOIN modelos
    ON modelos.marca_id = marcas.id_marca
    AND modelos.nombre = 'Corolla'
WHERE propietarios.rut = '11111111-1'
ON DUPLICATE KEY UPDATE patente = VALUES(patente);
