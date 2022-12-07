# Importem les llibreries necessàries
import tkinter as tk
import os

# Creem la finestra amb el títol i la mida de la pantalla
root = tk.Tk()
root.title("Llançador ràpid d'aplicacions")
root.geometry("720x400")

# Afegim els iconos de tkinter a la finestra
root.iconbitmap("assets/coet.ico")

# Li posem una imatge al fons i la situem al mig
imatgeFons = tk.PhotoImage(file="assets/xp.png")
textLabel = tk.Label(root, image=imatgeFons)
textLabel.place(x=0, y=0, relwidth=1, relheight=1)

# Crea un grid per als botons de 3x3 i els posem al centre de la finestra
for row in range(3):
    root.rowconfigure(row, weight=1, minsize=50)
    root.columnconfigure(row, weight=1, minsize=75)

def obrirAppSistema(nombre):
    root.destroy() # Tanquem la finestra actual
    os.system(nombre) # Obrim l'aplicació del sistema

# -- Creem els botons i els posem al grid --
# Botó 1 - Imatge - Paint
paint = tk.PhotoImage(file="assets/paint.png")
paint = paint.subsample(2, 2)

# Botó 1 - Funció - Paint
paint_button = tk.Button(root, image=paint, command=lambda: obrirAppSistema("mspaint"))
paint_button.grid(row=0, column=0)
paint_label = tk.Label(root, text="Paint")
paint_label.place(x=100, y=150)

# Botó 2 - Imatge - BlocDeNotes 
notepad = tk.PhotoImage(file="assets/bloc.png")
notepad = notepad.subsample(2, 2)

# Botó 2 - Funció - BlocDeNotes 
notepad_button = tk.Button(root, image=notepad, command=lambda: obrirAppSistema("notepad"))
notepad_button.grid(row=0, column=1)
notepad_label = tk.Label(root, text="Bloc de notes")
notepad_label.place(x=325, y=150)

# Botó 3 - Imatge - Explorador
explorer = tk.PhotoImage(file="assets/explorer.png")
explorer = explorer.subsample(2, 2)
explorer_button = tk.Button(root, image=explorer, command=lambda: obrirAppSistema("explorer"))
explorer_button.grid(row=0, column=2)
explorer_label = tk.Label(root, text="Explorador d'arxius")
explorer_label.place(x=545, y=150)

# Botó 4 - Imatge - TicTacToe
tictactoe = tk.PhotoImage(file="assets/tictactoe.png")
tictactoe = tictactoe.subsample(4, 4)

# Botó 5 - Funció - TicTacToe
def open_tictactoe():
    root.destroy() # Tanquem la finestra actual
    os.system("python otherRunners/tictactoe.py -f") # Executem el programa TicTacToe

tictactoe_button = tk.Button(root, image=tictactoe, command=open_tictactoe)
tictactoe_button.grid(row=2, column=1)
tictactoe_label = tk.Label(root, text="Tres en ratlla")
tictactoe_label.place(x=325, y=225)

# Fem un botó per sortir de la finestra
exit_button = tk.Button(root, text="Salir", command=root.destroy)
exit_button.place(x=650, y=350)

# Fem que la finestra mai es pugui redimensionar
root.resizable(False, False)

# Fem que la finestra es mostri
root.mainloop()
