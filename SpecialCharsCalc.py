import pandas as pd


def UnsupportedCharsTable(df, unsupportedChars, required_columns):
    correctedUnsopportedChars = '[' + unsupportedChars.replace('[', '\[').replace(']', '\]') + ']'
    specialCharsTable = {}
    for colName in required_columns:
        if colName != 'Email':
            notEmptyRows = []
            specialChars = []
            df[colName] = df[colName].astype(str)
            notEmptyRows = df[(df[colName].notna()) & (df[colName].notnull())]
            specialChars = notEmptyRows[notEmptyRows[colName].str.contains(correctedUnsopportedChars)]

            if (len(specialChars) == 0):
                specialChars = pd.DataFrame(columns=['There are no unsupported characters in this column.'])
                specialCharsTable[colName] = specialChars
            else:
                if colName == 'Unique Identifier':
                    specialCharsTable[colName] = specialChars[[colName]]
                else:
                    specialCharsTable[colName] = specialChars[['Unique Identifier', colName]]
    return specialCharsTable
        
