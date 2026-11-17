import json
from pathlib import Path

from .modeli import Rezervacija


class CsvIzvorRezervacija:
    """Format reda: gost,noci,cijena_noci"""

    def __init__(self, putanja: str | Path) -> None:
        self.putanja = Path(putanja)

    def ucitaj(self) -> list[Rezervacija]:
        rezervacije = []
        with self.putanja.open(encoding="utf-8") as f:
            for linija in f:
                if not linija.strip():
                    continue
                gost, noci, cijena = linija.strip().split(",")
                rezervacije.append(Rezervacija(gost, int(noci), float(cijena)))
        return rezervacije


class JsonIzvorRezervacija:
    def __init__(self, putanja: str | Path) -> None:
        self.putanja = Path(putanja)

    def ucitaj(self) -> list[Rezervacija]:
        with self.putanja.open(encoding="utf-8") as f:
            podaci = json.load(f)
        return [Rezervacija(p["gost"], int(p["noci"]), float(p["cijena_noci"])) for p in podaci]
