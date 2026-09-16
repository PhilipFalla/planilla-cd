"""Equivalence Partitioning sobre las reglas de calculo.py.

Un valor representativo por clase de comportamiento (no por rango numerico):
entrada valida vs invalida donde el README lo exige, y las tres clases del
tramo de ISR.
"""

import pytest

from planilla.calculo import (
    descuento_isr,
    pago_horas_extra,
    valor_hora,
)


def test_valor_hora_con_salario_valido() -> None:
    assert valor_hora(6000) == pytest.approx(25.0)


def test_valor_hora_con_salario_negativo() -> None:
    with pytest.raises(ValueError):
        valor_hora(-500)


def test_horas_extra_dentro_del_rango_permitido() -> None:
    assert pago_horas_extra(4000, 10) == pytest.approx(250.0)


def test_horas_extra_fuera_del_rango_permitido() -> None:
    with pytest.raises(ValueError):
        pago_horas_extra(4000, 100)


def test_isr_tramo_renta_no_imponible() -> None:
    """Salario bajo: renta imponible anual cae a cero o menos, no paga ISR."""
    assert descuento_isr(3000) == pytest.approx(0.0)


def test_isr_tramo_cinco_por_ciento() -> None:
    """Renta imponible entre 0 y Q300,000 anuales: tramo del 5%."""
    assert descuento_isr(10000) == pytest.approx(300.0)


def test_isr_tramo_siete_por_ciento() -> None:
    """Renta imponible arriba de Q300,000 anuales: tramo del 7% sobre el excedente."""
    assert descuento_isr(50000) == pytest.approx(2720.0)
