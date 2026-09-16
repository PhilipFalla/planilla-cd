"""Cobertura funcional de cli.py.

El gate de coverage cuenta todo src/planilla, incluida la CLI: sin estos
casos el umbral de 80% no se alcanza probando solo calculo.py.
"""

import pytest

from planilla.cli import USO, main, parse_args


def test_parse_args_convierte_valores_numericos() -> None:
    datos = parse_args(["salario_base=4000", "horas_extra=8"])
    assert datos == {"salario_base": 4000.0, "horas_extra": 8.0}


def test_parse_args_conserva_valores_no_numericos() -> None:
    datos = parse_args(["afiliado_igss=no"])
    assert datos == {"afiliado_igss": "no"}


def test_parse_args_ignora_argumentos_sin_signo_igual() -> None:
    datos = parse_args(["--help", "salario_base=1"])
    assert datos == {"salario_base": 1.0}


def test_main_sin_salario_base_imprime_uso(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    monkeypatch.setattr("sys.argv", ["planilla"])
    codigo = main()
    salida = capsys.readouterr().out
    assert codigo == 1
    assert USO in salida


def test_main_con_argumentos_validos_imprime_resumen(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    monkeypatch.setattr(
        "sys.argv",
        [
            "planilla",
            "salario_base=4000",
            "horas_extra=0",
            "dias_trabajados=30",
            "cuota_prestamo=0",
        ],
    )
    codigo = main()
    salida = capsys.readouterr().out
    assert codigo == 0
    assert "Liquido: Q4056.8" in salida
    assert "Descuentos: Q193.2" in salida


def test_main_respeta_afiliado_igss_no(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    monkeypatch.setattr(
        "sys.argv",
        [
            "planilla",
            "salario_base=4000",
            "horas_extra=0",
            "dias_trabajados=30",
            "cuota_prestamo=0",
            "afiliado_igss=no",
        ],
    )
    codigo = main()
    salida = capsys.readouterr().out
    assert codigo == 0
    assert "Descuentos: Q0.0" in salida
