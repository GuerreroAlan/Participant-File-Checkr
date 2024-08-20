import pandas as pd

def DuplicatedCellsTable(df, required_columns):

    duplicatedRowsTable = {}

    for colName in required_columns:
        notEmptyRows = df[(df[colName].notna()) & (df[colName].notnull())]
        duplicatedRows = []
        duplicatedRows = notEmptyRows[notEmptyRows[colName].duplicated()].sort_values(by=['Unique Identifier'])

        if (len(duplicatedRows) == 0):
            duplicatedRows = pd.DataFrame(columns=['There are no duplicated values in this column.'])
            duplicatedRowsTable[colName] = duplicatedRows
        else:
            duplicatedRowsTable[colName] = duplicatedRows[['Unique Identifier', 'First Name', 'Last Name', 'Email']]

    return duplicatedRowsTable