# Belföldi Időjárás Figyelő

## Hallgató
Németh Péter

## Feladat leírása
A program egy grafikus felülettel rendelkező belföldi időjárás-lekérdező alkalmazás. A felhasználó által megadott magyarországi településhez lekéri a földrajzi koordinátákat, majd megjeleníti az aktuális időjárási adatokat és a 3 napos előrejelzést az Open-Meteo API segítségével.

## Indításhoz szükséges modulok
- `tkinter` (beépített grafikai modul)
- `requests` (külső HTTP kliens modul, telepítés: `pip install requests`)

## Modulok és a modulokban használt függvények

### `main.py` (Főprogram)
- `kereses_esemeny(event)`: Enter billentyű lenyomását kezelő eseménykezelő függvény.
- `szoveg_kiirasa(tartalom)`: A lekérdezett adatok megjelenítése a grafikus szövegdobozban.
- `adatok_frissitese()`: A gombnyomás eseménykezelője, amely összeköti a felhasználói bevitelt az API lekérdezésekkel.

### `idojaras_np.py` (Saját modul)
- `idojaras_adat_lekeres_np(lat, lon)`: Saját függvény, amely a megadott koordináták alapján lekéri az aktuális és a 3 napos időjárási adatokat (`requests.get`).
- `hely_kereses(varos_nev)`: Metódus, amely lekéri a belföldi település koordinátáit és vármegyéjét (`requests.Session`, `requests.utils.quote`).

## Osztályok
- `IdojarasAlkalmazas` (`main.py`): A Tkinter alapú grafikus felületet és az eseménykezelést megvalósító osztály.
- `IdojarasKezeloNP` (`idojaras_np.py`): A saját modulban található osztály, amely a települések geokódolását és a HTTP munkamenetet kezeli.