# import numpy as np
import pandas as pd
import os
import sqlite3
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from Calculations import cwd_root

#### Baseprices Creating table, deleting table


root_cwd = cwd_root
# Creates a table with 6 materials based on the baseprice excel
def create_table_bp():
    db_conn = sqlite3.connect('Database.db')
    cursor = db_conn.cursor()
    cursor.execute(
        """
        CREATE TABLE Baseprices (
            Material_number INTEGER,
            Material_description TEXT,
            Vendor_code INTEGER,
            Vendor_Name TEXT,
            Planned_Delivery_Time Integer,
            Standard_Quantity Integer,
            MOQ Integer,
            Purchasing_Group Integer,
            Gross_Price REAL,
            Currency_gp TEXT,
            Surcharge_ZB00 REAL,
            Currency_ZB00 TEXT,
            Discount_RA01 REAL,
            Validity_from BLOB,
            Validity_to BLOB,
            
            PRIMARY KEY(Material_number)
            );
            """
    )
    baseprice = pd.read_excel(
        askopenfilename(),
        engine='openpyxl',
        header=0
    )
    baseprice.to_sql('Baseprices', db_conn, if_exists='append', index=False)
    db_conn.close()
    print("Table Created")


# Deletes the table so we can make a new one for the next year
def delete_table_bp():
    db_conn = sqlite3.connect('Database.db')
    cursor = db_conn.cursor()
    cursor.execute(
        """
        DROP TABLE Baseprices
        """
    )
    db_conn.close()
    print("Table deleted")



# Prints the database to Excel
def print_baseprice():
    db_conn = sqlite3.connect('Database.db')
    db_base = pd.read_sql("SELECT * FROM Baseprices ", db_conn)
    db_conn.close()
    cwd = root_cwd()
    os.chdir(filedialog.askdirectory(title="Select output location"))
    db_base.to_excel('Baseprices.xlsx', index=False)
    os.chdir(cwd)


####

def create_table_map():
    db_conn = sqlite3.connect('Database.db')
    cursor = db_conn.cursor()
    cursor.execute(
        """
            CREATE TABLE MAP (
                Material_number INTEGER,
                MAP REAL,
                Currency TEXT,
                PRIMARY KEY(Material_number)
                );
                """
    )
    file_map = pd.read_excel(
        askopenfilename(),
        engine='openpyxl',
        header=0
    )
    file_map.to_sql('MAP', db_conn, if_exists='append', index=False)
    db_conn.close()
    print("Table Created")


# Deletes the table so we can make a new one for the next year
def delete_table_map():
    db_conn = sqlite3.connect('Database.db')
    cursor = db_conn.cursor()
    cursor.execute(
        """
        DROP TABLE MAP
        """
    )
    db_conn.close()
    print("Table deleted")


# Prints the database to Excel
def print_map_list():
    db_conn = sqlite3.connect('Database.db')
    db_base = pd.read_sql("SELECT * FROM MAP ", db_conn)
    db_conn.close()
    cwd = root_cwd()
    os.chdir(filedialog.askdirectory(title="Select output location"))
    db_base.to_excel('MAP-List.xlsx', index=False)
    os.chdir(cwd)


####

def create_table_currency():
    db_conn = sqlite3.connect('Database.db')
    cursor = db_conn.cursor()
    cursor.execute(
        """
        CREATE TABLE Currencies (
            Date BLOB,
            Currency TEXT,
            To_EUR REAL,
            PRIMARY KEY(Currency)
            );
            """
    )
    file_currency = pd.read_excel(
        askopenfilename(),
        engine='openpyxl',
        header=0
    )
    file_currency.to_sql('Currencies', db_conn, if_exists='append', index=False)
    db_conn.close()
    print("Table Created")


# Deletes the table so we can make a new one for the next year
def delete_table_currency():
    db_conn = sqlite3.connect('Database.db')
    cursor = db_conn.cursor()
    cursor.execute(
        """
        DROP TABLE Currencies
        """
    )
    db_conn.close()
    print("Table deleted")


# Prints the database to Excel
def print_currency_list():
    db_conn = sqlite3.connect('Database.db')
    db_base = pd.read_sql("SELECT * FROM Currencies ", db_conn)
    db_conn.close()
    cwd = root_cwd()
    os.chdir(filedialog.askdirectory(title="Select output location"))
    db_base.to_excel('Currency-List.xlsx', index=False)
    os.chdir(cwd)


####
