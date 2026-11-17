# Originalni monolitni kod sa slajda 17 (Nedjelja 2 – OOP i SOLID), bez izmjena.
# Dodat je samo blok za pokretanje na dnu.

class UpravljanjeRezervacijama:
    def __init__(self, putanja):
        self.putanja = putanja

    def ucitaj(self):
        return [l.strip().split(",")
                for l in open(self.putanja)]

    def izracunaj_iznos(self, r):
        return int(r[1]) * float(r[2])

    def sacuvaj_izvjestaj(self, iznosi):
        open("izvjestaj.txt", "w").write(str(iznosi))

    def posalji_mail(self, iznosi):
        print("Poslato:", sum(iznosi))


if __name__ == "__main__":
    u = UpravljanjeRezervacijama("data/rezervacije.csv")
    iznosi = [u.izracunaj_iznos(r) for r in u.ucitaj()]
    u.sacuvaj_izvjestaj(iznosi)
    u.posalji_mail(iznosi)
