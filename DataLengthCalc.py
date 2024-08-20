import pandas as pd

def ExcessiveLength(df):
    required_columns = df.columns.values
    LengthExceedTable = {}

    for colName in required_columns:
        df[colName] = df[colName].astype(str)
        df ["rowLength"] = df[colName].str.len()
        
        LengthExceed = []
        if colName in ['First Name', 'Last Name']:
            LengthExceed = df[df['rowLength'] > 49]
        elif colName in ['Email', 'Unique Identifier']:
            LengthExceed = df[df['rowLength'] > 99]
        else:
            LengthExceed = df[df['rowLength'] > 1000]

        if (len(LengthExceed) > 0):
            LengthExceedTable[colName] = LengthExceed[['Unique Identifier', colName]]
        else:
            LengthExceed = pd.DataFrame(columns=['None of the cells exceeded the maximum number of characters in this column.'])
            LengthExceedTable[colName] = LengthExceed

    return LengthExceedTable




