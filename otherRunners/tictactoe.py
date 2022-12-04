# Importem les llibreries necessàries
import tkinter as tk
from itertools import cycle
from tkinter import font
from typing import NamedTuple

# Fem 2 clases per als jugadors i els moviments que fan
class JugadorClase(NamedTuple):
    label: str
    color: str

class MovimentClase(NamedTuple):
    row: int
    col: int
    label: str = ""

# Definim la mida del tauler
MIDA_TAULER = 3

# Definim fent servir la clase, cada jugador y el seu color
JUGADORS_DEFAULT = (JugadorClase(label="X", color="blue"), JugadorClase(label="O", color="green"))

class TicTacToeGame:
    def __init__(self, jugadors=JUGADORS_DEFAULT, midaTauler=MIDA_TAULER):
        # Definim totes les variables que utilitzarem
        self._jugadors = cycle(jugadors) # Jugadors 
        self.midaTauler = midaTauler # Mida del tauler
        self.jugadorActual = next(self._jugadors) # Jugador actual
        self.comboGuanyador = [] # Combinació guanyadora
        self._movimentsActuals = [] # Moviments actuals
        self.hiGuanyador = False # Hi ha guanyador?
        self._comboGuanyador = [] # Combinació guanyadora
        self._setup_tauler() # Inicialitzem el tauler

    def _setup_tauler(self):
        # Inicialitza el tauler amb els moviments inicials.
        self._movimentsActuals = [
            [MovimentClase(row, col) for col in range(self.midaTauler)]
            for row in range(self.midaTauler)
        ] 
        self._comboGuanyador = self.getComboGuanyador() # Definim la classe del tauler

    def getComboGuanyador(self):
        # Retorna una llista de tuples que contenen les coordenades de les caselles que formen una combinació guanyadora.
        files = [
            [(move.row, move.col) for move in row]
            for row in self._movimentsActuals
        ]
        columnes = [list(col) for col in zip(*files)]
        primeraDiagonal = [row[i] for i, row in enumerate(files)]
        segonaDiagonal = [col[j] for j, col in enumerate(reversed(columnes))]
        return files + columnes + [primeraDiagonal, segonaDiagonal]

    def cambiaJugador(self):
        # Retorna un jugador commutat.
        self.jugadorActual = next(self._jugadors)

    def esMovimentValid(self, move):
        # Retorna Cert si el moviment és vàlid i Fals en cas contrari.
        row, col = move.row, move.col
        movimentNoJugat = self._movimentsActuals[row][col].label == ""
        noGuanyador = not self.hiGuanyador
        return noGuanyador and movimentNoJugat

    def processaMoviment(self, move):
        # Processa el moviment actual i comprova si és una victòria.
        row, col = move.row, move.col
        self._movimentsActuals[row][col] = move
        for combo in self._comboGuanyador:
            results = set(self._movimentsActuals[n][m].label for n, m in combo)
            esGuanyadora = (len(results) == 1) and ("" not in results)
            if esGuanyadora:
                self.hiGuanyador = True
                self.comboGuanyador = combo
                break

    def guanyadorActiuFuncio(self):
        # Retorna Cert si la partida té un guanyador i Fals en cas contrari.
        return self.hiGuanyador

    def esEmpate(self):
        # Retorna Cert si la partida està lligada, i Fals en cas contrari.
        noGuanyador = not self.hiGuanyador
        movimentsJugatsActius = (move.label for row in self._movimentsActuals for move in row)
        return noGuanyador and all(movimentsJugatsActius)

    def reset_game(self):
        # Restableix l'estat del joc per a tornar a jugar.
        for row, row_content in enumerate(self._movimentsActuals):
            for col, _ in enumerate(row_content):
                row_content[col] = MovimentClase(row, col)
        self.hiGuanyador = False
        self.comboGuanyador = []

class TicTacToeBoard(tk.Tk):
    def __init__(self, joc):
        super().__init__()
        # Definim les variables que utilitzarem dins la nostra finestra
        self.title("3enlínia - Multijugador")
        self._cells = {}
        self.superGame = joc
        self._creemMenu()
        self._creemTauler()
        self._creemGrid()

    def _creemMenu(self):
        # Creem el menú
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar)
        file_menu.add_command(label="Tornar a jugar", command=self.reset_board)
        file_menu.add_separator()
        file_menu.add_command(label="Sortir", command=quit)
        menu_bar.add_cascade(label="Arxiu", menu=file_menu)

    def _creemTauler(self):
        # Creem la finestra amb els textos
        display_frame = tk.Frame(master=self)
        display_frame.grid(row=0, column=0, columnspan=3, sticky="nsew")
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(master=display_frame, text="Preparats?", font=font.Font(size=28, weight="bold"))
        self.display.pack()

    def _creemGrid(self):
        # Creem el tauler amb els grids i els botons
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        for row in range(self.superGame.midaTauler):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(self.superGame.midaTauler):
                button = tk.Button(master=grid_frame, text="", font=font.Font(size=36, weight="bold"), fg="black", width=3, height=2, highlightbackground="lightblue")
                self._cells[button] = (row, col)
                button.bind("<ButtonPress-1>", self.play)
                button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

    def play(self, event):
        # Gestiona el moviment d'un jugador.
        butoClick = event.widget
        row, col = self._cells[butoClick]
        move = MovimentClase(row, col, self.superGame.jugadorActual.label)
        if self.superGame.esMovimentValid(move):
            self.actualitzarBotoJugador(butoClick)
            self.superGame.processaMoviment(move)
            if self.superGame.esEmpate():
                self.actualitzarPantallaOrdinador(msg="Partida empatada!", color="red")
            elif self.superGame.guanyadorActiuFuncio():
                self._highlight_cells()
                msg = f'El jugador: "{self.superGame.jugadorActual.label}" ha guanyat!'
                color = self.superGame.jugadorActual.color
                self.actualitzarPantallaOrdinador(msg, color)
            else:
                self.superGame.cambiaJugador()
                msg = f"És el torn de {self.superGame.jugadorActual.label}"
                self.actualitzarPantallaOrdinador(msg)

    def actualitzarBotoJugador(self, butoClick):
        butoClick.config(text=self.superGame.jugadorActual.label)
        butoClick.config(fg=self.superGame.jugadorActual.color)

    def actualitzarPantallaOrdinador(self, msg, color="black"):
        self.display["text"] = msg
        self.display["fg"] = color

    def _highlight_cells(self):
        for button, coordinates in self._cells.items():
            if coordinates in self.superGame.comboGuanyador:
                button.config(highlightbackground="red")

    def reset_board(self):
        # Restableix el tauler del joc per a tornar a jugar.
        self.superGame.reset_game()
        self.actualitzarPantallaOrdinador(msg="Preparats?")
        for button in self._cells.keys():
            button.config(highlightbackground="lightblue")
            button.config(text="")
            button.config(fg="black")

def main():
    # Creeu el tauler del joc i executeu el seu bucle principal.
    joc = TicTacToeGame()
    tauler = TicTacToeBoard(joc)
    tauler.geometry("600x600")
    tauler.mainloop()

if __name__ == "__main__":
    main()