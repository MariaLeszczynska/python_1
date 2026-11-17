import requests


class DownloadError(Exception):
    pass


class NotFoundError(DownloadError):
    pass


class AccessDeniedError(DownloadError):
    pass


def download_new_file(adres_url, nazwa_pliku="latest.txt"):
    response = requests.get(adres_url, timeout=60)

    if response.status_code == 404:
        raise NotFoundError(f"Nie znaleziono pliku: {adres_url}")

    if response.status_code == 403:
        raise AccessDeniedError(f"Brak dostępu do pliku: {adres_url}")

    response.raise_for_status()

    with open(nazwa_pliku, "wb") as plik:
        plik.write(response.content)

    print(f"saved {nazwa_pliku}")



if __name__ == "__main__":
    pliki = [
        ("https://oleksandr-fedoruk.com/sggw/podyplomowe/file", "latest.txt"),
        ("https://oleksandr-fedoruk.com/sggw/podyplomowe/file", "moj_plik.txt"),
        ("http://oleksandr-fedoruk.com/sggw/podyplomowe/404", "test404.txt"),
        ("http://oleksandr-fedoruk.com/sggw/podyplomowe/403", "test403.txt"),
    ]

    for adres_url, nazwa_pliku in pliki:
        try:
            download_new_file(adres_url, nazwa_pliku)
        except NotFoundError as blad:
            print(f"NotFoundError: {blad}")
        except AccessDeniedError as blad:
            print(f"AccessDeniedError: {blad}")
        except requests.exceptions.RequestException as blad:
            print(f"Błąd pobierania: {blad}")