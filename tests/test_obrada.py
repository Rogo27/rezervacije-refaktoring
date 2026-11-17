from pathlib import Path

import pytest

from original.obrada import UpravljanjeRezervacijama
from rezervacije import (CsvIzvorRezervacija, FajlIzvjestac, JsonIzvorRezervacija,
                         ObradaRezervacija, Rezervacija)

DATA = Path(__file__).resolve().parent.parent / "data"


class LazniIzvor:
    def __init__(self, rezervacije: list[Rezervacija]) -> None:
        self.rezervacije = rezervacije

    def ucitaj(self) -> list[Rezervacija]:
        return self.rezervacije


class LazniIzvjestac:
    def __init__(self) -> None:
        self.sacuvano: list[float] | None = None

    def sacuvaj(self, iznosi: list[float]) -> None:
        self.sacuvano = iznosi


class LazniObavjestavac:
    def __init__(self) -> None:
        self.poslato: list[float] = []

    def posalji(self, ukupno: float) -> None:
        self.poslato.append(ukupno)


def pokreni(rezervacije: list[Rezervacija]):
    izvjestac, obavjestavac = LazniIzvjestac(), LazniObavjestavac()
    iznosi = ObradaRezervacija(LazniIzvor(rezervacije), izvjestac, obavjestavac).obradi()
    return iznosi, izvjestac, obavjestavac


def test_servis_racuna_iznose_iz_zamjenskog_izvora():
    iznosi, _, _ = pokreni([Rezervacija("Ana", 3, 80), Rezervacija("Marko", 2, 50)])
    assert iznosi == [240.0, 100.0]


def test_izvjestac_i_obavjestavac_dobijaju_podatke():
    _, izvjestac, obavjestavac = pokreni([Rezervacija("Ana", 3, 80), Rezervacija("Marko", 2, 50)])
    assert izvjestac.sacuvano == [240.0, 100.0]
    assert obavjestavac.poslato == [340.0]


def test_prazan_izvor():
    iznosi, izvjestac, obavjestavac = pokreni([])
    assert iznosi == []
    assert izvjestac.sacuvano == []
    assert obavjestavac.poslato == [0]


@pytest.mark.parametrize("noci, cijena", [(0, 80), (-2, 80), (3, -10)])
def test_neispravna_rezervacija_baca_gresku(noci, cijena):
    with pytest.raises(ValueError):
        Rezervacija("Ana", noci, cijena)


def test_csv_i_json_izvor_daju_iste_rezervacije():
    csv = CsvIzvorRezervacija(DATA / "rezervacije.csv").ucitaj()
    json = JsonIzvorRezervacija(DATA / "rezervacije.json").ucitaj()
    assert csv == json


def test_csv_ignorise_prazne_linije(tmp_path):
    fajl = tmp_path / "r.csv"
    fajl.write_text("Ana,3,80\n\nMarko,2,50\n", encoding="utf-8")
    assert len(CsvIzvorRezervacija(fajl).ucitaj()) == 2


def test_fajl_izvjestac_upisuje_isti_format_kao_original(tmp_path):
    fajl = tmp_path / "izvjestaj.txt"
    FajlIzvjestac(fajl).sacuvaj([240.0, 100.0])
    assert fajl.read_text(encoding="utf-8") == "[240.0, 100.0]"


def test_ponasanje_isto_kao_originalni_kod():
    """Refaktoring ne smije promijeniti rezultat obračuna."""
    stari = UpravljanjeRezervacijama(str(DATA / "rezervacije.csv"))
    ocekivano = [stari.izracunaj_iznos(r) for r in stari.ucitaj()]
    iznosi, _, _ = pokreni(CsvIzvorRezervacija(DATA / "rezervacije.csv").ucitaj())
    assert iznosi == ocekivano
