from desafio_tunts import __version__
from desafio_tunts.sheet_funcs import calc_final, get_total_classes


def test_version():
    assert __version__ == "0.1.0"


def test_calc_final():
    assert calc_final(50) == 50


def test_get_total_classes():
    sheet_values = [[""], ["Total de aulas no semestre: 60"]]
    assert get_total_classes(sheet_values) == 60
