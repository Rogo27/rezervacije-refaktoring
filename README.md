# Refaktoring obrade rezervacija

**Predmet:** Napredno programiranje (FIST4NP) – Mini projekat 1
**Student:** Viktor Roganović, indeks 25/024
**Univerzitet Donja Gorica – FIST**

Dati monolitni kod (klasa `UpravljanjeRezervacijama` sa slajda 17, Nedjelja 2) refaktorisan je po principima **S** (Single Responsibility) i **D** (Dependency Inversion). Za izvor podataka, izvještavanje i obavještavanje uvedeni su `Protocol`-i.

## Pokretanje

```bash
pip install -r requirements.txt
python main.py            # CSV izvor -> izvjestaj.txt + "Poslato: 918.5"
python main.py json       # JSON izvor, isti rezultat, servis nije mijenjan
python original/obrada.py # originalni kod, isti izlaz
pytest -v                 # 10 testova
mypy --strict rezervacije main.py
```

## Analiza originalnog koda

```python
class UpravljanjeRezervacijama:
    def ucitaj(self): ...             # 1. učitavanje podataka
    def izracunaj_iznos(self, r): ... # 2. obračun
    def sacuvaj_izvjestaj(self, iznosi): ... # 3. čuvanje izvještaja
    def posalji_mail(self, iznosi): ...      # 4. obavještavanje
```

| Problem | Princip |
|---|---|
| Klasa ima četiri razloga za promjenu: format fajla, način obračuna, format izvještaja, kanal obavještavanja | **S** narušen |
| Putanja do CSV-a i `izvjestaj.txt` su zakucani, a servis sam otvara fajlove. Ne može se testirati bez diska | **D** narušen |
| Rezervacija je lista stringova (`r[1]`, `r[2]`), bez tipova i bez validacije | čitljivost / tipovi |
| `open()` bez `with`, pa se fajlovi ne zatvaraju eksplicitno. Nema `encoding`. Prazna linija u CSV-u ruši program | ispravnost |

## Nova struktura

```
rezervacije/
├── modeli.py        # Rezervacija (dataclass, frozen) – podaci, validacija, iznos
├── protokoli.py     # IzvorRezervacija, Izvjestac, Obavjestavac (Protocol)
├── izvori.py        # CsvIzvorRezervacija, JsonIzvorRezervacija
├── izvjestaji.py    # FajlIzvjestac, KonzolniIzvjestac
├── obavjestenja.py  # KonzolniObavjestavac
└── servis.py        # ObradaRezervacija – koordinira korake
```

### S – jedna odgovornost po klasi

| Odgovornost iz originala | Nova klasa |
|---|---|
| `ucitaj` | `CsvIzvorRezervacija` / `JsonIzvorRezervacija` |
| `izracunaj_iznos` | `Rezervacija.iznos` (property) |
| `sacuvaj_izvjestaj` | `FajlIzvjestac` |
| `posalji_mail` | `KonzolniObavjestavac` |
| redoslijed koraka | `ObradaRezervacija` |

### D – zavisnost od apstrakcija

```python
class IzvorRezervacija(Protocol):
    def ucitaj(self) -> list[Rezervacija]: ...

class Izvjestac(Protocol):
    def sacuvaj(self, iznosi: list[float]) -> None: ...

class Obavjestavac(Protocol):
    def posalji(self, ukupno: float) -> None: ...
```

`ObradaRezervacija` prima sve tri zavisnosti kroz konstruktor (injekcija zavisnosti) i ne zna da li podaci dolaze iz CSV-a, JSON-a ili memorije. Konkretne klase se biraju u `main.py`.

**O kao posljedica:** `JsonIzvorRezervacija` je dodat kao drugi izvor bez ijedne izmjene u `ObradaRezervacija` (zadatak 4 sa vježbe na slajdu 17).

## Testovi

`tests/test_obrada.py` ima 10 testova. Servis se testira sa zamjenskim objektima `LazniIzvor`, `LazniIzvjestac` i `LazniObavjestavac`:
- obračun iznosa iz zamjenskog izvora,
- izvještač i obavještavač dobijaju ispravne podatke,
- prazan izvor,
- validacija: 0 ili negativan broj noći, negativna cijena,
- CSV i JSON izvor daju iste rezervacije,
- CSV ignoriše prazne linije,
- `FajlIzvjestac` piše isti format kao original,
- **test očuvanja ponašanja**: rezultat se poredi sa originalnom klasom `UpravljanjeRezervacijama`.

## Rad sa AI alatom

Korišćen je AI asistent **Claude (Anthropic)**.

### Upotrijebljeni upiti

1. *„Ovo je domaći br 1. Odradi mi ga i daj mi korak po korak kako da ga pushujem i šta da pošaljem profesoru onda u mail."*, uz sliku slajda sa zadatkom.
2. *„To je zadatak sa ove prezentacije, ako ti je potrebno da koristiš to što je on dao (preuzeti dati monolitni). Ako se nalazi negdje u prezentaciji, izmijeni i prilagodi kako je tražio."*, uz prezentaciju `Nedjelja_02_OOP_i_SOLID.pptx`.

### Ispravke generisanog koda

| # | Šta je uočeno u generisanom rješenju | Ispravka |
|---|---|---|
| 1 | Prva verzija nije koristila dati kod. AI je napisao sopstveni monolitni skript, jer sa slajda zadatka nije bilo jasno koji je „dati” skript | Uz prezentaciju je pronađen kod sa slajda 17 i rješenje je urađeno ispočetka nad njim |
| 2 | Prva verzija je uvela pravila koja original nema (tipovi soba, kapaciteti, popust, poseban validator). To su apstrakcije koje problem ne zahtijeva (slajd 16, YAGNI) | Uklonjene. Zadržana je samo funkcionalnost originala |
| 3 | Pogrešan naziv test klase (`LaznIzvor`) | Ispravljeno u `LazniIzvor` |
| 4 | Trebalo je dokazati da refaktoring ne mijenja ponašanje | Dodat test koji poredi rezultat sa originalnom klasom. Ručno provjereno da obje verzije daju `Poslato: 918.5` i isti `izvjestaj.txt` |
| 5 | Prazna linija u CSV-u ruši original (`ValueError`) | `CsvIzvorRezervacija` preskače prazne linije, uz test |
| 6 | Provjera tipova | `mypy --strict` prolazi bez grešaka |
<!-- Ako sam nešto mijenjao nakon pregleda, dopisati ovdje kao red 7. -->
