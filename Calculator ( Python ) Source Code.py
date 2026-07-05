import tkinter as tk
from tkinter import font


class CalculatriceGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculatrice")
        self.geometry("360x520")
        self.resizable(False, False)
        self.config(bg="#1b1b1b", padx=12, pady=12)

        self.ecran_valeur = tk.StringVar(value="0")
        self.creer_widgets()

    def creer_widgets(self):
        titre = tk.Label(
            self,
            text="Calculatrice",
            font=font.Font(size=18, weight="bold"),
            bg="#1b1b1b",
            fg="#e6e6e6",
        )
        titre.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 8), padx=10)

        ecran = tk.Entry(
            self,
            textvariable=self.ecran_valeur,
            justify="right",
            font=font.Font(size=34, weight="bold"),
            bg="#2b2b2b",
            fg="#f5f5f5",
            bd=0,
            insertbackground="#f5f5f5",
            relief="flat",
            highlightthickness=0,
        )
        ecran.grid(row=1, column=0, columnspan=4, sticky="nsew", pady=(0, 18), padx=8)
        ecran.bind("<Key>", lambda event: "break")

        bouton_style = {
            "font": font.Font(size=20, weight="bold"),
            "bd": 0,
            "relief": "flat",
            "fg": "#ffffff",
            "activeforeground": "#ffffff",
            "width": 4,
            "height": 2,
        }

        num_bg = "#2f2f2f"
        num_active = "#3a3a3a"
        op_bg = "#404040"
        op_active = "#4a4a4a"
        clr_bg = "#6b6b6b"
        clr_active = "#7a7a7a"

        boutons = [
            [("C", self.effacer, clr_bg, clr_active),
             ("⌫", self.retirer_dernier, op_bg, op_active),
             ("±", self.inverser_signe, op_bg, op_active),
             ("%", lambda: self.ajouter_operateur("%"), op_bg, op_active)],
            [("7", lambda: self.taper("7"), num_bg, num_active),
             ("8", lambda: self.taper("8"), num_bg, num_active),
             ("9", lambda: self.taper("9"), num_bg, num_active),
             ("÷", lambda: self.ajouter_operateur("÷"), op_bg, op_active)],
            [("4", lambda: self.taper("4"), num_bg, num_active),
             ("5", lambda: self.taper("5"), num_bg, num_active),
             ("6", lambda: self.taper("6"), num_bg, num_active),
             ("×", lambda: self.ajouter_operateur("×"), op_bg, op_active)],
            [("1", lambda: self.taper("1"), num_bg, num_active),
             ("2", lambda: self.taper("2"), num_bg, num_active),
             ("3", lambda: self.taper("3"), num_bg, num_active),
             ("-", lambda: self.ajouter_operateur("-"), op_bg, op_active)],
            [("0", lambda: self.taper("0"), num_bg, num_active),
             (".", lambda: self.taper("."), num_bg, num_active),
             ("=", self.calculer, op_bg, op_active, "span2")],
        ]

        for ligne, rang in enumerate(boutons, start=2):
            colonne = 0
            for texte, commande, couleur, couleur_active, *extras in rang:
                bouton = tk.Button(
                    self,
                    text=texte,
                    command=commande,
                    bg=couleur,
                    activebackground=couleur_active,
                    **bouton_style,
                )
                if extras and extras[0] == "span2":
                    bouton.grid(row=ligne, column=colonne, columnspan=2, sticky="nsew", padx=6, pady=6)
                    colonne += 2
                else:
                    bouton.grid(row=ligne, column=colonne, sticky="nsew", padx=6, pady=6)
                    colonne += 1

        for i in range(7):
            self.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

    def taper(self, caractere):
        valeur = self.ecran_valeur.get()
        if valeur == "0" or valeur == "Erreur":
            self.ecran_valeur.set(caractere if caractere != "." else "0.")
            return

        if caractere == ".":
            parties = (
                valeur
                .replace("+", " ")
                .replace("-", " ")
                .replace("*", " ")
                .replace("/", " ")
                .replace("×", " ")
                .replace("÷", " ")
                .replace("%", " ")
                .split()
            )
            last = parties[-1] if parties else ""
            if "." in last:
                return

        self.ecran_valeur.set(valeur + caractere)

    def ajouter_operateur(self, operateur):
        valeur = self.ecran_valeur.get()
        if valeur[-1] in "+-*/%.":
            valeur = valeur[:-1]
        self.ecran_valeur.set(valeur + operateur)

    def inverser_signe(self):
        valeur = self.ecran_valeur.get()
        if valeur == "0":
            return
        if valeur.startswith("-"):
            self.ecran_valeur.set(valeur[1:])
        else:
            self.ecran_valeur.set("-" + valeur)

    def effacer(self):
        self.ecran_valeur.set("0")

    def retirer_dernier(self):
        valeur = self.ecran_valeur.get()
        if valeur in ("0", "Erreur"):
            self.ecran_valeur.set("0")
            return
        self.ecran_valeur.set(valeur[:-1] or "0")

    def calculer(self):
        expression = self.ecran_valeur.get()
        expression = expression.replace("×", "*").replace("÷", "/").replace("%", "/100")
        try:
            resultat = eval(expression)
            if isinstance(resultat, float) and resultat.is_integer():
                resultat = int(resultat)
            self.ecran_valeur.set(str(resultat))
        except Exception:
            self.ecran_valeur.set("Erreur")


if __name__ == "__main__":
    app = CalculatriceGUI()
    app.mainloop()
