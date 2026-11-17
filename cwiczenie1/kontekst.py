class Logger:
    def __enter__(self):
        print("Start sekcji logowania")
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        print("Koniec sekcji logowania")
        return False


class FileWriter:
    def __init__(self, sciezka):
        self.sciezka = sciezka

    def __enter__(self):
        self.plik = open(self.sciezka, "w", encoding="utf-8")
        return self.plik

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.plik.close()

        if exc_value is not None:
            print(f"Błąd podczas zapisu: {exc_value}")

        return False


class SafeDivision:
    def __enter__(self):
        return self

    def divide(self, a, b):
        return a / b

    def __exit__(self, exc_type, exc_value, exc_tb):
        if isinstance(exc_value, ZeroDivisionError):
            print("Nie można dzielić przez zero")
            return True

        return False


if __name__ == "__main__":
    with Logger():
        print("Wykonuję kod wewnątrz sekcji")

    with FileWriter("tekst.txt") as plik:
        plik.write("Przykładowy tekst zapisany do pliku.\n")

    print("Zapisano tekst.txt")

    with SafeDivision() as dzielenie:
        print(dzielenie.divide(10, 2))
        print(dzielenie.divide(10, 0))

    print("Program działa dalej po dzieleniu przez zero")

    with FileWriter("blad.txt") as plik:
        plik.write("Tekst zapisany przed wystąpieniem błędu.\n")
        raise ValueError("Celowy błąd testowy")