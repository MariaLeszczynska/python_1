import requests


def download_new_file(adres_url, nazwa_pliku="latest.txt"):
    response = requests.get(adres_url, timeout=60)
    response.raise_for_status()

    with open(nazwa_pliku, "wb") as plik:
        plik.write(response.content)

    print(f"saved {nazwa_pliku}")


if __name__ == "__main__":
    download_new_file("https://oleksandr-fedoruk.com/sggw/podyplomowe/file")
    download_new_file("https://oleksandr-fedoruk.com/sggw/podyplomowe/file", "moj_plik.txt")