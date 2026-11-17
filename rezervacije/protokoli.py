from typing import Protocol

from .modeli import Rezervacija


class IzvorRezervacija(Protocol):
    def ucitaj(self) -> list[Rezervacija]: ...


class Izvjestac(Protocol):
    def sacuvaj(self, iznosi: list[float]) -> None: ...


class Obavjestavac(Protocol):
    def posalji(self, ukupno: float) -> None: ...
