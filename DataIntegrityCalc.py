import pandas as pd
from tkinter import messagebox
import sys

def DataIntegrityList(df, required_columns):
    missing_Columns = []
    for colName in required_columns:
        if colName not in df:
            missing_Columns.append(colName)

    missing_ColumnsDF = pd.DataFrame(list(missing_Columns))

    # renaming the "Missing Required Columns" column
    missing_ColumnsDF.rename(columns={0: 'Missing Required Columns'}, inplace=True)

    if len(missing_ColumnsDF) > 0:
        messagebox.showerror("Error", "Missing Required Columns: \n" + '\n'.join(missing_Columns) + '\n\nBefore continue, please add missing columns \nto the selected file.')
        sys.exit()

    return missing_ColumnsDF