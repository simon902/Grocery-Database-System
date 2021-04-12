import tkinter as tk
from tkinter import ttk
import sqlite3


class Table(tk.LabelFrame):

    def __init__(self, parent):
        tk.LabelFrame.__init__(self, parent, padx = 5, pady = 5)
        self.grid(row = 1, column = 0, rowspan = 2, pady = 5)

        # Create Treeview Table
        cols = ("Produkt", "Ablaufdatum", "Preis")
        self.tree_ = ttk.Treeview(self, columns = cols, show = "headings")
        
        for column in cols:
            self.tree_.heading(column, text = column)
        self.tree_.pack()

        # Database
        self.conn_ = sqlite3.connect("grocery.db")
        self.cursor_ = self.conn_.cursor()

        self.cursor_.execute("""CREATE TABLE IF NOT EXISTS grocery(
                product text,
                exp_date text,
                price real
            );""")

        self.cursor_.execute("""SELECT * FROM grocery""")
        self.updateTable(self.cursor_.fetchall())


        # User Input
        Search(parent ,self)
        Entry(parent, self)
    

    def __del__(self):
        self.conn_.commit()
        self.conn_.close()
    
    def updateTable(self, rows):
        self.tree_.delete(*self.tree_.get_children())
        for row in rows:
            self.tree_.insert("", "end", values = row)


class Search(tk.Frame):

    def __init__(self, parent, table):
        tk.LabelFrame.__init__(self, parent, text = "Search")
        self.grid(row = 1, column = 1, ipadx = 20, padx = 5)
        
        self.table_ = table

        self.search_ = tk.StringVar()

        tk.Label(self, text = "Suchen").grid(row = 0, column = 0, padx = 5, pady = 3)
        self.entry_ = tk.Entry(self, textvariable = self.search_)
        self.entry_.grid(row = 0, column = 1, padx = 5, pady = 3)

        tk.Button(self, text = "Suchen", command = self.search).grid(row = 1, column = 0, padx = 5, pady = 2)
        tk.Button(self, text = "Reset", command = self.reset).grid(row = 1, column = 1, padx = 5, pady = 2)


    def search(self):
        self.table_.cursor_.execute("""SELECT * FROM grocery
            WHERE product = :prod""", {"prod": self.search_.get()})
        self.table_.updateTable(self.table_.cursor_.fetchall())


    def reset(self):
        self.entry_.delete(0, "end")

        self.table_.cursor_.execute("SELECT * FROM GROCERY")
        self.table_.updateTable(self.table_.cursor_.fetchall())




class Entry(tk.LabelFrame):

    def __init__(self, parent, table):
        tk.LabelFrame.__init__(self, parent, text = "Entry")
        self.grid(row = 2, column = 1, ipadx = 10, padx = 5, pady = 3)

        self.table_ = table

        self.product_ = tk.StringVar()
        self.exp_date_ = tk.StringVar()
        self.price_ = tk.StringVar()
        
        tk.Label(self, text = "Produkt").grid(row = 0, column = 0, padx = 5, pady = 3)
        tk.Entry(self, textvariable = self.product_).grid(row = 0, column = 1, padx = 5, pady = 3)

        tk.Label(self, text = "Ablaufdatum").grid(row = 1, column = 0, padx = 5, pady = 3)
        tk.Entry(self, textvariable = self.exp_date_).grid(row = 1, column = 1, padx = 5, pady = 3)

        tk.Label(self, text = "Preis").grid(row = 3, column = 0, padx = 5, pady = 3)
        tk.Entry(self, textvariable = self.price_).grid(row = 3, column = 1, padx = 5, pady = 3)
        
        tk.Button(self, text = "Hinzufügen", command = self.addEntry).grid(row = 4, column = 0, padx = 5, pady = 3)
        tk.Button(self, text = "Löschen", command = self.deleteEntry).grid(row = 4, column = 1, padx = 5, pady = 3)



    def addEntry(self):
        if self.product_.get() != '' and self.exp_date_.get() != '' and self.price_.get() != '':
            
            self.table_.cursor_.execute("INSERT INTO grocery VALUES (:prod, :exp_date, :price)", 
                {"prod":self.product_.get(), "exp_date":self.exp_date_.get(), "price":self.price_.get()})

            

            self.table_.cursor_.execute("SELECT * FROM grocery")
            self.table_.updateTable(self.table_.cursor_.fetchall())

            self.table_.conn_.commit()


    def deleteEntry(self):
        if self.product_.get() != '' and self.exp_date_.get() != '' and self.price_.get() != '':
            self.table_.cursor_.execute("""DELETE FROM grocery
                WHERE product = :prod AND exp_date = :exp_date AND price = :price""",
                {"prod": self.product_.get(), "exp_date": self.exp_date_.get(), "price": self.price_.get()})
            

            self.table_.cursor_.execute("SELECT * FROM grocery")
            self.table_.updateTable(self.table_.cursor_.fetchall())

            self.table_.conn_.commit()



        
        


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Grocery-Database-System")
    root.geometry("980x600")

    tk.Label(root, text = "Grocery-Database-System", font = ("Arial", 40)).grid(row = 0, column = 0)

    frame = tk.LabelFrame(root, text = "Program")
    frame.grid(row = 1, column = 0)

    table = Table(root)
    

    
    root.mainloop()