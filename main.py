from Database import *
from Calculations import *
import tkinter as tk
from tkinter import filedialog, messagebox


# A simple popup window for login
def security():
    global txtb_pw
    global win_login
    win_login = tk.Toplevel()
    win_login.title("Login")
    win_login.geometry("200x200")
    txtb_lbl = tk.Label(win_login, text="Enter Password")
    txtb_pw = tk.Entry(win_login)
    btn_login = tk.Button(win_login, text="Login", command=login)
    txtb_lbl.pack()
    txtb_pw.pack()
    btn_login.pack()


# A simple "login" to prohibit unwanted changes to db
def login():
    password = "Swisslog"
    if txtb_pw.get() == password:
        win_login.destroy()
        manage_db()
    else:
        win_login.destroy()


# A window for everything regarding the database
def manage_db():
    global win
    win = tk.Toplevel()
    win.title("Database management")
    win.geometry("400x400")
    global btn_create_baseprice
    global btn_create_map
    global btn_create_currency
    btn_create_baseprice = tk.Button(win, text="Baseprice", command=new_baseprice, state=tk.DISABLED)
    btn_create_map = tk.Button(win, text="MAP", command=new_map, state=tk.DISABLED)
    btn_create_currency = tk.Button(win, text="Currency", command=new_currency, state=tk.DISABLED)
    btn_print_baseprice = tk.Button(win, text="Baseprice", command=print_base_btn)
    btn_print_map = tk.Button(win, text="MAP", command=print_map_btn)
    btn_print_currency = tk.Button(win, text="Currency", command=print_curr_btn)
    txtb_delete_lbl = tk.Label(win, text="Deletes the old database and then uploads the new one")
    txtb_print_lbl = tk.Label(win, text="Select which database records to print")
    btn_create_baseprice.grid(row=2, column=0)
    btn_create_map.grid(row=2, column=1)
    btn_create_currency.grid(row=2, column=2)
    btn_print_baseprice.grid(row=4, column=0)
    btn_print_map.grid(row=4, column=1)
    btn_print_currency.grid(row=4, column=2)
    txtb_delete_lbl.grid(row= 1, columnspan=3)
    txtb_print_lbl.grid(row= 3, columnspan=3)
    btn = tk.Button(win, text="Activate buttons", command=change_state)
    btn.grid(row=2, column=3)



def change_state():
    if btn_create_baseprice['state'] == 'disabled':
        btn_create_baseprice.config(state=tk.NORMAL)
        btn_create_currency.config(state=tk.NORMAL)
        btn_create_map.config(state=tk.NORMAL)
    else:
        btn_create_baseprice.config(state=tk.DISABLED)
        btn_create_currency.config(state=tk.DISABLED)
        btn_create_map.config(state=tk.DISABLED)

def new_baseprice():
    mbox = messagebox.askyesno(title="Safety", message="Are you sure you want to proceed?", parent=win)
    if mbox:
        try:
            delete_table_bp()
        except:
            x = 1
        create_table_bp()
        win.destroy()
        messagebox.showinfo("Done", "Script completed successfully")
        manage_db()
    else:
        win.destroy()
        manage_db()

def new_map():
    mbox = messagebox.askyesno(title="Safety", message="Are you sure you want to proceed?", parent=win)
    if mbox:
        try:
            delete_table_map()
        except:
            x = 1
        create_table_map()
        win.destroy()
        messagebox.showinfo("Done", "Script completed successfully")
        manage_db()
    else:
        win.destroy()
        manage_db()

def new_currency():
    mbox = messagebox.askyesno(title="Safety", message="Are you sure you want to proceed?", parent=win)
    if mbox:
        try:
            delete_table_currency()
        except:
            x = 1
        create_table_currency()
        win.destroy()
        messagebox.showinfo("Done", "Script completed successfully")
        manage_db()
    else:
        win.destroy()
        manage_db()



def print_base_btn():
    print_baseprice()
    messagebox.showinfo("Done", "Script completed successfully")

def print_map_btn():
    print_map_list()
    messagebox.showinfo("Done", "Script completed successfully")

def print_curr_btn():
    print_currency_list()
    messagebox.showinfo("Done", "Script completed successfully")



root = tk.Tk()
root.geometry("250x300")
root.title("Purchasing Tool")
root_cwd = cwd_root()
btn_db = tk.Button(root, text="Manage database", command=security)
btn_db.grid(column=1, row=1)
lbl_db = tk.Label(root, text="Change and print from database")
lbl_db.grid(row=0, column=1)

btn_main = tk.Button(root, text="Run analysis", command=clean_main)
btn_main.grid(column=1, row=3,)
lbl_main = tk.Label(root, text="Creates the report ")
lbl_main.grid(row=2, column=1)

btn_clean_pir = tk.Button(root, text="Clean raw PIR", command=clean_pir)
btn_clean_pir.grid(column=1, row=5,)
lbl_pir = tk.Label(root, text="Cleans a 'raw' PIR excel sheet")
lbl_pir.grid(row=4, column=1)

root.mainloop()


