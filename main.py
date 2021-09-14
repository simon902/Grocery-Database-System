import tkinter as tk
from tkinter import ttk
import sqlite3
import datetime
import sys

# Fix for setting text colour for Tkinter 8.6.9
# From: https://core.tcl.tk/tk/info/509cafafae
def fixed_map(option, style):

    # Returns the style map for 'option' with any styles starting with
    # ('!disabled', '!selected', ...) filtered out.

    # style.map() returns an empty list for missing options, so this
    # should be future-safe.
    return [elm for elm in style.map('Treeview', query_opt=option) if
        elm[:2] != ('!disabled', '!selected')]



class Table(tk.LabelFrame):

    def __init__(self, parent):

        tk.LabelFrame.__init__(self, parent, padx = 5, pady = 5)
        self.grid(row = 1, column = 0, columnspan = 3, padx = 5, pady = 7)

        # Fix for setting text colour for Tkinter 8.6.9
        # From: https://core.tcl.tk/tk/info/509cafafae
        if tk.Tcl().eval('info patchlevel') == '8.6.9':
            style = ttk.Style()
            style.map('Treeview', foreground=fixed_map('foreground', style), background=fixed_map('background', style))

        # Create Treeview Table
        cols = ("ID", "Produkt", "Ablaufdatum", "Preis")
        self.tree_ = ttk.Treeview(self, columns = cols, show = "headings", selectmode = "browse")

        self.tree_.column("ID", anchor = "w", width = 80)
        self.tree_.column("Produkt", anchor = "center", width = 200)
        self.tree_.column("Ablaufdatum", anchor = "center", width = 200)
        self.tree_.column("Preis", anchor = "center", width = 110)

        for column in cols:
            self.tree_.heading(column, text = column)
        self.tree_.pack(side = "left")


        # Scrollbar
        scroll_ = ttk.Scrollbar(self, orient = "vertical", command = self.tree_.yview)
        scroll_.pack(side = "right", fill = "y")
        self.tree_.configure(yscrollcommand = scroll_.set)

        # Database
        self.conn_ = sqlite3.connect(sys.argv[1])
        self.cursor_ = self.conn_.cursor()

        self.cursor_.execute("""CREATE TABLE IF NOT EXISTS grocery(
                product text,
                exp_date text,
                price real
            );""")

        self.cursor_.execute("""SELECT rowid, * FROM grocery""")
        self.updateTable(self.cursor_.fetchall())


        # User Input
        Search(parent ,self)
        Entry(parent, self)


        # Legend
        legend = tk.LabelFrame(parent, text = "Legende", padx = 5, pady = 3)
        legend.grid(row = 2, column = 0, padx = 5)

        tk.Label(legend, bg = "#ff0000", width = 5).grid(row = 0, column = 1, padx = 5, pady = 3)
        tk.Label(legend, text = "Ablaufdatum in 1 Tag", ).grid(row = 0, column = 0, padx = 5, pady = 3)

        tk.Label(legend, bg = "#FFFF00", width = 5).grid(row = 1, column = 1, padx = 5, pady = 3)
        tk.Label(legend, text = "Ablaufdatum in 3 Tagen", ).grid(row = 1, column = 0, padx = 5, pady = 3)
    

    def __del__(self):

        self.conn_.commit()
        self.conn_.close()
    
    
    def updateTable(self, rows):

        self.tree_.delete(*self.tree_.get_children())

        for row in rows:

            tag = self.checkDate(row[2]) # checks date of tuple
            self.tree_.insert("", "end", values = row, tag = str(tag))
        
        self.tree_.tag_configure(tagname = "red", background = "#ff0000")
        self.tree_.tag_configure(tagname = "yellow", background = "#FFFF00")


    def checkDate(self, date):

        today = datetime.date.today()

        one_day = datetime.timedelta(days = 1)
        three_days = datetime.timedelta(days = 3)

        # Compares two strings in a lexicographical manner
        if str(today + one_day) >= str(date):
            return "red"

        elif str(today + three_days) >= str(date):
            return "yellow"
        
        else:
            return "default"



