import re


def texto_obligatorio(valor, nombre):
    texto = str(valor).strip()
    if not texto:
        raise ValueError(f"{nombre} es obligatorio.")
    return texto


def entero_positivo(valor, nombre, permitir_cero=False):
    try:
        numero = int(valor)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{nombre} debe ser un número entero.") from error

    minimo = 0 if permitir_cero else 1
    if numero < minimo:
        raise ValueError(f"{nombre} debe ser igual o mayor que {minimo}.")
    return numero


def normalizar_patente(valor):
    patente = re.sub(r"[^A-Za-z0-9]", "", str(valor)).upper()
    if not 5 <= len(patente) <= 10:
        raise ValueError("La patente debe contener entre 5 y 10 caracteres alfanuméricos.")
    return patente


def normalizar_vin(valor):
    vin = re.sub(r"\s+", "", str(valor)).upper()
    if len(vin) != 17 or not re.fullmatch(r"[A-HJ-NPR-Z0-9]{17}", vin):
        raise ValueError("El VIN debe tener 17 caracteres y no incluir I, O ni Q.")
    return vin


def validar_anio(valor):
    anio = entero_positivo(valor, "Año")
    if not 1950 <= anio <= 2100:
        raise ValueError("El año debe estar entre 1950 y 2100.")
    return anio


def validar_monto(valor, nombre):
    from decimal import Decimal, InvalidOperation

    try:
        monto = Decimal(str(valor))
    except (InvalidOperation, TypeError, ValueError) as error:
        raise ValueError(f"{nombre} debe ser un monto numérico.") from error

    if not monto.is_finite() or monto < 0:
        raise ValueError(f"{nombre} no puede ser negativo ni inválido.")
    return monto
