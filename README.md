# Control de Vehículos y Mantenciones

Evaluación 2 de Programación Orientada a Objetos.

El sistema registra vehículos y sus mantenciones. La estructura separa datos,
negocio y presentación, siguiendo la organización utilizada en las clases.

## Requisitos

- Python 3.11 o superior.
- MySQL Server iniciado en el computador.
- Visual Studio Code.

La persistencia usa MySQL mediante Peewee y PyMySQL. El esquema utiliza los
tipos relacionales del ejemplo de clases: `INTEGER`, `VARCHAR`, `DATE`,
`DATETIME`, `DECIMAL`, `TINYINT`, claves primarias y claves foráneas.

## Estructura

```text
control_vehiculos_eval2/
├── modelo_clases.mmd
├── modelo_clases.png
├── main.py
├── consola.py
├── datos/
│   ├── auxiliar.py
│   ├── conexion.py
│   ├── modelos/
│   ├── repositorio/
│   └── sql/
├── negocio/
├── presentacion/
├── tests/
├── requirements.txt
├── .env                 
└── .env.example
```

`datos/modelos` contiene las clases del dominio y el mapeo de tablas.
`datos/repositorio` concentra el acceso a persistencia. `datos/conexion.py`
configura la conexión. `datos/sql` contiene el esquema y los datos de
demostración. `negocio` aplica las reglas del sistema. `presentacion` contiene
el menú y la salida en consola. `main.py` inicia el programa.

Las clases del dominio declaran al menos cuatro métodos propios. El diagrama UML
muestra sus operaciones en la sección inferior de cada clase. Los métodos de
`BaseModel` son operaciones comunes heredadas por los modelos persistentes.

## Preparación en Windows y VS Code

Abre en VS Code la carpeta del proyecto, que contiene `main.py` y
`requirements.txt`. Durante la instalación de Python, activa **Add Python to
PATH**. En una terminal PowerShell nueva, confirma la instalación:

```powershell
python --version
```

Crea el entorno virtual y actívalo:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

El ZIP incluye un archivo `.env` local de ejemplo y `.env.example`. Edita `.env`
con los datos de acceso a tu servidor MySQL. Si el `.env` local no está presente
después de clonar el repositorio, créalo desde la plantilla:

```powershell
Copy-Item .env.example .env
```

Instala las dependencias:

```powershell
python -m pip install -r requirements.txt
```


## Ejecutar el menú

Desde la carpeta raíz y con el entorno activado:

```powershell
python main.py
```

También puede iniciarse directamente con:

```powershell
python consola.py
```

El menú permite listar, consultar, crear, actualizar y eliminar vehículos;
registrar mantenciones; asociar repuestos; consultar el historial; revisar
mantenciones pendientes y marcarlas como completadas. Los datos de salida se
presentan en bloques verticales para facilitar su lectura en la terminal.

La eliminación de vehículos con mantenciones registradas se bloquea mediante
claves foráneas para conservar el historial.

## Pruebas

Las pruebas de validación y cálculo de costos no requieren conectarse a MySQL:

```powershell
python -m pytest -q
```



## GitHub

Desde la carpeta del proyecto:

```powershell
git init
git add .
git status
git commit -m "Implementa sistema de control de vehículos"
git branch -M main
git remote add origin URL_DEL_REPOSITORIO
git push -u origin main
```

Antes de publicar, confirma que `.env` no aparezca como archivo agregado y que
`git status` no muestre credenciales.
