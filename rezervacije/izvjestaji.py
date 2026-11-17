from pathlib import Path


class FajlIzvjestac:
    def __init__(self, putanja: str | Path = "izvjestaj.txt") -> None:
        self.putanja = Path(putanja)

    def sacuvaj(self, iznosi: list[float]) -> None:
        self.putanja.write_text(str(iznosi), encoding="utf-8")


class KonzolniIzvjestac:
    def sacuvaj(self, iznosi: list[float]) -> None:
        for i, iznos in enumerate(iznosi, 1):
            print(f"{i}. {iznos:.2f} EUR")
