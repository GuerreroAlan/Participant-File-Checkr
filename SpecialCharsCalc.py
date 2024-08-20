import pandas as pd


def UnsopportedCharsTable(df, unsopportedChars, required_columns):
    correctedUnsopportedChars = '[' + unsopportedChars.replace('[', '\[').replace(']', '\]') + ']'
    specialCharsTable = {}
    for colName in required_columns:
        notEmptyRows = []
        specialChars = []
        notEmptyRows = df[(df[colName].notna()) & (df[colName].notnull())]
        specialChars = notEmptyRows[notEmptyRows[colName].str.contains(correctedUnsopportedChars)]

        if (len(specialChars) == 0):
            specialChars = pd.DataFrame(columns=['There are no unsupported characters in this column.'])
            specialCharsTable[colName] = specialChars
        else:
            specialCharsTable[colName] = specialChars[['Unique Identifier', colName]]
    
    return specialCharsTable
        
