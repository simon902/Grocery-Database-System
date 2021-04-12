import tkinter as tk
from tkinter import ttk
import sqlite3




class Database:

    def __init__(self):
        self.conn_ = sqlite3.connect("grocery.db")
        self.cursor_ = self.conn_.cursor()

        self.cursor_.execute("""CREATE TABLE IF NOT EXISTS grocery(
                product text,
                exp_date text,
                price real
        );""")



class Table(tk.LabelFrame):

    def __init__(self, parent):
        tk.LabelFrame.__init__(self, parent, padx = 5, pady = 5)
        self.grid(row = 1, column = 0, rowspan = 2, pady = 5)

        self.search_ = Search(parent)
        self.entry_ = Entry(parent)

        cols = ("Produkt", "Ablaufdatum", "Preis")
        self.tree = ttk.Treeview(self, columns = cols, show = "headings")
        
        for column in cols:
            self.tree.heading(column, text = column)
        self.tree.pack()




class Search(tk.Frame):

    def __init__(self, parent):
        tk.LabelFrame.__init__(self, parent, text = "Search")
        self.grid(row = 1, column = 1, ipadx = 20, padx = 5)
        
        
        self.search_ = tk.StringVar()

        tk.Label(self, text = "Suchen").grid(row = 0, column = 0, padx = 5, pady = 3)
        tk.Entry(self, textvariable = self.search_).grid(row = 0, column = 1, padx = 5, pady = 3)

        tk.Button(self, text = "Suchen").grid(row = 1, column = 0, padx = 5, pady = 2)
        tk.Button(self, text = "Reset").grid(row = 1, column = 1, padx = 5, pady = 2)


class Entry(tk.LabelFrame):

    def __init__(self, parent):
        tk.LabelFrame.__init__(self, parent, text = "Entry")
        self.grid(row = 2, column = 1, ipadx = 10, padx = 5, pady = 3)


        self.product = tk.StringVar()
        self.exp_date = tk.StringVar()
        self.price = tk.StringVar()
        
        tk.Label(self, text = "Produkt").grid(row = 0, column = 0, padx = 5, pady = 3)
        tk.Entry(self, textvariable = self.product).grid(row = 0, column = 1, padx = 5, pady = 3)

        tk.Label(self, text = "Ablaufdatum").grid(row = 1, column = 0, padx = 5, pady = 3)
        tk.Entry(self, textvariable = self.exp_date).grid(row = 1, column = 1, padx = 5, pady = 3)

        tk.Label(self, text = "Preis").grid(row = 3, column = 0, padx = 5, pady = 3)
        tk.Entry(self, textvariable = self.price).grid(row = 3, column = 1, padx = 5, pady = 3)
        
        tk.Button(self, text = "Hinzufügen", command = self.addEntry).grid(row = 4, column = 0, padx = 5, pady = 3)
        tk.Button(self, text = "Löschen", command = self.addEntry).grid(row = 4, column = 1, padx = 5, pady = 3)



    def addEntry(self):
        print(1)







if __name__ == "__main__":
    root = tk.Tk()
    root.title("Grocery-Database-System")
    root.geometry("980x600")

    tk.Label(root, text = "Grocery-Database-System", font = ("Arial", 40)).grid(row = 0, column = 0)

    frame = tk.LabelFrame(root, text = "Program")
    frame.grid(row = 1, column = 0)

    table = Table(root)
    

    
    root.mainloop()