"""Boundary Value Analysis sobre las reglas de calculo.py.

Cada caso ataca el valor exacto donde una regla del README cambia de
comportamiento, con su vecino invalido o su vecino del otro tramo.
"""

import pytest

from planilla.calculo import (
    bonificacion_incentivo,
    descuento_prestamo,
    isr_anual,
    pago_horas_extra,
    valor_hora,
)


def test_salario_base_en_cero_es_invalido() -> None:
    """0 es el primer valor invalido del rango 'mayor que cero'."""
    with pytest.raises(ValueError):
        valor_hora(0)


def test_horas_extra_por_debajo_de_cero() -> None:
    with pytest.raises(ValueError):
        pago_horas_extra(4000, -1)


def test_horas_extra_en_el_maximo_permitido() -> None:
    """48 es el ultimo valor valido del rango 0-48."""
    assert pago_horas_extra(4000, 48) == pytest.approx(1200.0)


def test_horas_extra_por_encima_del_maximo() -> None:
    with pytest.raises(ValueError):
        pago_horas_extra(4000, 49)


def test_dias_trabajados_en_cero() -> None:
    """0 es el primer valor valido del rango 0-30 (bonificacion proporcional nula)."""
    assert bonificacion_incentivo(0) == pytest.approx(0.0)


def test_dias_trabajados_justo_antes_del_mes_completo() -> None:
    assert bonificacion_incentivo(29) == pytest.approx(250.0 * 29 / 30)


def test_dias_trabajados_en_el_mes_completo() -> None:
    """30 es el ultimo dia valido, donde la bonificacion deja de ser proporcional."""
    assert bonificacion_incentivo(30) == pytest.approx(250.0)


def test_dias_trabajados_por_encima_del_mes() -> None:
    with pytest.raises(ValueError):
        bonificacion_incentivo(31)


def test_isr_en_el_limite_del_tramo_uno() -> None:
    """Renta imponible de Q300,000 exactos: todavia tramo del 5%."""
    assert isr_anual(348000) == pytest.approx(15000.0)


def test_isr_justo_arriba_del_limite_del_tramo_uno() -> None:
    """Renta imponible de Q300,001: ya entra al tramo del 7% sobre el excedente."""
    assert isr_anual(348001) == pytest.approx(15000.07)


def test_prestamo_en_el_piso_exacto_del_30_por_ciento() -> None:
    """El liquido antes del prestamo cae justo en el piso: no se descuenta nada."""
    assert descuento_prestamo(300, 1000, 5) == pytest.approx(0.0)


def test_prestamo_justo_arriba_del_piso() -> None:
    """Un quetzal de margen sobre el piso: el prestamo se topa a ese margen."""
    assert descuento_prestamo(301, 1000, 5) == pytest.approx(1.0)


def test_cuota_prestamo_negativa_es_invalida() -> None:
    with pytest.raises(ValueError):
        descuento_prestamo(1000, 1000, -1)
