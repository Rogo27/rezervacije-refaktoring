from dataclasses import dataclass


@dataclass(frozen=True)
class Rezervacija:
    gost: str
    noci: int
    cijena_noci: float

    def __post_init__(self) -> None:
        if self.noci <= 0:
            raise ValueError(f"Broj noćenja mora biti pozitivan: {self.noci}")
        if self.cijena_noci < 0:
            raise ValueError(f"Cijena ne može biti negativna: {self.cijena_noci}")

    @property
    def iznos(self) -> float:
        return self.noci * self.cijena_noci