class Search(tk.Frame):

    def __init__(self, parent, table):

        tk.LabelFrame.__init__(self, parent, text = "Search")
        self.grid(row = 2, column = 1, ipadx = 5, padx = 5, sticky = "W")
        
        self.table_ = table

        self.search_ = tk.StringVar()
        # Incremental Search
        self.search_.trace("w", lambda name, index, mode: self.search())

        tk.Label(self, text = "Suchen").grid(row = 0, column = 0, padx = 5, pady = 3)
        self.entry_ = tk.Entry(self, textvariable = self.search_, width = 10)
        self.entry_.grid(row = 0, column = 1, padx = 5, pady = 3)

        #tk.Button(self, text = "Suchen", command = self.search).grid(row = 1, column = 0, padx = 5, pady = 2)
        #tk.Button(self, text = "Reset", command = self.reset).grid(row = 1, column = 1, padx = 5, pady = 2)
        tk.Button(self, text = "Löschen", command = self.deleteEntry).grid(row = 2, column = 1, padx = 5, pady = 3)


    def search(self):
        self.table_.cursor_.execute("""SELECT rowid, * FROM grocery
            WHERE product LIKE :prod OR rowid = :id""", {"prod": '%' + self.search_.get() + '%', "id": self.search_.get()})
        self.table_.updateTable(self.table_.cursor_.fetchall())


    def reset(self):

        self.entry_.delete(0, "end")

        self.table_.cursor_.execute("SELECT rowid, * FROM GROCERY")
        self.table_.updateTable(self.table_.cursor_.fetchall())


    def deleteEntry(self):

        if self.search_ != '':
            self.table_.cursor_.execute("""DELETE FROM grocery
                WHERE rowid = :id """, {"id": self.search_.get()})
            

            self.table_.cursor_.execute("SELECT rowid, * FROM grocery")
            self.table_.updateTable(self.table_.cursor_.fetchall())

            self.table_.conn_.commit()



class Entry(tk.LabelFrame):

    def __init__(self, parent, table):

        tk.LabelFrame.__init__(self, parent, text = "Entry")
        self.grid(row = 2, column = 2, ipadx = 10, padx = 5, pady = 3, sticky = "W")

        self.table_ = table

        self.product_ = tk.StringVar()
        self.exp_date_ = tk.StringVar()
        self.price_ = tk.StringVar()
        
        
        tk.Label(self, text = "Produkt").grid(row = 0, column = 0, padx = 5, pady = 3)
        tk.Entry(self, textvariable = self.product_, width = 15).grid(row = 0, column = 1, padx = 5, pady = 3)

        tk.Label(self, text = "Ablaufdatum").grid(row = 1, column = 0, padx = 5, pady = 3)
        tk.Entry(self, textvariable = self.exp_date_, width = 15).grid(row = 1, column = 1, padx = 5, pady = 3)

        tk.Label(self, text = "Preis").grid(row = 3, column = 0, padx = 5, pady = 3)
        tk.Entry(self, textvariable = self.price_, width = 15).grid(row = 3, column = 1, padx = 5, pady = 3)

        tk.Button(self, text = "Hinzufügen", command = self.addEntry).grid(row = 4, column = 0, padx = 5, pady = 3)


    def addEntry(self):

        if self.product_.get() != '' and self.exp_date_.get() != '' and self.price_.get() != '':
            
            self.table_.cursor_.execute("INSERT INTO grocery VALUES (:prod, :exp_date, :price)", 
                {"prod":self.product_.get(), "exp_date":self.exp_date_.get(), "price":self.price_.get()})


            self.table_.cursor_.execute("SELECT rowid, * FROM grocery")
            self.table_.updateTable(self.table_.cursor_.fetchall())

            self.table_.conn_.commit()



def main():

    root = tk.Tk()
    root.title("Grocery-Database-System")
    root.configure(bg = "#BDEDFF")
    root.geometry("770x470")
    #root.attributes('-fullscreen', True)
    # TODO: root windows Icon


    header = tk.Label(root, text = "Grocery-Database-System", font = ("Arial", 40), relief = "sunken", bg = "#ADD8E6")
    header.grid(row = 0, column = 0, columnspan = 3, pady = 3)

    Table(root)
    root.mainloop()


if __name__ == "__main__":
    
    main()
