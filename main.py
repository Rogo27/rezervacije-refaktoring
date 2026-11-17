import sys
from pathlib import Path

from rezervacije import (CsvIzvorRezervacija, FajlIzvjestac, JsonIzvorRezervacija,
                         KonzolniObavjestavac, ObradaRezervacija)
from rezervacije.protokoli import IzvorRezervacija

DATA = Path(__file__).parent / "data"


def main() -> None:
    izvor: IzvorRezervacija
    if len(sys.argv) > 1 and sys.argv[1] == "json":
        izvor = JsonIzvorRezervacija(DATA / "rezervacije.json")
    else:
        izvor = CsvIzvorRezervacija(DATA / "rezervacije.csv")

    obrada = ObradaRezervacija(izvor, FajlIzvjestac("izvjestaj.txt"), KonzolniObavjestavac())
    obrada.obradi()


if __name__ == "__main__":
    main()
