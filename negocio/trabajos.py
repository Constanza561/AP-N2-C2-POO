from abc import ABC, abstractmethod
from decimal import Decimal


class TrabajoMantencion(ABC):
    """Abstracción común para los costos de trabajos de mantención."""

    def __init__(self, costo_mano_obra, costo_repuestos):
        self._costo_mano_obra = Decimal(str(costo_mano_obra))
        self._costo_repuestos = Decimal(str(costo_repuestos))
        self.validar_costos()

    @property
    def costo_mano_obra(self):
        return self._costo_mano_obra

    @property
    def costo_repuestos(self):
        return self._costo_repuestos

    def validar_costos(self):
        if self._costo_mano_obra < 0 or self._costo_repuestos < 0:
            raise ValueError("Los costos no pueden ser negativos.")
        return True

    def subtotal(self):
        return self._costo_mano_obra + self._costo_repuestos

    @abstractmethod
    def calcular_costo(self):
        """Calcula el costo final con las reglas de cada tipo de trabajo."""

    @abstractmethod
    def requiere_diagnostico(self):
        """Indica si el tipo de trabajo considera diagnóstico."""

    def resumen(self):
        return (
            f"Mano de obra: ${self.costo_mano_obra:,.0f}; "
            f"repuestos: ${self.costo_repuestos:,.0f}"
        )


class MantencionPreventiva(TrabajoMantencion):
    def calcular_costo(self):
        return self.subtotal()

    def requiere_diagnostico(self):
        return False

    def es_programable(self):
        return True

    def resumen(self):
        return f"Mantención preventiva | {super().resumen()}"


class Reparacion(TrabajoMantencion):
    def __init__(self, costo_mano_obra, costo_repuestos, costo_diagnostico=0):
        super().__init__(costo_mano_obra, costo_repuestos)
        self._costo_diagnostico = Decimal(str(costo_diagnostico))
        if self._costo_diagnostico < 0:
            raise ValueError("El costo de diagnóstico no puede ser negativo.")

    def validar_costos(self):
        super().validar_costos()
        costo_diagnostico = getattr(self, "_costo_diagnostico", Decimal("0"))
        if costo_diagnostico < 0:
            raise ValueError("El costo de diagnóstico no puede ser negativo.")
        return True

    def calcular_costo(self):
        return self.subtotal() + self._costo_diagnostico

    def requiere_diagnostico(self):
        return True

    def es_programable(self):
        return False

    def resumen(self):
        return (
            f"Reparación | diagnóstico: ${self._costo_diagnostico:,.0f}; "
            f"{super().resumen()}"
        )
