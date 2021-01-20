import pandas as pd
import sqlite3
from tkinter.filedialog import askopenfilename
from tkinter import filedialog, messagebox
from datetime import date
import os
import lxml
import html5lib
import bs4
pd.options.mode.chained_assignment = None


def generate_currencies():
    # Gets the exchange rates from database, iterates over each row and create key value pairs
    db_conn = sqlite3.connect('Database.db')
    df_curr = pd.read_sql("SELECT Currency, To_EUR FROM Currencies", db_conn)
    db_conn.close()

    currency = {}
    for i in df_curr.itertuples(index=False, name=None):
        key = i[0]
        value = i[1]
        currency[key] = value
    return currency

def cwd_root():
    cwd_root = os.getcwd()
    return cwd_root

root_cwd = cwd_root
# generate purchasing price for the baseprice df
def generate_baseprice():
    currency = generate_currencies()
    db_conn = sqlite3.connect('Database.db')
    global df_baseprices
    df_baseprices = pd.read_sql("SELECT * FROM baseprices ", db_conn)
    db_conn.close()
    true_price = []
    for row in df_baseprices.itertuples(index=False, name=None):
        # 8 = Grossprice, currency 9, quantity 5, surcharge 10, discount 12
        try:
            true_price.append(calculate_true_price(row[5], row[8], row[10], row[12], currency[row[9]]))
        except:
            true_price.append("Error")
            error_num.append(row[0])
            error_type.append("Bad bad data (baseprice)")
    df_baseprices['Purchasing Price (EUR)'] = true_price
    return df_baseprices


def generate_pirprice():
    # First we import file and cleans it up
    global df_pirprices

    df_pirprices = pd.read_excel(
        askopenfilename(),
        engine='openpyxl',
        header=0,
        index_col=None,
        usecols="D:G, O:P, R:T, AA:AB, AE:AF, AK:AL"
    )


    # Generates the dictionary containing the exchange rates
    currency = generate_currencies()
    # Creates the list that we fill with values based on the for loop and then we will place this into the dataframe
    true_price_pir = []
    global error_num
    global error_type
    error_num = []
    error_type = []
    for row in df_pirprices.itertuples(index=False, name=None):
        try:
            true_price_pir.append(calculate_true_price(row[5], row[7], row[9], row[11], currency[row[8]]))
        except:
            true_price_pir.append("Error")
            error_num.append(row[0])
            error_type.append("Bad data (Pir price")
    df_pirprices['Purchasing Price (EUR)'] = true_price_pir
    return df_pirprices


# Function to calculate the purchasing price of a material
def calculate_true_price(quantity, price, surcharge, discount, rate):
    true_price = (price * (-discount / 100) + price + (surcharge / quantity)) * rate
    return round(true_price, 2)


# Function to merge the two different dataframes.
def append_lists(pir, baseprice):
    df_output = pir.merge(baseprice, left_on='SAP material number', right_on='Material_number')
    return df_output


def compare_supplier(df):
    comparation_supplier = []
    for row in df.itertuples(index=False, name=None):
        a = row[2]
        b = row[18]
        if a == b:
            c = "True"
        else:
            c = "False"
        comparation_supplier.append(c)
    return comparation_supplier


def compare_leadtime(df):
    comparation_leadtime = []
    for row in df.itertuples(index=False, name=None):
        a = row[4]
        b = row[20]
        if (a == b):
            c = "True"
        else:
            c = "False"
        comparation_leadtime.append(c)
    return comparation_leadtime


def compare_price(df):
    comparation_price = []
    for row in df.itertuples(index=False, name=None):
        a = row[15]
        b = row[31]
        if a == "Error" or b == "Error":
            comparation_price.append("Error")
            error_num.append(row[0])
            error_type.append("Bad price data")
        else:
            c = (a - b)
            if c == 0:
                c = "Same price"
                comparation_price.append(c)
            else:
                comparation_price.append(c)
    return comparation_price


