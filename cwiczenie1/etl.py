import csv
from datetime import datetime
from functools import wraps

def log_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Poczatek {func.__name__}: {datetime.now():%H:%M:%S.%f}")

        try:
            return func(*args, **kwargs)
        finally:
            print(f"Koniec {func.__name__}: {datetime.now():%H:%M:%S.%f}")

    return wrapper


class ETLFILE:
    def __init__(self, file_name="latest.txt"):
        self.file_name = file_name

    def extract(self):
        with open(self.file_name, encoding="utf-8", newline="") as plik:
            reader = csv.reader(plik)

            for row in reader:
                if row:
                    yield [wartosc.strip() for wartosc in row]

    def transform(self, rows):
        for row in rows:
            numer = int(row[0])

            wartosci = [
                float(wartosc)
                for wartosc in row[1:]
                if wartosc != "-"
            ]

            missing = [
                indeks
                for indeks, wartosc in enumerate(row[1:], start=1)
                if wartosc == "-"
            ]

            suma = sum(wartosci)
            srednia = suma / len(wartosci) if wartosci else None

            yield numer, suma, srednia, missing

    def load(self, wyniki):
        with (
            open("values.csv", "w", encoding="utf-8", newline="") as values_file,
            open("missing_values.csv", "w", encoding="utf-8", newline="") as missing_file,
        ):
            values_writer = csv.writer(values_file)
            missing_writer = csv.writer(missing_file)

            values_writer.writerow(["numer", "suma", "srednia"])
            missing_writer.writerow(["numer", "indeksy_brakujacych"])

            for numer, suma, srednia, missing in wyniki:
                srednia_zapis = f"{srednia:.6f}" if srednia is not None else ""

                values_writer.writerow([
                    numer,
                    f"{suma:.6f}",
                    srednia_zapis,
                ])

                missing_writer.writerow([
                    numer,
                    ";".join(str(indeks) for indeks in missing),
                ])

    @log_time
    def run(self):
        self.load(self.transform(self.extract()))
        print("saved values.csv")
        print("saved missing_values.csv")


if __name__ == "__main__":
    etl = ETLFILE("latest.txt")
    etl.run()