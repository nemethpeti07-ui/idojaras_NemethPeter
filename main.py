import tkinter as tk
from tkinter import messagebox

import idojaras_np


class IdojarasAlkalmazas:
    def __init__(self, ablak):
        self.ablak = ablak
        self.ablak.title("Belföldi Időjárás Figyelő")
        self.ablak.geometry("460x420")
        self.ablak.resizable(False, False)

        self.kezelo = idojaras_np.IdojarasKezeloNP()

        self.cim_label = tk.Label(
            self.ablak,
            text="Belföldi település időjárása",
            font=("Arial", 14, "bold")
        )
        self.cim_label.pack(pady=10)

        self.bekero_keret = tk.Frame(self.ablak)
        self.bekero_keret.pack(pady=5)

        self.varos_label = tk.Label(
            self.bekero_keret,
            text="Település:",
            font=("Arial", 11)
        )
        self.varos_label.pack(side=tk.LEFT, padx=5)

        self.varos_entry = tk.Entry(self.bekero_keret, font=("Arial", 11), width=22)
        self.varos_entry.pack(side=tk.LEFT, padx=5)
        self.varos_entry.bind("<Return>", self.kereses_esemeny)

        self.keres_gomb = tk.Button(
            self.bekero_keret,
            text="Lekérdezés",
            font=("Arial", 10, "bold"),
            command=self.adatok_frissitese
        )
        self.keres_gomb.pack(side=tk.LEFT, padx=5)

        self.eredmeny_szoveg = tk.Text(
            self.ablak,
            height=16,
            width=50,
            font=("Consolas", 10),
            state=tk.DISABLED
        )
        self.eredmeny_szoveg.pack(pady=15, padx=15)

    def kereses_esemeny(self, event):
        self.adatok_frissitese()

    def szoveg_kiirasa(self, tartalom):
        self.eredmeny_szoveg.config(state=tk.NORMAL)
        self.eredmeny_szoveg.delete("1.0", tk.END)
        self.eredmeny_szoveg.insert(tk.END, tartalom)
        self.eredmeny_szoveg.config(state=tk.DISABLED)

    def adatok_frissitese(self):
        varos = self.varos_entry.get().strip()
        if not varos:
            messagebox.showwarning("Hiányzó adat", "Adj meg egy településnevet!")
            return

        hely = self.kezelo.hely_kereses(varos)
        if hely is None:
            messagebox.showerror(
                "Nincs találat",
                f"A(z) '{varos}' nevű belföldi település nem található."
            )
            return

        nev, varmegye, lat, lon, _ = hely
        idojaras = idojaras_np.idojaras_adat_lekeres_np(lat, lon)

        if idojaras is None:
            messagebox.showerror(
                "Hálózati hiba",
                "Nem sikerült lekérni az időjárási adatokat."
            )
            return

        aktualis = idojaras["current"]
        napi = idojaras["daily"]

        kimenet = (
            f"Település: {nev} ({varmegye})\n"
            f"{'-' * 46}\n"
            f"Hőmérséklet:   {aktualis['temperature_2m']:.1f} °C\n"
            f"Hőérzet:       {aktualis['apparent_temperature']:.1f} °C\n"
            f"Páratartalom:  {aktualis['relative_humidity_2m']} %\n"
            f"Szélsebesség:  {aktualis['wind_speed_10m']} km/h\n"
            f"Csapadék:      {aktualis['precipitation']} mm\n\n"
            f"3 napos előrejelzés:\n"
        )

        for i in range(len(napi["time"])):
            datum = napi["time"][i]
            t_min = napi["temperature_2m_min"][i]
            t_max = napi["temperature_2m_max"][i]
            csapadek = napi["precipitation_sum"][i]
            kimenet += (
                f"{datum} | Min: {t_min:5.1f}°C | "
                f"Max: {t_max:5.1f}°C | {csapadek} mm\n"
            )

        self.szoveg_kiirasa(kimenet)


if __name__ == "__main__":
    root = tk.Tk()
    app = IdojarasAlkalmazas(root)
    root.mainloop()