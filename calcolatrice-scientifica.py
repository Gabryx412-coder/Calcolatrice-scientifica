import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import sympy as sp
import math
import fractions
import random
import matplotlib.pyplot as plt
import numpy as np

class CalcolatriceScientifica:
    def __init__(self, master):
        """Inizializza la calcolatrice scientifica."""
        self.master = master
        self.master.title("Calcolatrice Scientifica")
        self.master.geometry("500x800")
        self.master.config(bg="#2e2e2e")

        self.espressione = ""
        self.storia = []
        self.memoria = 0

        # Schermo della calcolatrice
        self.schermo = tk.Entry(master, font=("Arial", 24), bd=10, insertwidth=2, width=16, borderwidth=4)
        self.schermo.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

        self.result_label = tk.Label(master, text="", font=("Arial", 16), bg="#2e2e2e", fg="#ffffff")
        self.result_label.grid(row=1, column=0, columnspan=4)

        # Pulsanti
        self.crea_pulsanti()
        
        # Variabile per il tema
        self.theme = "dark"

    def crea_pulsanti(self):
        """Crea i pulsanti della calcolatrice."""
        pulsanti = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+',
            'sin', 'cos', 'tan', 'log',
            'sqrt', 'pow', 'fact', '(', 
            ')', 'C', 'History', 
            'Save', 'Undo', 'π', 
            'e', 'arcsin', 'arccos', 
            'arctan', 'Circumference', 'Area',
            'mod', 'hypot', 'exp', 'inhypot',
            'Memory', 'Random', 'Plot', 
            'Stats', 'Convert', 'Help'
        ]

        riga = 2
        colonna = 0
        for pulsante in pulsanti:
            tk.Button(self.master, text=pulsante, padx=20, pady=20, font=("Arial", 15),
                      bg="#3e3e3e", fg="#ffffff", activebackground="#4e4e4e", command=lambda x=pulsante: self.click(x)).grid(row=riga, column=colonna, sticky="nsew")
            colonna += 1
            if colonna > 3:
                colonna = 0
                riga += 1

        # Pulsante per cambiare tema
        tk.Button(self.master, text="Change Theme", padx=20, pady=20, font=("Arial", 15),
                  bg="#3e3e3e", fg="#ffffff", activebackground="#4e4e4e", command=self.cambia_tema).grid(row=riga, columnspan=4, sticky="nsew")

        # Rendi i pulsanti di dimensioni uguali
        for i in range(5):
            self.master.grid_columnconfigure(i, weight=1)

    def click(self, pulsante):
        """Gestisce il clic sui pulsanti."""
        if pulsante == '=':
            self.calcola()
        elif pulsante == 'C':
            self.schermo.delete(0, tk.END)
            self.result_label.config(text="")
            self.espressione = ""
        elif pulsante == 'History':
            self.mostra_storia()
        elif pulsante == 'Save':
            self.salva_risultato()
        elif pulsante == 'Undo':
            self.undo()
        elif pulsante == 'Circumference':
            self.calcola_circonferenza()
        elif pulsante == 'Area':
            self.calcola_area()
        elif pulsante == 'Random':
            self.genera_numero_casuale()
        elif pulsante == 'Plot':
            self.plot_funzione()
        elif pulsante == 'Memory':
            self.gestione_memoria()
        elif pulsante == 'Stats':
            self.calcola_statistiche()
        elif pulsante == 'Convert':
            self.converti_unita()
        elif pulsante == 'Help':
            self.mostra_help()
        elif pulsante == 'Exit':
            self.master.quit()
        elif pulsante in ('π', 'e'):
            self.espressione += str(sp.pi if pulsante == 'π' else sp.E)
            self.aggiungi_a_schermo()
        elif pulsante == 'mod':
            self.espressione += '%'
            self.aggiungi_a_schermo()
        elif pulsante == 'hypot':
            self.calcola_hypot()
        elif pulsante == 'exp':
            self.espressione += 'exp('
            self.aggiungi_a_schermo()
        elif pulsante == 'inhypot':
            self.calcola_inhypot()
        else:
            self.espressione += str(pulsante)
            self.aggiungi_a_schermo()

    def aggiungi_a_schermo(self):
        """Aggiorna lo schermo della calcolatrice."""
        self.schermo.delete(0, tk.END)
        self.schermo.insert(0, self.espressione)

    def calcola(self):
        """Calcola il risultato dell'espressione."""
        try:
            # Sostituzione dell'operatore di potenza per compatibilità con sympy
            espressione_modificata = self.espressione.replace("^", "**")
            
            if '=' in espressione_modificata:
                # Se è un'equazione, separare in due parti
                lhs, rhs = espressione_modificata.split('=')
                x = sp.symbols('x')
                equazione = sp.Eq(sp.sympify(lhs), sp.sympify(rhs))
                soluzione = sp.solve(equazione, x)
                risultato = f"x = {soluzione}" if soluzione else "Nessuna soluzione trovata."
            else:
                risultato = sp.sympify(espressione_modificata)

            self.storia.append(f"{self.espressione} = {risultato}")
            self.result_label.config(text=f"Risultato: {risultato}")

            # Mostra il risultato per un tempo limitato
            self.master.after(3000, self.azzera_risultato)

            self.espressione = ""
            self.aggiungi_a_schermo()
        except Exception as e:
            messagebox.showerror("Errore", str(e))
            self.espressione = ""

    def azzera_risultato(self):
        """Azzera il risultato dopo un certo tempo."""
        self.result_label.config(text="")

    def calcola_circonferenza(self):
        """Calcola la circonferenza di un cerchio dato il raggio."""
        try:
            raggio = float(self.schermo.get())
            circonferenza = 2 * math.pi * raggio
            self.result_label.config(text=f"Circonferenza: {circonferenza}")
        except ValueError:
            messagebox.showerror("Errore", "Inserisci un valore valido per il raggio.")
    
    def calcola_area(self):
        """Calcola l'area di un cerchio dato il raggio."""
        try:
            raggio = float(self.schermo.get())
            area = math.pi * (raggio ** 2)
            self.result_label.config(text=f"Area: {area}")
        except ValueError:
            messagebox.showerror("Errore", "Inserisci un valore valido per il raggio.")

    def calcola_hypot(self):
        """Calcola l'ipotenusa dati i cateti."""
        try:
            cateto1, cateto2 = map(float, self.schermo.get().split(','))
            ipotenusa = math.hypot(cateto1, cateto2)
            self.result_label.config(text=f"Ipotenusa: {ipotenusa}")
        except ValueError:
            messagebox.showerror("Errore", "Inserisci due cateti separati da una virgola.")

    def calcola_inhypot(self):
        """Calcola i cateti dati l'ipotenusa e un cateto."""
        try:
            ipotenusa, cateto = map(float, self.schermo.get().split(','))
            cateto2 = math.sqrt(ipotenusa ** 2 - cateto ** 2)
            self.result_label.config(text=f"Cateto: {cateto2}")
        except ValueError:
            messagebox.showerror("Errore", "Inserisci un'ipotenusa e un cateto separati da una virgola.")

    def mostra_storia(self):
        """Mostra la storia delle operazioni effettuate."""
        if not self.storia:
            messagebox.showinfo("Storia", "Nessuna operazione registrata.")
        else:
            storia_formattata = "\n".join(self.storia)
            messagebox.showinfo("Storia", storia_formattata)

    def salva_risultato(self):
        """Salva il risultato in un file di testo."""
        try:
            with filedialog.asksaveasfile(mode='w', defaultextension=".txt", filetypes=[("Text Files", "*.txt")]) as file:
                file.write(self.result_label.cget("text"))
            messagebox.showinfo("Salvato", "Risultato salvato con successo.")
        except Exception as e:
            messagebox.showerror("Errore", str(e))

    def undo(self):
        """Annulla l'ultima operazione effettuata."""
        if self.espressione:
            self.espressione = self.espressione[:-1]
            self.aggiungi_a_schermo()

    def cambia_tema(self):
        """Cambia il tema dell'interfaccia grafica."""
        if self.theme == "dark":
            self.master.config(bg="#ffffff")
            self.schermo.config(bg="#f0f0f0", fg="#000000")
            self.result_label.config(bg="#ffffff", fg="#000000")
            self.theme = "light"
        else:
            self.master.config(bg="#2e2e2e")
            self.schermo.config(bg="#3e3e3e", fg="#ffffff")
            self.result_label.config(bg="#2e2e2e", fg="#ffffff")
            self.theme = "dark"

    def genera_numero_casuale(self):
        """Genera e mostra un numero casuale."""
        numero_casuale = random.randint(1, 100)
        self.result_label.config(text=f"Numero casuale: {numero_casuale}")

    def plot_funzione(self):
        """Visualizza una funzione matematica."""
        try:
            x = np.linspace(-10, 10, 400)
            y = eval(self.schermo.get())
            plt.plot(x, y)
            plt.title("Grafico della Funzione")
            plt.xlabel("x")
            plt.ylabel("f(x)")
            plt.grid(True)
            plt.show()
        except Exception as e:
            messagebox.showerror("Errore", "Impossibile plottare la funzione.")

    def gestione_memoria(self):
        """Gestisce la memoria per salvare un valore."""
        try:
            comando = simpledialog.askstring("Memoria", "Scrivi 'save' per salvare o 'recall' per richiamare.")
            if comando == 'save':
                self.memoria = float(self.schermo.get())
                messagebox.showinfo("Memoria", "Valore salvato in memoria.")
            elif comando == 'recall':
                self.schermo.delete(0, tk.END)
                self.schermo.insert(0, str(self.memoria))
            else:
                messagebox.showerror("Errore", "Comando non valido.")
        except ValueError:
            messagebox.showerror("Errore", "Inserisci un valore valido.")

    def calcola_statistiche(self):
        """Calcola la media, mediana e deviazione standard."""
        try:
            dati = list(map(float, self.schermo.get().split(',')))
            media = sum(dati) / len(dati)
            mediana = np.median(dati)
            deviazione = np.std(dati)
            self.result_label.config(text=f"Media: {media}, Mediana: {mediana}, Deviazione: {deviazione}")
        except Exception as e:
            messagebox.showerror("Errore", str(e))

    def converti_unita(self):
        """Converte unità di misura."""
        try:
            valore = float(self.schermo.get())
            unita = simpledialog.askstring("Unità di Misura", "Inserisci 'm' per metri a chilometri o 'km' per chilometri a metri.")
            if unita == 'm':
                risultato = valore / 1000
                self.result_label.config(text=f"{valore} metri sono {risultato} chilometri.")
            elif unita == 'km':
                risultato = valore * 1000
                self.result_label.config(text=f"{valore} chilometri sono {risultato} metri.")
            else:
                messagebox.showerror("Errore", "Unità non valida.")
        except ValueError:
            messagebox.showerror("Errore", "Inserisci un valore valido.")

    def mostra_help(self):
        """Mostra un messaggio di aiuto con le funzionalità disponibili."""
        help_message = (
            "Funzionalità disponibili:\n"
            "- Operazioni di base: +, -, *, /\n"
            "- Potenze: ^\n"
            "- Trigonometriche: sin, cos, tan\n"
            "- Logaritmi: log\n"
            "- Frazioni: usa la sintassi a/b\n"
            "- Statistiche: media, mediana, deviazione standard\n"
            "- Conversioni: metri <-> chilometri\n"
            "- Memoria: salva e richiama un valore\n"
            "- Plottare funzioni: inserisci un'espressione di x"
        )
        messagebox.showinfo("Aiuto", help_message)

if __name__ == "__main__":
    root = tk.Tk()
    calcolatrice = CalcolatriceScientifica(root)
    root.mainloop()
