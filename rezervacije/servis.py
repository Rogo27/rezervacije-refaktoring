from .protokoli import IzvorRezervacija, Izvjestac, Obavjestavac


class ObradaRezervacija:
    def __init__(self, izvor: IzvorRezervacija, izvjestac: Izvjestac,
                 obavjestavac: Obavjestavac) -> None:
        self.izvor = izvor
        self.izvjestac = izvjestac
        self.obavjestavac = obavjestavac

    def obradi(self) -> list[float]:
        iznosi = [r.iznos for r in self.izvor.ucitaj()]
        self.izvjestac.sacuvaj(iznosi)
        self.obavjestavac.posalji(sum(iznosi))
        return iznosi
