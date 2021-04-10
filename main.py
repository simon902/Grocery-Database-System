import tkinter as tk
from tkinter import ttk

class Table(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent, padx = 5, pady = 5, bg = "grey")
        
        cols = ("Produkt", "Ablaufdatum", "Preis")
        tree = ttk.Treeview(self, columns = cols, show = "headings")

        for column in cols:
            tree.heading(column, text = column)
        tree.pack()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Grocery-Database-System")
    root.geometry("980x600")

    tk.Label(root, text = "Grocery-Database-System", font = ("Arial", 40)).grid(row = 0, column = 0)

    table = Table(root)
    table.grid(row = 1, column = 0)


    
    root.mainloop()
 