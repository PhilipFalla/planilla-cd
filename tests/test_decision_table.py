"""Decision Table sobre liquidar(): afiliado_igss x mes completo x prestamo topado.

Las tres condiciones son independientes entre si y liquidar() las combina en
un solo resultado, asi que se prueban las 2**3 = 8 combinaciones completas.
salario_base=4000 y horas_extra=0 se mantienen fijos en todas las filas para
aislar el efecto de las tres condiciones (con esos valores el ISR siempre da
cero, asi que tampoco interfiere).

afiliado_igss  dias_trabajados  cuota_prestamo  prestamo topado?
     Y               30 (completo)   100 (no topa)
     Y               30 (completo)  5000 (topa)
     Y               15 (incompleto) 100 (no topa)
     Y               15 (incompleto)5000 (topa)
     N               30 (completo)   100 (no topa)
     N               30 (completo)  5000 (topa)
     N               15 (incompleto) 100 (no topa)
     N               15 (incompleto)5000 (topa)
"""

import pytest

from planilla.calculo import liquidar

FILAS = [
    pytest.param(True, 30, 100, 100, 3956.8, id="Y-completo-notopa"),
    pytest.param(True, 30, 5000, 2856.8, 1200.0, id="Y-completo-topa"),
    pytest.param(True, 15, 100, 100, 3831.8, id="Y-incompleto-notopa"),
    pytest.param(True, 15, 5000, 2731.8, 1200.0, id="Y-incompleto-topa"),
    pytest.param(False, 30, 100, 100, 4150.0, id="N-completo-notopa"),
    pytest.param(False, 30, 5000, 3050.0, 1200.0, id="N-completo-topa"),
    pytest.param(False, 15, 100, 100, 4025.0, id="N-incompleto-notopa"),
    pytest.param(False, 15, 5000, 2925.0, 1200.0, id="N-incompleto-topa"),
]


@pytest.mark.parametrize(
    "afiliado, dias, cuota, prestamo_esperado, liquido_esperado", FILAS
)
def test_liquidar_combina_afiliacion_mes_y_tope_de_prestamo(
    afiliado, dias, cuota, prestamo_esperado, liquido_esperado
) -> None:
    resultado = liquidar(4000, 0, dias, afiliado, cuota)
    assert resultado.prestamo == pytest.approx(prestamo_esperado)
    assert resultado.liquido == pytest.approx(liquido_esperado)


def test_prestamo_topado_nunca_deja_el_liquido_bajo_el_piso() -> None:
    """En las cuatro filas donde el prestamo se topa, el liquido cae exacto en
    el 30% del salario ordinario (Q1200.0) sin importar afiliacion ni mes."""
    for afiliado in (True, False):
        for dias in (30, 15):
            resultado = liquidar(4000, 0, dias, afiliado, 5000)
            assert resultado.liquido == pytest.approx(1200.0)