def list_errors():
    for row in df_pirprices.itertuples(index=False, name=None):
        if not row[0] in df_baseprices.values:
            error_num.append(row[0])
            error_type.append("New Material number")
    df_errors = pd.DataFrame(list(zip(error_num, error_type)), columns=['Mat num', 'Error type'])
    return df_errors


def main():
    pir = generate_pirprice()
    baseprice = generate_baseprice()
    df_output = append_lists(pir, baseprice)
    df_output['Same supplier?'] = compare_supplier(df_output)
    df_output['Same leadtime?'] = compare_leadtime(df_output)
    df_output['Price diff "EUR"'] = compare_price(df_output)
    return df_output


def clean_main():
    today = date.today()
    df_final = main()
    errors = list_errors()
    # creating xlsx objects
    writer = pd.ExcelWriter('Output ' + str(today) + '.xlsx', engine='xlsxwriter')
    df_final.to_excel(writer, sheet_name='Analyses', index=False, startrow=2)
    errors.to_excel(writer, sheet_name='Errors', index=False)
    workbook = writer.book
    worksheet = writer.sheets['Analyses']

    # Setting formats

    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'align': 'center',
        'bg_color': '#878e99',
        'border': True
    })
    header_format1 = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'align': 'center',
        'bg_color': '#38a834',
        'border': True
    })
    header_format2 = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'align': 'center',
        'bg_color': '#19a6c2',
        'border': True
    })
    header_format3 = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'align': 'center',
        'bg_color': '#bf3939',
        'border': True
    })
    # Formatting the file and then save it
    for col_num, value in enumerate(df_final.columns.values):
        worksheet.write(2, col_num, value, header_format)

    worksheet.set_row(0, None, None, {'hidden': True})
    worksheet.merge_range('A2:P2', 'Data from PIR', header_format1)
    worksheet.merge_range('Q2:AF2', 'Data from Baseprice', header_format2)
    worksheet.merge_range('AG2:AM2', 'Calculated data', header_format3)
    worksheet.write('AJ3', "Purchased volume period", header_format)
    worksheet.write('AK3', "Diff period", header_format)
    worksheet.write('AL3', "Purchased volume YTD", header_format)
    worksheet.write('AM3', "Diff YTD", header_format)
    cwd = root_cwd()
    os.chdir(filedialog.askdirectory(title="Select output location"))
    writer.save()
    os.chdir(cwd)
    messagebox.showinfo("Done", "Script completed successfully")


def clean_pir():
    today = date.today()
    cwd = root_cwd()
    book = askopenfilename()
    try:
        df_raw = pd.read_excel(
            book,
            header=0)
    except:
        df_raw = pd.read_csv(book, engine='python', header=0, delimiter='\t')

    df_clean = df_raw.loc[df_raw['Fixed vendor in Source List - flag (X=YES, BLANK=NO)'] == 'X']
    values = []
    for value in df_clean['Discount RA01']:
        if "-" in value:
            value = value.replace('-', '')
            values.append(value)
        else:
            values.append(value)
    df_clean['Discount RA01'] = values

    df_clean['Standard Quantity'] = df_clean['Standard Quantity'].str.replace(',', '.', regex=True).astype(float)
    df_clean['Gross Price - condition ZPB0'] = df_clean['Gross Price - condition ZPB0'].str.replace(',', '.', regex=True).astype(float)
    df_clean['Surcharge ZB00'] = df_clean['Surcharge ZB00'].str.replace(',', '.', regex=True).astype(float)
    df_clean['Discount RA01'] = df_clean['Discount RA01'].str.replace(',', '.', regex=True).astype(float)

    # df_clean = df_clean['Discount RA01'].str.replace('-', '', regex=True).astype(int)

    #
    os.chdir(filedialog.askdirectory(title="Select output location"))
    df_clean.to_excel('PIR ' + str(today) + '.xlsx', index=False)
    os.chdir(cwd)
    messagebox.showinfo("Done", "Script completed successfully")
